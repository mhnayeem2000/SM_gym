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
3. Install dependencies

    ```bash
        pip install -r requirements.txt
4. Create .env file in root
    ```bash
    SECRET_KEY=your-very-long-random-secret-key-change-this
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
5. Run migrations

    ```bash
        python manage.py makemigrations
        python manage.py migrate    

6. Start the development server

    ```bash
    python manage.py runserver


7. Important URLs:

   1.  Login: /api/auth/token/
   2.  Swagger Docs: /api/schema/swagger-ui/

8. User Role and Permissions : 

| Role        | Can Do                                              | Cannot Do                      |
| ----------- | --------------------------------------------------- | ------------------------------ |
| Super Admin | Full access, create branches & users, view all data | —                              |
| Gym Manager | Create trainers & members (own branch), list users  | Access other branches          |
| Trainer     | Create workout plans, assign tasks (own branch)     | Assign tasks to other branches |
| Member      | View own tasks, update task status                  | View other users or plans      |


9. API Endpoints: 

| Method | Endpoint                    | Description         | Access                  |
| ------ | --------------------------- | ------------------- | ----------------------- |
| POST   | `/api/auth/token/`          | Login (JWT tokens)  | Everyone                |
| POST   | `/api/auth/token/refresh/`  | Refresh token       | Everyone                |
| GET    | `/api/accounts/users/me/`   | Get own profile     | Logged-in user          |
| GET    | `/api/accounts/users/`      | List users          | Super Admin, Manager    |
| POST   | `/api/accounts/users/`      | Create user         | Super Admin, Manager    |
| GET    | `/api/branches/branches/`   | List branches       | Logged-in users         |
| POST   | `/api/branches/branches/`   | Create branch       | Super Admin             |
| GET    | `/api/workouts/plans/`      | List workout plans  | Admin, Manager, Trainer |
| POST   | `/api/workouts/plans/`      | Create workout plan | Trainer                 |
| GET    | `/api/workouts/tasks/`      | List tasks          | All users               |
| POST   | `/api/workouts/tasks/`      | Assign task         | Trainer                 |
| PATCH  | `/api/workouts/tasks/{id}/` | Update task         | Trainer / Member        |


10. 📬 How to Use the Postman Collection
        Download ([Here](https://github.com/mhnayeem2000/SM_gym/tree/main/Postman%20File)) json file from Postman File in the Root directory 

11. Test User : 

| Role        | Email                                               | Password | Branch   |
| ----------- | --------------------------------------------------- | -------- | -------- |
| Super Admin | [admin@gmail.com](mailto:admin@gmail.com)               | admin | —        |
| Manager     | [manager@gmail.com](mailto:manager1@gmail.com) | manager12345678   | Branch 1 |
| Trainer     | [trainer@gmail.com](mailto:trainer1@gmail.com) | trainer12345678    | Branch 1 |
| Member      | [member@gmail.com](mailto:member1@gmail.com)   | member12345678   | Branch 1 |
