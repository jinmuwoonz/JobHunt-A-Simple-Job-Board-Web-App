from flask import Blueprint, render_template, send_from_directory, current_app, request, redirect
from flask_login import login_required, current_user
from app import db
from app.models import User, Applicant, Employer, Job, JobApplication

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')