# Smart Classroom and Timetable Scheduler: Backend

Backend for the Smart Classroom and Timetable Scheduler, built by **Team TENSORS**. The platform automates timetable creation for higher education institutions using constraint-satisfaction algorithms, reducing clashes, balancing faculty workload, and improving classroom utilisation in line with the NEP 2020 multidisciplinary framework.

The frontend lives in a separate repository.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Scheduling Workflow](#scheduling-workflow)
- [Contributing](#contributing)
- [License](#license)

---

## Problem Statement

- Static timetables that cannot react to real-time changes
- Limited classrooms and overlapping schedules
- Faculty constraints and uneven workload distribution
- Complex elective and multidisciplinary course structures
- Manual, error-prone scheduling in spreadsheets

## Solution Overview

A web-based platform that:

- Collects institutional data: faculty, classrooms, subjects, and student groups
- Generates optimised, conflict-free timetables
- Adjusts schedules when circumstances change, such as faculty leave or room unavailability
- Provides role-based dashboards and approval workflows

## Key Features

- Role-based Authentication (Admin, HOD, Faculty, Student)
- Dynamic AI-based Scheduling (Google OR-Tools / OptaPlanner)
- Multi-department & Multi-shift support
- Analytics Dashboard (faculty workload, classroom utilization)
- Real-time timetable updates & conflict resolution
- Export options (PDF/Excel) + Website embedding
- Policy-compliant scheduling (AICTE norms, NEP 2020 ready)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Django 6.1 |
| Database | PostgreSQL (via `psycopg` 3) |
| Configuration | `django-environ` |
| Frontend (separate repo) | React (Vite), Tailwind CSS |
| Scheduling engine | Google OR-Tools, rule-based logic |

## Getting Started

### Prerequisites

- Python 3.12 or newer
- PostgreSQL, running locally on port 5432
- Git

### 1. Clone and install

1. Clone the repository and move into it.
2. Create a virtual environment named `.venv` and activate it.
3. Install dependencies with `pip install -r requirements.txt`.

### 2. Create the database

1. Open `psql` as the `postgres` superuser.
2. Create a database named `scheduler`.
3. Create a role named `tensor` with a password of your choice.
4. Make `tensor` the owner of `scheduler`. On PostgreSQL 15 and newer, this avoids permission errors on the `public` schema during migrations.

### 3. Configure environment variables

1. Copy `.env.example` to `.env` in the repository root, next to `requirements.txt`.
2. Fill in the values:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | A long random string. Do not reuse the example value. |
| `DEBUG` | `True` for local development only |
| `ALLOWED_HOSTS` | Comma-separated hosts, for example `127.0.0.1,localhost` |
| `DB_NAME` | `scheduler` |
| `DB_USER` | `tensor` |
| `DB_PASSWORD` | The password you set for the `tensor` role |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `5432` |

`.env` is gitignored. Never commit it.

### 4. Migrate and run

1. Change into the `src/` directory, where `manage.py` lives.
2. Run `python manage.py migrate`.
3. Run `python manage.py createsuperuser`. A username, a unique email, and a password are required. Superusers receive the `Management` role automatically.
4. Run `python manage.py runserver`.
5. Open `http://127.0.0.1:8000/admin/` and sign in.

## Project Structure

```
.
├── .env.example        # Template for local environment variables
├── requirements.txt    # Pinned Python dependencies
└── src/
    ├── manage.py
    ├── config/         # Project settings, URL configuration, WSGI/ASGI
    └── users/          # Custom User model, manager, admin
```

## Scheduling Workflow

1. **Base generation:** a constraint-satisfaction model (Google OR-Tools) produces the initial timetable.
2. **Incremental updates:** localised changes, such as a single faculty absence, are re-solved without regenerating everything.
3. **Minor adjustments:** a rule-based swapping system handles small corrections.

## Contributing

Team members should read [CONTRIBUTING.md](CONTRIBUTING.md) before starting work. External contributions are not accepted.

## License

This is a proprietary project owned by Team TENSORS. All code, designs, and documentation are the property of the team. Unauthorised use, copying, modification, distribution, or sharing is prohibited.
