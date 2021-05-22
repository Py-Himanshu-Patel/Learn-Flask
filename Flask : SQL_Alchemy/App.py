from re import M
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from faker import Faker
import random

fake = Faker()

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


# define functions to populate database

def add_customer():
    ''' add 100 customers to database '''
    for _ in range(100):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.street_address(),
            postcode=fake.city(),
            email=fake.email()
        )
        db.session.add(customer)
    db.session.commit()


def add_orders():
    ''' add 1000 orders from random customers '''
    customers = Customer.query.all()

    for _ in range(1000):
        # choose a random customer
        customer =  random.choice(customers)

        ordered_date = fake.date_time_this_year()
        shipped_date = random.choices([
            None,
            fake.date_time_between(start_date=ordered_date)
        ],
        [10, 90]
        )[0]

        # if shipped then check delivered date else None
        delivered_date = None
        if shipped_date:
            delivered_date = random.choices([
                None,
                fake.date_time_between(start_date=shipped_date)
            ],
            [50, 50]
            )[0]
        
        # choose a random coupon out of 4
        coupon_code = random.choices([
            None, 
            '50OFF', 
            'FREESHIPPING', 
            'BUYONEGETONE'
        ],
        [80, 5, 5, 10]
        )[0]

        order = Order(
            customer_id=customer.id,
            order_date=ordered_date,
            shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code
        )

        db.session.add(order)
    db.session.commit()


def add_products():
    for _ in range(10):
        product = Product(
            name=fake.color_name(),
            price=random.randint(10, 100)
        )
        db.session.add(product)
    db.session.commit()

def add_order_products():
    orders = Order.query.all()
    products = Product.query.all()

    for order in orders:
        # select random k in range 1, 2, 3
        k = random.randint(1, 3)
        # select random k products
        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)

    db.session.commit()

def create_random_data():
    # delete the existing database before calling
    # create a new database
    db.create_all()
    add_customer()
    add_products()
    add_orders()


if __name__ == "__main__":
    app.run(debug=True)
