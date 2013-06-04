"""
nyaa checker csv reader/updater
Faiz Ilham (faizilham.com) 2013

Manages fetch database.

the database (nyaa_checklist.csv) is a comma-seperated values of:
series_id, search_url, regex_pattern, last_downloaded

series_id : the series name
search_url : nyaa.eu search url
regex_pattern : regex pattern of desired result
last_downloaded: the last downloaded file's name, without .torrent extension

you may use any csv editor (text editor, Excel, etc) to add database entry.
leave last_downloaded with NULL for new entries

how to use:
1) build a NyaaDB object. you may use a custom file as long as it is consistent with the format above
	db = NyaaDB()
2) load the database
	db.load()
	it will return a dictionary of key series_id and values list [search_url, regex_pattern, last_downloaded]. ex: {series1: [url, pattern, filename]}
	you can also access this list using db.data
	
3) add and updates
	db.add(new_data)
	add new_data to database
	new_data is a dictionary of key series_id and values list [search_url, regex_pattern, last_downloaded]. ex: {series1: [url, pattern, filename]}
	
	db.delete(keys)
	delete entries with key keys from database
	keys is list of series_id. ex: [series1, series2, series3]
	
	db.update(updates)
	update database with updates
	updates is a dictionary of key series_id and values list [search_url, regex_pattern, last_downloaded]. ex: {series1: [url, pattern, filename]}
	if url, pattern or filename is not empty / None, it will be updated to the database
	please make sure the last_downloaded is the last downloaded file's name, without .torrent extension
	
	db.write()
	write changes to database file. write() is automatically called by add, delete and update
"""

class NyaaDB:
	def __init__(self, DB_NAME = "nyaa_checklist.csv"):
		self.DB_NAME = DB_NAME
		self.data = []
	
	def load(self):
		f = open(self.DB_NAME, "r")
		self.data = {}
		for ln in f:
			line = ln.strip()
			if(len(line)>0 and line[0]!="#"): # if not empty lines and comment
				entry = line.split(",")
				for i in range(len(entry)): entry[i] = entry[i].strip()
				key = entry.pop(0)
				self.data[key] = entry
		f.close()
		return self.data
	
	def add(self, new_data):
		for key, val in new_data.items():
			self.data[key] = val
		self.write()

	def update(self, updates):				
		if (self.data):
			for key, val in updates.items():
				for i in range(len(val)):
					if val[i]: self.data[key][i] = val[i]
			self.write()
			
	def delete(self, keys):
		if(self.data):
			for e in keys:
				del self.data[e]
			self.write()
	
	def write(self):
		f = open(self.DB_NAME, "w")
		for key, val in self.data.items():
			f.write(key + ",")
			f.write(val[0] + ",")
			f.write(val[1] + ",")
			f.write(val[2] + "\n")
		f.close()
