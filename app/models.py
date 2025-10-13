# This is models.py from the app folder

from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    user_type = db.Column(db.String(20))

    # Relationships
    applicant_profile = db.relationship('Applicant', backref='user', uselist=False, cascade='all, delete-orphan') # backref creates a reverse relationship automatically
    employer_profile = db.relationship('Employer', backref='user', uselist=False, cascade='all, delete-orphan') # uselist indicates a one-to-one relationship:
    jobs_posted = db.relationship('Job', backref='employer', foreign_keys='Job.employer_id')

    def get_id(self):
        return str(self.user_id)

class Applicant(db.Model):
    __tablename__ = 'Applicant'

    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)

    # Relationship for jobs applied (many-to-many with Job)
    jobs_applied = db.relationship('JobApplication', backref='applicant')

class Employer(db.Model):
    __tablename__ = 'Employer'

    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)

    # Relationship for jobs posted (handled in User model)
    
class Job(db.Model):
    __tablename__ = 'Job'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    location = db.Column(db.String(150))
    salary_min = db.Column(db.Float(50))
    salary_max = db.Column(db.Float(50))
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), nullable=True)
    no_of_applicants = db.Column(db.Integer, default=0)

    # Relationship for applicants (many-to-many through JobApplication)
    applicants = db.relationship('JobApplication', backref='job')

class JobApplication(db.Model):
    __tablename__ = 'JobApplication'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('Applicant.user_id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('Job.id'), nullable=False)
    application_date = db.Column(db.DateTime(timezone=True), default=func.now())
    phone = db.Column(db.String(20))
    resume_path = db.Column(db.String(255))
    cover_letter_path = db.Column(db.Text)
    status = db.Column(db.String(150)) # 'applied', 'reviewed', 'accepted', 'rejected'
