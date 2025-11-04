# 🚀 Quick Reference Card

## ✅ Your .env File Setup

### 1. Create the .env file:
```bash
cd /Users/tu15/Documents/AstrobotTu/astrobottu
cp env.template .env
```

### 2. Edit .env and add your token:
```bash
# Open in any text editor
nano .env
# OR
open .env
# OR
code .env
```

### 3. Minimum required in .env:
```
envtoken=YOUR_DISCORD_BOT_TOKEN_HERE
API_BASE_URL=http://localhost:8000
```

---

## 🔒 Git Protection Status

✅ **CONFIRMED: `.env` is in `.gitignore`**

Your `.env` file **WILL NOT be pushed** to GitHub/Git! ✅

```
.gitignore contains: .env
Status: ✅ Protected
```

To double-check anytime:
```bash
git status --ignored
# .env should show as "Ignored files"
```

---

## 🏃 Running the Complete App

### Terminal 1 - Django API:
```bash
cd /Users/tu15/Documents/AstrobotTu/astrobottu
python manage.py migrate  # First time only
python manage.py runserver
```

### Terminal 2 - Discord Bot:
```bash
cd /Users/tu15/Documents/AstrobotTu/astrobottu
python main.py
```

---

## 📝 Environment Variables Reference

| Variable | Required? | Default | Description |
|----------|-----------|---------|-------------|
| `envtoken` | ✅ YES | None | Discord bot token |
| `API_BASE_URL` | No | `http://localhost:8000` | Django API endpoint |
| `DJANGO_SECRET_KEY` | No | Built-in default | Django secret key |
| `DB_NAME` | No | Built-in default | Database name |
| `DB_USER` | No | Built-in default | Database user |
| `DB_PASSWORD` | No | Built-in default | Database password |
| `DB_HOST` | No | Built-in default | Database host |
| `DB_PORT` | No | `5432` | Database port |

---

## 🎯 Common Tasks

### Get Discord Bot Token:
1. Go to https://discord.com/developers/applications
2. Select your application (or create one)
3. Go to "Bot" tab
4. Click "Reset Token" or "Copy"
5. Paste into `.env` file

### Enable Bot Intents (Required!):
1. Go to https://discord.com/developers/applications
2. Select your application
3. Go to "Bot" tab
4. Scroll to "Privileged Gateway Intents"
5. Enable: ☑️ MESSAGE CONTENT INTENT
6. Enable: ☑️ SERVER MEMBERS INTENT
7. Click "Save Changes"

### Test API Locally:
```bash
# While Django is running:
curl http://localhost:8000/api/random/
```

### Add Questions via Django Admin:
```bash
python manage.py createsuperuser  # First time only
python manage.py runserver
# Visit: http://localhost:8000/admin
```

---

## 🔴 Troubleshooting

### Bot says "Bot token not found!":
- Make sure `.env` file exists
- Make sure it has `envtoken=YOUR_TOKEN`
- No quotes needed around the token

### Bot doesn't respond to commands:
- Enable MESSAGE CONTENT INTENT in Discord Developer Portal
- Invite bot with proper permissions (Send Messages, Read Messages)
- Check that prefix is `a!` (e.g., `a!quest`)

### API connection errors:
- Make sure Django is running (`python manage.py runserver`)
- Check `API_BASE_URL` in `.env` matches Django URL
- Run migrations: `python manage.py migrate`

---

## 📄 Documentation Files

- `README.md` - Project overview and quick start
- `SETUP.md` - Detailed setup instructions
- `LOCAL_SETUP.md` - How to run Django API locally
- `QUICK_REFERENCE.md` - This file!
- `env.template` - Template for .env file

---

## 🎉 You're All Set!

Once you have:
1. ✅ Created `.env` with your Discord token
2. ✅ Run `python manage.py migrate`
3. ✅ Started Django API (`python manage.py runserver`)
4. ✅ Started Discord bot (`python main.py`)

Your bot should be online and ready to use! 🤖

