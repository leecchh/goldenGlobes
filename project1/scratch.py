import json
import nltk
import textblob
from textblob import TextBlob
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

from pprint import pprint

data = json.load(open('gg2018.json'))

tweets = list()
ids = list()

for tw  in data:
	tweets.append(tw['text'])
	ids.append(tw['id_str'])


#will concatenate to .* or (?!RT) as needed... just used for key words
patterns = {"best dressed": "((best.*dressed)|(looked.*(great|amazing|beautiful|stylish|handsome))|((beautiful|stylish|fancy|).*outfit))",
			"most controversial" : "(([Rr]obbed)|([sS]tole)|([uU]nfair)|([cC]heated)|([Cc]ontroversial)|([wW]rong((ed)?)))" }

#search finds more tweets but is a lot slower than match
def tweetSearch(twts, patternKey, keepRTs):
	relevantTweets = list()
	if keepRTs:
		pat = ".*"+patterns[patternKey]+".*"
	else:
		pat = "(?!RT).*"+patterns[patternKey]+".*"
	pattern = re.compile(pat)
	for tweet in twts:
		if pattern.match(tweet):
			relevantTweets.append(tweet)
	return relevantTweets


def isTitle(word):
	return word.istitle()

def retTrue(x):
	return True

#returns list of ngrams with ocurrence number
def getGrams(twts, gramness, pred):
	gramDict = {}
	for tweet in twts:
		blob = TextBlob(tweet)
		grams = blob.ngrams(n=gramness)
		for gram in grams:
			for word in gram:
				if pred(word):
					text = ""
					for w in gram:
						text = text+w.lower()+" "
					text = text[:-1]
					if text in gramDict:
						gramDict[text] = gramDict[text]+1
					else:
						gramDict[text] = 1
					break
	
	gramList = list()
	for key,value in gramDict.items():
		gramList.append((key,value))
	gramList = sorted(gramList, key=lambda pair: pair[1])
	return gramList

print(getGrams(tweetSearch(tweets, "best dressed", True),2, isTitle))

#filtering by nltk tag and counting recurrences
def filtByTag(twts, tag):
	for tweet in twts:
		nameDict = {}
		tokens = nltk.word_tokenize(tweet)
		tagged = nltk.pos_tag(tokens)
		for tup in tagged:
			if tup[1] == tag:
				text = tup[0]
				if text in nameDict:
					nameDict[text] = nameDict[text]+1
				else:
					nameDict[text] = 1
	nameList = list()
	for key,value in nameDict.items():
		nameList.append((key,value))
	nameList = sorted(nameList, key=lambda pair: pair[1])
	return nameList	

#print(filtByTag(tweetSearch(tweets,"most controversial", True), "NNP"))

def scrape_awards():
    webUrl = 'https://www.goldenglobes.com/winners-nominees/2018/all'
    webFile = urlopen(webUrl)
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("a", {"href": re.compile("/winners-nominees/2018/all#category-")})
    award_names = []
    count = 0
    for match in webAll:
        award_names.append(match.string)
        count = count+1
        #print (match.string)
    #print("\n\n", count)
    return award_names


def scrape_nominees():
    webUrl = 'https://www.goldenglobes.com/winners-nominees/2018/all'
    webFile = urlopen(webUrl)
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("div", {"class": "primary-nominee"})
    nominees = []
    count = 0
    for match in webAll:
        #print (match.a.string)
        count = count+1
        nominees.append(match.a.string)
    #print ("\n\n", count)
    return nominees

# Worst Dressed

# Most Talked About

# Most Controversial


# print ("\n\n\tAwards\n", scrape_awards())
# print ("\n\n\tNominees\n", scrape_nominees())
