#!/usr/bin/env python
"""
dbeditor
(not yet tested in windows!)
"""

from Tkinter import *
from nyaa_db import NyaaDB, NyaaSQLiteDB
import tkSimpleDialog
import tkMessageBox

db = NyaaSQLiteDB()
data = db.load()

class App:
	def __init__(self, master):
		frame = Frame(master, width=650, height=320)
		frame.pack()
		lf = Frame(frame, width=150, height=300)
		lf.place(x=10,y=10)
		self.rf = Frame(frame, width=470, height=300)
		# rf.place(x=170,y=10)
		
		# left frame
		self.listbox = Listbox(lf, width=200, height=16)
		self.listbox.place(x=0, y=0)
		self.listbox.bind("<<ListboxSelect>>", self.show_entry_bind)
		self.update_list()
		
		Button(lf,text="+", command=self.additem).place(x=0, y=265)
		
		self.delbutton = Button(lf,text="-", state=DISABLED, command=self.delitem)
		self.delbutton.place(x=40, y=265)
		
		# right frame
		self.series_id = StringVar()
		Label(self.rf, text="Series  : ").place(x=0, y=0)
		lblid = Label(self.rf, textvariable = self.series_id )
		lblid.place(x=55, y=0)
		
		Label(self.rf, text="URL     : ").place(x=0, y=30)
		self.series_url = Entry(self.rf, width=50)
		self.series_url.place(x=55, y=30)
		self.series_url.bind("<Key>", self.textupdated)

		Label(self.rf, text="Regex  : ").place(x=0, y=60)
		self.series_regex = Entry(self.rf, width=50)
		self.series_regex.place(x=55, y=60)
		self.series_regex.bind("<Key>", self.textupdated)
		
		Label(self.rf, text="Last dl : ").place(x=0, y=90)
		self.series_last = Entry(self.rf, width=50)
		self.series_last.place(x=55, y=90)
		self.series_last.bind("<Key>", self.textupdated)
		
		self.updatebtn = Button(self.rf, text="Update", state=DISABLED, command=self.updatedata)
		self.updatebtn.place(x=390, y=120)
	
	def additem(self):
		key = tkSimpleDialog.askstring("Add Series","Series ID (unique, immutable)")
		if key and not db.data.get(key):
			db.add({key : ["NONE", "NONE", "NONE"]})
			self.update_list()
			i = sorted(db.data.keys()).index(key)
			self.listbox.select_set(i)
			self.show_entry(i)
			
	def delitem(self):
		key = self.series_id.get()
		ans = tkMessageBox.askyesno("Delete Series", 'Delete "' + key + '"?')
		if ans:
			self.listbox.delete(0, END)
			db.delete([key])
			self.update_list()
			self.listbox.select_set(-1)
			self.show_entry(-1)
	
	def updatedata(self):
		self.updatebtn.config(state=DISABLED)
		updates = {}
		data = []
		data.append(self.series_url.get())
		data.append(self.series_regex.get())
		data.append(self.series_last.get())
		updates[self.series_id.get()] = data
		db.update(updates)
		
	def textupdated(self, event):
		self.updatebtn.config(state=NORMAL)
		
	def show_entry_bind(self, event):
		i = self.listbox.curselection()
		self.show_entry(i)
		
	def show_entry(self, i):
		if (i >=0):
			key = self.listbox.get(i)
			self.series_id.set(key)
			self.series_url.delete(0,END)
			self.series_url.insert(0,db.data[key][0])
			
			self.series_regex.delete(0,END)
			self.series_regex.insert(0,db.data[key][1])
			
			self.series_last.delete(0,END)
			self.series_last.insert(0,db.data[key][2])
			
			self.delbutton.config(state=NORMAL)
			self.rf.place(x=170,y=10)
		else:
			self.rf.place_forget()
			self.delbutton.config(state=DISABLED)

	def update_list(self):
		self.listbox.delete(0, END)
		for e in sorted(db.data.keys()):
			self.listbox.insert(END, e)

root = Tk()
root.wm_title("Nyaa Feed Database Editor")
root.resizable(width=FALSE, height=FALSE)
img = PhotoImage(file='icon.gif')
root.tk.call('wm', 'iconphoto', root._w, img)
app = App(root)
root.mainloop()
