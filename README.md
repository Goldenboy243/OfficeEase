# OfficeEase

OfficeEase is a Django learning platform for Microsoft Office skills.

It currently supports:
- Structured learning paths for Word, Excel, and PowerPoint
- Step-by-step progression (theory -> MCQ -> workshop)
- Locked modules that unlock only after required steps are passed
- Workshop file upload and validation for progression
- Multi-language support (English, French, Burmese, Hindi)
- Basic SEO setup (meta tags, sitemap, robots)

## Tech Stack

- Python 3.13
- Django 6.0.x
- SQLite (development)
- Tailwind CSS (via CDN)
- modeltranslation

## Project Structure

- `my_project/` Django project settings and root URLs
- `core/` home/about/how-it-works pages + sitemap and robots view
- `accounts/` authentication and account flow
- `courses/` course models, admin, progression logic, and templates
- `templates/` base layout
- `static/` global static assets
- `locale/` translation files

## Quick Start

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure environment variables.
5. Run migrations.
6. Seed initial structured Word content.
7. Run the server.

### 1) Clone

```bash
git clone https://github.com/Goldenboy243/OfficeEase.git
cd OfficeEase
```

### 2) Virtual Environment (Windows PowerShell)

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

### 3) Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing in your local copy, install at least:

```bash
pip install django==6.0.4 django-modeltranslation deep-translator
```

### 4) Environment Variables

Copy `.env.example` to `.env` and set a strong secret key:

```bash
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
```

`my_project/settings.py` reads:
- `DJANGO_SECRET_KEY` from environment

### 5) Migrate

```bash
python manage.py migrate
```

### 6) Seed Structured Word Modules

```bash
python manage.py seed_structured_word
```

This creates 3 starter modules for Microsoft Word with ordered steps:
- Theory 1
- Theory 2
- MCQ 1
- MCQ 2
- Workshop

### 7) Run Server

```bash
python manage.py runserver
```

App: `http://127.0.0.1:8000/`
Admin: `http://127.0.0.1:8000/admin/`

## Admin Setup

Create a superuser:

```bash
python manage.py createsuperuser
```

Then log in to `/admin/`.

## Learning Flow Rules

For structured courses, learners must pass required steps in order:

1. Theory step(s)
2. MCQ step(s)
3. Workshop upload step

Only after passing required steps does progression unlock the next step/module.

## Workshop Upload Validation

Workshop checks are server-side and include:
- File must be uploaded
- File extension must be `.docx`
- File text is extracted from `word/document.xml`
- Minimum word count check (`workshop_min_words`)
- Required phrase check (`workshop_required_text`)

If validation passes:
- Workshop step is marked passed
- Next step/module unlocks

If validation fails:
- Student gets feedback and remains blocked on that workshop step

## SEO

Implemented SEO features:
- Global metadata in base template
- Per-page title and description blocks
- Canonical URLs
- Open Graph and Twitter tags
- `robots.txt`
- `sitemap.xml`
- Structured data (JSON-LD) for website/course pages

SEO endpoints:
- `/robots.txt`
- `/sitemap.xml`

## Security and Privacy

Repository protections are configured in `.gitignore`:
- `.env` files
- `db.sqlite3`
- `media/` uploads
- `__pycache__/` and `.pyc`
- `.venv/`

Do not commit:
- Real user uploads
- API keys/tokens
- Production secrets

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py seed_structured_word
python manage.py runserver
```

## Notes

- Development currently uses SQLite.
- For production, move to PostgreSQL and use a real file storage strategy for uploads.
- Keep `DEBUG=False` in production and configure allowed hosts and secure settings.
