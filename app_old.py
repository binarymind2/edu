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
# Нужно больше цитат? https://tproger.ru/devnull/programming-quotes/

for quote in quotes:
    quote['rating'] = 1

# Resource(Ресурс)
class Quote(Resource):
   def get(self, id=0):
       """
       Обрабатываем GET запросы
       :param id: id цитаты
       :return: http-response("текст ответа", статус)
       """

       if id == 0:
           return quotes[random.randrange(0,len(quotes))]

       for quote in quotes:
           if quote["id"] == id:
               return quote, 200
       return "Quote not found", 404

   def post(self):
       parser = reqparse.RequestParser()
       parser.add_argument("author")
       parser.add_argument("quote")
       parser.add_argument("rating")
       new_quote = dict(parser.parse_args())
       new_quote["id"] = quotes[-1]["id"] + 1
       quotes.append(new_quote)
       # print("params = ", params)
       # print("params = ", type(params))
       return new_quote, 201

   def put(self, id):
       parser = reqparse.RequestParser()
       parser.add_argument("author")
       parser.add_argument("quote")
       parser.add_argument("rating")
       params = dict(parser.parse_args())

       quotefind = False
       for quote in quotes:
           if id == quote['id']:
               print(quote)
               print(params['author'])
               quotefind = True
               quote['author'] = params['author']
               quote['quote'] = params['quote']
               quote['rating'] = params['rating']
               return quote, 200

       if quotefind == False:
           new_quote = params
           new_quote["id"] = quotes[-1]["id"] + 1
           quotes.append(new_quote)
           return new_quote, 201

   def delete(self, id):
       i = 0
       for quote in quotes:
           i += 1
           if id == quote['id']:
               del quotes[i-1]

       return f"Quote with id {id} is deleted.", 200



class QuoteList(Resource):
   def get(self):
       parser = reqparse.RequestParser()
       parser.add_argument("author")
       parser.add_argument("quote")
       data = parser.parse_args()
       print(data)

       return quotes, 200

class QuoteCount(Resource):
   def get(self):
       return {"count": len(quotes)}

# Route(Маршрут)
api.add_resource(QuoteList, "/quotes", "/quotes/filter")  # GET
api.add_resource(Quote, "/quotes/<int:id>", "/quotes")  # GET POST
api.add_resource(QuoteCount, "/count-quotes")  # GET

if __name__ == '__main__':
   app.run(debug=True)