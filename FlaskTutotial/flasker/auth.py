import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flasker.db import get_db

auth_blueprint = Blueprint('authentication', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['POST', 'GET'])
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
				# name_of_blueprint.name_of_view_function
				return redirect(url_for("authentication.login"))
		
		flash(error)

	return render_template('auth/register.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		db = get_db()
		error = None
		user = db.execute(
			"SELECT * FROM user WHERE username = ?", (username,)
		).fetchone()

		if user is None:
			error = 'Incorrect Username'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password'
		
		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')


@auth_blueprint.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()


@auth_blueprint.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			# name_of_blueprint.name_of_view_function
			return redirect(url_for('authentication.login'))
		return view(**kwargs)
	return wrapped_view
