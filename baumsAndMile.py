from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import requests
import os

def linkAccepted(link):
    if(link.__contains__("Boys") or link.__contains__("BOYS") or link.__contains__("boys")):
        if(link.__contains__("II") or link.__contains__("Gold")):
            return True
        elif(link.__contains__("Varsity") and not(link.__contains__("Junior")) and not(link.__contains__("I"))):
            print("This should say false")
            print(not link.__contains__("Junior"))
            return True
        else:
            return False

site = "milesplit"
meetName = "/6231/perry-outdoor-family-center-xc-course"
dirName = "madison"
mileSplitName = "u-wanna-come-back"

if not os.path.exists(dirName):
    os.mkdir(dirName)


#Baumspage meet names: cardinal, walsh
#MileSplit Meet Names: 
#Riverside = /27366/riverside-hs
#mileSplitName = "riverside-kickoff-classic-night-invitational"
#Cardinal = 24848/cardinal-high-school-ohio
#mileSplitName = "cardinal-middlefield"
#Madison = /6231/perry-outdoor-family-center-xc-course
#mileSplitName = "u-wanna-come-back"

startYear = 2021
endYear = 2023

if(site=="milesplit"):
    for year in range(startYear, endYear):
        year = str(year)

        if not os.path.exists(dirName+"/"+year): #Making Directory for the Year
            os.mkdir(dirName+"/"+year)

        venueRequest = Request("https://oh.milesplit.com/venues"+meetName) #Opens the Meet Location Page
        venuePage = urlopen(venueRequest)
        venueSoup = BeautifulSoup(venuePage, "lxml")

        subVenueLink = ""
        print("https://oh.milesplit.com/venues/"+meetName)
        for link in venueSoup.findAll("a"): #Searches for the a tag
            currentLink = link.get('href') #Gets the link from the tag
            #print(currentLink)
            if currentLink.__contains__(mileSplitName) and currentLink.__contains__(year):
                subVenueLink = currentLink + "/results" #If the link is what we're looking for, add /results to get to the desired site
                #print(subVenueLink)


        print("\n\n\n|||OPENING: "+subVenueLink+"|||\n\n\n")

        raceRequest = Request(subVenueLink)
        racePage = urlopen(raceRequest)
        raceSoup = BeautifulSoup(racePage, "lxml")
        
        testFileContents = requests.get(subVenueLink)
        open("test.txt", "wb").write(testFileContents.content)
        
        for link in raceSoup.findAll("a"):
            currentLink = link.get("href")
            #print("CurrentLink in Riverside: "+str(currentLink))
            try:
                linkText = link.contents[0] #Incase the link is on an image or something
            except:
                continue
            if linkAccepted(linkText):
                raceLink = currentLink + "/raw" #Goes to the desired page
                print("Approved: "+raceLink)

        raceResultsReq = Request(raceLink)
        resultsPage = urlopen(raceResultsReq)
        raceResultsSoup = BeautifulSoup(resultsPage, "lxml")
        results = raceResultsSoup.find_all('pre') 
        #print(results)
        open("./"+dirName+"/"+year+"/results.txt", "w").write(str(results))



elif(site=="baumspage"):
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