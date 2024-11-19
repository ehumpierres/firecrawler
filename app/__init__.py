from flask import Flask
from flask_pymongo import PyMongo
from os import environ

app = Flask(__name__)
app.config["MONGODB_URI"] = environ.get("MONGODB_URI")
mongo = PyMongo(app)
db = mongo.db
