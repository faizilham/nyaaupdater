#!/usr/bin/env python
"""
sample usage


"""

from nyaa_parser import fetch, download
from nyaa_db import NyaaDB

def checkUpdate(res):
	links = []
	update = []
	for e in res:
		ret = fetch(e[1],e[2])
		if (ret):
			n = 0
			while(n < len(ret) and ret[n][0] != e[3]):
				links.append((ret[n][1], ret[n][0] + ".torrent"))
				n = n + 1
			if (n ==0): print e[0], "is already updated"
			else:
				update.append(e[0])
				update.append(ret[0][0])
				print e[0], "has", n, "new update(s)!"
				for i in range(n): print ret[i][0]
		print
	return links, update
	

db = NyaaDB()
links, update = checkUpdate(db.load())
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
		db.updateDownloads(update)
