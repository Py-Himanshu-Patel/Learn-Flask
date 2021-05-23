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

## Apps

1. [**User Login: JWT and SQLAlchemy**](./User-Login:%20JWT%20and%20SQLAlchemy/README.md)

    User login API implemented using JWT for token and SQLAlchemy for sqlite3 database.

2. [**Flask: SQLAlchemy and Advanced Database**](./Flask%20:%20SQL_Alchemy/README.md)

    Use SQLAlchemy for sqlite3 database.
