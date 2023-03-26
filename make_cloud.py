from wordcloud import WordCloud

def create_cloud(text, max_id):

    wordcloud = WordCloud(background_color="black", width=600, height=400, max_words=100 ).generate(text)


    wordcloud.to_file("./static/image/wordcloud"+str(max_id)+".png")
