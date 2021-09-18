from flask import Flask

app = Flask(__name__)

FLASK_DEBUG=0

@app.route('/')
def hello_world():
	return "<p>Hello Flask</p>"


if __name__ == "__main__":
	app.run(debug=True)
