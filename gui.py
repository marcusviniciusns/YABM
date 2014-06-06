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

    header  = self.format("Name", 12) + "|"
    header += self.format("Active", 6) + "|"
    header += self.format("Source", 20) + "|"
    header += self.format("Destination", 20) 

    self.lbConfigs.insert(END, header)
    
    self.cm.load_all()
    for config in self.cm.configs:
      row  = self.format(str(config.name), 12) + "|"
      row += self.format(str(config.enabled), 6) + "|"
      row += self.format(str(config.command.source), 20) + "|"
      row += self.format(str(config.command.destination), 20)
      self.lbConfigs.insert(END, row) 

  def format(self, str, size):
    if len(str) < size:
      return str + (" " * (size - len(str)))
    if len(str) == size:
      return str 
    return str[:size-3] + "..."


def test(*args):
  print "test"


