# HIT237 Group 7 — Youth Justice & Crime App

A Django web application built for HIT237 Building Interactive 
Software at Charles Darwin University.

## About the App
This app provides a case management system for youth justice 
in the Northern Territory. It allows caseworkers to manage 
young persons, record offences, assign interventions, and 
track court hearings.

## How to Run

1. Clone the repository
2. Create a virtual environment:
   python -m venv venv
3. Activate it:
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate
4. Install dependencies:
   pip install -r requirements.txt
5. Run migrations:
   python manage.py migrate
6. Start the server:
   python manage.py runserver
7. Open browser at http://127.0.0.1:8000

## Group Members
- Susan Acharya (S383819)
- Subodh Shrestha (S404921)
- Milan Sapkota (S396875)
- Sisan Pandey (S382718)

## Unit
HIT237 — Charles Darwin University, 2026

## System Design
This project follows the Model-View-Template (MVT) architecture of Django.
- Models handle the database structure and relationships
- Views control the application logic
- Templates (future scope) will manage the user interface

## Project Structure
- justice/ – configuration files
- youthjustice/ – core application logic and models
- manage.py – application entry point
- requirements.txt – project dependencies

## Future Enhancements
- Add role-based access control
- Improve validation and error handling
- Implement reporting dashboard

## Additional Notes
This project was reviewed and documentation was improved to ensure clarity in setup and structure.