# 🏠 Running Django API Locally

Since the Heroku endpoint is no longer active, you'll need to run the Django API locally or deploy it somewhere.

## Quick Local Setup

### 1. Run Migrations
```bash
cd /Users/tu15/Documents/AstrobotTu/astrobottu
python manage.py migrate
```

### 2. Create a Superuser (Optional - for admin access)
```bash
python manage.py createsuperuser
```

### 3. Add Some Test Questions via Django Admin
```bash
python manage.py runserver
# Then visit: http://localhost:8000/admin
```

### 4. Update API Endpoint in main.py

Change these lines in `main.py`:

**Line 18 - Change FROM:**
```python
response = requests.get("https://mysterious-headland-81216-a50424fcfa47.herokuapp.com/api/random/")
```

**TO:**
```python
response = requests.get("http://localhost:8000/api/random/")
```

**Line 33 - Change FROM:**
```python
response = requests.get("https://mysterious-headland-81216-a50424fcfa47.herokuapp.com/api/allusers/")
```

**TO:**
```python
response = requests.get("http://localhost:8000/api/allusers/")
```

### 5. Run Both Services

**Terminal 1 - Django API:**
```bash
python manage.py runserver
```

**Terminal 2 - Discord Bot:**
```bash
python main.py
```

---

## 🌐 Alternative: Deploy to New Heroku App

### 1. Install Heroku CLI
```bash
brew install heroku/brew/heroku
```

### 2. Login and Create App
```bash
heroku login
heroku create your-astrobot-api
```

### 3. Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

### 4. Deploy
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 5. Update main.py with new URL
Replace the old Heroku URL with your new one.

---

## 🐳 Alternative: Use Docker (Advanced)

Coming soon...

---

## 📝 Using SQLite Instead of PostgreSQL (Simplest)

If you don't need PostgreSQL, you can switch to SQLite for local development:

**Edit `astrobot/settings.py`:**
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

This avoids needing PostgreSQL installed locally!

