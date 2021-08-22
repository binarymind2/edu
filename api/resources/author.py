from flask_restful import Resource, reqparse
from api.models.author import AuthorModel
from api import db

class AuthorResource(Resource):
    def get(self, id):
        author = AuthorModel.query.get(id)
        if author:
            return author.to_dict(), 200
        return {"message": f"quote with id={id} not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        author_data = parser.parse_args()
        new_author = AuthorModel(**author_data)
        db.session.add(new_author)
        db.session.commit()
        return new_author.to_dict(), 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        data = parser.parse_args()
        author = AuthorModel.query.get(id)
        if author:
            author.name = data["name"] or author.name
            author.surname = data["surname"] or author.surname
            db.session.commit()
            return author.to_dict(), 200
        else:
            new_author = AuthorModel(**data)
            db.session.add(new_author)
            db.session.commit()
            return new_author.to_dict(), 200

    def delete(self, id):
        author = AuthorModel.query.get(id)
        if author:
            db.session.delete(author)
            db.session.commit()
            return author.to_dict(), 200
        return "Not found", 404

class AuthorListResource(Resource):
    def get(self):
        authors = AuthorModel.query.all()
        authors = [author.to_dict() for author in authors]
        return authors, 200