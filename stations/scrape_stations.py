import requests
import os 
import sqlite3
import time



def get_places():
	'''
		Get a list of locations 

	'''
	places = []
	url = "http://radio.garden/api/ara/content/places"
	response = requests.get(url)
	json_data = response.json()
	data = json_data['data']['list']
	for record in data:
		places.append((record['id'], record['title'], record['country']))
	return places

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
	 				stations['stations'].append((station_id, item['title'], f"https://radio.garden/api/ara/content/listen/{station_id}/channel.mp3", locationID ))

	return stations

def is_nearby(content):
	return  content['title'].lower() in [  'popular stations', 'selected stations']  or  'actionPage' in content.keys() 


def db_connect(dbName):
	conn = None
	try:
		conn = sqlite3.connect(dbName)
		
	except sqlite3.Error as e:
		print("Uh Oh!: ", e)

	return conn

def create_table(conn, query):
	try:
		c = conn.cursor()
		c.execute(query)
	except sqlite3.Error as e:
		print("Uh Oh!: " , e)

def insert_places(conn , place):
	query = """INSERT OR IGNORE INTO places(locationID, title, country) VALUES(?,?,?);"""
	if select_place(conn, place[0]) == []:
		c = conn.cursor()
		c.execute(query, place)
		conn.commit()

def select_place(conn, locationID):
	query = f"SELECT title FROM places WHERE locationID='{locationID}'"
	c = conn.cursor()
	c.execute(query)
	result = c.fetchall()
	#print("Result: ".ljust(5) + str(result))
	return result

def insert_station(conn, station):
	query =  """INSERT OR IGNORE INTO stations(stationID, title, url, locationID) VALUES(?,?,?,?);"""
	if select_station(conn, station[0]) == []:
		c = conn.cursor()
		c.execute(query, station)
		conn.commit()
		return 1
	return 0 

def select_station(conn, stationID):
	query = f"SELECT title FROM stations WHERE stationID='{stationID}'"
	c = conn.cursor()
	c.execute(query)
	result = c.fetchall()
	#print("Result: ".ljust(5) + str(result))
	return result

def main():
	dbName = "internet_radio_database.db"
	conn = db_connect(dbName)
	conn.execute("PRAGMA foreign_keys = 1")

	query_places_table = """CREATE TABLE IF NOT EXISTS places (locationID TEXT PRIMARY KEY, 
								title TEXT NOT NULL,
								country TEXT NOT NULL);
						 """
	query_stations_tables = """CREATE TABLE IF NOT EXISTS stations (stationID TEXT PRIMARY KEY, 
									title TEXT NOT NULL, url TEXT NOT NULL, locationID TEXT NOT NULL,  FOREIGN KEY(locationID) REFERENCES places(locationID));

							"""
	if conn is not None:
		create_table(conn, query_places_table)
		create_table(conn, query_stations_tables)
	else:
		print("Error! cannot create the database connection.")

	places = get_places()
	for place in places:
		insert_places(conn, place) 

	success = 0 
	for place in places:
		try:
			data = get_location_data(place[0])

		except Exception as e:
			print("Uh Oh! : " + e )

		else:
			for station in data['stations']:
				success = insert_station(conn, station)
				if success:
					print("Added station: ".ljust(10) + station[1])
					time.sleep(1)
	print("Scrape Completed!")

if __name__ == "__main__":
	main()