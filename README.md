# AstroBot Tu 🤖

A Discord trivia bot powered by Django REST API.

## ⚡ Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file with your bot token:**
   ```bash
   cp env.template .env
   # Then edit .env and add your Discord bot token
   ```

3. **⚠️ IMPORTANT: Set up the Django API first!**
   
   The old Heroku endpoint is no longer active. You need to either:
   - **Run Django locally** (easiest): See [LOCAL_SETUP.md](LOCAL_SETUP.md)
   - Deploy to a new hosting service
   
   ```bash
   # Quick local setup:
   python manage.py migrate
   python manage.py runserver  # Keep this running in Terminal 1
   ```

4. **Run the bot (in a new terminal):**
   ```bash
   python main.py
   ```

📖 **For detailed setup instructions, see [SETUP.md](SETUP.md)**

🏠 **For API setup instructions, see [LOCAL_SETUP.md](LOCAL_SETUP.md)**

## 🎮 Commands

- `a!info` - Display server information
- `a!quest` - Start a trivia question

## 🔧 Recent Fixes (November 2024)

### Discord Bot:
✅ Fixed discord.py deprecations (updated to 2.4.0)  
✅ Fixed UI button type hints  
✅ Fixed security issue with hardcoded token  
✅ Cleaned up unused imports

### Security & Dependencies:
✅ **Already using Django 4.2.16 LTS** (latest, secure until 2026)  
✅ **Zero SQL injection vulnerabilities** (all queries use Django ORM)  
✅ Updated aiohttp, psycopg2, yarl (actual security fixes)  
ℹ️ Dependabot warnings are mostly low-risk static files (see [VULNERABILITY_SUMMARY.md](VULNERABILITY_SUMMARY.md))
