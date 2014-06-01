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
  def __init__(self):
    self.minute = None
    self.hour = None
    self.dom = None
    self.month = None
    self.dow = None

  def parse_schedule(self, schedule):
    pass

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

  @staticmethod
  def get_value(key, metadata):
    pattern = "(^|.*,[ ]*)" + key + "=([^,^ ]*)($|.*)"
    match = re.match(pattern, metadata)

    if match:
      return match.groups(1)

    return None

  @staticmethod
  def is_config(metadata):
    # Jobs containing tool=YABM are managed by YABM
    value = Config.get_value("tool", metadata)
    if value == None:
      return False
    return value == "YABM"
  
  def parse_metadata(self, metadata):
    self.id = Config.get_value("id", metadata)
    self.name = Config.get_value("name", metadata)

    type = Config.get_value("type", metadata)
    if type == "local":
      self.type = ConfigType.LOCAL
    elif type == "remote":
      self.type = ConfigType.REMOTE

    mode = Config.get_value("mode")
    if mode == "simple":
      self.type = ConfigMode.SIMPLE
    elif type == "expert":
      self.type = ConfigMode.EXPERT

  def parse_command(self, command):
    pattern = "rsync[ ]+(.*)[ ]+([^ ]+)[ ]+([^ ]+)$"    
    m = re.match(pattern, command)
    if not m == None:
      self.command_options = m.groups(0)
      self.source = m.groups(1)
      self.destination = m.groups(2)
