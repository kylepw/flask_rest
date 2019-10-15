from flask import Flask
from flask_pymongo import PyMongo
from flask_rest.utils import MongoJSONEncoder


app = Flask(__name__)
mongo = PyMongo(app, uri='mongodb://localhost:27017/shops')
app.json_encoder = MongoJSONEncoder


import flask_rest.views