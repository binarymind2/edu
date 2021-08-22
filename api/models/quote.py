from api import db
from api.models.author import AuthorModel

class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    quote = db.Column(db.String(255), unique=False)
    rate = db.Column(db.Integer)

    def __init__(self, author, quote):
        self.author = author
        self.quote = quote

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d

    def __str__(self):
        return f"Quote. Author: {self.author}, q: {self.quote[:10]}..."

    def __repr__(self):
        return self.__str__()