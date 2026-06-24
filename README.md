# Task Manager API

A Task Management System built with Django, Django REST Framework, Channels, Celery, and WebSockets. It allows users to create, assign, track, and manage tasks with real-time notifications and chat functionality.

## Features

* User authentication with JWT
* Role-based access (Admin, Manager, Employee)
* Task creation and assignment
* Task status tracking
* Real-time notifications using WebSockets
* Real-time chat
* File attachments
* Celery background tasks
* RESTful APIs with Django REST Framework
* Pagination, filtering, and search
* Audit logs and activity tracking

## Tech Stack

* Python
* Django
* Django REST Framework
* Django Channels
* Redis
* Celery
* SQLite/PostgreSQL
* JavaScript
* HTML/CSS

## Installation

### Clone the repository

```bash
git clone https://github.com/hasti-tagline/task_manager.git
cd task_manager
```

### Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Start Redis

```bash
redis-server
```

### Start Celery Worker

```bash
celery -A main worker -l info
```

### Start Celery Beat

```bash
celery -A main beat -l info
```

### Run the development server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

* `POST /api/token/`
* `POST /api/token/refresh/`

### Users

* `GET /api/users/`
* `POST /api/users/`

### Tasks

* `GET /api/tasks/`
* `POST /api/tasks/`
* `GET /api/tasks/<id>/`
* `PUT /api/tasks/<id>/`
* `DELETE /api/tasks/<id>/`

### Notifications

* `GET /notifications/`

### Chat

* Real-time chat using WebSockets.

## Running Tests

```bash
python manage.py test
```

## Future Improvements

* Docker support
* GitHub Actions CI/CD
* PostgreSQL deployment
* Email notifications
* Analytics and reports

## Author

Hasti Panseriya
