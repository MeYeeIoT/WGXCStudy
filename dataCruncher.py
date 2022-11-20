import mariadb
import matplotlib.pyplot as plt
import numpy as np


def hasNumber(string):
	return any(char.isdigit() for char in string)
def getData():
	results = []
	mydb = mariadb.connect(host="localhost", username="stats", password="crossCountry2048", database="statsProject")
	c = mydb.cursor()
	#c.execute("SELECT * FROM TeamData FULL OUTER JOIN MeetData WHERE TeamData.meetDate=MeetData.meetDate")
	#Command to run
	#SELECT TeamData.teamName,TeamData.runner1,TeamData.runner2,TeamData.runner3,TeamData.runner4,TeamData.runner5,TeamData.runner6,TeamData.runner7,MeetData.meetDate,MeetData.temp,MeetData.humidity,MeetData.dewPoint,MeetData.precip,MeetData.windspeed,MeetData.cloudcover FROM TeamData LEFT JOIN MeetData ON TeamData.meetId=MeetData.meetId;
	c.execute("SELECT * FROM TeamData")
	placeholder = c.fetchall()
	#placeholder = placeholder[1]
	print(placeholder)
	for r in placeholder:
		innerList = []
		for v in r:
			innerList.append(v)
		results.append(r)
	return results
def main():

    print(getData())
        
    #Plots to Have:
    #Meet Avg Time vs Temperature
    #Meet Avg Time vs Days into the Season
    #Meet Avg Time vs Humidity
    #Meet Avg Time vs Cloud Cover
    #Meet Avg Time vs Windspeed

    #WG Avg Time vs Temperature
    #WG Avg Time vs Days into the Season
    #WG Avg Time vs Humidity
    #WG Avg Time vs Cloud Cover
    #WG Avg Time vs Windspeed
    #WG Avg Time vs Number of people at the meet

    #Best Runner Time vs all of these

    #Most impactful variable on average time (steepest slope)

    variables = ["Temperature (°C)", "Humidity %", "Cloud Cover %", "Windspeed (mph)", "Days into Season"]
    slopes = []
    for i in range(len(variables)):
        #xArray = 
        #yArray = 

        a, b = np.polyfit(xArray, yArray, 1)

        slopes.append(a)

        plt.scatter(xArray, yArray)

        plt.plot(x, a*x+b)

        plt.text(1, 16, ' = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + variables[i], size=14)

        #Do we need to find some way to account for people just getting better over the season? Maybe not

        plt.xlabel(variables[i])
        plt.ylabel("Average Time")
        plt.savefig("team"+variables[i]+".png")
        i=i+1


if (__name__=="__main__"):
	main()
