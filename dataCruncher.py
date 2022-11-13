import mariadb
def hasNumber(string):
	return any(char.isdigit() for char in string)
def getData():
	results = []
	mydb = mariadb.connect(host="localhost", username="stats", password="crossCountry2048", database="statsProject")
	c = mydb.cursor()
	c.execute("SELECT * FROM TeamData FULL OUTER JOIN MeetData WHERE TeamData.meetDate=MeetData.meetDate")
	placeholder = c.fetchall()
	placeholder = placeholder[0]
	for r in placeholder:
		innerList = []
		for v in r:
			innerList.append(v)
		results.append(r)
	return results
def main():
	#Do some data crunching
if (__name__=="__main__"):
	main()
