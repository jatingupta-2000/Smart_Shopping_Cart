"""
This module establishes a connection to the database using SQLAlchemy.
Attributes:
    db (SQLAlchemy): An instance of SQLAlchemy used for database operations.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

