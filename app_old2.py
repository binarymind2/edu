import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
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
   surname = db.Column(db.String(32), unique=False)
   quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

   def __init__(self, name, surname):
       self.name = name
       self.surname = surname

class QuoteModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   author_id = author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
   quote = db.Column(db.String(255), unique=False)
   rate = db.Column(db.Integer)

   def __init__(self, author, quote, rate):
       self.author = author
       self.quote = quote
       self.rate = rate

class Quote(Resource):

    @staticmethod
    def to_dict(value, author_id):
        author = AuthorModel.query.all(author_id)
        author = str(author.name) + ' ' + str(author.surname)
        keys = ["id", author, "quote"]
        print('author', author)
        print('keys', keys)
        return dict(zip(keys, value))

    def get(self, id=None):

        if id:
            quote = QuoteModel.query.get(id)
            ret_quote = [quote.id, quote.author, quote.quote]
            ret_quote = Quote.to_dict(ret_quote)
            return ret_quote, 200

        quotes = QuoteModel.query.all()

        # print(quote.id)
        res = []
        for quote in quotes:
            ret_quote = [quote.id, quote.author, quote.quote]
            res.append(Quote.to_dict(ret_quote))

        return res, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        parser.add_argument("quote")
        parser.add_argument("rate")
        data = parser.parse_args()

        print('data', data)
        # new_quote = QuoteModel(data['author'], data['quote'])

        if data['name'] and data['surname']:
            authors = AuthorModel.query.all()
            if len(authors) > 0:
                for author in authors:
                    if author.name == data['name'] and author.surname == data['surname']:
                        author_id = author.id
                        break
            else:
                author = AuthorModel(data['name'], data['surname'])
                db.session.add(author)
                db.session.commit()
                author_id = author.id


        # new_quote = QuoteModel(author.id, data['quote'], data['rate'])

        # db.session.add(new_quote)
        # db.session.commit()

        # get_new_quote = Quote.to_dict([new_quote.id, new_quote.quote], author.id)

        return "", 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        data = parser.parse_args()

        ch_quote = QuoteModel.query.get(id)
        if data['author']:
            ch_quote.author = data['author']
            db.session.commit()
        if data['quote']:
            ch_quote.quote = data['quote']
            db.session.commit()

        ch_quote = Quote.to_dict([ch_quote.id, ch_quote.author, ch_quote.quote])
        return ch_quote, 201

    def delete(self, id):
        del_quote = QuoteModel.query.get(id)
        db.session.delete(del_quote)
        db.session.commit()
        return "Deleted", 200


api.add_resource(Quote, "/quotes/<int:id>", "/quotes")  # GET POST
if __name__ == '__main__':
    app.run(debug=True)