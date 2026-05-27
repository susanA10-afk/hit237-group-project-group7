# HIT237 Group 7 — Youth Justice & Crime App

A Django web application built for HIT237 Building Interactive
Software at Charles Darwin University.

## Test Evidence

All test result screenshots are located in the `assessment4/evidence/` folder of this repository. Screenshots show all 18 unit tests passing. Tests can also be run locally using:cd assessment4 python manage.py test

## About the App

This app is a case management system for youth justice in the
Northern Territory. Caseworkers can manage young persons, record
offences, assign interventions, and track court hearings. Admin
users have access to a statistics dashboard and full system oversight.

## How to Run

1. Clone the repository:
   git clone https://github.com/susanA10-afk/hit237-group-project-group7.git

2. Navigate to the assessment4 folder:
   cd hit237-group-project-group7/assessment4

3. Create a virtual environment:
   python -m venv venv

4. Activate it:
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Run migrations:
   python manage.py migrate

7. Create a superuser:
   python manage.py createsuperuser

8. Start the server:
   python manage.py runserver

9. Open browser at http://127.0.0.1:8000

10. Login with the superuser credentials you created

## User Roles

The app has two roles — admin and caseworker.
- Admin users can access the statistics dashboard and all features
- Caseworker users can manage young persons, offences, interventions and hearings

To set a user's role, go to http://127.0.0.1:8000/admin and edit
the user's role field under the Accounts section.

## How to Run Tests

python manage.py test

Test results and screenshots are in assessment4/evidence/

## Project Structure

- assessment4/accounts/ — custom user model with role-based access
- assessment4/justice/ — models, views, services, exceptions, tests
- assessment4/youthjustice/ — project settings and URL routing
- assessment4/evidence/ — test result screenshots
- docs/ — ERD, class diagrams, sequence diagrams
- ADR.md — architecture decision records
- GROUP-CONTRACT-GROUP7.md — group contract and project plan

## Group Members

- Susan Acharya (S383819)
- Subodh Shrestha (S404921)
- Milan Sapkota (S396875)
- Sisan Pandey (S382718)

## Unit

HIT237 — Charles Darwin University, 2026
