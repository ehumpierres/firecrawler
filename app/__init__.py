from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

# Make sure to handle potential missing environment variable
mongodb_uri = os.environ.get('MONGO_URI')
if not mongodb_uri:
    raise ValueError("No MONGO_URI environment variable set")

app.config['MONGO_URI'] = mongodb_uri
mongo = PyMongo(app)
db = mongo.db
