from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import string
import re
from collections import Counter


#removes non ascii characters
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
#loads data file
data = json.load(open('/Users/nickparedes/Desktop/gg2018.json'))


tweets = list()
ids = list()

#creates list of tweets/ids with data
for tw  in data:
	tweets.append(removeNonAscii(tw['text']))
	ids.append(tw['id_str'])

#returns names from text
def get_continuous_chunks(text):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    chunks = nltk.chunk.ne_chunk(tagged)
    
    entity_names = []
    for word_tuple in chunks.pos():
            if word_tuple[1] == 'PERSON' or word_tuple[1] == 'ORGANIZATION':
                    if word_tuple[0][0].lower() != "golden" and word_tuple[0][0].lower() != "globes" and word_tuple[0][0].lower() != "goldenglobes" and word_tuple[0][0].lower() != "best":
                            entity_names.append(word_tuple[0])
    return entity_names



def contain(wordlist, tweet):
    x = False
    for word in wordlist:
        if word in tweet:
            x = True
            return x
    return x
        

winner_words = ['winner', 'win', 'won', 'goes to', 'ongrat', 'goes to']



handle_pattern = r"(^[@].*[" "])"

handle_pattern = r"(^[@][0-9a-zA-Z_]+)"

globe_words = ["Globe", 'goldenglobe','GoldenGlobe']



def get_most_common(listt):
    x = []
    for item in listt:
        x.append([item[0], item[1]])
    return x
        
        
def consolidate_names(names_list):
    for item1 in names_list:
        for item2 in names_list:
            if (item1[0] in item2[0]):
                item2[1] = item1[1] + item2[1]
                if (item1 in names_list):
                    names_list.remove(item1)
    return names_list

host = list()
host_list = []
noms = []
noms_list = []
winners = []
winners_list = []
#gets relevant people
def get_names(tweetz):
    for tweet in tweetz:
        if (not ("RT" in tweet)):
            if("omin" in tweet):
                x = get_continuous_chunks(tweet)
                if (x != []):
                    noms.append(x)
            elif("host" in tweet):
                x = get_continuous_chunks(tweet)
                if (x != []):
                    host.append(x)
            else:
                if contain(winner_words, tweet):
                    x = get_continuous_chunks(tweet)
                    if (x != []):
                        winners.append(x)
    for sublist in host:
        for item in sublist:
            if (not contain(globe_words, item)):
                host_list.append(item[0])
    for sublist in noms:
        for item in sublist:
            if (not contain(globe_words, item)):
                noms_list.append(item[0])
    for sublist in winners:
        for item in sublist:
            if (not contain(globe_words, item)):
                winners_list.append(item[0])
    data = Counter(winners_list)
    return consolidate_names(get_most_common(data.most_common()))

sentiments = list()
def get_sentiment(tweetz):
    for tweet in tweetz:
        x = TextBlob(tweet)
        sentiments.append(x.sentiment)
    return sentiments



print(get_names(tweets))

#print(a.sentiment)
#textt = "hey Mark."
#print(tweets[1000:1015])
#print(get_continuous_chunks(tweets[0]))
#print(get_sentiment(tweets))
                    









