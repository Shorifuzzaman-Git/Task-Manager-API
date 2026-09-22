# Task Manager API

A secure and scalable **Task Manager REST API** built with **FastAPI, MySQL, SQLAlchemy, JWT authentication, and email OTP verification**.

The API allows users to register, verify their email, log in securely, and manage their own tasks with complete ownership protection.

---

## 🚀 Features

### 🔐 Authentication & Security

* User registration
* Secure password hashing using Argon2
* Email verification using OTP
* OTP expiration
* Resend OTP
* JWT-based authentication
* Protected API endpoints
* Current authenticated user profile
* User-specific task authorization
* Users cannot access or modify another user's tasks

### 📝 Task Management

* Create tasks
* Get all tasks belonging to the logged-in user
* Get a specific task
* Update tasks
* Delete tasks
* Task ownership protection
* Task status validation

### 🗄️ Database

* MySQL database
* SQLAlchemy ORM
* Alembic database migrations
* Foreign key relationships
* Automatic timestamps

### 📚 API Documentation

FastAPI automatically provides:

* Swagger UI
* ReDoc

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Pydantic Settings
* PyMySQL
* Alembic

### Authentication & Security

* JWT
* Python-Jose
* Argon2
* pwdlib
* Email OTP

### Email

* Gmail SMTP
* aiosmtplib

### Database

* MySQL

### Testing

* Pytest
* HTTPX

---

## 📁 Project Structure

```text
Task Manager API/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── otp.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── auth.py
│   │   └── otp.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── tasks.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── otp_service.py
│   │   └── email_service.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   └── utils/
│       └── helpers.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_users.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── alembic.ini
└── README.md
```

> **Important:** Never commit your `.env` file or any passwords, API keys, JWT secrets, or Gmail App Passwords to GitHub.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Move into the project:

```bash
cd "Task Manager API"
```

---

## 2. Create a Virtual Environment

Linux/macOS:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you haven't created `requirements.txt` yet:

```bash
pip freeze > requirements.txt
```

---

# 🗄️ MySQL Database Setup

Open MySQL:

```bash
mysql -u root -p
```

Create the database:

```sql
CREATE DATABASE task_manager;
```

Create a dedicated database user:

```sql
CREATE USER 'task_manager_user'@'localhost'
IDENTIFIED BY 'YOUR_DATABASE_PASSWORD';
```

Grant permissions:

```sql
GRANT ALL PRIVILEGES ON task_manager.*
TO 'task_manager_user'@'localhost';

FLUSH PRIVILEGES;
```

Check the database:

```sql
SHOW DATABASES;
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://task_manager_user:YOUR_PASSWORD@localhost:3306/task_manager

SECRET_KEY=your-long-random-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_FROM=your-email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

### Example `.env.example`

For GitHub, create:

```env
DATABASE_URL=mysql+pymysql://task_manager_user:YOUR_PASSWORD@localhost:3306/task_manager

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_FROM=your-email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

Do **not** put real credentials in `.env.example`.

---

# 📧 Gmail OTP Configuration

The project uses Gmail SMTP to send verification OTPs.

You should use a **Gmail App Password**, not your normal Gmail password.

### Requirements

1. Enable 2-Step Verification on your Google account.
2. Generate a Gmail App Password.
3. Put the generated App Password in:

```env
MAIL_PASSWORD=your-gmail-app-password
```

Never upload the App Password to GitHub.

---

# 🗃️ Database Migration

Initialize the database tables using Alembic.

Run:

```bash
alembic upgrade head
```

Check migration status:

```bash
alembic current
```

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

## ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔑 Authentication Flow

The authentication system works as follows:

```text
Register
   ↓
User Account Created
   ↓
OTP Sent to Email
   ↓
Verify OTP
   ↓
Email Verified
   ↓
Login
   ↓
JWT Access Token
   ↓
Access Protected APIs
```

---

# 🔐 Authentication Endpoints

## Register

```http
POST /api/v1/auth/register
```

Request:

```json
{
  "name": "Shuvo",
  "email": "shuvo@example.com",
  "password": "StrongPassword123"
}
```

A verification OTP will be sent to the user's email.

---

## Verify Email

```http
POST /api/v1/auth/verify-otp
```

Request:

```json
{
  "email": "shuvo@example.com",
  "otp_code": "123456"
}
```

Successful response:

```json
{
  "message": "Email verified successfully"
}
```

---

## Resend OTP

```http
POST /api/v1/auth/resend-otp
```

Request:

```json
{
  "email": "shuvo@example.com"
}
```

Response:

```json
{
  "message": "A new OTP has been sent to your email"
}
```

---

## Login

```http
POST /api/v1/auth/login
```

Request:

```json
{
  "email": "shuvo@example.com",
  "password": "StrongPassword123"
}
```

Response:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

---

# 👤 User Endpoints

## Get Current User

```http
GET /api/v1/users/me
```

Requires:

```text
Authorization: Bearer <access_token>
```

Example response:

```json
{
  "id": 1,
  "name": "Shuvo",
  "email": "shuvo@example.com",
  "is_verified": true
}
```

---

# 📝 Task Endpoints

All task endpoints require JWT authentication.

---

## Create Task

```http
POST /api/v1/tasks
```

Request:

```json
{
  "title": "Learn FastAPI",
  "description": "Complete Task Manager API"
}
```

The `user_id` is automatically taken from the authenticated user.

Example response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Complete Task Manager API",
  "status": "pending",
  "user_id": 1,
  "created_at": "2026-09-22T10:00:00",
  "updated_at": "2026-09-22T10:00:00"
}
```

---

## Get My Tasks

```http
GET /api/v1/tasks
```

Returns only the tasks belonging to the authenticated user.

Example:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "description": "Complete Task Manager API",
    "status": "pending",
    "user_id": 1,
    "created_at": "2026-09-22T10:00:00",
    "updated_at": "2026-09-22T10:00:00"
  }
]
```

---

## Get Single Task

```http
GET /api/v1/tasks/{task_id}
```

Example:

```http
GET /api/v1/tasks/1
```

The API verifies that the requested task belongs to the authenticated user.

---

## Update Task

```http
PUT /api/v1/tasks/{task_id}
```

Example:

```http
PUT /api/v1/tasks/1
```

Request:

```json
{
  "title": "Learn FastAPI and SQLAlchemy",
  "description": "Complete the backend project",
  "status": "in_progress"
}
```

---

## Delete Task

```http
DELETE /api/v1/tasks/{task_id}
```

Example:

```http
DELETE /api/v1/tasks/1
```

Successful response:

```text
204 No Content
```

---

# 📌 Task Status

Tasks support the following statuses:

```text
pending
in_progress
completed
```

Example:

```json
{
  "status": "completed"
}
```

Invalid values are rejected by FastAPI validation.

---

# 🔒 Authorization & Ownership Protection

Task ownership is enforced at the database query level.

For example, retrieving a task uses:

```python
.filter(
    Task.id == task_id,
    Task.user_id == current_user.id
)
```

This means:

```text
User 1
 ├── Task 1
 └── Task 2

User 2
 ├── Task 3
 └── Task 4
```

User 1 can access:

```text
Task 1
Task 2
```

but cannot access:

```text
Task 3
Task 4
```

The same ownership protection applies to:

* Get task
* Update task
* Delete task

This prevents users from modifying or accessing another user's tasks by changing the `task_id`.

---

# 🧪 Testing

The project uses:

* Pytest
* HTTPX

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_auth.py
```

```bash
pytest tests/test_tasks.py
```

```bash
pytest tests/test_users.py
```

---

# 🧩 Architecture

The project follows a layered architecture:

```text
                    Client
                      │
                      ▼
                 FastAPI Router
                      │
                      ▼
                   Service
                      │
                      ▼
                  SQLAlchemy
                      │
                      ▼
                    MySQL
```

Authentication:

```text
Client
  │
  ▼
Login
  │
  ▼
JWT Token
  │
  ▼
Authentication Dependency
  │
  ▼
Current User
  │
  ▼
Protected Resource
```

---

# 🔄 Request Flow Example

Creating a task:

```text
POST /api/v1/tasks
        │
        ▼
JWT Authentication
        │
        ▼
get_current_user()
        │
        ▼
Current User ID
        │
        ▼
Task Service
        │
        ▼
SQLAlchemy
        │
        ▼
MySQL
        │
        ▼
Task Response
```

---

# 🛡️ Security Features

The project currently implements:

* Password hashing with Argon2
* JWT authentication
* Protected endpoints
* Email verification
* OTP expiration
* OTP invalidation on resend
* User-specific authorization
* Database foreign key constraints
* Environment variable configuration
* No `user_id` supplied by clients when creating tasks

---

# 🚧 Future Improvements

Planned improvements include:

* [ ] Convert task update endpoint from `PUT` to `PATCH`
* [ ] Add stronger password validation
* [ ] Hash OTP values in the database
* [ ] Add OTP resend rate limiting
* [ ] Add login rate limiting
* [ ] Add pagination
* [ ] Add task filtering by status
* [ ] Add task search
* [ ] Add consistent global exception handling
* [ ] Add comprehensive automated tests
* [ ] Add CORS configuration
* [ ] Add Docker support
* [ ] Add CI/CD with GitHub Actions
* [ ] Add production deployment
* [ ] Add API monitoring and logging

---

# 📊 API Summary

| Method | Endpoint                  | Authentication | Description       |
| ------ | ------------------------- | -------------- | ----------------- |
| POST   | `/api/v1/auth/register`   | ❌              | Register user     |
| POST   | `/api/v1/auth/verify-otp` | ❌              | Verify email      |
| POST   | `/api/v1/auth/resend-otp` | ❌              | Resend OTP        |
| POST   | `/api/v1/auth/login`      | ❌              | Login             |
| GET    | `/api/v1/users/me`        | ✅              | Get current user  |
| POST   | `/api/v1/tasks`           | ✅              | Create task       |
| GET    | `/api/v1/tasks`           | ✅              | Get user's tasks  |
| GET    | `/api/v1/tasks/{task_id}` | ✅              | Get specific task |
| PUT    | `/api/v1/tasks/{task_id}` | ✅              | Update task       |
| DELETE | `/api/v1/tasks/{task_id}` | ✅              | Delete task       |

---

# 💻 Example Commands

Start the development server:

```bash
uvicorn app.main:app --reload
```

Run migrations:

```bash
alembic upgrade head
```

Run tests:

```bash
pytest -v
```

---

# 📦 Requirements

Recommended environment:

```text
Python 3.12+
MySQL 8+
FastAPI
SQLAlchemy
Alembic
PyMySQL
Pydantic
JWT
Argon2
Pytest
```

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

---

# 👨‍💻 Author

**Shorifuzzaman Shuvo**

Software Engineering Student
Interested in Backend Development, AI, Computer Vision, and Deep Learning.

---

# 📄 License

This project is created for educational and portfolio purposes.
