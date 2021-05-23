from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

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


@app.route("/user", methods=["GET"])
def get_all_users():
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
def get_one_user_(public_id):
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
    hashed_password = generate_password_hash(data["password"], method="sha256")
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
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No such user"})
    user.admin = True
    db.session.commit()

    return jsonify({"message": "user has beed promoted"})


@app.route("/user/<public_id>", methods=["DELETE"])
def delete_user(public_id):
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
        token = jwt


if __name__ == "__main__":
    app.run(debug=True)
