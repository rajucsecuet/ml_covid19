import string
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud,STOPWORDS

stopwords = set(STOPWORDS)
seed = 123
sample = pd.read_csv('C:\\Users\\Raju\\OneDrive - Systems Solutions & Development Technologies Sdn Bhd\\UM\\ML\\assignment\\test.csv')
print(sample[['text','sentiment']])

punct =[]
punct += list(string.punctuation)
punct += '’'
punct.remove("'")
def remove_punctuations(text):
    for punctuation in punct:
        text = text.replace(punctuation, ' ')
    return text

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

# lowercase everything
sample['refine_text'] = sample['text'].apply(lambda x: x.lower())
# get rid of '\n' from whitespace
sample['refine_text'] = sample['refine_text'] .apply(lambda x: x.replace('\n', ' '))
# regex remove hyperlinks
sample['refine_text'] = sample['refine_text'] .str.replace('http\S+|www.\S+', '', case=False)
# removing '&gt;'
sample['refine_text'] = sample['refine_text'] .apply(lambda x: x.replace('&gt;', ''))
# Removing Stop Words
sample['refine_text'] = sample['refine_text'] .apply(lambda tweets: ' '.join([word for word in tweets.split() if word not in stopwords]))
# Removing Emojis from tokens
sample['refine_text'] = sample['refine_text'] .apply(lambda x: deEmojify(x))
# remove punctuations
sample['refine_text'] = sample['refine_text'] .apply(remove_punctuations)
# remove ' s ' that was created after removing punctuations
sample['refine_text'] = sample['refine_text'] .apply(lambda x: str(x).replace(" s ", " "))

print(sample[['text','sentiment','refine_text']])


def categoriser(diction):
    if(diction['neg']>0):
        return("negative")
    elif(diction['pos']>0):
        return('positive')
    else:
        return('neutral')

def SentiAnlyser(df):
    analyser= SentimentIntensityAnalyzer()
    df['polarity']=df['refine_text'].apply(lambda x: analyser.polarity_scores(x))
    df['prediction']=df['polarity'].apply(lambda x:categoriser(x))
    return df

train = SentiAnlyser(sample)
print(train[['sentiment','prediction']])
target_names=['negative', 'positive','neutral']
print(classification_report(train['sentiment'], train['prediction'], target_names=target_names))
