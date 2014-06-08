#!/usr/bin/python

from Tkinter import *
from cronmanager import *
from tkFileDialog import askdirectory

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

    self.name = StringVar()

    self.minute = StringVar()
    self.hour = StringVar()
    self.dom = StringVar()
    self.month = StringVar()
    self.dow = StringVar()

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
    frmBot = Frame(configWindow)
    frmBot.grid(row=1, column=0, padx=2, pady=2, sticky=N+S+E+W)

    # Name widgets
    Label(frmTop, width=12, text="Name").grid(row=0, column=0, sticky=W)
    Entry(frmTop, width=40, textvariable=self.name).grid(row=0, column=1, columnspan=3, sticky=W)

    # Type widgets
    lblType = Label(frmTop, width=12, text="Type")
    lblType.grid(row=1, column=0, sticky=W)
    frmType = Frame(frmTop)
    frmType.grid(row=1, column=1, columnspan=3, sticky=W)
    self.type_ = IntVar()
    Radiobutton(frmType, text="Local", variable=self.type_, value=0).grid(row=0, column=0, sticky=W)
    Radiobutton(frmType, text="Remote (Network)", variable=self.type_, value=1).grid(row=0, column=1, sticky=W)

    # Source widgets
    lblSource = Label(frmTop, width=12, text="Source")
    lblSource.grid(row=2, column=0, sticky=W)
    self.entSource = Entry(frmTop, width=35)
    self.entSource.grid(row=2, column=1, columnspan=2, sticky=W)
    btnSourceLoad = Button(frmTop, text="...", command=self.select_source)
    btnSourceLoad.grid(row=2, column=3, sticky=W)

    # Destination widgets
    lblDestination = Label(frmTop, width=12, text="Destination")
    lblDestination.grid(row=3, column=0, sticky=W)
    self.entDestination = Entry(frmTop, width=35)
    self.entDestination.grid(row=3, column=1, columnspan=2, sticky=W)
    btnDestinationLoad = Button(frmTop, text="...", command=self.select_destination)
    btnDestinationLoad.grid(row=3, column=3, sticky=W)

    # User widgets
    lblUser = Label(frmTop, width=12, text="User")
    lblUser.grid(row=4, column=0, sticky=W)
    entUser = Entry(frmTop, width=12, state=DISABLED)
    entUser.grid(row=4, column=1, sticky=W)

    # Password widgets
    lblPass = Label(frmTop, width=12, text="Password")
    lblPass.grid(row=5, column=0, sticky=W)
    entPass = Entry(frmTop, width=12, state=DISABLED)
    entPass.grid(row=5, column=1, sticky=W)

    # Schedule Widgets
    Label(frmTop, width=12, text="Minute").grid(row=6, column=0, sticky=W)
    Entry(frmTop, width=6, textvariable=self.minute).grid(row=6, column=1, sticky=W)
    Label(frmTop, width=12, text="Hour").grid(row=7, column=0, sticky=W)
    Entry(frmTop, width=6, textvariable=self.hour).grid(row=7, column=1, sticky=W)
    Label(frmTop, width=12, text="Day of Month").grid(row=8, column=0, sticky=W)
    Entry(frmTop, width=6, textvariable=self.dom).grid(row=8, column=1, sticky=W)
    Label(frmTop, width=12, text="Month").grid(row=9, column=0, sticky=W)
    Entry(frmTop, width=6, textvariable=self.month).grid(row=9, column=1, sticky=W)
    Label(frmTop, width=12, text="Day of Week").grid(row=10, column=0, sticky=W)
    Entry(frmTop, width=6, textvariable=self.dow).grid(row=10, column=1, sticky=W)

    # Options Frame
    lblFrmOpt = LabelFrame(frmTop, text="Options")
    lblFrmOpt.grid(row=4, column=2, rowspan=4, columnspan=2, sticky=E)
    lblStatus = Label(lblFrmOpt, text="Status")
    lblStatus.grid(row=0, column=0, sticky=W)
    self.active = IntVar()
    chkStatus = Checkbutton(lblFrmOpt, text="Active", variable=self.active)
    chkStatus.grid(row=0, column=1, columnspan=2, sticky=W)
    lblMode = Label(lblFrmOpt, text="Mode")
    lblMode.grid(row=1, column=0, sticky=W)
    self.mode = IntVar()
    Radiobutton(lblFrmOpt, text="Simple", variable=self.mode, value=0).grid(row=1, column=1, sticky=W)
    Radiobutton(lblFrmOpt, text="Expert", variable=self.mode, value=1).grid(row=1, column=2, sticky=W)
    self.lblDesc = Label(lblFrmOpt, text="Command line options:")
    self.lblDesc.grid(row=2, column=0, columnspan=3, sticky=W)
    self.entCmdOptions = Entry(lblFrmOpt)
    self.entCmdOptions.grid(row=3, column=0, columnspan=3, sticky=W)

    # Buttons
    btnDelete = Button(frmBot, text="Delete", command=self.delete)
    btnDelete.grid(row=0, column=0, sticky=N+S+W)
    btnSave = Button(frmBot, text="Save", command=self.save)
    btnSave.grid(row=0, column=1, sticky=N+S+E)
    btnExecute = Button(frmBot, text="Execute", command=self.execute)
    btnExecute.grid(row=0, column=2, sticky=N+S+E)

  def select_source(self):
    self.select_directory(self.entSource)

  def select_destination(self):
    self.select_directory(self.entDestination)

  def select_directory(self, entry):
    path = askdirectory()
    if path == None or path == "":
      return
    entry.delete(0, END)
    entry.insert(0, path)

  def delete(self):
    print "Delete clicked"

  def save(self):
    print "Save clicked"

  def execute(self):
    print askdirectory()   


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

