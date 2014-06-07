#!/usr/bin/python

from Tkinter import *
from cronmanager import *

class MainWindow:
  def __init__(self):
    self.cm = CronManager()
    self.lbConfigs = None

    self.root = Tk()
    self.root.title("YABM - Yet Another Backup Manager")
    
    frmTop = Frame(self.root)
    frmTop.grid(row=0, column=0, padx=2, pady=2, sticky=N+S+E+W)
    frmBottom = Frame(self.root)
    frmBottom.grid(row=1, column=0, padx=2, pady=2, sticky=E)

    lblSelect = Label(frmTop, text="Please select a configuration to load:")
    lblSelect.grid(row=0, column=0, sticky=W)

    sbConfigs = Scrollbar(frmTop, orient=VERTICAL)
    self.lbConfigs = Listbox(frmTop, yscrollcommand=sbConfigs.set, width=75)
    self.lbConfigs.config(font=("TkFixedFont"))
    self.lbConfigs.grid(row=1, column=0, sticky=N+S+E+W)
    sbConfigs.config(command=self.lbConfigs.yview)
    sbConfigs.grid(row=1, column=1, sticky=N+S+E+W)
 
    btnNew = Button(frmBottom, text="New")
    btnNew.grid(row=0, column=0)
    btnNew.bind("<Button-1>", self.new)
    btnLoad = Button(frmBottom, text="Load")
    btnLoad.grid(row=0, column=1)
    btnLoad.bind("<Button-1>", self.load)

    self.load_configs()

    self.root.mainloop()
  
  def load_configs(self):
    self.lbConfigs.delete(0, END)

    header  = self.format("Name", 15) + "|"
    header += self.format("Source", 20) + "|"
    header += self.format("Destination", 20) + "|"
    header += self.format("Type", 6) + "|"
    header += self.format("Active", 6)
    self.lbConfigs.insert(END, header)
    
    self.cm.load_all()
    for config in self.cm.configs:
      row  = self.format(str(config.name), 15) + "|"
      row += self.format(str(config.command.source), 20) + "|"
      row += self.format(str(config.command.destination), 20) + "|"
      row += self.format(str(config.type), 6) + "|"
      row += self.format(str(config.enabled), 6)
      self.lbConfigs.insert(END, row) 

  def format(self, str, size):
    if len(str) < size:
      return str + (" " * (size - len(str)))
    if len(str) == size:
      return str 
    return str[:size-3] + "..."

  def new(self, event):
    configWindow = ConfigWindow(self.root, None) 

  def load(self, event):
    items = self.lbConfigs.curselection()
    if len(items) == 0 or len(items) > 1 or int(items[0]) == 0:
      dialog = InfoDialog(self.root, "Please select a valid configuration")      
    else:
      configWindow = ConfigWindow(self.root, self.cm.configs[int(items[0])]) 

class ConfigWindow:
  def __init__(self, parent, config):

    title = ""
    if config == None:
      title = "New Configuration"
    else:
      title = config.name
    
    configWindow = Toplevel(master=parent)
    configWindow.title(title)


class InfoDialog:
  def __init__(self, parent, info):
    self.dialog = Toplevel(parent)

    frmTop = Frame(self.dialog)
    frmTop.grid(row=0, column=0, padx=2, pady=2, sticky=N+S+E+W)
    frmBottom = Frame(self.dialog)
    frmBottom.grid(row=1, column=0, padx=2, pady=2, sticky=N+S+E+W)

    lblInfo = Label(self.dialog, text=info)
    lblInfo.grid(row=0, column=0)
    btnOk = Button(self.dialog, text="OK", command=self.ok)
    btnOk.grid(row=1, column=0)

  def ok(self):
    self.dialog.destroy()

