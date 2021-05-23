# User Login : Using JWT and SQLAlchemy

Install PyJWT

```bash
pipenv install pyjwt
```

Enter flask shell

```bash
flask shell
```

Then initialize the database based on the models created in App.py

```bash
>>> from App import db
>>> db.create_all()
>>> exit()
```

After database gets created use sqlite installed on linux to open and explore the database.sqlite creaed now.

```bash
$ sqlite3 database.sqlite3
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
```

Inside sqlite shell type

```bash
sqlite> .tables
to_do  user
```

See the schema generated in MySQL format

```bash
sqlite> .schema
CREATE TABLE user (
        id INTEGER NOT NULL, 
        public_id VARCHAR(50), 
        name VARCHAR(50), 
        password VARCHAR(80), 
        admin BOOLEAN, 
        PRIMARY KEY (id), 
        UNIQUE (public_id)
);
CREATE TABLE to_do (
        id INTEGER NOT NULL, 
        text VARCHAR(50), 
        complete BOOLEAN, 
        user_id INTEGER, 
        PRIMARY KEY (id)
);
```
