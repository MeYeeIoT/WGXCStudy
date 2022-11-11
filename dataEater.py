from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import requests
import os
from time import sleep
from datetime import datetime
import mariadb
startYear = 2017
endYear = 2022
valleyDivision = ["Grand Valley", "Crestwood", "Independence", "Wickliffe", "Cardinal", "Kirtland", "Berkshire", "Trinity", "Richmond"]
chagrinDivision = ["West Geauga", "Hawken", "Orange", "Edgewood", "Chagrin Falls", "Geneva", "Beachwood", "Perry", "Lakeside", "Harvey"]
class ListTooLong(Exception):
	pass
def hasNumber(string):
	return any(char.isdigit() for char in string)
def averageTimeCalculator(times):
	timeList = []
	for t in times:
		timeSplit = t.split(":")
		minutes = int(timeSplit[0])*60
		seconds = int(timeSplit[1])
		time = minutes+seconds
		timesList.append(time)
	averageTime = sum(timeList)/len(timeList)
	averageTimeMinutes = math.floor(averageTime/60)
	averageTimeSeconds = round(averageTime%60, 4)
	if (averageTimeSeconds<10):
		return str(averageTimeMinutes)+":0"+str(averageTimeSeconds)
	else:
		return str(averageTimeMinutes)+":"+str(averageTimeSeconds)
def checkLink(link, y, t):
	if (link=="Varsity Boys" or link=="\"Completed\" Results" or link=="Boys D2 Varsity" or link=="D2 Varsity" or link=="Varsity Results" or link=="boys varsity" or link=="Varsity D2/3 Results"):
		return True
	elif (link=="Boys DI/DII" or link=="D2 Boys" or link=="Boys Results" or link=="Small School Division" or link=="HS Boys Varsity" or link=="Region 5"):
		return True
	elif (y<2019 and t=="Hawken"  and (link=="Varsity Boys - Valley" or link=="Boys Valley" or link=="boys valley varsity" or link=="Valley Division")):
		return True
	elif ((t in valleyDivision) and (link=="Varsity Boys - Valley" or link=="Boys Valley" or link=="boys valley varsity" or link=="Valley Division" or link=="Valley Varsity Boys")):
		return True
	elif ((t in chagrinDivision) and (link=="Varsity Boys - Chagrin" or link=="boys chagrin varsity" or link=="Boys Chagrin" or link=="boys chagrin varsity" or link=="Chagrin Division" or link=="Chagrin Varsity Boys")):
		return True
	else:
		return False
def getWeatherData(location, date, time):
	weatherData = []
	city = location.split(",")[0]
	state = location.split(",")[1].strip()
	response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"+city+"%2C%20"+state+"/"+date+"/"+date+"?unitGroup=metric&include=hours&key=U36K99V5F9CQN7A6LPRAT3SYP&contentType=json")
	data = response.json()
	for item in data["days"][0]["hours"]:
		if (item["datetime"]==time):
			weatherData.append(item["temp"])
			weatherData.append(item["humidity"])
			weatherData.append(item["dew"])
			weatherData.append(item["precip"])
			weatherData.append(item["windspeed"])
			weatherData.append(item["windgust"])
			weatherData.append(item["cloudcover"])
	return weatherData
def getTeams():
	teams = []
	request = Request("https://oh.milesplit.com/meets/501164-ohsaa-division-2-district-madison-2022/teams")
	page = urlopen(request)
	soup = BeautifulSoup(page, "lxml")
	for tag in soup.find_all("td", "name"):
			urlString = str(tag.find("a").get("href"))
			teamName = str(tag.find("a").text.strip())
			teamNumber = [int(x) for x in urlString if x.isdigit()]
			cNum = ""
			for n in teamNumber:
				cNum+=str(n)
			teams.append([int(cNum), teamName])
	return teams
def getMeets(team, year):
	meetsData = []
	response = requests.get("https://oh.milesplit.com/api/v1/teams/"+str(team[0])+"/schedules?season=cc&year="+str(year))
	meetData = response.json()
	for x in meetData["data"]:
		for y in range(len(meetData["data"][x])):
			for d in range(len(meetData["data"][x][y]["items"])):
				name = meetData["data"][x][y]["items"][d]["name"]
				meetLink = meetData["data"][x][y]["items"][d]["link"]
				meetsData.append([name, meetLink])
	return meetsData
def getMeetResults(meetData, year, team):
	teamName = team[1].split()
	if (len(teamName)==1):
		team[1] = team[1]
	elif (teamName[0].__contains__(".")):
		team[1] = teamName[1]
	elif (teamName[1].__contains__(".")):
		team[1] = teamName[1]
	else:
		team[1] = team[1]
	name = (meetData[0]).lower()
	name = name.replace(" - ", " ")
	name = name.replace(" ", "-")
	meetLink = meetData[1]+"-"+name+"-"+str(year)+"/results"
	resultsRequest = Request(meetLink)
	resultPage = urlopen(resultsRequest)
	resultSoup = BeautifulSoup(resultPage, "lxml")
	raceLink = None
	results = None
	date = None
	for link in resultSoup.findAll("a"):
		currentLink = link.get("href")
		try:
			linkText = link.contents[0].strip()
		except:
			continue
		if(currentLink.__contains__("https://www.milesplit")):
			continue
		if checkLink(linkText, year, team[1]):
			print(linkText)
			if (currentLink.__contains__("/raw")):
				raceLink = currentLink
			else:
				raceLink = currentLink + "/raw"
	if raceLink is not None:
		resultsRequest = Request(raceLink)
		resultsPage = urlopen(resultsRequest)
		sleep(0.5)
		resultSoup = BeautifulSoup(resultsPage, "lxml")
		sleep(0.5)
		date = resultSoup.find("time").text.strip()
		date = datetime.strptime(date, "%b %d, %Y").isoformat()[:10]
		location = resultSoup.find("div", "venueCity").text.strip()
		results = str(resultSoup.find("div", id="meetResultsBody"))
	else:
		return None
	if (results.__contains__("Girls") or results.__contains__("girls")):
		bSplit = results.split("5K")
		if (len(bSplit)<2):
			bSplit = results.split("5,000")
		for b in range(1, len(bSplit)):
			lines = bSplit[b].split("\n")
			prevLines = bSplit[b-1].split("\n")
			if ((lines[0].__contains__("Run") and prevLines[-1].__contains__("Boys")) or (lines[0].__contains__("Varsity") and prevLines[-1].__contains__("Boys"))):
				results = bSplit[b]
			elif ((lines[0].__contains__("run") and prevLines[-1].__contains__("boys")) or (lines[0].__contains__("varsity") and prevLines[-1].__contains__("boys"))):
				results = bSplit[b]
			elif ((lines[0].__contains__("Run") and prevLines[-1].__contains__("boys")) or (lines[0].__contains__("Varsity") and prevLines[-1].__contains__("boys"))):
				results = bSplit[b]
			elif ((lines[0].__contains__("run") and prevLines[-1].__contains__("Boys")) or (lines[0].__contains__("varsity") and prevLines[-1].__contains__("Boys"))):
				results = bSplit[b]
			if (team[1] in chagrinDivision):
				if (lines[0].__contains__("Chagrin") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("Varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("chagrin") and prevLines[-1].__contains__("boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("Chagrin") and prevLines[-1].__contains__("boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("chagrin") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("chagrin") and prevLines[-1].__contains__("boys") and lines[0].__contains__("Varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("Chagrin") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("chagrin") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("Varsity")):
					results = bSplit[b]
			elif (team[1] in valleyDivision):
				if (lines[0].__contains__("Valeey") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("Varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("valley") and prevLines[-1].__contains__("boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("Valley") and prevLines[-1].__contains__("boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("valley") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("valley") and prevLines[-1].__contains__("boys") and lines[0].__contains__("Varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("Valley") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("varsity")):
					results = bSplit[b]
				elif (lines[0].__contains__("valley") and prevLines[-1].__contains__("Boys") and lines[0].__contains__("Varsity")):
					results = bSplit[b]
	times = []
	lines = results.split("\n")
	try:
		for line in lines:
			if (line.__contains__(team[1])):
				for item in line.split():
					if (len(item.split(":"))>2):
						item = item[2:]
					if (hasNumber(item) and item.__contains__(":") and int(item.split(":")[0])>13 and int(item.split(":")[0])<45):
						print(item)
						if (len(times)>=7):
							raise ListTooLong
						else:
							times.append(item)
	except ListTooLong:
		pass
	while (len(times)<7):
		times.append("NULL")
	return [meetData[0], times, date, location, team[1]]
def enterMeetData(meetData, c, mydb):
	strCommand = "INSERT INTO MeetData VALUES ('"+meetData[0]+"', '"+meetData[2]+"'"
	nullMark = False
	for data in meetData[5]:
		if (data is None):
			strCommand+=", NULL"
		else:
			strCommand+=", "+str(data)
	strCommand+=")"
	c.execute(strCommand)
	mydb.commit()
def enterTeamData(meetData, c, mydb):
	strCommand = "INSERT INTO TeamData VALUES ('"+meetData[4]+"', '"+meetData[2]
	nullMark = False
	for time in meetData[1]:
		if (time=="NULL" and not nullMark):
			strCommand+=("', "+time)
			nullMark = True
		elif (time=="NULL" and nullMark):
			strCommand+=(", "+time)
			nullMark = True
		elif (nullMark):
			strCommand+=(", '"+time)
			nullMark = False
		else:
			strCommand+=("', '"+time)
			nullMark = False
	if (nullMark):
		strCommand+=")"
	else:
		strCommand+="')"
	c.execute(strCommand)
	mydb.commit()
def main():
	mydb = mariadb.connect(host="localhost", username="stats", password="crossCountry2048", database="statsProject")
	cursor = mydb.cursor()
	cursor.execute("SHOW tables")
	result = cursor.fetchall()
	meetTableExists = False
	teamTableExists = False
	for r in result:
		if (r[0]=="MeetData"):
			cursor.execute("SELECT * FROM MeetData")
			r = cursor.fetchall()
			if (r!=[]):
				cursor.execute("DELETE FROM MeetData")
				mydb.commit()
			meetTableExists = True
		elif (r[0]=="TeamData"):
			cursor.execute("SELECT * FROM TeamData")
			r = cursor.fetchall()
			if (r!=[]):
				cursor.execute("DELETE FROM TeamData")
				mydb.commit()
			teamTableExists = True
	if (not meetTableExists):
		cursor.execute("CREATE TABLE MeetData (meetName VARCHAR(255) NOT NULL, meetDate DATE NOT NULL, temp FLOAT, humidity FLOAT, dewPoint FLOAT, precip FLOAT, windspeed FLOAT, windgust FLOAT, cloudcover FLOAT)")
	if (not teamTableExists):
		cursor.execute("CREATE TABLE TeamData (teamName VARCHAR(255) NOT NULL, meetDate DATE NOT NULL, runner1 TIME, runner2 TIME, runner3 TIME, runner4 TIME, runner5 TIME, runner6 TIME, runner7 TIME)")
	results = []
	teams = getTeams()
	for year in range(startYear, endYear):
		print(year)
		for team in teams:
			if (team[1]=="Beaumont"):
				continue
			print(team[1])
			meets = getMeets(team, year)
			for meet in meets:
				if (meet[0].__contains__("McQuaid")):
					continue
				print(meet[0])
				results = getMeetResults(meet, year, team)
				if results is None:
					print("Link not found")
					continue
#				results.append(getWeatherData(results[3], results[2], "10:00:00"))
#				enterMeetData(results, cursor, mydb)
				enterTeamData(results, cursor, mydb)
	mydb.close()
if __name__=="__main__":
	main()
