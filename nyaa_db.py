"""
Nyaa.eu Feed Updater

Nyaa Feed Database Manager
Faiz Ilham (faizilham.com) 2013

Manages feed database.
"""
import sqlite3


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
			if(len(line)>0 and line[0] != "#"): # if not empty lines and comment
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
	
	# write changes to database. auto-called by add, update, and delete
	def write(self):
		f = open(self.DB_NAME, "w")
		for key, val in self.data.items():
			f.write(key + ",")
			f.write(val[0] + ",")
			f.write(val[1] + ",")
			f.write(val[2] + "\n")
		f.close()

# SQLite Version
class NyaaSQLiteDB:
	def __init__(self, DB_NAME = "nyaa_checklist.db", autoclose=True):
		self.DB_NAME = DB_NAME
		self.autoclose = autoclose
		self.data = {}
		self.conn = None
	
	def connect(self):
		if (self.conn==None): self.conn = sqlite3.connect(self.DB_NAME)
		return self.conn
		
	def close(self):
		if(self.conn!=None):
			self.conn.close()
			self.conn = None
	
	def load(self):
		conn = self.connect()
		conn.execute('CREATE TABLE IF NOT EXISTS series (name TEXT PRIMARY KEY, url TEXT NOT NULL, pattern TEXT NOT NULL, last TEXT)')
		self.data = {}
		for row in conn.execute('SELECT * FROM series ORDER BY name'):
			self.data[row[0]] = [row[1], row[2], row[3]]
		
		conn.commit()
		if(self.autoclose): self.close()
		
	def add(self, new_data):
		conn = self.connect()
		ndata = []
		for key, val in new_data.items():
			self.data[key] = val
			ndata.append((key, val[0], val[1], val[2]))
		
		conn.executemany('INSERT INTO series VALUES (?, ?, ?, ?)', ndata)
		conn.commit()
		if(self.autoclose): self.close()
		
	def delete(self, keys):
		conn = self.connect()
		
		for name in keys:
			conn.execute('DELETE FROM series WHERE name=?', (name,))
			del self.data[name]
		
		conn.commit()
		if(self.autoclose): self.close()
		
	def update(self, updates):
		conn = self.connect()
		ndata = []
		for key, val in updates.items():
			v = []
			
			# checking None values
			for i in range(len(val)):
				if val[i]: 
					v.append(val[i])
					self.data[key][i] = val[i]
				else: v.append(self.data[key][i])
				
			ndata.append((v[0], v[1], v[2], key))
		
		conn.executemany('UPDATE series SET url=?, pattern=?, last=? WHERE name=?', ndata)
		conn.commit()
		if(self.autoclose): self.close()
	
	def write(self):
		pass
