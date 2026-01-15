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

Create virtual environment & activateBashpython -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
Install dependenciesBashpip install -r requirements.txt
Create .env file in root (example content)envSECRET_KEY=your-very-long-random-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
Run migrationsBashpython manage.py makemigrations
python manage.py migrate
Create a Super Admin userBashpython manage.py createsuperuser
Start the development serverBashpython manage.py runserverAPI base URL:
http://127.0.0.1:8000

Live Hosted API
Base URL: https://your-gym-api.railway.app
(replace with your actual deployed URL)
Interactive Swagger documentation:
https://your-gym-api.railway.app/api/schema/swagger-ui/
User Roles & Permissions



































RoleDescriptionMain PermissionsRestrictionsSuper AdminSystem ownerFull access: create branches, users, see everything—Gym ManagerManages one branchCreate trainers & members in own branch
List users/tasks in own branchCannot access other branchesTrainerBelongs to one branch (max 3 per branch)Create workout plans
Assign tasks to members in own branch
Update tasksCannot assign to other branch membersMemberRegular gym userView own assigned tasks
Update own task status (e.g. mark completed)Cannot see other members or plans
Authentication: All endpoints except /api/auth/token/ require Authorization: Bearer <access_token>
Important API Endpoints

































































MethodEndpointWhat it doesWho can usePOST/api/auth/token/Login → get access & refresh tokenEveryonePOST/api/auth/token/refresh/Refresh access tokenEveryoneGET/api/accounts/users/me/Get current user profileAuthenticatedGET/api/accounts/users/List users (filtered by branch for managers)Super Admin + ManagerPOST/api/accounts/users/Create trainer or memberSuper Admin + ManagerGET/POST/api/branches/branches/List / Create gym branchesSuper Admin (create)GET/POST/api/workouts/plans/List / Create workout plansTrainer (create)GET/POST/api/workouts/tasks/List / Assign tasksTrainer (assign), Member (list own)PATCH/api/workouts/tasks/{id}/Update task statusTrainer or Member (own task)
Full interactive docs → /api/schema/swagger-ui/
How to Test with Postman

Go to folder postman/ in this repository
Import these files into Postman:
Gym_Management_API.postman_collection.json
Gym_API_Dev.postman_environment.json (optional)

Select environment: Gym API - Dev
First step — run Auth → Login request
Change email/password to a real test user
Send → tokens will be saved automatically

Now test each role folder:
Super Admin
Manager
Trainer
Member


Tip: If token expires → run Refresh token request.
Pre-created Test Users
Use these credentials for quick testing:



































RoleEmailPasswordBranchSuper Adminadmin@gym.comadmin123—Managermanager1@branch1.commgr123Branch 1Trainertrainer1@branch1.comtr123Branch 1Membermember1@branch1.commem123Branch 1
(You can create more via Super Admin or Manager API)
API Documentation

Interactive Swagger UI: /api/schema/swagger-ui/
Redoc (clean docs): /api/schema/redoc/
Raw OpenAPI JSON: /api/schema/

You can try every endpoint directly in the browser (after login).
Deployment Notes

Recommended platforms: Railway, Render, Fly.io
Use PostgreSQL in production
Set DEBUG=False and secure SECRET_KEY
Use Gunicorn + Nginx / uvicorn for serving

License
MIT License (feel free to use and modify)
Made with 💪 for fitness lovers!
Last updated: January 2026