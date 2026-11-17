# Multi-Bank Recruitment Demo Portal

Django-based local demonstration recruitment portal using fictional bank profiles only. Every page and PDF clearly states this is not an official bank website.

## Features
- Responsive banking-inspired interface and fictional bank themes
- Demo vacancy listing and filtering
- Application form with server-side validation
- Optional profile photo and supporting document uploads
- Unique application reference and A4 PDF receipt
- Django admin for bank profiles, vacancies and applications
- SQLite local database

## Windows PowerShell setup
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py test
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```
Open http://127.0.0.1:8000 and /admin/ for administration.

## Ngrok
In a second PowerShell window run `ngrok http 8000`. Use the HTTPS forwarding URL printed by ngrok. This temporarily exposes your local development server. Use fictional data and sample files only; do not expose the admin site publicly. Stop ngrok when testing is complete.

## Important
- Never enter Aadhaar, PAN, bank account, card, password or OTP information.
- Uploads are stored locally in `media/`; private storage is required before any real deployment.
- PDF receipts are explicitly marked DEMO and state that no real recruitment application was submitted.
