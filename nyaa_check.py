#!/usr/bin/env python
"""
sample usage
Faiz Ilham (faizilham.com) 2013

checks torrent updates and downloads it
"""

from nyaa_parser import fetch, download
from nyaa_db import NyaaDB

def checkUpdate(res):
	links = []
	updates = {}
	for key, val in res.items():
		ret = fetch(val[0],val[1])
		if (ret):
			n = 0
			while(n < len(ret) and ret[n][0] != val[2]):
				links.append((ret[n][1], ret[n][0] + ".torrent"))
				n = n + 1
			if (n ==0): print key, "is already updated"
			else:
				updates[key] = [None, None, ret[0][0]]
				print key, "has", n, "new update(s)!"
				for i in range(n): print ret[i][0]
		print
	return links, updates
	

db = NyaaDB()
links, updates = checkUpdate(db.load())
n = len(links)
if n > 0:
	print "Download all", n, "torrent(s)? y/n",
	var = raw_input()
	if var=="y":
		for e in links:
			try:
				download(e[0],e[1])
				print "Downloaded", e[1]
			except IOError:
				print "Connection Error"
		db.update(updates)
