import json
import nltk
from nltk.corpus import *
# from nltk.collocations import *
# from nltk.corpus import PlaintextCorpusReader
# from nltk.metrics.association import QuadgramAssocMeasures
from difflib import SequenceMatcher
import textblob
from textblob import TextBlob
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import enchant
dictionary = enchant.Dict("en_US")

#will concatenate to .* or (?!RT) as needed... just used for key words
patterns = {"best dressed": "((best.*dressed)|([oO]utfit)|(looked.*(great|amazing|beautiful|stylish|handsome))|((beautiful|stylish|fancy|).*outfit))",
			"most controversial" : "(([Rr]obbed)|([uU]nfair)|([cC]heated)|([Cc]ontroversial)|([wW]rong((ed)?)))",
			"cecil award": "Cecil B. DeMille Award",
			"awards": "([bB]est ([Mm]otion)|([Pp]erformance)|([dD]irector)|([oO]riginal)|([Tt]elevision))"}
			#"awards": "(([bB]est)|([Aa]ctor)|([Aa]ctress)|([mM]ovie)|([Pp]icture)|([sS]how)|([aA]ward))"}

junk = "(([gG]olden)|([gG]lobes)|(RT))"

badPats = {"cecil": "(([cC]ecil)|([aA]ward)|([dD]e[Mm]ille))"}

junkPat = ".*"+junk+".*"
junkPattern = re.compile(junkPat)

junkWords = ['Golden','golden','Globes','globes','globe','and','i','a','me','they','are','I','s','t','we','there',
			'this','that','then','after','before','during','with','within','without','is','isn\'t','can','be',
			'goldenglobes','GoldenGlobes','was','is','if','http','https']

#cleans out most, still misses some
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00010000-\U0010FFFF"
                           "]+", flags=re.UNICODE)

url_pattern = re.compile(r'^https?:\/\/.*[\r\n]*', flags=re.MULTILINE)

def cleanTweets(tws):
	cleaned = list()
	for tweet in tws:
		#remove emojis
		tweet = emoji_pattern.sub(r'', tweet)
		tweet = url_pattern.sub(r'', tweet)
		cleaned.append(tweet)
	return cleaned

def stripJunk(tws):
	new_list = list()
	for tweet in tws:
		for s in junkWords:
			tweet = tweet.replace(s,"")
		new_list.append(tweet)
	return new_list

#search finds more tweets but is a lot slower than match
def tweetSearch(twts, patternKey, keepRTs):
	print('Searching and filtering tweets... \n')
	relTweets = list()
	if keepRTs:
		pat = ".*"+patterns[patternKey]+".*"
	else:
		pat = "(?!RT).*"+patterns[patternKey]+".*"
	pattern = re.compile(pat)
	for tweet in twts:
		if pattern.match(tweet):
			relTweets.append(tweet)
	return relTweets


#returns list of ngrams with ocurrence number
def getGrams(twts, gramness):
	gramDict = {}
	for tweet in twts:
		blob = TextBlob(tweet)
		grams = blob.ngrams(n=gramness)
		for gram in grams:
			junk = False
			for word in gram:
				if word in junkWords:#junkPattern.search(word):
					junk = True
			if not junk:
				text = ""		
				for w in gram:
					text = text+w+" "
				text = text[:-1]
				if text in gramDict:
					gramDict[text] = gramDict[text]+1
				else:
					gramDict[text] = 1		
	
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
			if not junkPattern.search(name):
				if name in nameDict:
					nameDict[name] = nameDict[name]+1
				else:
					nameDict[name] = 1

	nameList = list()
	for key,value in nameDict.items():
		nameList.append((key,value))
	nameList = sorted(nameList, key=lambda pair: pair[1], reverse=True)
	return nameList


def findCecil(tws):
	#Cecil B. DeMille Award
	print("\nCecil B. DeMille Award Winner:")
	ls = findNames(tweetSearch(tws, "cecil award", ))
	ls = ls[0:10]
	pattern = re.compile(badPats['cecil'])
	for i in ls:
		if not pattern.search(i[0]):
			print(i[0])
			break

def substring_before(s, delim):
    return s.partition(delim)[0]

def substring_after(s, delim):
    return s.partition(delim)[2]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def  printOut(tws):
	#BEST DRESSED
	print("\n Best Dressed \n")
	ls = findNames(tweetSearch(tws, "best dressed", True))
	for i in range(0,5):
		print(ls[i][0]+"\n")

	#most controversial
	print("\n Most Controversial \n")
	ls = findNames(tweetSearch(tws, "most controversial", True))
	for i in range(0,5):
		print(ls[i][0]+"\n")

def removeDups(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

scrapedAwards = scrape_awards()
scrapedNominess = scrape_nominees()

data = json.load(open('gg2018.json'))
tweets = list()
ids = list()

for tw  in data:
	tweets.append(tw['text'])
	ids.append(tw['id_str'])

cleanedTweets = cleanTweets(tweets)



#list of list of ngrams, by degree of gramness
def findAwards(tws):

	# strippedTweets = list()
	# p = re.compile('[bB]est.*')
	# for tweet in cleanedTweets:
	# 	if p.match(tweet):
	# 		found = p.findall(tweet)
	# 		best = found[0]
	# 		for f in found:
	# 			if len(f)>len(best):
	# 				best = f
	# 		strippedTweets.append(best.lower())

	strippedTweets = list()
	p = re.compile('[bB]est .*')
	for tweet in cleanedTweets:
		found = p.findall(tweet)
		if len(found)>0:
			best = found[0]
			for f in found:
				if len(f)>len(best):
					best = f
			strippedTweets.append(best.lower())

	print(strippedTweets)
	print(len(strippedTweets))

	ngrams = list()
	gramness = [7, 8, 10]
	print('beginning gram creation... \n')
	p = re.compile('[bB]est.*')
	for i in gramness:
		relGrams = list()
		grams = getGrams(strippedTweets,i)
		for g in grams:
			if p.match(g[0]):
				relGrams.append(g)
		topGrams = relGrams[0:100]
		ngrams.append(topGrams)
		print(topGrams)
		print(str(i)+"-gram complete... \n")


	postAwardPhrases = ['goes to',':', 'category','for'] #'nominee','winner','presenter','presented',
	#Searching for classic winner tweet format
	cleaned_ngrams = list()
	for group in ngrams:
		for gram in group:
			added = False
			text = gram[0].lower()
			for phrase in postAwardPhrases:
				text = substring_before(text, phrase)

			if (len(text)<len(gram[0])) and (len(nltk.word_tokenize(text))>1):
				cleaned_ngrams.append(text)
				added=True
	
	awards = list()
	for i in cleaned_ngrams:
		awards.append(substring_before(i, 'goes to'))


	awards = removeDups(awards)

	for award in awards:
		tokens = nltk.word_tokenize(award)
		if len(tokens)<3:
			awards.remove(award)
		else:
			for token in tokens:
				if not dictionary.check(token):
					awards.remove(award)
					break
			print(award)
	print(len(awards))

#findAwards(cleanedTweets)

for i in range(0,10):
	if i == 5:
		break
	print(i)




