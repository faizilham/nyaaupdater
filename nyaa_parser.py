"""
Nyaa.eu Feed Updater

nyaa.eu HTML Parser
Faiz Ilham (faizilham.com) 2013

Fetching and parsing nyaa.eu search.
"""

import urllib
import urllib2
import re
from xml.etree import ElementTree

# download from url
def download(url, filename, retry_num=5):
	n = 0
	while n < retry_num:
		try:
			urllib.urlretrieve(url, filename)
			return True
		except:
			n = n + 1
	return False

# fetch from url, return list of feed dictionary {name, link, page, desc, date}
def fetch(url, pattern, retry_num=5):
	n = 0
	while n < retry_num: 
		try:
			handler = urllib2.urlopen(url)
			content = handler.read()
			return parse(content, pattern)

		except:
			n = n + 1
			
	return None

# parse xml data and build the list of feed dictionary
def parse(raw_xml_string, pattern):
	channel = ElementTree.fromstring(raw_xml_string).find('channel')
	result = []
	for item in channel.findall('item'):
		name = item.find('title').text				# filename
				
		if(re.match(pattern, name)):
			link = item.find('link').text			# download link
			desc = item.find('description').text	# torrent info
			guid = item.find('guid').text			# information page link
			pubdate = item.find('pubDate').text		# publish date
				
			result.append({'name': name, 'link': link, 'page':guid, 'desc': desc,'date': pubdate})
		
	return result
