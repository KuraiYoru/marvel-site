from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3

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
    print(Heroes.query.first())
    return 'Hello World!'


def main():
    print(Heroes.query)


if __name__ == '__main__':
    main()

