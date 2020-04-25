#!/usr/bin/env python
# coding: utf-8

# In[15]:


import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
import lxml
import warnings
from bs4 import BeautifulSoup
from requests import get


# In[4]:


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    #To remove repetetive words like aa bbb ccc
    phrase = re.sub(r"(.)\1{2,}","", phrase)
    return phrase


# In[6]:


def cleanIt(sentence):
    stopwords= set(['br', 'the', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",            "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',             'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their',            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',             'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',             'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',             'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',            'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very',             's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',             've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',            "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',            "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",             'won', "won't", 'wouldn', "wouldn't"])
    sentence = decontracted(sentence)
    sentence = re.sub("\S*\d\S*", "", sentence).strip()
    sentence = re.sub('[^A-Za-z]+', ' ', sentence)
    # https://gist.github.com/sebleier/554280
    sentence = ' '.join(e.lower() for e in sentence.split() if e.lower() not in stopwords)
    sentence = sentence.strip()
    
    return sentence.strip()


# Web Scraping Functions

# To get the URL of the Movie
def getUrl(title,year):
        listYears=[]
        listYears.append(year)
        listYears.append(year+1)
        listYears.append(year-1)
        
        a=""
        aa=""
        url= "https://www.imdb.com/find?q="+title+"&ref_=nv_sr_sm"
        url2=""
        page = get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        content = soup.find(id="main")
        subContent = content.find_all("div", class_="findSection")

        #If the movie is in first page,this code works
        for i in subContent:
            if("Titles" in i.find_all(class_="findSectionHeader")[0]):
                      a=i.find_all("td",class_="result_text")

        for it in a:
            if((str(year+1) in str(it)) or (str(year) in str(it))  or (str(year-1) in str(it)) ):
                aa=it.find_all("a")[0]['href']
                if aa.strip():
                    url2="http://imdb.com"+aa
                    return url2
                break
        #If movie is in MORE TITLE MATCHES,it goes to second page and scrapes there
        for i in subContent:
            if("Titles" in i.find_all(class_="findSectionHeader")[0]):
                      a=i.find_all(class_="findMoreMatches")
        for it in a:
            aa = it.find_all('a')
        
        url2 = "http://imdb.com" + aa[0]['href']
        page2 = get(url2)
        soup = BeautifulSoup(page2.content, 'lxml')
        content = soup.find(id="main")
        subContent = content.find_all("div", class_="findSection")
        
        for i in subContent:
            if("Titles" in i.find_all(class_="findSectionHeader")[0]):
                      a=i.find_all("td",class_="result_text")
        for it in a:
            if((str(year+1) in str(it)) or (str(year) in str(it))  or (str(year-1) in str(it)) ):
                aa=it.find_all("a")[0]['href']
                url2="http://imdb.com"+aa
                return url2
        return url2

# To get the Storyline of the Movie
def getOverview(url):
    storyLine=""
    #global iterV
    try:
        page = get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        content = soup.find(id="main_bottom")
        subContent = content.find("div", class_="article",id="titleStoryLine")
        story = subContent.find("p")   
        storyLine = story.find("span").text.replace("span","").strip()
    except:
        #iterV+=1
        #print("Dude, your code sucked "+str(iterV)+" times :(" )
        return "NaN"
    
    return storyLine





