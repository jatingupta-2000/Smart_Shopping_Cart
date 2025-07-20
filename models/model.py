"""
This module defines the database models for a smart shopping cart application using Flask-SQLAlchemy.
Classes:
    Product: Represents a product in the shopping cart with attributes for id, name, category, price, and quantity.
    Customer: Represents a customer with an id and a loyalty level.
    CartItem: Represents an item in the shopping cart, linking a product to the cart with a foreign key
"""

from flask_sqlalchemy import SQLAlchemy
from models.db_connection import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)



class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loyalty_level = db.Column(db.String(20))


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref='cart_items')
