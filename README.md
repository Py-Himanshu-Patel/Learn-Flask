# Learn-Flask

Learning Flask (python web framework) for APIs and Web Apps.

***

## Setting up Flask and other libraries

Install Flask

```bash
pipenv install flask
```

Install Flask-SQLAlchemy

```bash
pipenv install Flask-SQLAlchemy
```

Install faker to populate database with data

```bash
pipenv install faker
```

To free up PORT even after closing flask server if it's not free. 5000 here is the port we want to free up.

```bash
sudo fuser -k 5000/tcp
```

Start app using `python` and not `flask`

```bash
python App.py   # correct - debug mode is turned ON
flask run       # incorrect - debug mode remain OFF
```

```bash
# set FLASK_DEBUG to 0 or 1 in order to prevent DEBUG mode to be off or on, before running flask app
export FLASK_DEBUG=0
```

Install python-dotenv to use env variables from env files for flask like .env or .flaskenv

```bash
# install lib
pipenv install python-dotenv
```

```bash
# .flaskenv
FLASK_APP=TestApp
FLASK_DEBUG=1
```

To set a port on which to run flask either add it as a command argument or put the in .flaskenv

```bash
flask run --port 8000
```

To make flask ignore dot-env file even if `python-dotenv` is installed.

```bash
# on CLI
export FLASK_SKIP_DOTENV=1
```

## Apps

1. [**User Login: JWT and SQLAlchemy**](./User-Login:%20JWT%20and%20SQLAlchemy/README.md)

    User login API implemented using JWT for token and SQLAlchemy for sqlite3 database.

2. [**Flask: SQLAlchemy and Advanced Database**](./Flask%20:%20SQL_Alchemy/README.md)

    Use SQLAlchemy for sqlite3 database.
