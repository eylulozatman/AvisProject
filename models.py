from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    cityname = db.Column(db.String(100), nullable=False)

class Office(db.Model):
    __tablename__ = 'office'

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    officename = db.Column(db.String(100), unique=True, nullable=False)

    location = db.relationship("Location", backref="offices")

class Car(db.Model):
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    transmission = db.Column(db.String(100), nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(100), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=False)

    office = db.relationship("Office", backref="cars")
