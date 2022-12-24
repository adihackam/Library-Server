
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Books(db.Model):
    id = db.Column('book_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    year_published = db.Column(db.Integer)
    type = db.Column(db.Integer)

    def __init__(self, name, author, year_published, type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = type


class Customers(db.Model):
    id = db.Column('customer_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age


class Loans(db.Model):
    id = db.Column('loan_id', db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    loan_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    def __init__(self, customer_id, book_id, loan_date,return_date ):
        self.customer_id = customer_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date
