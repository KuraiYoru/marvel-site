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
    comics = db.relationship("Comics", secondary=association_table, backref='heroes', lazy='dynamic')

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

