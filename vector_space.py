# -*- coding: utf-8 -*-
"""vector_space.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zAoCeslDvDwOp3o36smfP_M_UG2Uyq2u
"""

from google.colab import drive
drive.mount('/content/gdrive')

import re 
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk import PorterStemmer
import math
import numpy as np
import pickle
from collections import Counter

nltk.download('stopwords')

os.getcwd()

path = "/content/gdrive/MyDrive/CS-582_project"
os.chdir(path)
os.getcwd()

stopwords=nltk.corpus.stopwords.words('english')
ps = PorterStemmer()

# storing document lengths
web_page_length = {}

#calculating idf for tokens in web pages
web_page_idf = {}

#

with open("Pickle_Folder/" + "6000_inverted_index.pickle", "rb") as f:
    inverted_index = pickle.load(f)

with open("Pickle_Folder/" + "6000_url_pages.pickle", "rb") as f:
    url_pages = pickle.load(f)

doc_count = len(url_pages)
doc_count

"""Invert Document Frequency"""

def inverted_freq(data, inv_freq, count):
    for i in data.keys():
        inv_freq[i] = math.log(count/len(data[i]), 2)

"""Calculating Document length."""

def document_length(data, count, length, inv_freq):
    for i in data:
        for j in data[i].keys():
            if j not in length:
                length[j] = (data[i][j] * inv_freq[i])**2
            else:
                length[j] += (data[i][j] * inv_freq[i])**2
    return length

# inverted document frequency 
inverted_freq(inverted_index, web_page_idf, doc_count)

# calculating web page length
document_length(inverted_index, doc_count, web_page_length, web_page_idf)
# web_page_length = dict(sorted(web_page_length.items(), key=lambda x: x[0]))
web_page_length["1"]

"""Tokenize query data"""

def tokenize_query(data):
  data = data.lower()
  data = re.sub('[^a-z]+', ' ', data)                 
  words = data.split()
  stop_words_rem = [i for i in words if (len(i)>2 and i not in stopwords)]
  word_clean = [ps.stem(i) for i in stop_words_rem if len(ps.stem(i))>2]
  return word_clean

"""Query length"""

def query_length(data, inv_freq):

  length = 0

  for j in data.keys():
    length += (data[j] * inv_freq[j])**2
    
  return length

cosine_sim = {}
cosine_sim.keys()

"""Cosine Similarity"""

def cosine_similarity(query_tf):
  for j in query_tf:
      if j in inverted_index.keys():
          word_in_docs = list(inverted_index[j].keys())
          for k in word_in_docs:
            if k not in cosine_sim.keys():
              cosine_sim[k] = (query_tf[j]*web_page_idf.get(j,0)*inverted_index[j][k]*web_page_idf.get(j,0))/(math.sqrt(web_page_length[k]*query_len))
            else:
              cosine_sim[k] += (query_tf[j]*web_page_idf.get(j,0)*inverted_index[j][k]*web_page_idf.get(j,0))/(math.sqrt(web_page_length[k]*query_len))

  return cosine_sim

"""Input query"""

print("\n                     ---UIC Web Search Engine---\n")
# query input 
query = str(input("Enter  search query: "))
print("\n")
# tokenize input query
tokenized_query = tokenize_query(query)

# calculating term frequency for given query
query_tf = Counter(tokenized_query)
# calculating query length
query_len = query_length(query_tf, web_page_idf)
query_len

# cosine similarity
cos_sim_val = cosine_similarity(query_tf)
sorted_relevant_pages = dict(sorted(cos_sim_val.items(), key=lambda x: x[1], reverse=True))

def display_relevant_pages(count, webpages):
    for i in range(count, count + 10):
      try:
        url_num = int(webpages[i])
        # print(url_no)
      
      # executed when there are no more relevant pages.
      except Exception as e:
        print("\nNo more relevant pages!!")
        break

      if url_pages.get(url_num, None):
        print(i + 1, url_pages.get(url_num))

inputs = {"yes", "y"}
# to implement do-while loop
first_pass = True
count = 0

while first_pass or answer.lower() in inputs:
    display_relevant_pages(count, list(sorted_relevant_pages.keys()))
    answer = str(input("\nDo you want more web page results? "))
    count += 10
    first_pass = False

