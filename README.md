# JobFinder — Django Job Board

A Django web application connecting job seekers and employers. Users can register, browse job listings, and submit applications.

## Features

- User authentication (registration, login, logout)
- Job listing creation and browsing
- Application submission
- HTML template-based frontend
- Environment configuration via `.env`

## Quick Start

### 1. Clone

```bash
git clone https://github.com/samandar-hamrayev/jobfinder.git
cd jobfinder
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure `.env`

```env
SECRET_KEY=django-insecure-your-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### 4. Run migrations and start server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## Admin Panel

```bash
python manage.py createsuperuser
# Visit http://127.0.0.1:8000/admin/
```

## Project Structure

```
jobfinder/
├── accounts/        # User authentication
├── jobs/            # Job listings and applications
├── templates/       # HTML templates
├── static/          # CSS, JS assets
├── media/           # Uploaded files
├── .env             # Environment config
├── manage.py
└── requirements.txt
```

## Tech Stack

- Python 3.9+ · Django 4+
- SQLite (default)
- HTML/CSS templates

## License

MIT — [Samandar Hamrayev](https://github.com/samandar-hamrayev)
