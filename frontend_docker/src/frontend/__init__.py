from flask import Flask,jsonify, render_template,request,Response
import pandas as pd
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)

scraper_server = "scraper"
lda_server = "lda"

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template(
            "index.html"
        )

@app.route("/extract", methods=["GET"])
def extract():
    if request.method=="GET":
        logging.info("Extracting ...")
        res = requests.get("http://{}:5002/loading".format(scraper_server))
        if res.status_code < 300:
            logging.info("Finish Extracting ...")
            return Response(status=200)
        else:
            logging.info("There was an error when extracting")
            return Response(status=400)

@app.route("/result", methods=["GET", "POST"])
def get_result_from_model():
    if request.method == "POST":
        logging.info("Going to LDA")
        req = requests.get("http://{}:5001/lda".format(lda_server))
        logging.info("Going back from LDA")
        respuesta = json.loads(req.text)

        df_categories = pd.read_json(respuesta["df_categories"])
        df_classification = pd.read_json(respuesta["df_classification"])
        graphhtml = respuesta["graphhtml"]
        logging.info("I got the resulting dataframes")
        rows_categories, col_categories = df_categories.shape
        rows_classification, col_classification = df_classification.shape

        #********************************************************************
        #       Returning dataframes of categories and news classification
        return render_template("result.html",df_categories=df_categories,df_classification=df_classification,
                                rows_categories=rows_categories,col_categories=col_categories,
                                rows_classification=rows_classification,col_classification=col_classification,graphhtml=graphhtml)

@app.route('/about')
def about_page():

    return render_template('about.html')
