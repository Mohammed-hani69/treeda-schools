![Treeda Expo](treeda%20schools.png)

# Treeda Expo — School Exhibition Platform

**Treeda Expo** is a bilingual (Arabic/English) virtual school exhibition platform built with Flask. It enables schools to create rich digital profiles, showcase facilities through media galleries, and connect directly with parents and students.

## Features

- **School Profiles** — Cover images, logos, galleries, videos, activities, services, grades, and contact info
- **Smart Filtering & Search** — Filter schools by type, city, gender, or keyword
- **Subscription Plans** — Tiered plans with configurable limits (images, videos, storage, employees)
- **Admin Dashboard** — Full CRUD for schools, plans, subscriptions, categories, homepage sections, gallery, testimonials, FAQs, and more
- **Parent Dashboard** — Browse schools, view details, and connect with administration
- **Bilingual UI** — Full Arabic/English support with instant language switching
- **Responsive Design** — Modern, mobile-first interface with dark/light theme toggle
- **AI Assistant** — Built-in chatbot for user inquiries
- **Permission System** — Per-plan limits enforced on uploads (images, videos, storage)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, Flask 3.1 |
| ORM | SQLAlchemy + Flask-Migrate |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Bootstrap 5.3 RTL, Chart.js, AOS animations |
| Templates | Jinja2 |
| Auth | Flask-Login, bcrypt |
| Caching | Flask-Caching |
| Icons | Bootstrap Icons |

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd school_exhibition

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env   # Edit variables as needed

# Run database migrations
flask db upgrade

# Seed admin account
python seed.py

# Start development server
python run.py
```

The app will be available at `http://127.0.0.1:5000`.

### Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@school-exhibition.com` | `admin123` |
| School | `gov1@school.com` … `gov6@school.com` | `school123` |

## Project Structure

```
school_exhibition/
├── app/
│   ├── admin/            # Admin Blueprint routes
│   ├── api/              # REST API endpoints
│   ├── forms/            # WTForms definitions
│   ├── models/           # SQLAlchemy models
│   ├── parent/           # Parent Blueprint routes
│   ├── routes/           # Main routes
│   ├── school/           # School Blueprint routes
│   ├── services/         # Business logic layer
│   ├── static/           # CSS, JS, uploads
│   ├── templates/        # Jinja2 templates
│   ├── translations/     # Bilingual JSON files
│   └── utils/            # Helpers, decorators, translations
├── migrations/           # Alembic migration files
├── instance/             # SQLite database (dev)
├── config.py             # App configuration
├── run.py                # Entry point
├── seed.py               # Database seeder
└── wsgi.py               # Production WSGI entry
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/schools` | List approved schools |
| GET | `/api/schools/<id>` | School details |
| GET | `/api/categories` | List categories |
| GET | `/api/plans` | List active plans |

## Configuration

Key environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///school_exhibition.db` |
| `MAIL_SERVER` | SMTP server for emails | `smtp.gmail.com` |
| `MAIL_USERNAME` | SMTP username | — |
| `MAIL_PASSWORD` | SMTP password | — |
| `UPLOAD_FOLDER` | Media upload path | `app/static/uploads` |
| `MAX_CONTENT_LENGTH` | Max upload size (bytes) | `52428800` (50MB) |

## License

Copyright © 2026 **Hany Zezo**. All rights reserved.

This software and its source code are the intellectual property of **Hany Zezo**.  
Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited without prior written consent from the author.

**No permission is granted** to any person or entity to copy, modify, merge, publish, distribute, sublicense, or sell copies of this software without explicit written authorization.

---

## Contact

**Developer:** Hany Zezo

- **Email:** [hanizezo72@gmail.com](mailto:hanizezo72@gmail.com)
- **Phone:** [+201145425207](tel:+201145425207)

---

*Built with dedication by Hany Zezo — Treeda Expo Platform © 2026*
