import tkFileDialog as fd
from Tkinter import *
from os import getcwd, path
from tkSnack import initializeSnack,Sound
cwd = getcwd()
win = Tk()
initializeSnack(win)
class single(object):
	def __init__(self, pos=[0,0]):
		self.img = PhotoImage(file="%s/icons/button_off.gif" % (cwd))
		self.but = Button(win, image=self.img, command=lambda: self.switch())
		self.state = False
		self.but.grid(row=pos[0], column=pos[1])
	def switch(self):
		if self.state==False:
			self.state = True
			self.img = PhotoImage(file="%s/icons/button_on.gif" % (cwd))
			self.but.configure(image=self.img)
		else:
			self.state = False
			self.img = PhotoImage(file="%s/icons/button_off.gif" % (cwd))
			self.but.configure(image=self.img)
	def active(self, st=False):
		high = ""
		state = "off"
		if self.state==True: state = "on"
		if st==True: high = "_highlight"
		self.img = PhotoImage(file="%s/icons/button_%s%s.gif" % (cwd,state,high))
		self.but.configure(image=self.img)
class row(object):
	def __init__(self, row=0, length=5):
		self.snd = Sound()
		self.buts = {}
		self.act = True
		self.des = False
		self.row = row
		self.pos = 5
		self.o_i = PhotoImage(file="%s/icons/open.gif" % (cwd))
		self.open = Button(win, image=self.o_i, command=lambda: self.l_file())
		self.a_i = PhotoImage(file="%s/icons/add.gif" % (cwd))
		self.a = Button(win, image=self.a_i, command=lambda: self.add())
		self.r_i = PhotoImage(file="%s/icons/sub.gif" % (cwd))
		self.r = Button(win, image=self.r_i, command=lambda: self.rem())
		self.d_i = PhotoImage(file="%s/icons/destroy.gif" % (cwd))
		self.d = Button(win, image=self.d_i, command=lambda: self.destroy())
		self.m_i = PhotoImage(file="%s/icons/mute_off.gif" % (cwd))
		self.m = Button(win, image=self.m_i, command=lambda: self.mute())
		self.a.grid(row=row, column=4)
		self.r.grid(row=row, column=3)
		self.open.grid(row=row, column=2)
		self.d.grid(row=row, column=0)
		self.m.grid(row=row, column=1)
		self.length = length
		for num in range(5,length+5):
			self.buts[num] = single([row,num])
	def l_file(self):
		fname = fd.askopenfilename(filetypes=[("Audio Files",".wav")])
		if fname != "": self.snd.read(fname); self.open.configure(state=DISABLED)
	def add(self):
		if self.length+1 > len(self.buts): self.buts[self.length+5] = single([self.row, self.length+5])
		else: self.buts[self.length+5].but.grid(row=self.row, column=self.length+5)
		self.length+=1
	def rem(self): 
		if self.length != 0: 
			self.buts[self.length+4].but.grid_remove() 
			self.length -= 1
	def mute(self):
		if self.act:
			self.act = False
			self.m_i = PhotoImage(file="%s/icons/mute_on.gif" % (cwd))
			self.m.configure(image=self.m_i)
		else:
			self.act = True
			self.m_i = PhotoImage(file="%s/icons/mute_off.gif" % (cwd))
			self.m.configure(image=self.m_i)
	def next(self):
		if self.act:
			self.buts[self.pos].active(False)
			self.pos += 1
			if self.pos > self.length+4: self.pos=5
			if self.buts[self.pos].state==True: self.snd.play()
			self.buts[self.pos].active(True)
	def destroy(self):
		self.act = False
		self.des = True
		self.open.grid_remove()
		self.a.grid_remove()
		self.r.grid_remove()
		self.m.grid_remove()
		self.d.grid_remove()
		for b in self.buts:
			self.buts[b].but.grid_remove()
class master(object):
	def __init__(self, de=100):
		self.rows={}
		self.delay = de
		self.st = False
		self.a_i = PhotoImage(file="%s/icons/add.gif" % (cwd))
		self.a = Button(win, image=self.a_i, command=lambda: self.add())
		self.a.grid(row=len(self.rows), column=0)
		self.s_i = PhotoImage(file="%s/icons/start.gif" % (cwd))
		self.s = Button(win, image=self.s_i, command=lambda: self.start())
		self.s.grid(row=len(self.rows), column=1)
		self.sto_i = PhotoImage(file="%s/icons/stop.gif" % (cwd))
		self.sto = Button(win, image=self.sto_i, command=lambda: self.stop())
		self.sto.grid(row=len(self.rows), column=2)
		self.add()
		self.add()
	def stop(self): self.st = True; self.s.configure(state=NORMAL)
	def add(self):
		ind = len(self.rows)+1
		self.rows[ind] = row(ind)
		self.a.grid(row=ind+1, column=0)
		self.s.grid(row=ind+1, column=1)
		self.sto.grid(row=ind+1, column=2)
	def start(self):
		self.s.configure(state=DISABLED)
		for row in self.rows:
			self.rows[row].buts[self.rows[row].pos].active(False)
			self.rows[row].pos = 5
		self.st = False
		self.loop()
	def loop(self):
		for row in self.rows: self.rows[row].next()
		if not self.st: win.after(self.delay, lambda: self.loop())

master()
win.mainloop()