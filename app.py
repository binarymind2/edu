from api import api, app
from api.resources.author import AuthorResource, AuthorListResource
from api.resources.quote import QuoteResource, QuoteRatingResource, QuoteListResource, QuotesByAuthorsResource


api.add_resource(AuthorListResource, "/author")  # Все авторы с их цитатами
api.add_resource(AuthorResource, "/author/<int:id>", "/author")  # Тоже вывод цитат по авторам (оставил для себя) и добавление нового автора и редактирвоание текущего

api.add_resource(QuoteListResource, "/quotes")  # Все цитаты
api.add_resource(QuoteResource, "/quotes", "/author/<int:author_id>/quotes")  # Цитаты с методом post и по id автора
api.add_resource(QuoteRatingResource, "/quotes/<int:id>/addrating") # GET
api.add_resource(QuotesByAuthorsResource, "/author/<int:author_id>/quotes/<int:quote_id>")  # работа с цитататами по id автора и id цитаты? Метод Put не работает корректно, пока не смог разобраться по какой причине

if __name__ == '__main__':
    app.run(debug=True)