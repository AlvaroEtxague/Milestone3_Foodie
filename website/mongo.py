import os
from flask import Blueprint
from flask_pymongo import PyMongo
from flask_pymongo.wrappers import MongoClient

if os.path.exists("env.py"):
    import env

mongo = Blueprint("mongo", __name__)

# mapping the mongo cluster from env.py
CLUSTER = os.environ.get("MONGO_URI")

# mapping the db from env.py
DB = os.environ.get("MONGO_DBNAME")

# mapping the collections from env.py
COLLECTION_USERS = "users"
COLLECTION_POSTS = "posts"
COLLECTION_RATINGS = "ratings"
COLLECTION_FAVOURITE = "favourite"

# function to check db connection
def mongo_connect(url):
    # this will display a success message and return the db connection
    try:
        conn = MongoClient(url)
        print("Mongo is connected")
        return conn
    # this will display a failure message
    except PyMongo.errors.ConnectionFailure as e:
        print("Connection failure: %s") % e
