# AstroBot Setup Guide 🤖

## Changes Made to Fix Deprecations

### ✅ Fixed Issues:

1. **Type Hint Errors (CRITICAL FIX)**
   - Changed `discord.ui.button` → `discord.ui.Button` (capital B)
   - This was causing the bot to crash on button interactions
   - Fixed in all 4 button handlers

2. **Security Fix**
   - Removed hardcoded bot token (security risk!)
   - Now properly uses environment variable from .env file
   - Added validation to ensure token exists before running

3. **Dependency Updates**
   - Updated `discord.py` from 2.3.1 → 2.4.0
   - Updated Django from 4.2.3 → 4.2.16 (security patches)
   - Updated all other dependencies to latest stable versions
   - Removed `asyncio==3.4.3` (conflicts with Python's built-in asyncio)

4. **Code Cleanup**
   - Removed unused imports: `guild`, `Client`, `view`, `sleep`
   - Cleaner, more maintainable code

## 🚀 How to Run the Bot

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the project root with:
```
# Discord Bot Token (REQUIRED)
envtoken=YOUR_DISCORD_BOT_TOKEN_HERE

# Django Settings (OPTIONAL - has defaults)
DJANGO_SECRET_KEY=your-secret-key-here

# Database Settings (OPTIONAL - has defaults)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
```

**To get your Discord bot token:**
- Go to https://discord.com/developers/applications
- Select your application (or create one)
- Go to "Bot" section
- Copy the token

**Note:** Database and Django settings have defaults configured, so they're optional unless you want to override them.

### 3. Enable Required Intents
In the Discord Developer Portal:
- Go to your application
- Navigate to "Bot" section
- Enable these **Privileged Gateway Intents**:
  - ✅ MESSAGE CONTENT INTENT (required for `intents.message_content`)
  - ✅ SERVER MEMBERS INTENT (if you need member data)

### 4. Run the Bot
```bash
python main.py
```

## 🎮 Bot Commands

- `a!info` - Shows server ID
- `a!quest` - Starts a trivia question with 4 answer buttons

## 📊 Django API Setup

The bot connects to a Django REST API for questions. To run the Django server:

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 🔧 Troubleshooting

### Bot doesn't respond to commands:
- Ensure MESSAGE CONTENT INTENT is enabled in Discord Developer Portal
- Check that your bot has proper permissions in the server
- Verify the bot token is correct in `.env`

### Button interactions fail:
- This should be fixed now with the `discord.ui.Button` type hint corrections
- Ensure you're using discord.py 2.4.0 or higher

### Database errors:
- Run `python manage.py migrate` to set up the database
- Check that PostgreSQL is running (if using production settings)

## 📝 Notes

- The bot uses a 10-second timeout for questions
- Users can only answer once per question
- Points system is integrated with the Django backend

## ⚠️ IMPORTANT: API Endpoint No Longer Active

**The prior Heroku endpoint was closed, as well as the account.** This code now can be implemented with other options:

**You have 3 options:**

1. **Run Django API locally** (Recommended for testing)
   - See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed instructions
   - Default: `http://localhost:8000`

2. **Deploy to a new Heroku app**
   - Follow the deployment guide in [LOCAL_SETUP.md](LOCAL_SETUP.md)

3. **Deploy to another service** (Railway, Render, DigitalOcean, etc.)

The API endpoint is now configurable via the `API_BASE_URL` environment variable in your `.env` file.



