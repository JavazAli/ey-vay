# AP_Project - Cinema Reservation System

## Description
This is a Django project for managing cinema reservations.  
It includes apps for accounts, cinemas, movies, and reservations.  
PostgreSQL is used as the database backend.

## Requirements
- Python 3.11+  
- PostgreSQL 18+  
- Django 6.0  
- Dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:
git clone https://hamgit.ir/sut-ie-ap-04051/kheirandish-javadi-baghaei/ap_project.git
cd ap_project

2. Create and activate a virtual environment:
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

3. Install dependencies:
pip install -r requirements.txt

4. Create a .env file in the project root with your database settings:
DB_NAME=cinema_reservation_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5433
SECRET_KEY=your-secret-key
DEBUG=True

5. Apply database migrations:
python manage.py migrate

6. Run the development server:
python manage.py runserver

The project should now be running at http://127.0.0.1:8000/

Apps:
accounts - user management
cinemas - cinema information
movies - movie management
reservations - seat reservations

Notes:
.env is ignored in Git for security. Use .env.example as a reference.
Make sure PostgreSQL is running on the correct port (5433 by default).
