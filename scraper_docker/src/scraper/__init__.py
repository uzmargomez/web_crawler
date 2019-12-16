import scraper_functions
from flask import Flask,request,Response
import logging
import pymongo
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

mongo_server = "mongo"

myclient = MongoClient("mongodb://{}:5003/".format(mongo_server))
mydb = myclient["mydatabase"]
mycol = mydb["prueba"]

app = Flask(__name__)

@app.route("/loading", methods=["GET"])
def scraper():
    logging.info("I will see if there are new articles")

    if request.method == "GET":
        my_list = scraper_functions.extract_articles()
        if len(my_list) > 0:
            x = mycol.insert_many(my_list)
            logging.info("I updated the mongo database")
        else:
            logging.info("No new articles")

        return Response(status=200)

    else:
        logging.info("You screw up")
        return Response(status=400)
