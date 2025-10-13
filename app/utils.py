from werkzeug.utils import secure_filename
import os

def secure_unique_filename(filename, unique_id):
    base, ext = os.path.splitext(secure_filename(filename))
    return f'{base}_{unique_id}{ext}'