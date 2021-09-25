import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.user_agent import UserAgent
from flasker.db import db, get_db

auth_blueprint = Blueprint('authentication', __name__, url_prefix='/auth')


@auth_blueprint('/register', method=['POST', 'GET'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = "Username is not defined"
		if not password:
			error = "Password is required"

		if error is None:
			try:
				db.execute(
					"INSERT INTO user (username, password) VALUES (?, ?)",
					(username, generate_password_hash(password))
				)
				db.commit()
			except db.IntegrityError:
				error = f"User {username} is already registered"
			else:
				return redirect(url_for("authentication.login"))
		
		flash(error)

	return render_template('auth/register.html')
