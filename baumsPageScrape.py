from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import requests
import os

meetName = "cardinal"


if not os.path.exists(meetName):
    os.mkdir(meetName)


for year in range(2017, 2022):
    year = str(year)
    if not os.path.exists(meetName+"/"+year):
        os.mkdir(meetName+"/"+year)

    req = Request("https://www.baumspage.com/cc/"+meetName+"/"+year+"/")
    page = urlopen(req)

    soup = BeautifulSoup(page, "lxml")

    links = []
    for link in soup.findAll("a"):
        currentLink = link.get('href')
        currentLink = currentLink.replace('//', '')
        currentLink = "http://"+currentLink  
        if "Boys" in currentLink:
            print(currentLink)
            response = requests.get(currentLink)
            nameIndex = currentLink.index("Boys")
            name = currentLink[nameIndex:len(currentLink)]
            open("./"+meetName+"/"+year+"/"+name, "wb").write(response.content)
            links.append(currentLink)
        elif "BOYS" in currentLink:
            print(currentLink)
            response = requests.get(currentLink)
            nameIndex = currentLink.index("BOYS")
            name = currentLink[nameIndex:len(currentLink)]
            open("./"+meetName+"/"+year+"/"+name, "wb").write(response.content)
            links.append(currentLink)
        else:    
            print("WOMAN")

    print(links)