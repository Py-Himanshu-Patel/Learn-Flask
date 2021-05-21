from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SECRET_KEY"] = "top-secret-key-to-be-kept-secret-in-env-var"
db = SQLAlchemy(app)
# db.init_app(app)
# db.create_all()


class User(db.Model):
	# id column is compulsory while making model in flask
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    todos = db.relationship('ToDo', backref='user')


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



@app.route("/user", methods=["GET"])
def get_all_users():
	users = User.query.all()
	output = []
	for user in users:
		user_data = {}
		user_data['public_id'] = user.public_id
		user_data['name'] = user.name
		user_data['password'] = user.password
		user_data['admin'] = user.admin
		output.append(user_data)
	return jsonify({"users": output})


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user():
    return ""


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()  # get json data from request
    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_user = User(
        public_id=str(uuid.uuid4()),
        name=data["name"],
        password=hashed_password,
        admin=False,
    )

    # add user to sessions
    db.session()
    db.session.commit()
    return jsonify({"message": "New User Created"})


@app.route("/user/<user_id>", methods=["PUT"])
def promote_user():
    return ""


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user():
    return ""


if __name__ == "__main__":
    app.run(debug=True)
