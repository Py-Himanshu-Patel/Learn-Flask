from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# instantiate flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
# db.init_app(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    # let field 'order' refer 'Order' table, to all the orders customer had made
    # and backref means any order obj can refer to its customer using '.customer' 
    orders = db.relationship("Order", backref="customer")


# association table
# first arg: name of table
order_product = db.Table('order_product',
    # if we have multiple primary keys then it's a composite primary key
    # we can we they in a combined way to make a primary key

    # col name, col datatype, foreign key, other constaint
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))

    # put reference model name in lowercase followed by field name
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    # to get all products included in one order
    products = db.relationship('Product', secondary=order_product)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)


if __name__ == "__main__":
    app.run(debug=True)
