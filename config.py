# This is config.py from the root folder

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # require env var in prod
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # require env var
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER_RESUME = 'app/static/uploads/resumes'
    UPLOAD_FOLDER_COVER_LETTER = 'app/static/uploads/cover_letter'