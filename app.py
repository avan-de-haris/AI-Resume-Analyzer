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

if __name__ == '__main__':
    app.run(debug=True)