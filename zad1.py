from flask import Flask
from flask_restful import Api, Resource, reqparse, output_json
import random


class UnicodeApi(Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app.config['RESTFUL_JSON'] = {
            'ensure_ascii': False,
        }


app = Flask(__name__)
api = UnicodeApi(app)

quotes = [
    {
        "id": 1,
        "author": "Rick Cook",
        "quote": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "quote": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "quote": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "quote": "В теории, теория и практика неразделимы. На практике это не так."
    },

]

for quote in quotes:
    quote['rating'] = '1'

# Нужно больше цитат? https://tproger.ru/devnull/programming-quotes/

# Resource(Ресурс)
class Quote(Resource):
    def find_by_id(self, id):
        for quote in quotes:
            if quote["id"] == id:
                return quote
        return None

    def get(self, id):
        """
        Обрабатываем GET запросы
        :param id: id цитаты
        :return: http-response("текст ответа", статус)
        """
        
        if id == 0:
            return random.choice(quotes), 200
        quote = self.find_by_id(id)
        if quote:
            return quote, 200
        return "Quote not found", 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        parser.add_argument("rating")
        new_quote = parser.parse_args()
        new_quote["id"] = quotes[-1]["id"] + 1
        if not new_quote['rating']:
            new_quote['rating'] = '1'
        quotes.append(new_quote)
        return new_quote, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        parser.add_argument("rating")
        data = parser.parse_args()

        quote = self.find_by_id(id)
        if quote:
            quote["author"] = data["author"] or quote["author"]
            quote["quote"] = data["quote"] or quote["quote"]
            quote["rating"] = data["rating"] or quote["rating"]
            return quote, 200
            
        new_quote = data
        new_quote["id"] = quotes[-1]["id"] + 1
        
        if not new_quote['rating']:
            new_quote['rating'] = '1'
        quotes.append(new_quote)
        return new_quote, 201

    def delete(self, id):
        quote = self.find_by_id(id)
        if quote:
            quotes.remove(quote)
            return quote, 200
        return f"Quote with id {id} not found.", 404


class QuoteRating(Resource):
    def find_by_id(self, id):
        for quote in quotes:
            if quote["id"] == id:
                return quote
        return None
    
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("rating")
        rating = parser.parse_args()
        quote = self.find_by_id(id)
        if quote:
            quote["rating"] = rating["rating"] or quote["rating"]
            return quote, 200
        return f"Quote with id {id} not found.", 404

class QuoteList(Resource):
    def quote_filter(self, key, value):
        res = []
        for quote in self.quotes_list:
            if quote[key] == value:
                res.append(quote) 
 
        return res
        
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        parser.add_argument("rating")
        quote_param = parser.parse_args()
        
        if quote_param["author"] or quote_param["quote"] or quote_param["rating"]:
            self.quotes_list = quotes
            
            for k, v in quote_param.items():
                if v:
                    self.quotes_list = self.quote_filter(k, v)
            
            return self.quotes_list
        
        return quotes, 200

class QuoteCount(Resource):
    def get(self):
        return {"count": len(quotes)}, 200

    # Route(Маршрут)

api.add_resource(QuoteList, "/quotes", "/quotes/filter")  # GET
api.add_resource(Quote, "/quotes/<int:id>", "/quotes", "/quotes/<int:id>/rating")  # GET POST PUT
api.add_resource(QuoteRating, "/quotes/<int:id>/rating2")  # PUT
api.add_resource(QuoteCount, "/count-quotes")  # GET

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=65421)