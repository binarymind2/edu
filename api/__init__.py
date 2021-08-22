import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

base_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False