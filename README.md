# Gym Management & Member Workout System (API Only)

This is a **backend REST API** built with **Django + Django REST Framework** for managing multiple gym branches, trainers, members, workout plans, and assigned workout tasks.  
No frontend is included — only API endpoints.

## Main Features

- Multi-branch gym management
- Role-based access control (RBAC)
  - Super Admin
  - Gym Manager (per branch)
  - Trainer (max 3 per branch)
  - Member
- JWT authentication (access + refresh tokens)
- Strict branch isolation — users cannot access data from other branches
- Workout plans created by trainers
- Workout tasks assigned to members (same branch only)
- Members can view and update their own task status

## Technologies

- Python 3.11 / 3.12
- Django 5.1+
- Django REST Framework
- djangorestframework-simplejwt (JWT)
- PostgreSQL (production) / SQLite (development)

## Quick Setup (Local Development)

1. Clone the project

   ```bash
   git clone https://github.com/your-username/gym-management-api.git
   cd gym-management-api

2. Create virtual environment & activate

    ```bash
        python -m venv venv

        # Windows
        venv\Scripts\activate

        # Linux / macOS
        source venv/bin/activate