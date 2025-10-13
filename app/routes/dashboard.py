from flask import Blueprint, render_template, send_from_directory, current_app, request, redirect
from flask_login import login_required, current_user
from app import db
from app.models import User, Applicant, Employer, Job, JobApplication

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/my-applications')
@login_required
def my_applications():
    user_job_applications = JobApplication.query.filter_by(applicant_id=current_user.user_id).order_by(JobApplication.application_date.desc()).all()
    return render_template('my_applications.html', user_job_applications=user_job_applications)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_job_posted = Job.query.filter_by(employer_id=current_user.user_id).order_by(Job.date_posted.desc()).all()
    return render_template('dashboard.html', user_job_posted=user_job_posted)

@dashboard_bp.route('/applicants/<int:job_id>')
@login_required
def view_applicants(job_id):
    applications = JobApplication.query.filter_by(job_id=job_id).order_by(JobApplication.application_date.desc()).all()
    return render_template('applicants.html', applications=applications, job=Job.query.filter_by(id=job_id).first())

@dashboard_bp.route('/update-status', methods=['POST'])
def update_status():
    application_id = request.form.get('application_id')
    new_status = request.form.get('status')

    application = JobApplication.query.get(application_id)
    if application:
        application.status = new_status
        db.session.commit()
    
    return redirect(request.referrer)