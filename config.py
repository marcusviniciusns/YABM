import os
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

  def __str__(self):
    return self.serialize() 

  def serialize(self):
    schedule  = str(self.minute) + " "
    schedule += str(self.hour) + " "
    schedule += str(self.dom) + " "
    schedule += str(self.month) + " "
    schedule += str(self.dow) 
    return schedule
 
  def deserialize(self, schedule):
    pattern = "^([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*)$"
    m = re.match(pattern, schedule)
    if not m == None:
      self.minute = m.groups()[0]
      self.hour = m.groups()[1]
      self.dom = m.groups()[2]
      self.month = m.groups()[3]
      self.dow = m.groups()[4]

class ConfigCommand:
  """Represents a rsync command"""
  def __init__(self):
    self.options = None
    self.source = None
    self.destination = None

  def __str__(self):
    return self.serialize()

  def serialize(self):
    command  = "rsync "
    command += str(self.options) + " "
    command += str(self.source) + " "
    command += str(self.destination)
    return command

  def deserialize(self, command):
    pattern = "rsync[ ]+(.*)[ ]+([^ ]+)[ ]+([^ ]+)$"    
    m = re.match(pattern, command)
    if not m == None:
      self.options = m.groups()[0]
      self.source = m.groups()[1]
      self.destination = m.groups()[2]

class Config:
  """Represents an YABM Configuration"""
  def __init__(self):
    # Metadata fields
    self.name = None
    self.type = None
    self.mode = None
    self.enabled = True
    
    # Command, schedule and a reference to the cron job
    self.command = ConfigCommand() 
    self.schedule = ConfigSchedule()
    self.job = None

  def __str__(self):
    ret  = "name......: " + str(self.name) + "\n"
    ret += "type......: " + str(self.type) + "\n"
    ret += "mode......: " + str(self.mode) + "\n"
    ret += "enabled...: " + str(self.enabled) + "\n"
    ret += "command...: " + self.command.serialize() + "\n"
    ret += "schedule..: " + self.schedule.serialize() + "\n"
    ret += "job.......: " + str(self.job)
    return ret

  def serialize(self):
    config  = "tool=YABM"
    config += ",name=" + str(self.name)
    config += ",type=" + str(self.type)
    config += ",mode=" + str(self.mode)
    return config

  def deserialize(self, metadata, command, schedule):
    self.name = Config.get_value("name", metadata)
    self.type = int(Config.get_value("type", metadata))
    self.mode = int(Config.get_value("mode", metadata))
    self.command.deserialize(command)
    self.schedule.deserialize(schedule)

  def is_valid(self):
    if self.job == None:
      return False
    return self.job.is_valid()

  def execute(self):
    if self.is_valid():
      os.system(self.job.command)

  @staticmethod
  def is_config(metadata):
    # Jobs containing tool=YABM are managed by YABM
    value = Config.get_value("tool", metadata)
    if value == None:
      return False
    return value == "YABM"

  @staticmethod
  def get_value(key, metadata):
    pattern = "(^|.*,[ ]*)" + key + "=([^,]*)($|.*)"
    match = re.match(pattern, metadata)
    if match:
      return match.groups()[1]
    return None

