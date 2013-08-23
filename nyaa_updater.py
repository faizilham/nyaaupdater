#!/usr/bin/env python
"""
Nyaa.eu Feed Auto Updater

Faiz Ilham (faizilham.com) 2013
"""

from nyaa_parser import fetch, download
from nyaa_db import NyaaSQLiteDB
from threading import Thread
import os, stat

DBNAME = '/home/pi/db/nyaa.db'
DOWNLOAD_DIR = '/home/pi/download/update/'
NUM_UPDATER = 4
NUM_DOWNLOADER = 4

class DownloadJob(Thread):
	def __init__(self, links):
		Thread.__init__(self)
		self.links = links
		
	def run(self):
		for link in self.links:
			filename, url = DOWNLOAD_DIR + link[1] + ".torrent", link[2] 
			download(url, filename)
			os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

class UpdaterJob(Thread):
	def __init__(self, db):
		Thread.__init__(self)
		self.db = db
		
	def run(self):
		self.links = []
		self.updates = {}
		
		for series, val in self.db.items():
			url, pattern, last = val[0], val[1], val[2]

			feeds = fetch(url, pattern)
			
			if (feeds):
				n = 0
				while(n < len(feeds) and feeds[n]['name'] != last):
					self.links.append((series, feeds[n]['name'], feeds[n]['link'], feeds[n]['date']))
					n = n + 1
							
				if (n != 0):
					self.updates[series] = [None, None, feeds[0]['name']]


def db_updates(db, links, updates):
	
	db.update(updates) # update `series` table
	
	# update `updates` table
	conn = db.connect()
	conn.execute('CREATE TABLE IF NOT EXISTS updates (id_update INTEGER PRIMARY KEY AUTOINCREMENT, series_name TEXT NOT NULL, filename TEXT NOT NULL, url TEXT NOT NULL, pubdate TEXT NOT NULL)')
	
	conn.executemany('INSERT INTO updates(series_name, filename, url, pubdate) VALUES (?, ?, ?, ?)', links)
	conn.commit()
	db.close()
	
	# divide .torrent downloads into NUM_DOWNLOADER threads
	
	item_per_job = len(links) / NUM_DOWNLOADER + (0 if len(links) % NUM_DOWNLOADER == 0 else 1)
	
	temp, jobs = [], []
	n, total = 0, 0
	
	for link in links:
		temp.append(link)
		n, total = n + 1, total + 1
		
		if(n==item_per_job or total == len(links)):
			n = 0
			job = DownloadJob(temp)
			jobs.append(job)
			job.start()
			temp = []
	
	for job in jobs:
		job.join()
	
	# all download finish	
	

def update(db):
	data = db.load()
	
	# divide check series updates into NUM_UPDATER threads
	
	item_per_job = len(data) / NUM_UPDATER + (0 if len(data) % NUM_UPDATER == 0 else 1)
	
	temp, jobs = {}, []
	n, total = 0, 0
	for key, value in data.items():
		temp[key] = value
		n = n + 1
		total = total + 1
		if (n==item_per_job or total == len(data)):
			n = 0
			job = UpdaterJob(temp)
			jobs.append(job)
			job.start()
			temp = {}
				
	links, updates = [], {}
	for job in jobs:
		job.join()
		links = links + job.links
		updates.update(job.updates)
	
	# all series checked
	
	return links, updates

if __name__ == "__main__":
	db = NyaaSQLiteDB(DBNAME)
	links, updates = update(db)
	
	if (links):
		print len(links), "new updates found"
		db_updates(db, links, updates)
	else:
		db.close()
