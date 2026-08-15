# Command reference

## First run

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp env.template .env
python manage.py migrate
python manage.py createsuperuser
```

## Start processes

```bash
# terminal 1
source .venv/bin/activate
python manage.py runserver

# terminal 2
source .venv/bin/activate
python main.py
```

Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Discord commands

| Command | Result |
| --- | --- |
| `a!info` | Current Discord server ID |
| `a!quest` | Four-answer timed trivia question |

## Required Discord setting

Enable **Message Content Intent** in the Discord Developer Portal. The bot does not use Server Members Intent.
