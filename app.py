from flask import Flask, render_template, request
import pickle
import numpy as np
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='0000',db='test', charset='utf8')
curs = conn.cursor()

model = pickle.load(open('C://Users//vivid//바탕 화면//flask-test//nm30.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def man():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def home():
    category = request.form['ca']
    keyword1 = request.form['a']
    keyword2 = request.form['b']
    keyword3 = request.form['c']
    keyword4 = request.form['d']

    project_category = category
    selected_word = []
    selected_word.append(keyword1)
    selected_word.append(keyword2)

    t_cnt = 0
    w_cnt = 0

    similar_word_list=[]
    for i in selected_word:
        try:
            similar_word=model.wv.most_similar(positive=[i],topn=2)
        except:
            continue
        for j in similar_word:

            if len(j[0]) == 1:
                continue
            else:
                similar_word_list.append(j[0])

    if len(selected_word) < 5:
        similar_word_list = similar_word_list + selected_word

    similar_word_set = set(similar_word_list)
    similar_word_set
    res_list=[]

    for i in similar_word_set:
        sql = 'select pagename,trim(title) from test.crawl where category="%s" and title like "%%%s%%" and achieve>=90;'%(project_category,i)
        curs.execute(sql)
        pagename = curs.fetchall()

        length = len(pagename)
        if length >3:
            length = 3

        for k in range(0,length):
            res_list.append((pagename[k][0], pagename[k][1]))

    res_set = set(res_list)

    for k in res_set:
        if k[0] == 'tumblbug': t_cnt+=1
        elif k[0] == 'wadiz': w_cnt+=1
        else: continue

    return render_template('after.html', t_cnt = t_cnt, w_cnt = w_cnt, res_list = res_list, cnt = t_cnt+w_cnt)

    conn.close()

if __name__ == "__main__":
    app.run(port = 5500, debug=True)
