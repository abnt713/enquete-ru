from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object('enqueteru.config.DevelopmentConfig')

db = MongoAlchemy(app)
api = Api(app)