import string
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
#nltk.download('punkt')
#nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud,STOPWORDS
stopwords = set(STOPWORDS)
print(stopwords)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.covid19
#covid_df=db.tweet_en_test.find_one({"created_at":{"$regex":'.*Mar 31 19*'},"retweeted_status":None})
covid_df=db.tweet_en_test.find({"retweeted_status":None},{"full_text":1,"_id":0}).limit(1000000)
#covid_df=db.post_test.find({"retweeted_status":None, "created_at":{"$regex":'.*Mar 31 *'}},{"full_text":1,"_id":0})
tweets=pd.DataFrame(covid_df)

punct =[]
punct += list(string.punctuation)
punct += '’'
punct.remove("'")
def remove_punctuations(text):
    for punctuation in punct:
        text = text.replace(punctuation, ' ')
    return text
print(punct)
#remove the emoji
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')
def nlp(df):
    # lowercase everything
    df['token'] = df['full_text'].apply(lambda x: x.lower())
    # get rid of '\n' from whitespace
    df['token'] = df['token'].apply(lambda x: x.replace('\n', ' '))
    # regex remove hyperlinks
    df['token'] = df['token'].str.replace('http\S+|www.\S+', '', case=False)
    # removing '&gt;'
    df['token'] = df['token'].apply(lambda x: x.replace('&gt;', ''))
    # Removing Stop Words
    df['token'] = df['token'].apply(lambda tweets: ' '.join([word for word in tweets.split() if word not in stopwords]))
    # Removing Emojis from tokens
    df['token'] = df['token'].apply(lambda x: deEmojify(x))
    # remove punctuations
    df['token'] = df['token'].apply(remove_punctuations)
    # remove ' s ' that was created after removing punctuations
    df['token'] = df['token'].apply(lambda x: str(x).replace(" s ", " "))

    return df
def categoriser(diction):
    if(diction['neg']>0):
        return("Negative")
    elif(diction['pos']>0):
        return('Positive')
    else:
        return('Neutral')
def SentiAnlyser(df):
    analyser= SentimentIntensityAnalyzer()
    df['sentiment']=df['token'].apply(lambda x: analyser.polarity_scores(x))
    df['sentiment']=df['sentiment'].apply(lambda x:categoriser(x))
    return df
#Preprocessing
tweets1=(nlp(tweets))
print(tweets1)

#WordCloud
comment_words = ''
for val in tweets1.token:
    val = str(val)
    tokens = val.split()
    comment_words += " ".join(tokens) + " "

wordcloud1 = WordCloud(width=800, height=800,
                       background_color='white',
                       stopwords=STOPWORDS,
                       min_font_size=10).generate(comment_words)
plt.figure(figsize=(10, 10), facecolor=None)
plt.imshow(wordcloud1)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

#Sentiment Analysis using NLTK
tweets2=SentiAnlyser(tweets1)

tweet_sentiments=pd.DataFrame(tweets2['sentiment'].value_counts())
print(tweet_sentiments)
tweet_sentiments.plot.pie(y='sentiment',figsize=(25, 15),autopct='%1.1f%%', startangle=90)
plt.show()