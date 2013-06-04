"""
nyaa.eu html parser
Faiz Ilham (faizilham.com) 2013

library functions:
1)	fetch(url, regexPattern)
	connect to url (nyaa.eu search url) and fetch result by regexPattern using NyaaParser
	the result will be a list of tuple (filename, link)
2)	download(url, filename)
	download from url as filename

how to use NyaaParser:
1) 	build a NyaaParser object
	parser = NyaaParser(regexPattern [, parseAll=True])
	
	regexPattern is used to identify which search result should be taken
	parseAll is used to check whether feth all result or not. if it is False, NyaaParser only fetch the first result.
	
2)	feed with a nyaa.eu search result page (html)
	parser.feed(nyaaPage)
	
3)	fetch the result
	result = parser.result
	
	the result will be a list of tuple (filename, link)
"""

import urllib
import urllib2
import re
from HTMLParser import HTMLParser

def download(url, filename):
	urllib.urlretrieve(url, filename)

def fetch(url, pattern):
	try:
		handler = urllib2.urlopen(url)
		content = handler.read()
		parser = NyaaParser(pattern)
		parser.feed(content)
		return parser.result
	except IOError:
		print "Connection Error"

class NyaaParser(HTMLParser):
	
	# self.state = class tag <td>, 0: none/else, 1: tlistname, 2: tlistdownload
	def __init__(self, pattern, parseall=True):
		HTMLParser.__init__(self)
		self.pattern = pattern	
		self.parseall = parseall
		self.state = 0 
		self.temp = ""
		self.result = []
		
	# open tag handler
	def handle_starttag(self, tag, attrs):
		if (attrs and attrs[0][0]=="class"):
			if (attrs[0][1]=="tlistname"): self.state = 1
			elif (attrs[0][1]=="tlistdownload"): self.state = 2
		elif (tag=="a" and self.state==2 and len(self.temp) > 0):
			if(self.parseall or len(self.result) == 0):
				self.result.append((self.temp, attrs[0][1]))

	# close tag handler
	# restore state to 0 (none) if reads </td>
	def handle_endtag(self, tag):
		if (tag=="td"):
			if (self.state==2): self.temp = ""
			elif(self.state==1):
				if(not re.match(self.pattern, self.temp)): self.temp = ""
			self.state=0		
			
	# data handler
	# read data section only inside td class="tlistname"
	def handle_data(self, data):
		if (self.state==1): 
			self.temp = self.temp + data
	def handle_entityref(self, name):
		if (self.state==1): 
			c = unichr(name2codepoint[name])
			self.temp = self.temp + c
	def handle_charref(self, name):
		if (self.state==1):
			c = ""
			if name.startswith('x'):
				c = unichr(int(name[1:], 16))
			else:
				c = unichr(int(name))
			self.temp = self.temp + c
