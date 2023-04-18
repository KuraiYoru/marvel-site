from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marvel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
    comics = db.relationship("Comics", secondary=association_table, backref='heroes')

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
        return f"{self.title}" % self.id


@app.route('/')
def hello_world():
    # con = sqlite3.connect('marvel.db')
    # cur = con.cursor()
    # print(cur.execute('select * from heroes').fetchall())
    # heroes = Heroes.query.paginate(page=1, per_page=10)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    heroes = Heroes.query
    pages = heroes.paginate(page=page, per_page=24)
    return render_template('index.html', pages=pages)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()

