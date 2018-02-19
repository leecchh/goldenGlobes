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
#data = json.load(open('/Users/nickparedes/Desktop/goldenglobes.json'))

tweets = list()
ids = list()

#creates list of tweets/ids with data
for tw  in data:
	tweets.append(removeNonAscii(tw['text']))
	#ids.append(tw['id_str'])

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

def containz(wordlist, tweet):
    x = 0
    for word in wordlist:
        if word in tweet:
            x = x + 1
    if (x > 1):
        return True
    else:
        return False
        
        

winner_words = ['winner', 'win', 'won', 'goes to', 'ongrat', 'goes to']
#categories = [['icture', 'rama'], ['icture','usical', 'omedy'], ['ctress', 'rama'], ['ctor', 'rama'], ['ctress', 'usical', 'omedy'], ['ctor','usical', 'omedy'], ['ctress','upporting'], ['ctor', 'upporting'], ['irector'], ['creenplay'], ['nimated'], ['oreign', 'anguage'], ['score', 'ore'], ['Song', 'song'], ['elevision', 'rama'], ['elevision', 'usical', 'omedy'], ['elevision', 'imited', 'eries', 'ade for'], ['ctress','imited', 'eries', 'ade for'], ['ctor','imited', 'eries', 'ade for'], ['ctress', 'elevision', 'eries', 'rama'],['ctor', 'elevision', 'eries', 'rama'], ['ctress', 'elevision', 'eries', 'usical', 'omedy'],['ctor', 'elevision', 'eries', 'usical', 'omedy'], 'Best Performance by an Actress in a Supporting Role in a Series, Limited Series or Motion Picture Made for Television', 'Best Performance by an Actor in a Supporting Role in a Series, Limited Series or Motion Picture Made for Television', 'Cecil B. DeMille Award']
categories = ['Best Motion Picture - Drama', 'Best Motion Picture - Musical or Comedy', 'Best Performance by an Actress in a Motion Picture - Drama', 'Best Performance by an Actor in a Motion Picture - Drama', 'Best Performance by an Actress in a Motion Picture - Musical or Comedy', 'Best Performance by an Actor in a Motion Picture - Musical or Comedy', 'Best Performance by an Actress in a Supporting Role in any Motion Picture', 'Best Performance by an Actor in a Supporting Role in any Motion Picture', 'Best Director - Motion Picture', 'Best Screenplay - Motion Picture', 'Best Motion Picture - Animated', 'Best Motion Picture - Foreign Language', 'Best Original Score - Motion Picture', 'Best Original Song - Motion Picture', 'Best Television Series - Drama', 'Best Television Series - Musical or Comedy', 'Best Television Limited Series or Motion Picture Made for Television', 'Best Performance by an Actress in a Limited Series or a Motion Picture Made for Television', 'Best Performance by an Actor in a Limited Series or a Motion Picture Made for Television', 'Best Performance by an Actress In A Television Series - Drama', 'Best Performance by an Actor In A Television Series - Drama', 'Best Performance by an Actress in a Television Series - Musical or Comedy', 'Best Performance by an Actor in a Television Series - Musical or Comedy', 'Best Performance by an Actress in a Supporting Role in a Series, Limited Series or Motion Picture Made for Television', 'Best Performance by an Actor in a Supporting Role in a Series, Limited Series or Motion Picture Made for Television', 'Cecil B. DeMille Award']
#categories = ['best supporting actress in a television series limited series or television movie', 'best supporting actress in a limited series or television movie','best actress in a television series musical or comedy','best performance by an actress in a supporting role','best actor in a television series or limited series','best actor in a limited series or television movie', 'best actress in a motion picture musical or comedy', 'best supporting actress in a series limited series', 'best actress in a miniseries or television movie', 'best actor in a motion picture musical or comedy', 'best actress television series musical or comedy','best actress in a motion picture drama or comedy','best television limited series or motion picture']

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


def connect_winners(nameList, categories, tweets):
    results = []
    for tweet in tweets:
        for name in nameList:
            for category in categories:
                if(not ('lobe' in name) and (not (name in category))):
                    if ((name in tweet) and (category.lower() in tweet.lower())):
                        results.append([name, category])
    return results
                    

#finds number of occurences of all names in a set of tweets 
def findNames(tws):
	nameDict = {}
	tokenized_sentences = [nltk.word_tokenize(tweet) for tweet in tws]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

	for tree in chunked_sentences:
		names = extract_entity_names(tree)
		for name in names:
                    tempName = name.lower()
                    isAward = False
                    for cat in categories:
                        if tempName in cat.lower():
                            isAward = True
			if not junkPattern.match(name) and not isAward:
				if name in nameDict:
					nameDict[name] = nameDict[name]+1
				else:
					nameDict[name] = 1

	nameList = list()
	for key,value in nameDict.items():
		nameList.append((key,value))
        nameList = sorted(nameList, key=lambda pair: pair[1], reverse=True)

	i = 0
	n = 0
	length = len(nameList)
	print(len(nameList), 'namelist length')
	newset = set()
	while i < 1400:
            while n < 1400:
                if (nameList[i][0] in nameList[n][0]) and i != n:
                    newset.add(nameList[n][0])
                    i = i + 1
                    n = n + 1
                else:
                    n = n + 1
            newset.add(nameList[n][0])
            i = i + 1
            n = 0
                

                
        print(newset)
	return newset






junk = "(([gG][oO][lL][dD][eE][nN])|([gG][lL][oO][bB][eE][sS])|(RT))"
junkPat = ".*"+junk+".*"
junkPattern = re.compile(junkPat)


def concat(pplawardlist):
    x = []
    for ent1 in pplawardlist:
        for ent2 in pplawardlist:
            if (not ((ent1[0] in ent2[0]) and (ent1[1] == ent2[1]))):
                x.append(ent2[0] +' '+ ent2[1])
    return Counter(x).most_common()


def give_most_likely(connected_list, cats):
    answers = []
    for cat in cats:
        x = 0
        for ent in connected_list:
            if (cat in ent[0]) and x == 0:
                answers.append(ent[0])
                x = x + 1
    return answers
                
        



def get_names(tweetz):
    for tweet in tweetz:
        if (not ("RT" in tweet)):
            if("omin" in tweet):
                host.append(tweet)
            elif("host" in tweet):
                host.append(tweet)
            elif("best" in tweet):
                noms.append(tweet)
            else:
                if contain(winner_words, tweet):
                    noms.append(tweet)
    return give_most_likely(concat(connect_winners(findNames(noms), categories, noms)), categories)
#    return findNames(noms)[0:120]
 

sentiments = list()
def get_sentiment(tweetz):
    for tweet in tweetz:
        x = TextBlob(tweet)
        sentiments.append(x.sentiment)
    return sentiments


x = get_names(tweets)
print(x)
print(len(x), len(categories))
#print(a.sentiment)
#textt = "hey Mark."
#print(tweets[1000:1015])
#print(get_continuous_chunks(tweets[0]))
#print(get_sentiment(tweets))
 
