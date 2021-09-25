import os
from flask import Flask


def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='DEV_KEY',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)

	if test_config:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db, auth
	db.init_app(app)
	app.register_blueprint(auth.auth_blueprint)

	@app.route('/')
	def hello():
		return "Hello World!"

	return app
