from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import requests
import os
from selenium import webdriver


def linkAccepted(link):
    if(link.__contains__("Valley")) or (link.__contains__("Open")) or (link.__contains__("2500")) or (link.__contains__("2.15")):
        return False
    if(link.__contains__("Boys") or link.__contains__("BOYS") or link.__contains__("boys") and not(link.__contains__("Valley"))):
        if(link.__contains__("II") or link.__contains__("Gold")) or link.__contains__("2"):
            return True
        elif(link.__contains__("Varsity") and not(link.__contains__("Junior")) and not(link.__contains__("I")) and not(link.__contains__("1")) and not(link.__contains__("MS"))):
            #print("This should say false")
           # print(not link.__contains__("Junior"))
            return True
        elif(link.__contains__("High School Boys") and not(link.__contains__("1"))):
            return True
        
        else:
            return False
    elif(link.__contains__("Division 2 Results") or link.__contains__("Varsity D2/3 Results") or link.__contains__("Blue") and not(link.__contains__("1")) and not(link.__contains__("3")) and not(link.__contains__("Boys")) and not(link.__contains__("Girls")) and not(link.__contains__("MS"))):
        return True
    elif(link.__contains__("Blue") and link.__contains__("Boys") and not(link.__contains__("MS"))):
        return True
    elif(link.__contains__("\"Completed\" Results")):
        return True

site = "milesplit"
#meetName = "/6231/perry-outdoor-family-center-xc-course"
#dirName = "madison"
#mileSplitName = "u-wanna-come-back"


#Baumspage meet names: cardinal, walsh
#MileSplit Meet Names: 
#Riverside = /27366/riverside-hs
#mileSplitName = "riverside-kickoff-classic-night-invitational"
#Cardinal = 24848/cardinal-high-school-ohio
#mileSplitName = "cardinal-middlefield"
#Madison = /6231/perry-outdoor-family-center-xc-course
#mileSplitName = "u-wanna-come-back"


#options = webdriver.FirefoxOptions()
#options.add_argument('--headless')
#browser = webdriver.Firefox(options=options, executable_path='./geckodriver.exe')

#browser.get("https://oh.milesplit.com/teams/9454-west-geauga")
#html = browser.page_source
#teamSoup = BeautifulSoup(html, "lxml")



#print(teamSoup.findAll("ul", id="schedule"))

#teamSoup = BeautifulSoup(teamSoup.findAll("ul", id="schedule"), "lxml")
#for link in teamSoup.findAll("ul", id="schedule"): #Searches for the a tag
#        currentLink = link.get("href")
#        try:
#            linkText = link.contents[0] #Incase the link is on an image or something
#        except:
#            continue
#        print("Link:")
#        print(linkText)

startYear = 2019
endYear = 2023

if(site=="milesplit"):
    for year in range(startYear, endYear):
        year = str(year)

        response = requests.get("https://oh.milesplit.com/api/v1/teams/9454/schedules?season=cc&year="+year)
        open("test.json", "wb").write(response.content)

        f = open("test.json")

        r = open("meetNameID.txt", "w")

        fileContents = f.read()

        #print(fileContents)

        meetIDs = []

        strIndex = 0
        startIndex = 0
        endIndex = len(fileContents)
        i=0
        meetNum = 0
        while (i<len(fileContents)):
            strIndex = fileContents.find("meetId", startIndex)
            strIndex = strIndex + 9
            endQuoteIndex = fileContents.find("\"", strIndex)
            meetId = fileContents[strIndex:endQuoteIndex]
            startIndex = endQuoteIndex
            strIndex = fileContents.find("name", startIndex)
            strIndex = strIndex + 7
            endQuoteIndex = fileContents.find("\"", strIndex)
            name = fileContents[strIndex:endQuoteIndex]
            i = endQuoteIndex
            name = name.lower()
            name = name.replace(" - ", " ")
            name = name.replace(" ", "-")
            if meetId in meetIDs:
                i=i+10000
                continue
            if name=="west-geauga":
                i=i+1000
                continue
            meetIDs.append(meetId)
            meetNum = meetNum+1
            #print(i)
            #print(len(fileContents))
            #print(meetId)
            r.write("\n"+name+"\n"+meetId)
        r.close()

        meetFile = open("meetNameID.txt", "r")
        #print(meetFile.read())


        

        #venueRequest = Request("https://oh.milesplit.com/venues"+meetName) #Opens the Meet Location Page
        #venuePage = urlopen(venueRequest)
        #venueSoup = BeautifulSoup(venuePage, "lxml")

        #subVenueLink = ""
        #print("https://oh.milesplit.com/venues/"+meetName)
        #for link in venueSoup.findAll("a"): #Searches for the a tag
        #    currentLink = link.get('href') #Gets the link from the tag
            #print(currentLink)
        #    if currentLink.__contains__(mileSplitName) and currentLink.__contains__(year):
        #        subVenueLink = currentLink + "/results" #If the link is what we're looking for, add /results to get to the desired site
                #print(subVenueLink)
        readMeetId = ""
        readMeetName = ""
        meetFile.readline()
        #print("MeetNum"+str(meetNum))
        for p in range(meetNum):
            readMeetName = meetFile.readline()
            readMeetId = meetFile.readline()
            readMeetName = readMeetName.replace("\n", "")
            readMeetId = readMeetId.replace("\n", "")

            if not os.path.exists(readMeetName):
                os.mkdir(readMeetName)

            if not os.path.exists(readMeetName+"/"+year): #Making Directory for the Year
                os.mkdir(readMeetName+"/"+year)

            #print("**"+readMeetId+"**")
            print("Meet Name: "+readMeetName+" Year: "+year)
            subVenueLink = "https://oh.milesplit.com/meets/"+readMeetId+"-"+readMeetName+"-"+year+"/results"

            #print("\n\n\n|||OPENING: "+subVenueLink+"|||\n\n\n")

            raceRequest = Request(subVenueLink)
            racePage = urlopen(raceRequest)
            raceSoup = BeautifulSoup(racePage, "lxml")
            
            testFileContents = requests.get(subVenueLink)
            open("test.txt", "wb").write(testFileContents.content)
            raceLink = ""
            for link in raceSoup.findAll("a"):
                currentLink = link.get("href")
                #print(currentLink)
                #print("CurrentLink in Riverside: "+str(currentLink))
                try:
                    linkText = link.contents[0] #Incase the link is on an image or something
                except:
                    continue
                if(currentLink.__contains__("https://www.milesplit")):
                    continue

                #print(linkText)
                if linkAccepted(linkText):
                    #print("Link Accepted!")
                    if (currentLink.__contains__("/raw")):
                        raceLink = currentLink
                    else:
                        raceLink = currentLink + "/raw" #Goes to the desired page
                    print("Approved: "+raceLink)
                    

            try:
                raceResultsReq = Request(raceLink)
                resultsPage = urlopen(raceResultsReq)
                raceResultsSoup = BeautifulSoup(resultsPage, "lxml")
                results = raceResultsSoup.find_all('pre') 
                #print(results)
                open("./"+readMeetName+"/"+year+"/results.txt", "w").write(str(results))
                p = p+1
            except:
                p=p+1



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