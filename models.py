from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    addresses = db.relationship('Address', backref='user', lazy=True)
    sports = db.relationship('Sport', secondary='sports_users', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "phone": self.phone,
            "addresses": self.getAddresses()
        }

    def getAddresses(self):
        return list(map(lambda address: address.serialize(), self.addresses))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    user_id = db.Column(db.Integer, ForeignKey('users.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "address": self.address,
            "user_id": self.user_id,
            "user": {
                "name": self.user.name,
                "lastname": self.user.lastname
            }
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True


class Sport(db.Model):
    __tablename__ = "sports"
    id = db.Column(db.Integer, primary_key=True)
    sport_name = db.Column(db.String(200))
    users = db.relationship('User', secondary='sports_users', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "sport_name": self.sport_name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True


class UserSport(db.Model):
    __tablename__ = 'sports_users'
    sport_id = db.Column(db.Integer, ForeignKey('sports.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)