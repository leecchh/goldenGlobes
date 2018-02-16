import json
import nltk
from nltk.corpus import *
import textblob
from textblob import TextBlob
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from alchemyapi import AlchemyAPI
from pprint import pprint

data = json.load(open('gg2018.json'))

tweets = list()
ids = list()

for tw  in data:
	tweets.append(tw['text'])
	ids.append(tw['id_str'])


#will concatenate to .* or (?!RT) as needed... just used for key words
patterns = {"best dressed": "((best.*dressed)|([oO]utfit)|(looked.*(great|amazing|beautiful|stylish|handsome))|((beautiful|stylish|fancy|).*outfit))",
			"most controversial" : "(([Rr]obbed)|([sS]tole)|([uU]nfair)|([cC]heated)|([Cc]ontroversial)|([wW]rong((ed)?)))" }

junk = "(([gG]olden)|([gG]lobes)|(RT))"
junkPat = ".*"+junk+".*"
junkPattern = re.compile(junkPat)

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
				if pred(word) and not junkPattern.match(word):
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
	gramList = sorted(gramList, key=lambda pair: pair[1], reverse=True)
	return gramList



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
	nameList = sorted(nameList, key=lambda pair: pair[1], reverse=True)
	return nameList	

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


#helper for findNames
def extract_entity_names(t):
	entity_names = []
	if hasattr(t, 'label') and t.label:
		if t.label() == 'NE':
			entity_names.append(' '.join([child[0] for child in t]))
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))
	return entity_names

#finds number of occurences of all names in a set of tweets 
def findNames(tws):
	nameDict = {}
	tokenized_sentences = [nltk.word_tokenize(tweet) for tweet in tws]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

	for tree in chunked_sentences:
		names = extract_entity_names(tree)
		for name in names:
			if not junkPattern.match(name):
				if name in nameDict:
					nameDict[name] = nameDict[name]+1
				else:
					nameDict[name] = 1

	nameList = list()
	for key,value in nameDict.items():
		nameList.append((key,value))
	nameList = sorted(nameList, key=lambda pair: pair[1], reverse=True)
	return nameList




#BEST DRESSED
#print(findNames(tweetSearch(tweets, "best dressed", True))

#most controversial
ls = findNames(tweetSearch(tweets, "most controversial", True))
print(ls)




