import re

class ConfigType:
  """Enum-like class that represents the Configuration Type"""
  LOCAL = 0
  REMOTE = 1

class ConfigMode:
  """Enum-like class that represents the Configuration Mode"""
  SIMPLE = 0
  EXPERT = 1

class ConfigSchedule:
  """Holds the Configuration Schedule"""
  def __init__(self, minute, hour, dom, month, dow):
    self.minute = minute
    self.hour = hour 
    self.dom = dom 
    self.month = month 
    self.dow = dow 

  def serialize(self):
    return str(self)

  def __str__(self):
    ret  = str(self.minute) + " "
    ret += str(self.hour) + " "
    ret += str(self.dom) + " "
    ret += str(self.month) + " "
    ret += str(self.dow) 
    return ret

class Config:
  """Represents an YABM Configuration"""
  def __init__(self):
    # Metadata fields
    self.id = None
    self.name = None
    self.type = ConfigType.LOCAL
    self.mode = ConfigMode.SIMPLE
    self.active = None 
    
    # Command members
    self.command = "rsync"
    self.command_options = "-a" 
    self.source = None
    self.destination = None

    # Schedule fields
    self.schedule = None 

    # A reference to the cron job
    self.job = None

  def __str__(self):
    ret  = "id.............: " + str(self.id) + "\n"
    ret += "name...........: " + str(self.name) + "\n"
    ret += "type...........: " + str(self.type) + "\n"
    ret += "mode...........: " + str(self.mode) + "\n"
    ret += "active.........: " + str(self.active) + "\n"
    ret += "command........: " + str(self.command) + "\n"
    ret += "command_options: " + str(self.command_options) + "\n"
    ret += "source.........: " + str(self.source) + "\n"
    ret += "destination....: " + str(self.destination) + "\n"
    ret += "schedule.......: " + str(self.schedule) + "\n"
    ret += "job............: " + str(self.job)
    return ret

  @staticmethod
  def get_value(key, metadata):
    pattern = "(^|.*,[ ]*)" + key + "=([^,^ ]*)($|.*)"
    match = re.match(pattern, metadata)
    
    if match:
      return match.groups()[1]

    return None

  @staticmethod
  def is_config(metadata):
    # Jobs containing tool=YABM are managed by YABM
    value = Config.get_value("tool", metadata)
    if value == None:
      return False
    return value == "YABM"

  def load(self, command, metadata, enabled):
    self.parse_command(command)
    self.parse_metadata(metadata)
    self.active = enabled
    
  
  def parse_metadata(self, metadata):
    self.id = Config.get_value("id", metadata)
    self.name = Config.get_value("name", metadata)

    type = Config.get_value("type", metadata)
    if type == "local":
      self.type = ConfigType.LOCAL
    elif type == "remote":
      self.type = ConfigType.REMOTE

    mode = Config.get_value("mode", metadata)
    if mode == "simple":
      self.mode = ConfigMode.SIMPLE
    elif type == "expert":
      self.mode = ConfigMode.EXPERT

  def serialize_metadata(self):
    metadata  = "tool=YABM"
    metadata += ",id=" + str(self.id)
    metadata += ",name=" + str(self.name)
    
    metadata += ",type="
    if self.type == ConfigType.LOCAL:
      metadata += "local"
    elif self.type == ConfigType.REMOTE:
      metadata += "remote"

    metadata += ",mode="
    if self.mode == ConfigMode.SIMPLE:
      metadata += "simple"
    elif self.mode == ConfigMode.EXPERT:
      metadata += "expert"

    return metadata

  def parse_command(self, command):
    pattern = "rsync[ ]+(.*)[ ]+([^ ]+)[ ]+([^ ]+)$"    
    m = re.match(pattern, command)
    if not m == None:
      self.command_options = m.groups()[0]
      self.source = m.groups()[1]
      self.destination = m.groups()[2]

  def serialize_command(self):
    command  = "rsync "
    command += str(self.command_options) + " "
    command += str(self.source) + " "
    command += str(self.destination)
    return command

