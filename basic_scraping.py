import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def scrape_awards():
    webUrl = 'https://www.goldenglobes.com/winners-nominees/2016/all'
    webFile = urlopen(webUrl)
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("a", {"href": re.compile("/winners-nominees/[0-9]+/all#category-")})
    award_names = []
    count = 0
    for match in webAll:
        award_names.append(match.string)
        count = count+1
        #print (match.string)
    #print("\n\n", count)
    return award_names


def scrape_nominees():
    webUrl = 'https://www.goldenglobes.com/winners-nominees/2016/all'
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


print ("\n\n\tAwards\n", scrape_awards())
print ("\n\n\tNominees\n", scrape_nominees())
