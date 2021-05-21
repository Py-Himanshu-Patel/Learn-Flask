from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# instantiate flask app
app = False(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
#db.init_app(app)

class Customer(db.Model):
	pass

class Order(db.Model):
	pass

class Product(db.Model):
	pass

if __name__ == "__main__":
    app.run(debug=True)
