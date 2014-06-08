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
    configWindow = ConfigWindow(self.root, self, self.cm, Config()) 

  def load(self, event):
    items = self.lbConfigs.curselection()
    if len(items) == 0 or len(items) > 1 or int(items[0]) == 0:
      dialog = InfoDialog(self.root, "Please select a valid configuration")      
    else:
      configWindow = ConfigWindow(self.root, self, self.cm, self.cm.configs[int(items[0])-1]) 

class ConfigWindow:
  def __init__(self, parent, mainWindow, cm, config):
    self.parent = parent
    self.mainWindow = mainWindow
    self.cm = cm
    self.config = config

    self.name = StringVar()
    self.type = IntVar()
    self.source = StringVar()
    self.destination = StringVar()
    self.user = StringVar()
    self.password = StringVar()
    self.minute = StringVar()
    self.hour = StringVar()
    self.dom = StringVar()
    self.month = StringVar()
    self.dow = StringVar()
    self.active = IntVar()
    self.mode = IntVar()
    self.cmd_options = StringVar()

    self.window = None
    self.create_widgets(parent)
    self.load(config)

  def load(self, config):
    self.window.title(config.name)
    self.name.set(config.name)

    if config.type == ConfigType.LOCAL:
      self.local_selected()
    else:
      self.remote_selected()
    self.type.set(config.type)

    self.source.set(config.command.source)
    self.destination.set(config.command.destination)
    #self.user =
    #self.password
    self.minute.set(config.schedule.minute)
    self.hour.set(config.schedule.hour)
    self.dom.set(config.schedule.dom)
    self.month.set(config.schedule.month)
    self.dow.set(config.schedule.dow)
    if config.enabled:
      self.active.set(1)
    else:
      self.active.set(0)

    if config.mode == ConfigMode.SIMPLE:
      self.simple_selected()
    else:
      self.expert_selected()
    self.mode.set(config.mode)

    self.cmd_options.set(config.command.options)

  def select_source(self):
    path = askdirectory()
    if path == None or path == "":
      return
    self.source.set(path)

  def select_destination(self):
    path = askdirectory()
    if path == None or path == "":
      return
    self.destination.set(path)

  def local_selected(self):
    self.entUser.config(state=DISABLED)
    self.entPass.config(state=DISABLED)

  def remote_selected(self):
    self.entUser.config(state=NORMAL)
    self.entPass.config(state=NORMAL)

  def simple_selected(self):
    self.cmd_options.set("-a")
    self.entCmdOptions.config(state=DISABLED)

  def expert_selected(self):
    self.entCmdOptions.config(state=NORMAL)

  def delete(self):
    self.cm.remove(self.config)
    self.mainWindow.load_configs()
    InfoDialog(self.window, "Configuration deleted")

  def save(self):
    self.serialize()
    self.cm.save(self.config)
    self.mainWindow.load_configs()
    InfoDialog(self.window, "Configuration saved")


  def serialize(self): 
    self.config.name = self.name.get()
    self.config.type = self.type.get()
    self.config.command.source = self.source.get()
    self.config.command.destination = self.destination.get()
    #self.user = StringVar()
    #self.password = StringVar()
    self.config.schedule.minute = self.minute.get()
    self.config.schedule.hour = self.hour.get()
    self.config.schedule.dom = self.dom.get()
    self.config.schedule.month = self.month.get()
    self.config.schedule.dow = self.dow.get()
    if self.active.get() == 1:
      self.config.enabled = True
    else:
      self.config.enabled = False

    print self.config.enabled 
    self.config.mode = self.mode.get()
    self.config.command.options = self.cmd_options.get()

  def save_and_execute(self):
    self.serialize()
    self.cm.save(self.config)
    self.config.execute()
    InfoDialog(self.window, "Execution finished")

  def create_widgets(self, parent):
    # Window    
    self.window = Toplevel(master=parent)

    # Frames
    frmTop = Frame(self.window)
    frmTop.grid(row=0, column=0, padx=2, pady=2, sticky=N+S+E+W)
    frmBot = Frame(self.window)
    frmBot.grid(row=1, column=0, padx=2, pady=2, sticky=E)

    # Name widgets
    Label(frmTop, width=12, text="Name").grid(row=0, column=0, sticky=W)
    self.entName = Entry(frmTop, width=40, textvariable=self.name)
    self.entName.grid(row=0, column=1, columnspan=3, sticky=W)

    # Type widgets
    Label(frmTop, width=12, text="Type").grid(row=1, column=0, sticky=W)
    frmType = Frame(frmTop)
    frmType.grid(row=1, column=1, columnspan=3, sticky=W)
    Radiobutton(frmType, text="Local", variable=self.type, value=0, command=self.local_selected).grid(row=0, column=0, sticky=W)
    Radiobutton(frmType, text="Remote", variable=self.type, value=1, command=self.remote_selected).grid(row=0, column=1, sticky=W)

    # Source/Destination widgets
    Label(frmTop, width=12, text="Source").grid(row=2, column=0, sticky=W)
    Entry(frmTop, textvariable=self.source, width=35).grid(row=2, column=1, columnspan=2, sticky=W)
    Button(frmTop, text="...", command=self.select_source).grid(row=2, column=3, sticky=W)
    Label(frmTop, width=12, text="Destination").grid(row=3, column=0, sticky=W)
    Entry(frmTop, textvariable=self.destination, width=35).grid(row=3, column=1, columnspan=2, sticky=W)
    Button(frmTop, text="...", command=self.select_destination).grid(row=3, column=3, sticky=W)
    
    # User/Password widgets
    Label(frmTop, width=12, text="User").grid(row=4, column=0, sticky=W)
    self.entUser = Entry(frmTop, textvariable=self.user, width=40)
    self.entUser.grid(row=4, column=1, columnspan=3, sticky=W)
    Label(frmTop, width=12, text="Password").grid(row=5, column=0, sticky=W)
    self.entPass = Entry(frmTop, textvariable=self.password, width=40)
    self.entPass.grid(row=5, column=1, columnspan=3, sticky=W)

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
    lblFrmOpt = LabelFrame(frmTop, text="Options", padx=5, pady=5)
    lblFrmOpt.grid(row=6, column=2, rowspan=4, columnspan=2, sticky=E)

    Label(lblFrmOpt, text="Status").grid(row=0, column=0, sticky=W)
    Checkbutton(lblFrmOpt, text="Active", variable=self.active).grid(row=0, column=1, columnspan=2, sticky=W)

    Label(lblFrmOpt, text="Mode").grid(row=1, column=0, sticky=W)
    Radiobutton(lblFrmOpt, text="Simple", variable=self.mode, command=self.simple_selected, value=0).grid(row=1, column=1, sticky=W)
    Radiobutton(lblFrmOpt, text="Expert", variable=self.mode, command=self.expert_selected, value=1).grid(row=1, column=2, sticky=W)

    Label(lblFrmOpt, text="Command line options:").grid(row=2, column=0, columnspan=3, sticky=W)
    self.entCmdOptions = Entry(lblFrmOpt, textvariable=self.cmd_options, width=30)    
    self.entCmdOptions.grid(row=3, column=0, columnspan=3, sticky=W)

    # Buttons
    Button(self.window, text="Delete", command=self.delete).grid(row=1, column=0, sticky=W)
    Button(frmBot, text="Save", command=self.save).grid(row=0, column=1, sticky=E)
    Button(frmBot, text="Save and Execute", command=self.save_and_execute).grid(row=0, column=2, sticky=E)
    
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

