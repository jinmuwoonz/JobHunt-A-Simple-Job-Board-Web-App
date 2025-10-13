from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from flask_login import current_user, login_required
from datetime import datetime
import os
from app.models import User, Applicant, Employer, Job, JobApplication
from app import db
from app.utils import secure_unique_filename

jobs_bp = Blueprint('jobs_bp', __name__)

@jobs_bp.route('/')
@jobs_bp.route('/home')
def home():
    jobs = Job.query.order_by(Job.date_posted.desc()).all()
    return render_template('home.html', jobs=jobs)

@jobs_bp.route('/job-detail/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.is_authenticated:
        user_job_applications = JobApplication.query.filter_by(applicant_id=current_user.user_id).order_by(JobApplication.application_date.desc()).all()
        
        if user_job_applications:
            for application in user_job_applications:
                if application.job.id == job_id:
                    return render_template('job_detail.html', job=job, isApplied=True)

    return render_template('job_detail.html', job=job, isApplied=False)

@jobs_bp.route('/post-job', methods=['POST', 'GET'])
@login_required
def post_job():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        location = request.form.get('location')
        salary_min = float(request.form.get('salary-min'))
        salary_max = float(request.form.get('salary-max'))

        new_job = Job(
            employer_id=current_user.user_id,
            title=title,
            description=description,
            requirements=requirements,
            location=location,
            salary_min=salary_min,
            salary_max=salary_max
        )
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job Posted.', category='success')
        return redirect(url_for('dashboard_bp.dashboard'))
    
    return render_template('post_job.html', button_name='Post Job')

@jobs_bp.route('/apply/<int:job_id>', methods=['POST', 'GET'])
def job_apply(job_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
        resume = request.files['resume']
        cover_letter = request.files['coverLetter']
        phone_number = request.form.get('number')

        if resume and cover_letter:
            unique_id = f'{current_user.user_id}_{job_id}'
            resume_filename = secure_unique_filename(resume.filename, unique_id)
            cover_letter_filename = secure_unique_filename(cover_letter.filename, unique_id)
            resume_filepath = os.path.join(current_app.config['UPLOAD_FOLDER_RESUME'], resume_filename)
            cover_letter_filepath = os.path.join(current_app.config['UPLOAD_FOLDER_COVER_LETTER'], cover_letter_filename)

            resume.save(resume_filepath)
            cover_letter.save(cover_letter_filepath)

            new_job_application = JobApplication(
                applicant_id=current_user.user_id,
                job_id=job_id,
                phone=phone_number,
                resume_path=f'uploads/resumes/{resume_filename}',
                cover_letter_path=f'uploads/cover_letter/{cover_letter_filename}',
                status='applied'
            )
            job = Job.query.filter_by(id=job_id).first()
            job.no_of_applicants += 1
            db.session.add(new_job_application)
            db.session.commit()
            flash('Applied successfully!', category='success')
            return redirect(url_for('jobs_bp.home'))
        else:
            flash('No files uploaded', category='error')

    return render_template('apply_job.html', email=current_user.email, name=current_user.name)

@jobs_bp.route('/edit-job/<int:job_id>', methods=['POST', 'GET'])
def job_edit(job_id):
    job = Job.query.filter_by(id=job_id).first()
    if request.method == 'POST':
        if job:
            job.title = request.form.get('title')
            job.description = request.form.get('description')
            job.requirements = request.form.get('requirements')
            job.location = request.form.get('location')
            job.salary_min = request.form.get('salary-min')
            job.salary_max = request.form.get('salary-max')
            job.date_updated = datetime.utcnow()
            
            db.session.commit()
            flash('Job Updated Successfully.', category='success')
            return redirect(url_for('jobs_bp.home'))
        else:
            flash('Job does not exist.', category='error')

    return render_template('post_job.html', title=job.title, description=job.description, requirements=job.requirements, location=job.location, salary_min=job.salary_min, salary_max=job.salary_max, button_name='Update Job')

@jobs_bp.route('/delete-job/<int:job_id>', methods=['POST'])
def job_delete(job_id):
    job = Job.query.filter_by(id=job_id).first()
    if job:
        db.session.delete(job)
        db.session.commit()
        flash('Job Deleted Successfully.', category='success')
    else:
        flash('Job not found.', category='error')

    return redirect(url_for('jobs_bp.home'))