from flask import Flask, render_template ,request, redirect, session
import requests
from bs4 import BeautifulSoup
import psycopg2
from html import escape
from flask import make_response
from make_cloud import create_cloud
import nltk
import os
from googletrans import Translator
import psycopg2
import openai



app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']

@app.route('/')
def index():
    return render_template('index.html') #index.htmlを表示



@app.route("/result",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def insert():
    if request.method == 'POST':
        # index.htmlのフォームから質問文を入手する
        page_url = escape(request.form['page_url'])
        
        

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        
        if page_url.startswith("http") or page_url.startswith("https"):
        # スクレイピング処理

            res = requests.get(page_url, headers={'Content-Type': 'text/html; charset=UTF-8'})
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

            for title in soup.find_all('title'):
                title_text = title.text
                translator = Translator()
                title_text_ja = translator.translate(title_text, dest='ja')
                title_text_ja = title_text_ja.text


            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser")
            body_content = soup.find_all('p')

            for footer in soup.find_all('footer'):
                footer.decompose()
            nltk.download('punkt', quiet=True)
            text = ' '.join([tag.text for tag in body_content])

                        
            API_KEY = "・・・"
            openai.api_key = API_KEY
            url = page_url
            prompt = f"{url}を3行で要約してください。"

            response = openai.Completion.create(engine="text-davinci-002",
                                                prompt=prompt,
                                                max_tokens=300,
                                                temperature=0.5,
                                                echo=True)
            three_text =  response.choices[0].text
            three_text = three_text.strip().split(prompt)[-1]
            print(three_text)


            



        

                # page_titleを保存する
            cursor.execute(
                '''INSERT INTO urltable (page_url, page_title) VALUES (%s, %s)''',
                (page_url, three_text)
            )
            conn.commit()
            cursor.execute("SELECT MAX(id) FROM urltable")
            max_id = cursor.fetchone()[0]

            cursor.execute(
                '''SELECT page_title FROM urltable WHERE id = %s''',
                (max_id,)
            )
            page_title = cursor.fetchone()[0]
            

            #wordcloudを生成
            create_cloud(text, max_id)


            translator = Translator()
            summary = page_title
            changetext = translator.translate(summary, dest='ja')
            print(changetext.text)
            page_title = changetext.text
            

            page_url2 = page_url



            return render_template('result.html', page_title=page_title, max_id=max_id, page_url2=page_url2, title_text=title_text, title_text_ja=title_text_ja)






        else:
            # テキストを保存する
            text = page_url

            API_KEY = "・・・"
            openai.api_key = API_KEY
            url = text
            prompt = f"{url}を3行で要約してください。"

            response = openai.Completion.create(engine="text-davinci-002",
                                                prompt=prompt,
                                                max_tokens=300,
                                                temperature=0.5,
                                                echo=True)
            three_text =  response.choices[0].text
            three_text = three_text.strip().split(prompt)[-1]
            print(three_text)



            cursor.execute(
                '''INSERT INTO urltable (page_url, page_title) VALUES (%s, %s)''',
                (page_url, three_text)
            )
            conn.commit()
            cursor.execute("SELECT MAX(id) FROM urltable")
            max_id = cursor.fetchone()[0]   

            cursor.execute(
                '''SELECT page_title FROM urltable WHERE id = %s''',
                (max_id,)
            )
            page_title = cursor.fetchone()[0]
            
            #wordcloud生成
            create_cloud(text, max_id)

            translator = Translator()
            summary = page_title
            changetext = translator.translate(summary, dest='ja')
            print(changetext.text)
            page_title = changetext.text
            
    

            return render_template('result.html', page_title=page_title, max_id=max_id, page_url=page_url)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
