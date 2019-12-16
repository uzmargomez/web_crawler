#*******************************************************
#                 Necessary packages

import sys
import re
from pprint import pprint
from collections import defaultdict

import json
import os
import numpy as np
import pandas as pd
import statistics

# nltk
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt

from pymongo import MongoClient

mongo_server = "mongo"

#***********************************************************************
#                   Functions to get categories

def clean_data(text):
    text = re.sub('[" ]', '', text)
    sprt = text.split('+')
    list_data=[]
    for i in range(0,len(sprt)):
        ap = sprt[i].split('*')
        list_data.append(ap)
    return list_data

def find_max_mode(list1):
    list_table = statistics._counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = statistics.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list) # use the max value here
    return max_mode

def analize(aux,categories):
    decition = []
    for i in aux:
        flag = 0
        val=0
        tag = 'default'
        for x,y in categories.items(): #Just use y
            for z in y:
                if i[1]==z:
                    flag = 1
                    tag = x
                    break
            if flag != 0:
                break

        decition.append(tag)

    categorie=[]

    for i in decition:
        if i != 'default':
            categorie.append(i)

    if len(categorie)==0:
        categorie.append('default')
    categorie_topic = find_max_mode(categorie)
    return categorie_topic

def get_cat(text,categories):
    text = list(text)
    data = clean_data(text[1])
    categorie = analize(data,categories)
    return categorie

#***********************************************************************
#                         Model function
def model_function():
    #***********************************************************************
    #                Defining the different news categories

    categories = {'Sports': ['football','ball','team','play','win','season','fan','run','scoore','athletics','spectator',
                         'competition','tennis','yard','game','fun','cricket','stadium','uefa','concacaf','player',
                         'game','referee'],
             'Medical': ['patient','study','slave','food','eat','pain','treatment','syndrome','therapy','medicine',
                         'health','doctor','diagnosis','clinical','biomedical'],
          'World News': ['israel','war','kill','soldier','attack','war','government','racism','internet','newpaper',
                         'journalism','telephone','earth','country','conflict','civil','military','peace','war',
                         'hurt','army'],
            'Religion': ['god','evidence','christian','believe','reason','faith','exist','bible','religion',
                         'judaism','cult','belief','theology','church','symbol','homosexuality','hell'],
           'Lifestyle': ['trending','fashion','entertainment','society','person','mode','lifestyles','casual',
                        'healthy','chic','cosmopolitan','popular','social','fashionable','celebrity','carpet',
                        'red','body','dress','business','workplace','fun','holiday','buy','living','hobbies','hipster'],
             'Culture': ['education','knowledge','learn','learning','literacy','urbanity','class','civility','ignorance',
                         'civilization','life','values','legacy','tradition','society','philosophy','religion','nationalism',
                         'art','music','ritual','concept','humanism','classical'],
            'Politics': ['government','diplomatic','law','political','politics','governance','republic','state',
                         'police','monarchy','democratic','federation','city','company','country','latin','uk','usa'],
          'Technology': ['videogame','xbox','play','station','video','smartphone','nintendo','shooter','mobile',
                         'sony','gaming','electronics','engineering','science','robot','robotics','internet',
                         'computer','industry','automation','technological','energy','device','devices','application',
                         'app','technology'],
       'Entertainment': ['television','film','movie','animation','comedy','cinema','media','show','circus','dance',
                         'concert','online','radio','party','ceremony','tourist'],
                'Food': ['nutrition','rice','nutrient','beef','meat','cook','cooking','seafood','cereal','fat',
                         'soup','pasta','butter','agriculture','meal','milk','animals','chicken','plant','energy',
                         'vegetarian','protein','vitamin','nutriment','aliment','fruit','vegetable','restaurant',
                         'restaurants','eat','kitchen','pizza','taste'],
                 }

    #***********************************************************************
    #                  For eliminating unnecessary words

    add_stop_words = ['said','would','one','even','really','could','also']

    stop_words = stopwords.words('english')

    [stop_words.append(i) for i in add_stop_words]

    stop_words_set = set(stop_words)


    #***********************************************************************
    #                    Preparing the texts

    #***********************************************************************
    #                        Pulling Mongo Data
    myclient = MongoClient("mongodb://{}:5003/".format(mongo_server))
    mydb = myclient["mydatabase"]
    mycol = mydb["prueba"]

    res = mycol.find({}, {"Text": 1, "Title": 1, "Link": 1, "Time": 1})
    res_data_frame=pd.DataFrame(list(res))

    textos = res_data_frame["Text"]
    names = res_data_frame["Title"]
    urls = res_data_frame["Link"]
    time = res_data_frame["Time"]

    texts = []
    documents = []
    for t in textos:
        string = ''.join(t.splitlines())
        string = string.lower()
        word_tokens = word_tokenize(string)
        filtered_sentence = [w for w in word_tokens if not w in stop_words_set]
        documents.append(" ".join(filtered_sentence))
        texts.append(filtered_sentence)


    #***********************************************************************
    #                Model training and graph representation

    tokenized_list = [simple_preprocess(doc) for doc in documents]
    mydict = corpora.Dictionary()
    mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    word_counts = [[(mydict[id], count) for id, count in line] for line in mycorpus]
    lda_model = gensim.models.ldamodel.LdaModel(corpus=mycorpus,
                                            id2word=corpora.Dictionary(tokenized_list),
                                            num_topics=len(categories),
                                            random_state=100,update_every=1,
                                            chunksize=100, passes=30,
                                            alpha='auto', per_word_topics=True)

    vis = pyLDAvis.gensim.prepare(lda_model, mycorpus, corpora.Dictionary(tokenized_list),n_jobs=2)
    graphhtml=pyLDAvis.prepared_data_to_html(vis)

    table_data=[]
    for topic in lda_model.print_topics():
        topic_data=list(topic)
        cate = get_cat(topic,categories)
        table_data.append(topic_data)
        topic_data.append(cate)

    #********************************************************************
    #              DataFrame that tells the categories,
    #           their ID's and the words that create them

    df_categories = pd.DataFrame(table_data,columns = ['ID','Words','Categorie'])
    #********************************************************************

    get_document_topics = lda_model.get_document_topics(mycorpus)

    news_classification=[]
    for n in range(len(get_document_topics)):
        for i in range(len(table_data)):
            if get_document_topics[n][0][0]==table_data[i][0]:
                news_classification.append([get_document_topics[n][0][1],table_data[i][2],names[n],urls[n],time[n]])

    #********************************************************************
    #  DataFrame that tells the categories for each article and its url

    df_classification=pd.DataFrame(news_classification,columns=['Belonging','Classification','Title','Link','Time'])
    df_classification=df_classification.sort_values(by="Time",ascending=True)
    df_classification["Time"]=df_classification["Time"].apply(lambda x: x.ctime())

    return [df_categories,df_classification,graphhtml]
