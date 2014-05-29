from lib.crontab.crontab import CronTab
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
  def parse_schedule(self, chedule):
    pass

class Config:
  """Represents an YABM Configuration"""
  def __init__(self, metadata):
    self.id = None
    self.name = None
    self.type = ConfigType.LOCAL
    self.source = None
    self.destination = None
    self.schedule = None
    self.active = False
    self.mode = ConfigMode.SIMPLE
    self.command = "rsync"
    self.command_options = "-a" 
    
    self.parse_metadata(metadata)
  
  def parse_metadata(self, metadata):
    print "Parsing " + metadata

class YABM:
  """Interface to the functionalities of YABM"""
  def __init__(self):
    self.cron = CronTab(user=True)
    self.configs = []
  def load(self):
    # Load all Configs managed by YABM
    for job in self.cron:
      # Only the jobs managed by YABM should be loaded
      metadata = job.comment
      if re.match("(^|.+,)(tool=YABM)($|,.+)", metadata):
        config = Config(metadata)
        

        #job.enabled(not job.is_enabled())
        print str(job) + " Enabled = " + str(job.is_enabled())
  def save(selft):
    pass

  def execute(self):
    pass

