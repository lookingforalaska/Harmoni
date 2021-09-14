import requests
import os 



def get_places():
	'''
		Get a list of locations 

	'''
	url = "http://radio.garden/api/ara/content/places"
	response = requests.get(url)
	json_data = response.json()
	data = json_data['data']['list']
	for record in data:
		print()
		print("id: " + record['id'])
		print("title: " + record['title'])
		print("country: " + record['country'])
		print()


def get_location_data(locationID):
	stations = {}
	url = f"https://radio.garden/api/ara/content/page/{locationID}"
	location_data = requests.get(url).json()
	stations['location'] = location_data['data']['title']
	stations['stations'] = []
	for content in location_data['data']['content']:
	 	if is_nearby(content):
	 		for item in content['items']:
	 			if 'href' in item:
	 				station_id = item['href'].split("/")[-1]
	 				stations['stations'].append((item['title'], f"https://radio.garden/api/ara/content/listen/{station_id}/channel.mp3" ))
	print(stations)

def is_nearby(content):
	return  content['title'].lower() in [  'popular stations', 'selected stations']  or  'actionPage' in content.keys() 


def main():
	get_places()
	#get stations from sandiego
	get_location_data("Ho58GDOX")
	#add records 
main()