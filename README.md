Qatar Foundation Admin Portal - Backend API

A highly professional, modular backend built with Flask to power the Qatar Foundation Admin UI.

Architecture Highlights

Service-Layer Pattern: Complete decoupling between routing constraints and business logic.

Security Check: Database validation rules and strict authorization boundaries guard every single endpoint.

Environment Configuration: Safe secrets lifecycle using Python Dotenv.

Quickstart

Environment Setup

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Configuration
Copy the sample environment file:

cp .env.example .env


Start the Application

python app.py


The SQLite Database qatar_admin.db will initialize automatically. The server runs continuously at http://127.0.0.1:5000.

Notes for UI Team

The APIs align precisely with existing Ajax/Axios calls. Responses consist strictly of status, message, and optional data and redirect keys avoiding front-end refactoring needs entirely.