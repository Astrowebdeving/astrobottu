# Discord and application setup

## Discord application

1. Create or select an application in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Add a bot user and copy its token into `.env` as `DISCORD_BOT_TOKEN`.
3. Under **Bot > Privileged Gateway Intents**, enable **Message Content Intent**.
4. Generate an install URL with the `bot` scope. Grant `View Channels`, `Send Messages`, and `Read Message History` in the target server.

The code uses prefix commands through `commands.Bot`, so Message Content is required. Server Members and Presence intents are not used.

## Environment

```bash
cp env.template .env
```

For local development, the minimum useful values are:

```dotenv
DISCORD_BOT_TOKEN=replace-me
API_BASE_URL=http://localhost:8000
DJANGO_DEBUG=true
```

For a deployed API, generate independent values for the Django secret and bot/API shared key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Set the second value as `BOT_API_KEY` on both processes. The bot sends it in `X-API-Key`; Django checks it before returning the answer-bearing question payload.

## Question data contract

Each question used by `a!quest` must have:

- `is_active` enabled;
- exactly four related answers;
- exactly one answer marked correct;
- an integer point value.

Invalid records stay editable in Django admin, but the bot rejects them rather than rendering a broken game.

## Run order

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

After adding a valid question at [http://localhost:8000/admin/](http://localhost:8000/admin/), start the bot in another terminal:

```bash
python main.py
```

## API endpoints

| Path | Method | Description |
| --- | --- | --- |
| `/api/random/` | GET | One random active question; checks `X-API-Key` when configured |
| `/api/topusers/` | GET | Ten users ordered by points descending |
| `/api/allusers/` | GET | All users ordered by points descending |
| `/admin/` | GET/POST | Authenticated Django administration |

## Common failures

`a!quest` does not respond:

- confirm Message Content Intent is enabled in the portal and in code;
- confirm the bot can view and send messages in the channel;
- confirm the command prefix is `a!`.

The bot reports that no question is available:

- check that `python manage.py runserver` is still running;
- check that an active question has four answers and one correct answer;
- confirm both processes have the same non-empty `BOT_API_KEY` in production.
