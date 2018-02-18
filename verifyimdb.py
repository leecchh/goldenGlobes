import re
from urllib.request import urlopen
import sys
from bs4 import BeautifulSoup
import json



#Ask for name
title = input("Please enter a name: ")

#Search for spaces in the title string
raw_string = re.compile(r' ')

#Replace spaces with a plus sign
searchstring = raw_string.sub('+', title)

#Prints the search string
print (searchstring)

#The actual query
url = "http://www.imdb.com/search/name?name=" + searchstring 

print("\n", url)

webFile = urlopen(url)
webHtml = webFile.read()
soup = BeautifulSoup(webHtml,"html.parser")

webAll = soup.findAll("a", {"href": re.compile("/name/[a-zA-Z0-9]+")})

for match in webAll:
	if match.string != None:
		if title in match.string:
				print (match.string)
#print (webAll)