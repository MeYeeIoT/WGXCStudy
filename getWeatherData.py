from urllib.request import urlopen, Request
import requests
header = {"token":"ypTNQbNqvOgdhGFGryHRkiJYWzIZGHxj"}
def findLocationId(location):
	response = requests.get("https://www.ncei.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CITY&sortfield=name&limit=100&offset=300", headers=header)
	data = response.json()
	for item in data["results"]:
		if (item["name"].__contains__(location)):
			return item["id"]
def main():
	#cityId = findLocationId("Cleveland, OH")
	response = requests.get("https://www.ncei.noaa.gov/cdo-web/api/v2/datasets?locationid:CITY:US390010&startdate=", headers=header)
	#print(response.json())
	data = response.json()
	for item in data["results"]:
		print(item)
if __name__=="__main__":
	main()
