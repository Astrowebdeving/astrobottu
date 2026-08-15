# AstroBot

AstroBot is a Discord trivia bot backed by a Django REST API. Django stores questions and exposes the built-in admin site; a separate `discord.py` process fetches a random question and renders four answer buttons.

This is a small deployment project, not a finished multi-tenant product. The current implementation supports question management, timed games, and read-only leaderboard endpoints. It does not yet persist points from Discord answers to the `Qusers` table.

## Architecture

```text
Discord users
     |
     v
discord.py bot ---- HTTP + X-API-Key ----> Django API ----> SQLite (local)
                                             |              PostgreSQL (AWS)
                                             v
                                      Django admin site
```

The API and bot run as separate processes. In a future distributed deployment, the stateless API can scale independently, while the prefix-command bot should remain a single process unless event handling is redesigned to prevent duplicate responses.

## Implemented behavior

- `a!info` returns the current Discord server ID.
- `a!quest` fetches one active question and accepts one button response per user.
- Each question has a ten-second timeout by default.
- Answer state is scoped to a single question message, so games in different channels do not share state.
- Django admin manages questions, four inline answers, active status, difficulty, points, and leaderboard records.
- `/api/random/` can require a shared `X-API-Key` in deployed environments.

The bot uses `discord.py` 2.7.x. Prefix commands require the Message Content privileged intent. This bot does not require the Server Members intent.

## Local setup

Python 3.12 is the documented runtime.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp env.template .env
python manage.py migrate
python manage.py createsuperuser
```

Start Django in one terminal:

```bash
source .venv/bin/activate
python manage.py runserver
```

Open [http://localhost:8000/admin/](http://localhost:8000/admin/) and add a question with exactly four answers and one correct answer. Then start the bot in a second terminal:

```bash
source .venv/bin/activate
python main.py
```

Set `DISCORD_BOT_TOKEN` in `.env` before starting the bot. `envtoken` remains accepted as a temporary compatibility alias for older local configuration.

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for the full local/admin workflow and [SETUP.md](SETUP.md) for Discord configuration.

## Configuration

| Variable | Process | Required | Purpose |
| --- | --- | --- | --- |
| `DISCORD_BOT_TOKEN` | bot | yes | Discord bot token |
| `API_BASE_URL` | bot | no | Django base URL; defaults to `http://localhost:8000` |
| `BOT_API_KEY` | both | production | Shared key protecting the answer-bearing question endpoint |
| `DJANGO_SECRET_KEY` | API | production | Django signing key |
| `DJANGO_DEBUG` | API | no | Defaults to `true` for local work; set `false` when deployed |
| `DJANGO_ALLOWED_HOSTS` | API | production | Comma-separated hostnames accepted by Django |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | API | public HTTPS only | Comma-separated origins such as `https://bot.example.com` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | API | PostgreSQL only | Remote database connection |

If `DB_HOST` is unset, Django uses SQLite. A future multi-instance deployment should use PostgreSQL instead of a node-local SQLite file.

The repository previously contained default PostgreSQL credentials in `astrobot/settings.py`. They have been removed from the working tree, but they remain in git history. Treat those values as compromised and rotate them if the old database still exists.

## Verification

```bash
python manage.py check
python manage.py test
python -m unittest test_main.py
```

## Known limits

- Scores are displayed from question data but are not written back when a user answers.
- Random selection uses database-side random ordering, which is adequate for the current data size but not efficient for a large question bank.
- The shared API key is a basic service credential, not user authentication or key rotation.
- The Discord process is designed for one replica.
- AWS and Kubernetes infrastructure are intentionally not implemented in this repository yet.
