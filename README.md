# CivicTrack FS

A community-driven issue reporting platform for the Free State, South Africa —
built entirely with **Python, Django, HTML, and CSS** (no JavaScript), so it's
easy to read, extend, and maintain after the hackathon.

Team: CivicTrack FS

## What it does

- **Report an issue** — residents submit a title, description, category,
  district, optional name, and optional photo.
- **AI-assisted categorisation** — if a resident isn't sure which category
  fits, CivicTrack suggests one automatically from the description using a
  lightweight keyword classifier (`issues/ai.py`). Swap this for a trained
  NLP/ML model later without touching any other code.
- **Community map & feed** — an SVG map of the five Free State district
  municipalities with report markers, plus a filterable feed where residents
  can upvote ("I have this too") and comment on reports.
- **Municipal dashboard** — live counts, four server-rendered charts
  (matplotlib: category breakdown, district breakdown, status donut, and a
  cumulative trend line), and a table officials can use to update status.
- **Two views, one app** — a "Resident" / "Municipal official" switch (stored
  in the session) shows status-editing controls only to officials, without
  needing a full login system for the demo.

No JavaScript is used anywhere: filtering, voting, commenting, and status
updates are all plain HTML `<form>` submissions (GET for filters, POST for
actions), and the comment thread uses the native `<details>`/`<summary>`
disclosure element.

## Project layout

```
civictrack_fs/         Django project settings, root URLs
issues/                 The one Django app that runs everything
  models.py             Report, Comment
  forms.py              ReportForm, CommentForm, StatusUpdateForm
  views.py              All page logic (function-based views)
  ai.py                 suggest_category() — the AI-assisted classifier
  charts.py             matplotlib chart generation for the dashboard
  constants.py           Categories, districts, statuses — single source of truth
  admin.py              Django admin registration
  management/commands/seed_demo_data.py   Loads realistic sample reports
  templates/issues/     All HTML templates
  static/issues/css/    style.css — the only stylesheet
```

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations issues
python manage.py migrate

python manage.py seed_demo_data   # loads ~12 sample reports across the province
python manage.py createsuperuser  # optional, for /admin/

python manage.py runserver
```

Then open http://127.0.0.1:8000/.

- Use the **Resident / Municipal official** switch in the header to try both
  experiences. As a resident you can submit reports, vote, and comment. As an
  official you can additionally change a report's status.
- Visit `/admin/` (after `createsuperuser`) to manage reports and comments
  directly, or to edit a category the AI classifier got wrong.
- Re-run `python manage.py seed_demo_data --flush` at any point to reset the
  demo data.

## Extending it

- **Real GIS coordinates**: `Report.map_x` / `map_y` are illustrative
  positions inside each district's bounding box (see `DISTRICTS` in
  `constants.py`). Swap in real latitude/longitude plus a tile-based map
  (e.g. Leaflet with server-rendered static tiles, or Django GeoDjango +
  PostGIS) when you're ready to move beyond the prototype map.
- **Real AI categorisation**: replace the body of `suggest_category()` in
  `ai.py` with a call to a trained classifier or hosted NLP API. Every
  caller only expects a category id string back (or `None`), so nothing
  else needs to change.
- **PostgreSQL**: the commented-out block in `civictrack_fs/settings.py`
  under `DATABASES` shows the swap from SQLite to PostgreSQL/MySQL for
  production.
- **Authentication**: the Resident/Official toggle is a session flag for
  demo purposes only. Before a real deployment, replace it with Django's
  built-in auth system and `@login_required` / `@permission_required` on
  the officials-only views (`status_update`).

## Before you deploy

This ships with development-friendly defaults. Before putting it in front of
real users:

- Move `SECRET_KEY` into an environment variable and generate a new one.
- Set `DEBUG = False` and list your real domain(s) in `ALLOWED_HOSTS`.
- Serve over HTTPS and enable `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
  `SECURE_SSL_REDIRECT`, and `SECURE_HSTS_SECONDS` (all noted in
  `settings.py`).
- Switch to PostgreSQL (or MySQL) and run `collectstatic` behind a proper
  web server (Nginx/Gunicorn) or a platform like Render, Railway, or an
  Azure/AWS App Service.
- Add authentication for the "Municipal official" role instead of the
  session-based demo switch.
- Consider rate-limiting the report submission and comment endpoints
  (e.g. `django-ratelimit`) to reduce spam/abuse risk.
