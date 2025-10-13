from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, Applicant, Employer, Job, JobApplication
from app import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password2')
        user_type = request.form.get('userType')

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            user_type=user_type
        )
        db.session.add(new_user)
        db.session.commit()

        if new_user.user_type == 'applicant':
            applicant = Applicant(user_id=new_user.user_id)
            db.session.add(applicant)
            db.session.commit()
        else:
            employer = Employer(user_id=new_user.user_id)
            db.session.add(employer)
            db.session.commit()

        flash('Account created.', category='success')
        login_user(new_user, remember=True)
        return redirect(url_for('jobs_bp.home'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('jobs_bp.home'))
            else:
                flash('Incorrect password. Try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html')

@auth_bp.route('/log-out')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('jobs_bp.home'))