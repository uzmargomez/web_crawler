import lda_functions
from flask import Flask,jsonify, render_template,request,Response
import json
import logging


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/lda", methods = ["GET", "POST"])
def get_result_from_model():
    if request.method == "GET":
        logging.info("Starting LDA")

        #********************************************************************
        #       Returning dataframes of categories and news classification

        [df_categories, df_classification,graphhtml] = lda_functions.model_function()

        logging.info("Getting categories and classification dataframes")

        return json.dumps({
            "df_categories": df_categories.to_json(),
            "df_classification": df_classification.to_json(),
            "graphhtml": graphhtml,
            })
