from flask import Flask, render_template, request, redirect, session
from db import engine, BASE, SessionLocal
import models
import PyPDF2
import docx
import json

app = Flask(__name__)

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
        user_goal = request.form.get('role')
        resume_text = request.form.get('resume')

        file = request.files.get('file')

if __name__ == '__main__':
    app.run(debug=True)