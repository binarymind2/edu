import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, request
from flask_migrate import Migrate

base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

path = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(path, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    quotes = db.relationship('QuoteModel', backref='author', lazy='joined')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        # value = "name"
        # getattr(self, value) --> self.name
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        quotes = self.quotes
        d["quotes"] = [quote.to_dict() for quote in quotes]
        return d


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    quote = db.Column(db.String(255), unique=False)
    rate = db.Column(db.Integer)

    def __init__(self, author, quote):
        self.author = author
        self.quote = quote

    def to_dict(self):
        # value = "name"
        # getattr(self, value) --> self.name
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d

    def __str__(self):
        return f"Quote. Author: {self.author}, q: {self.quote[:10]}..."

    def __repr__(self):
        return self.__str__()


class Author(Resource):
    def get(self, id=None):
        if id == None:
            authors = AuthorModel.query.all()
            return [author.to_dict() for author in authors], 200

        author = AuthorModel.query.get(id)
        if author:
            return author.to_dict(), 200
        return {"message": f"author with id={id} not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        data = parser.parse_args()

        new_author = AuthorModel(data['name'])
        db.session.add(new_author)
        db.session.commit()
        return new_author.to_dict(), 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        data = parser.parse_args()
        author = AuthorModel.query.get(id)
        # print(data)
        # print(author.author)
        if author:
            author.author = data["name"] or author.author
            db.session.commit()
            return author.to_dict(), 200
        return {"message": f"author with id={id} not found"}, 404


class Quote(Resource):
    def get(self, id):
        quote = QuoteModel.query.get(id)
        if quote:
            return quote.to_dict(), 200
        return {"message": f"quote with id={id} not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        data = parser.parse_args()
        # author = request.args.get("author", type=str)
        # quote = request.args.get("quote", type=str)
        # print(author)
        # print(quote)
        new_quote = QuoteModel(**data)
        # new_quote = QuoteModel(author="Ivan", quote="цитата")
        db.session.add(new_quote)
        db.session.commit()
        return new_quote.to_dict(), 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        data = parser.parse_args()
        quote = QuoteModel.query.get(id)
        if quote:
            quote.author = data["author"] or quote.author
            quote.quote = data["quote"] or quote.quote
            db.session.commit()
            return quote.to_dict(), 200
        # ...

    def delete(self, id):
        quote = QuoteModel.query.get(id)
        if quote:
            db.session.delete(quote)
            db.session.commit()
            return quote.to_dict(), 200


class QuoteList(Resource):
    def get(self):
        quotes = QuoteModel.query.all()
        quotes = [quote.to_dict() for quote in quotes]
        return quotes, 200


api.add_resource(QuoteList, "/quotes", "/quotes/filter")  # GET
api.add_resource(Quote, "/quotes/<int:id>", "/quotes")  # GET POST
api.add_resource(Author, "/author/<int:id>", "/author")  # GET POST

if __name__ == '__main__':
    app.run(debug=True)