# Local API and admin access

Local development uses SQLite unless `DB_HOST` is set. No local PostgreSQL service is required.

## Native Python

From the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp env.template .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [http://localhost:8000/admin/](http://localhost:8000/admin/) and sign in with the superuser you created. Under **Questions**, add a title, point value, difficulty, active status, and four answers. Mark exactly one answer correct.

The admin site is an internal control interface for question and leaderboard data. It is not a public player-facing site.

## Run the API and bot separately

API terminal:

```bash
source .venv/bin/activate
python manage.py runserver
```

Bot terminal:

```bash
source .venv/bin/activate
python main.py
```

Useful checks:

```bash
curl -H "X-API-Key: $BOT_API_KEY" http://localhost:8000/api/random/
python manage.py check
python manage.py test
```
