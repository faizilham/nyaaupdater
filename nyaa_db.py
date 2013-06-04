"""
nyaa feed database manager
Faiz Ilham (faizilham.com) 2013

Manages feed database.
"""

class NyaaDB:
	def __init__(self, DB_NAME = "nyaa_checklist.csv"):
		self.DB_NAME = DB_NAME
		self.data = []
		
	# load database	
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
	
	# add values to database
	def add(self, new_data):
		for key, val in new_data.items():
			self.data[key] = val
		self.write()

	# update values to database
	def update(self, updates):				
		if (self.data):
			for key, val in updates.items():
				for i in range(len(val)):
					if val[i]: self.data[key][i] = val[i]
			self.write()
			
	# delete from database
	def delete(self, keys):
		if(self.data):
			for e in keys:
				del self.data[e]
			self.write()
	
	# write changes to database. auto-called by add, update and delete
	def write(self):
		f = open(self.DB_NAME, "w")
		for key, val in self.data.items():
			f.write(key + ",")
			f.write(val[0] + ",")
			f.write(val[1] + ",")
			f.write(val[2] + "\n")
		f.close()
