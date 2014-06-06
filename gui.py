#!/usr/bin/python

from Tkinter import *
from cronmanager import *

class MainWindow:
  def __init__(self):
    self.cm = CronManager()
    self.lbConfigs = None

    root = Tk()
    root.title("YABM - Yet Another Backup Manager")
    
    frmTop = Frame(root)
    frmTop.grid(row=0, column=0, sticky=N+S+E+W)
    frmBottom = Frame(root)
    frmBottom.grid(row=1, column=0, sticky=E)

    lblSelect = Label(frmTop, text="Please select a configuration to load:")
    lblSelect.grid(row=0, column=0, sticky=W)

    sbConfigs = Scrollbar(frmTop, orient=VERTICAL)
    self.lbConfigs = Listbox(frmTop, yscrollcommand=sbConfigs.set)
    self.lbConfigs.config(font=("TkFixedFont"))
    self.lbConfigs.grid(row=1, column=0, sticky=N+S+E+W)
    sbConfigs.config(command=self.lbConfigs.yview)
    sbConfigs.grid(row=1, column=1, sticky=N+S+E+W)
 
    btnNew = Button(frmBottom, text="New")
    btnNew.grid(row=0, column=0)
    btnLoad = Button(frmBottom, text="Load")
    btnLoad.grid(row=0, column=1)

    self.load_configs()

    root.mainloop()
  
  def load_configs(self):
    self.lbConfigs.delete(0, END)
    self.lbConfigs.insert(END, "Name        | Active")
    
    self.cm.load_all()
    for config in self.cm.configs:
      self.lbConfigs.insert(END, config.name)


def test(*args):
  print "test"


