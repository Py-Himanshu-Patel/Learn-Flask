import uuid
from functools import wraps
from datetime import datetime, timedelta

import jwt
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "top-secret-key-to-be-kept-in-env-var"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f"{self.name}"


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.text} of user {self.user_id}"


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        # send JWT in Authorization field of header withouf prefix
        # of Bearer or Token

        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token = token.split(" ")[-1]

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid"}), 401

        return func(current_user, *args, **kwargs)

    return wrapper


@app.route("/user", methods=["GET"])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"message": "Not an admin"})

    users = User.query.all()

    # we can't just return the users query object we need to
    # serialize the User object
    output = []
    for user in users:
        user_data = {}
        user_data["name"] = user.name
        user_data["password"] = user.password
        user_data["public_id"] = user.public_id
        user_data["admin"] = user.admin

        output.append(user_data)
    return jsonify({"users": output})


@app.route("/user/<public_id>", methods=["GET"])
@token_required
def get_one_user_(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No such user"})

    user_data = {}
    user_data["name"] = user.name
    user_data["password"] = user.password
    user_data["public_id"] = user.public_id
    user_data["admin"] = user.admin

    return jsonify({"user": user_data})


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="HS256")
    new_user = User(
        public_id=str(uuid.uuid4()),
        name=data["name"],
        password=hashed_password,
        admin=False,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New User Created"})


@app.route("/user/<public_id>", methods=["PUT"])
@token_required
def promote_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No such user"})
    user.admin = True
    db.session.commit()

    return jsonify({"message": "user has beed promoted"})


@app.route("/user/<public_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No such user"})

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user has beed deleted"})


@app.route("/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            "Could not verify your account",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response(
            "Could not verify your account",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )

        return jsonify({"token": token})

    return make_response(
        "Could not verify your account",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


@app.route("/todo", methods=["GET"])
@token_required
def get_all_todos(current_user):
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    output = []

    for todo in todos:
        output.append({"id": todo.id, "task": todo.text, "completed": todo.complete})

    return jsonify({"todos": output})


@app.route("/todo/<todo_id>", methods=["GET"])
@token_required
def get_one_todos(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({"message": "no todo found"})

    data = {"id": todo.id, "task": todo.text, "completed": todo.complete}

    return jsonify(data)


@app.route("/todo", methods=["POST"])
@token_required
def create_todos(current_user):
    data = request.get_json()
    new_todo = Todo(text=data["text"], complete=False, user_id=current_user.id)

    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"message": "Todo created"})


@app.route("/todo/<todo_id>", methods=["PUT"])
@token_required
def complete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({"message": "no todo found"})

    todo.complete = True
    db.session.commit()
    return jsonify({'message': 'Todo item completed'})


@app.route("/todo/<todo_id>", methods=["DELETE"])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({"message": "no todo found"})

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo item deleted'})


if __name__ == "__main__":
    app.run(debug=True)
