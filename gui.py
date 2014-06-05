#!/usr/bin/python

from Tkinter import * 

root = Tk()
root.title("YABM - Yet Another Backup Manager")

frmTop = Frame(root)
frmTop.grid(row=0, column=0, sticky=N+S+E+W)

frmBottom = Frame(root)
frmBottom.grid(row=1, column=0, sticky=E)

lblSelect = Label(frmTop, text="Please select a configuration to load:")
lblSelect.grid(row=0, column=0, sticky=W)

lbConfigs = Listbox(frmTop)
lbConfigs.grid(row=1, column=0)

btnNew = Button(frmBottom, text="New")
btnNew.grid(row=0, column=0)

btnLoad = Button(frmBottom, text="Load")
btnLoad.grid(row=0, column=1)

root.mainloop()

def test(*args):
  print "test"


