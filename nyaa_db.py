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
	it will return a list of tuple (series_id, search_url, regex_pattern, last_downloaded)
	you can also access this list using db.data
	
3) writing download updates
	db.updateDownloads(updates)
	updates is a list of series_id and last_downloaded. ex: [series1, last_download1, series2, last_download2, series3, last_download3]
	please make sure the last_downloaded is the last downloaded file's name, without .torrent extension
"""

class NyaaDB:
	def __init__(self, DB_NAME = "nyaa_checklist.csv"):
		self.DB_NAME = DB_NAME
		self.data = []
	
	def load(self):
		f = open(self.DB_NAME, "r")
		self.data = []
		for ln in f:
			line = ln.strip()
			if(len(line)>0 and line[0]!="#"):
				entry = line.split(",")
				for i in range(len(entry)): entry[i] = entry[i].strip()
				self.data.append(entry)
		f.close()
		return self.data
	
	def updateDownloads(self, updates):
		if (self.data):
			f = open(self.DB_NAME, "w")
			for e in self.data:
				f.write(e[0] + ",")
				f.write(e[1] + ",")
				f.write(e[2] + ",")
				if (e[0] in updates):
					i = updates.index(e[0]) + 1
					e[3] = updates[i]
				f.write(e[3] + "\n")
			f.close()
