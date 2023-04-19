from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

association_table = db.Table(
    "heroes_comics",
    db.metadata,
    db.Column("hero_id", db.ForeignKey("heroes.hero_id"), primary_key=True),
    db.Column("comics_id", db.ForeignKey("comics.comics_id"), primary_key=True),
)


class Heroes(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer,
                    primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    img = db.Column(db.String)
    hero_id = db.Column(db.Integer, unique=True)
    comics = db.relationship("Comics", lazy='dynamic', secondary=association_table, backref=db.backref('heroes', lazy='dynamic'))

    def __repr__(self):
        return f"{self.name}%r" % self.id


class Comics(db.Model):
    __tablename__ = 'comics'

    id = db.Column(db.Integer,
                           primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    comics_id = db.Column(db.Integer, unique=True)
    img = db.Column(db.String)

    def __repr__(self):
        return f"{self.title}%r" % self.id


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    email = db.Column(db.String(80))
    user_name = db.Column(db.String(80))
    data = db.Column(db.LargeBinary)
    hashed_password = db.Column(db.String(80))
    created_date = db.Column(db.DateTime,
                             default=datetime.now)

    def hash_password(self):
        self.hashed_password = generate_password_hash(self.hashed_password)

    def __repr__(self):
        return f'<User {self.user_name}>'

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

