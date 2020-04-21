#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify, render_template
import pickle
from clean import *

app = Flask(__name__)

model = pickle.load(open('model_RakelLG.pkl', 'rb'))
multiLabel = pickle.load(open("forGenre.pkl", 'rb'))
tf1 = pickle.load(open("tfidf1.pkl", 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    stringGenres = ""
    stringYear = request.form['year']
    stringOverview = request.form['experience']
    print(request.form['experience'])
    ssOverview = getOverview(getUrl(stringOverview.strip(),int(stringYear)))
    sOverview = decontracted(ssOverview)   
    listOverview = [sOverview]
    vec = tf1.transform(listOverview)
    pred = model.predict(vec)
    genresList = multiLabel.inverse_transform(pred)[0]
    pr = "I guess, the GENRE is :"
    for i in  genresList:
        stringGenres+=i+" "
    return render_template('index.html', prediction_text = genresList,overview = ssOverview,predicted = pr)


