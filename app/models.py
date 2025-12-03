# This is models.py from the app folder

from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
import enum

class UserType(enum.Enum):
    A = 'A'
    E = 'E'

class UserStatus(enum.Enum):
    Pending = 'Pending'
    Varified = 'Verified'
    Rejected = 'Rejected'

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.Text, nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    hashed_password = db.Column(db.String(200), nullable=False)
    verification_doc = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    status = db.Column(db.Enum(UserStatus), nullable=False)
    date_registered = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    # Relationships
    applicant_additional_details = db.relationship('Applicant', backref='user', uselist=False, cascade='all, delete-orphan') # backref creates a reverse relationship automatically
    employer_additional_details = db.relationship('Employer', backref='user', uselist=False, cascade='all, delete-orphan') # uselist indicates a one-to-one relationship:
    notifications = db.relationship('Notification', backref='user')

    def get_id(self):
        return str(self.user_id)

class Applicant(db.Model):
    __tablename__ = 'Applicant'

    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(200), nullable=True)
    skills = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(50), nullable=True)

    # Relationship for jobs applied (many-to-many with Job)
    jobs_applied = db.relationship('JobApplication', backref='applicant')

class Employer(db.Model):
    __tablename__ = 'Employer'

    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
    business_title = db.Column(db.String(50), nullable=False, unique=True)
    business_description = db.Column(db.String(255), nullable=False)
    position_title = db.Column(db.String(50), nullable=False)

    # Relationship for jobs posted
    jobs_posted = db.relationship('Job', backref='employer', foreign_keys='Job.employer_id')
    
class JobCategory(db.Model):
    __tablename__ = 'JobCategory'

    jobcat_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Relation ship for job
    job_category = db.relationship('Job', backref='jobcat', foreign_keys='Job.category_id')

class JobStatus(enum.Enum):
    Open = 'Actively Hiring'
    Closed = 'Closed'

class Job(db.Model):
    __tablename__ = 'Job'
    
    job_id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('Employer.user_id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('JobCategory.jobcat_id'), nullable=False)
    salary_range = db.Column(db.String(50), nullable=False)
    employment_type = db.Column(db.String(25), nullable=False)
    status = db.Column(db.Enum(JobStatus), nullable=False)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=True)
    no_of_applicants = db.Column(db.Integer, default=0, nullable=False)

    # Relationship for applicants (many-to-many through JobApplication)
    applicants = db.relationship('JobApplication', backref='job')

class JobApplicationStatus(enum.Enum):
    Pending = 'Pending'
    Accepted = 'Accepted'
    Rejected = 'Rejected'
    Withdrawn = 'Withdrawn'

class JobApplication(db.Model):
    __tablename__ = 'JobApplication'

    application_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('Job.job_id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('Applicant.user_id'), nullable=False)
    application_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    status = db.Column(db.Enum(JobApplicationStatus), nullable=False)
    resume_file = db.Column(db.Text, nullable=False)
    reason = db.Column(db.String(200), nullable=True)

class Notification(db.Model):
    __tablename__ = 'Notification'
    notif_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date_sent = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    is_read = db.Column(db.Integer, default=0)

class Admin(db.Model):
    __tablename__ = 'Admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(25), nullable=False)
