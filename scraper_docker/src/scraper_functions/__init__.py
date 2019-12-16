import time
import logging
from newspaper import Article
import newspaper
from datetime import datetime
from pymongo import MongoClient
from time import sleep
import json

logging.basicConfig(level=logging.INFO)

mongo_server = "mongo"

myclient = MongoClient("mongodb://{}:5003/".format(mongo_server))
mydb = myclient["mydatabase"]
mycol = mydb["prueba"]

#web_news = {'theguardian': 'https://www.theguardian.com/international/'}
web_news = {'huffpost': 'https://www.huffpost.com/','theguardian': 'https://www.theguardian.com/international/', 'latimes':'https://www.latimes.com/'}
def retrieve_elements(article):
    try:
        article.download()
        article.parse()
        return article
    except Exception as e:
        logging.info(e)
        logging.info(f"Failed fetching url {article}. Retrying in 10 seconds")
        #sleep(10)
        #return retrieve_elements(article)

def extract_articles():
    newspapers = []
    for company, link in web_news.items():
        i = 0
        paper = newspaper.build(link, memoize_articles=True)
        for content in paper.articles:
            content = retrieve_elements(paper.articles[i])
            if content is not None:
                i = i + 1
                if content.publish_date is None:
                    logging.info(f"nonetype {content.publish_date}")
                    continue
                elif content.publish_date.strftime("%Y%m%d") == datetime.today().strftime("%Y%m%d"):
                    logging.info(f"Downloading article {content.url}")
                    newspapers.append({'Title':content.title, 'Text': content.text, 'Link': content.url, 'Time': content.publish_date})

    # try:
    #     with open('articles.json', 'w') as outfile:
    #         json.dump(newspapers, outfile)
    # except Exception as e: logging.info(e)
    return newspapers
