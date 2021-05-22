# Flask : SQL Alchemy Special

A Backend utilising SQL Alchemy and basic concepts of Sqlite3 and database. Thanks to [Pretty Printed](https://courses.prettyprinted.com/courses/)

***

## Create Database

After making models it's time to make database.

Open flask shell. First set env variable. Writing code without `>>>` or `sqlite>` sign to facilitate copy paste of commands. (bash)

```bash
export FLASK_APP=App.py
flask shell
```

Import database and create objects. As soon we hit these commands we notice a db.sqlite appears among files. (flask shell)

```bash
from App import db
db.create_all()
exit()
```

sqlite3 must be pre installed to see the database generated. (bash)

```bash
sqlite3 db.sqlite3
```

Check the database created. Its tables and schema of tables. (sqlite shell)

```sqlite3
sqlite> .tables
customer       order          order_product  product
sqlite> .schema
CREATE TABLE customer (
        id INTEGER NOT NULL, 
        first_name VARCHAR(50) NOT NULL, 
        last_name VARCHAR(50) NOT NULL, 
        address VARCHAR(500) NOT NULL, 
        postcode VARCHAR(10) NOT NULL, 
        email VARCHAR(50) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (email)
);
CREATE TABLE product (
        id INTEGER NOT NULL, 
        name VARCHAR(50) NOT NULL, 
        price INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE TABLE IF NOT EXISTS "order" (
        id INTEGER NOT NULL, 
        order_date DATETIME NOT NULL, 
        shipped_date DATETIME, 
        delivered_date DATETIME, 
        coupon_code VARCHAR(50), 
        customer_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(customer_id) REFERENCES customer (id)
);
CREATE TABLE order_product (
        order_id INTEGER NOT NULL, 
        product_id INTEGER NOT NULL, 
        PRIMARY KEY (order_id, product_id), 
        FOREIGN KEY(order_id) REFERENCES "order" (id), 
        FOREIGN KEY(product_id) REFERENCES product (id)
);
```

To exit. (sqlite shell)

```bash
sqlite> .exit
```

## Insert Data

Inside flask shell. (flask shell)

```bash
from App import db, Product, Customer, Order

# create a customer
john = Customer(first_name='John', 
last_name='Doe', 
address='123 Fake Street',
postcode='123456',
email='john@invalid.com',
)

# add created obj to database and commit
db.session.add(john)
db.session.commit()

exit()
```

Now go check the db.sqlite3 database. (bash shell)

```bash
$ sqlite3 db.sqlite3 
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> 
```

Now check the records inserted. (sqlite shell)

```bash
sqlite> select * from customer;
1|John|Doe|123 Fake Street|123456|john@invalid.com

.exit
```

Create some products. (flask shell)

```bash
computer = Product(name="Laptop", price="50000")
db.session.add(computer)
db.session.commit()

phone = Product(name="apple", price="100000")
db.session.add(phone)
db.session.commit()
```

Check database. (sqlite shell)

```bash
sqlite3 db.sqlite3

sqlite> select * from product;
1|Laptop|50000
2|apple|100000
```

Now put some order into database. (flask shell)

```bash
>>> from App import db, Product, Order
>>> Product.query.all()
[<Product 1>, <Product 2>]
>>> laptop = Product.query.all()[0]
>>> laptop
<Product 1>
>>> phone = Product.query.all()[1]
>>> phone
<Product 2>
>>> phone.name
'apple'
```

We obtained the Product objects from database so as to make an order.

This do not work

```bash
order = Order(coupon_code="FREESHIPPING", customer_id=1, products=[1,2])
```

This works well

```bash
order = Order(coupon_code="FREESHIPPING", customer_id=1, products=[laptop, phone])
```

Commit data into database

```bash
>>> db.session.add(order)
>>> db.session.commit()
```

Check database

```bash
sqlite> .tables
customer       order          order_product  product      
sqlite> select * from order_product;
1|1
1|2
sqlite> select * from 'order';
1|2021-05-22 17:24:50.678658|||FREESHIPPING|1
```

We need to cover 'order' in quotes as its a reserved keyword in sqlite.

## Update Data

Update name of customer. (flask shell)

```bash
>>> from App import db, Customer
>>> Customer.query.all()
[<Customer 1>]
>>> c = Customer.query.all()[0]
>>> c.first_name
'John'
>>> c.first_name = "Pan"
>>> db.session.commit()
>>> exit()
```

Check database. (sqlite shell)

```bash
sqlite> select * from customer;
1|Pan|Doe|123 Fake Street|123456|john@invalid.com
```

## Delete Data

Create a new user

```bash
>>> from App import db, Customer
>>> jane = Customer(
... first_name="Jane",
... last_name="Chan",
... address="123 New Street",
... postcode="123345",
... email="jane@email.com"
... )
>>> jane
<Customer (transient 139732180221088)>
>>> db.session.add(jane)
>>> db.session.commit()
```

```bash
sqlite> select * from customer;
1|Pan|Doe|123 Fake Street|123456|john@invalid.com
2|Jane|Chan|123 New Street|123345|jane@email.com
```

Delete the object. (flask shell)

```bash
>>> from App import db, Customer
>>> jane = Customer.query.filter_by(first_name="Jane")
>>> jane = Customer.query.filter_by(first_name="Jane").first()
>>> jane
<Customer 2>
>>> jane.first_name
'Jane'
>>> db.session.delete(jane)
>>> db.session.commit()
>>> exit()
```

Check database. (sqlite shell)

```bash
sqlite> select * from customer;
1|Pan|Doe|123 Fake Street|123456|john@invalid.com
```

## Queries

Install faker lib. Add fake data to database first. (flask shell)

```bash
>>> from App import db, create_random_data
>>> create_random_data()
>>> exit()
```

Check out the database

```bash
sqlite> select count(*) from customer;
100
```
