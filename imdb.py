import re
from urllib.request import urlopen
import sys
from bs4 import BeautifulSoup
import json

def verify_name(act_name, string_name):

	#The actual query
	url = "http://www.imdb.com/search/name?name=" + string_name 

	webFile = urlopen(url)
	webHtml = webFile.read()	
	soup = BeautifulSoup(webHtml,"html.parser")

	webAll = soup.findAll("a", {"href": re.compile("/name/[a-zA-Z0-9]+")})

	for match in webAll:
		if match.string != None:
			if act_name.lower() in match.string.lower():
				#print(act_name.lower(), match.string.lower())
				return (match.string)	

def verify_title(act_title, string_name):

	#The actual query
	url = "http://www.imdb.com/search/title?title=" + string_name 

	webFile = urlopen(url)
	webHtml = webFile.read()	
	soup = BeautifulSoup(webHtml,"html.parser")

	webAll = soup.findAll("a", {"href": re.compile("/title/[a-zA-Z0-9]+")})

	for match in webAll:
		if match.string != None:
			if act_title.lower() in match.string.lower():
				#print(act_title.lower(), match.string.lower())
				return (match.string)	

def imdb(name):
	
	title = name	
	#Search for spaces in the title string
	raw_string = re.compile(r' ')
	new_list = []
	#Replace spaces with a plus sign
	searchstring = raw_string.sub('+', title)

	print ("Searching for: ", searchstring)

	if verify_name(title, searchstring) != None:
		new_list.append(verify_name(title, searchstring)[1:-1])
	else:
		new_list.append(None)
	new_list.append(verify_title(title, searchstring))

	return (new_list)

	

print(imdb('James Franco'), "\n\n")

print(imdb('Dunkirk'), "\n\n")

print(imdb('Shape of Water'), "\n\n")