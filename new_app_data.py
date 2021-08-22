import os
import sqlite3
from flask import Flask
from flask_restful import Api, Resource, reqparse, output_json

base_dir = os.path.dirname(os.path.abspath(__file__))



app = Flask(__name__)
api = Api(app)

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
        data = parser.parse_args()

        author = data['author']
        db_quote = data['quote']
        query = f"INSERT INTO quotes (author, quote) VALUES ('{author}', '{db_quote}'"
        path = os.path.join(base_dir, "db.sqlite")
        connect = create_connection(path)
        execute_query(connect, query)

        query = f"SELECT * FROM quotes WHERE quote={data['quote']}"

        new_quote = execute_read_query(connect, query)

        # print("params = ", params)
        # print("params = ", type(params))
        return new_quote, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        data = parser.parse_args()
        # print("data = ", data)
        quote = self.find_by_id(id)
        if quote:
            quote["author"] = data["author"] or quote["author"]
            quote["quote"] = data["quote"] or quote["quote"]
            return quote, 200
        new_quote = data
        new_quote["id"] = quotes[-1]["id"] + 1
        quotes.append(new_quote)
        return new_quote, 201

    def delete(self, id):
        quote = self.find_by_id(id)
        if quote:
            quotes.remove(quote)
            return quote, 200
        return f"Quote with id {id} not found.", 404

def create_connection(path):
   try:
       print("Connection to SQLite DB successful")
       return sqlite3.connect(path)
   except Error as e:
       print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
   """
   принимает объект connection и SELECT-запрос, а возвращает выбранную запись
   """
   cursor = connection.cursor()
   try:
       cursor.execute(query)
       result = cursor.fetchall()
       return result
   except Error as e:
       print(f"The error '{e}' occurred")

def execute_query(connection, query):
   cursor = connection.cursor()
   try:
       cursor.executescript(query)
       connection.commit()
       print("Query executed successfully")
   except Error as e:
       print(f"The error '{e}' occurred")


api.add_resource(Quote, "/quotes/<int:id>", "/quotes")  # GET POST

if __name__ == '__main__':
    app.run(debug=True)