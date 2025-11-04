# JobHunt: A Simple Job Board Web App

JobHunt App is a lightweight, full-featured job board application built with Flask. It allows users to post job listings, apply to jobs with resumes and cover letters, manage user profiles, and handle authentication. The app is designed for easy local development and can be extended for production deployment.

## Requirements

- **Python**: 3.8 or higher
- **Database**: MySQL 8.0+

## Installation

Follow these steps to set up and run the app locally in development mode.

### 1. Clone the Repository

```bash
git clone https://github.com/jinmuwoonz/JobHunt-A-Simple-Job-Board-Web-App.git
cd flask-jobhunt-app
```

### 2. Create and Activate a Virtual Environment

This isolates dependencies. Use Python 3.8+.

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Verify activation: Your prompt should show `(venv)`.

### 3. Install Dependencies

Upgrade pip first, then install from `requirements.txt`.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs core packages like:
- `Flask==2.3.3`
- `Flask-SQLAlchemy==3.0.5`
- `Flask-Migrate==4.0.5`
- `Flask-Login==0.6.3`
- `Werkzeug==2.3.7`

And others (full list in `requirements.txt`).

### 4. Configure the Environment

Copy the example env file and edit it:

```bash
cp .env.example .env
```

Create the MySQL database:

```sql
CREATE DATABASE jobhunt_db;
```

### 5. Initialize and Apply Database Migrations

Uses Flask-Migrate (Alembic backend).

**First-time setup** (initializes migrations):
```bash
flask db init  # Only once; creates migrations/ folder
flask db migrate -m "Initial migration"  # Detects models and generates script
flask db upgrade  # Applies migrations to DB
```

**Subsequent runs** (e.g., after model changes):
```bash
flask db migrate -m "Describe changes here"
flask db upgrade
```

This sets up tables for users, jobs, applications, etc. Check `migrations/versions/` for scripts.

### 6. Running the App

Run with Flask CLI:
```bash
flask run
```

Or directly via `run.py`:
```bash
python run.py
```

The app starts at `http://127.0.0.1:5000/` (or `http://localhost:5000`).

## Usage

- **Register / Login**: Create an account as a job seeker or employer.
- **Post a Job (Employers)**: Go to dashboard > Post Job. Fill details and submit.
- **Browse / Apply (Seekers)**: Search jobs, view details, upload resume/cover letter to apply.
- **Manage Applications**: View status in dashboard.
- **Profile**: Update info under `/profile/`.

File uploads are validated (size < 5MB, allowed types: PDF, DOCX). Uploaded files are stored in `uploads/` subfolders.
