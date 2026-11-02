import os
import ai
from flask import Flask, render_template, request, redirect, session
from db import engine, BASE, SessionLocal
import models
import PyPDF2
import docx
import json

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Use the secret key from the .env file

BASE.metadata.create_all(bind=engine)  # Create tables if they don't exist

# Home route
@app.route('/')
def home():
    if "user" in session:
        return redirect('/dashboard')
    return redirect('/login')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = SessionLocal()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = email.split('@')[0]  # Use the part before '@' as the username

        # Check if the user already exists
        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            return "User already exists. Please log in."

        user = models.User(email=email, password=password)  
        db.add(user)
        db.commit()

        return redirect('/login')
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    db = SessionLocal()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.query(models.User).filter_by(email=email, password=password).first()
        if user:
            session['user'] = user.email
            return redirect('/dashboard')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "user" not in session:
        return redirect('/login')

    result = None

    if request.method == 'POST':
        user_goal = request.form.get('role', '').strip()
        pasted_text = request.form.get('resume', '').strip()
        file = request.files.get('file')

        resume_text = ""

        # 1. Process uploaded file first
        if file and file.filename != '':
            if file.filename.lower().endswith('.pdf'):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text_parts = []
                    for page in pdf_reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text_parts.append(extracted)
                    resume_text = "\n".join(text_parts).strip()
                except Exception as e:
                    result = {"error": f"Error reading PDF file: {str(e)}"}

            elif file.filename.lower().endswith('.docx'):
                try:
                    doc = docx.Document(file)
                    resume_text = "\n".join([para.text for para in doc.paragraphs if para.text]).strip()
                except Exception as e:
                    result = {"error": f"Error reading DOCX file: {str(e)}"}
            else:
                result = {"error": "Unsupported file format. Please upload a PDF or DOCX file."}

        # 2. Fall back to pasted textarea text if no file was uploaded
        if not resume_text and pasted_text:
            resume_text = pasted_text

        # 3. Debug logging to terminal
        print(f"DEBUG: user_goal = '{user_goal}'")
        print(f"DEBUG: resume_text length = {len(resume_text)}")

        # 4. Trigger AI Analysis
        if resume_text and user_goal and not result:
            db = SessionLocal()
            try:
                print("DEBUG: Sending request to AI...")
                result = ai.analyze_resume(resume_text, user_goal)
                print(f"DEBUG: AI result received: {result}")

                # Save report to database
                user = db.query(models.User).filter_by(email=session['user']).first()
                if user:
                    report = models.Reports(
                        user_id=user.id,
                        resume_text=resume_text,
                        result=json.dumps(result)
                    )
                    db.add(report)
                    db.commit()
            except Exception as e:
                db.rollback()
                result = {"error": f"AI Error: {str(e)}"}
            finally:
                db.close()
        elif not resume_text and not result:
            result = {"error": "Please paste resume text or upload a valid PDF/DOCX file."}

    return render_template('dashboard.html', user=session['user'], result=result)


# History route
@app.route('/history')
def history():
    if "user" not in session:
        return redirect('/login')

    db = SessionLocal()
    try:
        user = db.query(models.User).filter_by(email=session['user']).first()
        reports = db.query(models.Reports).filter_by(user_id=user.id).all() if user else []

        history_list = []
        for r in reports:
            try:
                report_data = json.loads(r.result)
            except (json.JSONDecodeError, TypeError):
                report_data = {}

            history_list.append({
                "resume": r.resume_text,
                "result": report_data
            })
    finally:
        db.close()

    return render_template('history.html', reports=history_list)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)