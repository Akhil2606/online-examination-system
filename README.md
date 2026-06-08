# Online Examination System

## Overview

Online Examination System developed using FastAPI, SQLAlchemy, MySQL, and JWT Authentication.

The system supports:

* User Registration and Login
* JWT Authentication
* Role-Based Access Control (Admin & Student)
* Subject Management
* Question Bank Management
* Exam Management
* Student Exam Workflow
* Result Management
* Reporting Module

---

## Technologies Used

* Python 3.x
* FastAPI
* SQLAlchemy
* MySQL
* JWT Authentication
* Swagger UI
* Pydantic

---

## Project Structure

```text
online_exam_system
│
├── app
│   ├── core
│   ├── models
│   ├── schemas
│   ├── routers
│   ├── utils
│   └── main.py
│
├── .env
├── requirements.txt
├── README.md
└── venv
```

---

## Features

### Authentication

* User Registration
* User Login
* JWT Authentication

### User Roles

* Admin
* Student

### Subject Management

* Create Subject
* Get All Subjects
* Get Subject By ID
* Update Subject
* Delete Subject

### Question Bank

* Add Question
* View Questions
* Update Question
* Delete Question
* Categorize Questions by Subject

### Exam Management

* Create Exam
* Assign Questions to Exam
* Set Duration
* Set Passing Marks

### Student Exam

* Start Exam
* Submit Exam
* Auto Calculate Score

### Results

* View Results
* Pass/Fail Status
* Exam History

### Reports

* Top Scorers
* Subject-wise Performance
* Exam-wise Statistics

---

## Database Tables

* users
* roles
* subjects
* questions
* exams
* exam_questions
* student_exams
* results

---

## Environment Variables

Create a `.env` file in the project root.

```env
DB_USERNAME=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=online_exam_db

SECRET_KEY=mysecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Installation

### Clone Repository

```bash
git clone <repository_url>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## API Modules

### Authentication

* POST /auth/register
* POST /auth/login
* GET /auth/me

### Subjects

* POST /subjects
* GET /subjects
* GET /subjects/{id}
* PUT /subjects/{id}
* DELETE /subjects/{id}

### Questions

* POST /questions
* GET /questions
* GET /questions/{id}
* PUT /questions/{id}
* DELETE /questions/{id}
* GET /questions/subject/{subject_id}

### Exams

* POST /exams
* GET /exams
* POST /exams/assign-question

### Student Exam

* POST /student-exam/start
* POST /student-exam/submit
* GET /student-exam/results
* GET /student-exam/history

### Reports

* GET /exams/top-scorers
* GET /exams/statistics

---

## Author

Developed as part of the Online Examination System project using FastAPI and MySQL.
