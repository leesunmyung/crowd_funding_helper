import pickle

import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from future.utils import iteritems
from collections import Counter
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pymysql
from gensim.models import word2vec
from tqdm.notebook import tqdm
import os

import sys
if sys.version_info <= (2,7):
    reload(sys)
    sys.setdefaultencoding('utf-8')
import konlpy
from konlpy.tag import Kkma, Okt, Hannanum

article_data = pd.read_csv('C:\\Users\\vivid\\바탕 화면\\flask-test\\mixver10.txt', encoding='utf-8', header= None)
documents = [' '.join(i[0].split(' ')[1:]) for i in article_data.values]

as_one = ''
for document in documents:
    as_one = as_one + ' ' + document
words = as_one.split()

counts = Counter(words)

vocab = sorted(counts, key=counts.get, reverse=True)

word2idx = {word.encode("utf8").decode("utf8"): ii for ii, word in enumerate(vocab,1)}

idx2word = {ii: word for ii, word in enumerate(vocab)}

V = len(word2idx)
N = len(documents)

tf = CountVectorizer()

tf.fit_transform(documents)

tf.fit_transform(documents)[0:1].toarray()

tfidf = TfidfVectorizer(max_features = 1800, max_df=1, min_df=0)

#generate tf-idf term-document matrix
A_tfidf_sp = tfidf.fit_transform(documents)  #size D x V

tfidf_dict = tfidf.get_feature_names()

kkma = Kkma()
okt = Okt()
hannanum = Hannanum()
print('konlpy version = %s' % konlpy.__version__)

#conn = pymysql.connect(host='127.0.0.1', user='root', password='wdta2181',db='test', charset='utf8')
#curs = conn.cursor()

model = word2vec.Word2Vec.load('C:\\Users\\vivid\\바탕 화면\\flask-test\\NaverMovie30.model')
pickle.dump(model, open('C:\\Users\\vivid\\바탕 화면\\flask-test\\nm30.pkl', 'wb'))
