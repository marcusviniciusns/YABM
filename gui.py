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
      row += self.format(ConfigType.name(config.type), 6) + "|"
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

    # Window    
    configWindow = Toplevel(master=parent)
    configWindow.title(title)

    # Frames
    frmTop = Frame(configWindow)
    frmTop.grid(row=0, column=0, padx=2, pady=2, sticky=N+S+E+W)
    frmMid = Frame(configWindow)
    frmMid.grid(row=1, column=0, padx=2, pady=2, sticky=N+S+E+W)
    frmBot = Frame(configWindow)
    frmBot.grid(row=2, column=0, padx=2, pady=2, sticky=N+S+E+W)

    # Name widgets
    lblName = Label(frmTop, width=12, text="Name")
    lblName.grid(row=0, column=0, sticky=W)
    entName = Entry(frmTop, width=40)
    entName.grid(row=0, column=1, sticky=W)

    # Type widgets
    lblType = Label(frmTop, width=12, text="Type")
    lblType.grid(row=1, column=0, sticky=W)

    # Source widgets
    lblSource = Label(frmTop, width=12, text="Source")
    lblSource.grid(row=2, column=0, sticky=W)
    entSource = Entry(frmTop, width=35)
    entSource.grid(row=2, column=1, sticky=W)

    # Destination widgets
    lblDestination = Label(frmTop, width=12, text="Destination")
    lblDestination.grid(row=3, column=0, sticky=W)
    entDestination = Entry(frmTop, width=35)
    entDestination.grid(row=3, column=1, sticky=W)

    # User widgets
    lblUser = Label(frmMid, width=12, text="User")
    lblUser.grid(row=4, column=0, sticky=W)
    entUser = Entry(frmMid)
    entUser.grid(row=4, column=1, sticky=W)

    # Password widgets
    lblPass = Label(frmMid, width=12, text="Password")
    lblPass.grid(row=5, column=0, sticky=W)
    entPass = Entry(frmMid)
    entPass.grid(row=5, column=1, sticky=W)

    lblFrmOpt = LabelFrame(frmMid, text="Options")
    lblFrmOpt.grid(row=4, column=2, sticky=W)
    lblStatus = Label(lblFrmOpt, text="Status")
    lblStatus.grid(row=0, column=0, sticky=W)

    # Buttons
    btnDelete = Button(frmBot, text="Delete", command=self.delete)
    btnDelete.grid(row=0, column=0, sticky=N+S+W)
    btnSave = Button(frmBot, text="Save", command=self.save)
    btnSave.grid(row=0, column=1, sticky=N+S+E)
    btnExecute = Button(frmBot, text="Execute", command=self.execute)
    btnExecute.grid(row=0, column=2, sticky=N+S+E)

  def delete(self):
    print "Delete clicked"

  def save(self):
    print "Save clicked"

  def execute(self):
    print "Execute clicked"   


class InfoDialog:
  def __init__(self, parent, info):
    self.dialog = Toplevel(parent)

    frmTop = Frame(self.dialog)
    frmTop.grid(row=0, column=0, padx=5, pady=10, sticky=N+S+E+W)
    frmBottom = Frame(self.dialog)
    frmBottom.grid(row=1, column=0, padx=5, pady=10, sticky=N+S)

    lblInfo = Label(frmTop, text=info)
    lblInfo.grid(row=0, column=0)
    btnOk = Button(frmBottom, text="OK", command=self.ok)
    btnOk.grid(row=0, column=0)

  def ok(self):
    self.dialog.destroy()

