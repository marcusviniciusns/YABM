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

  def parse_schedule(self, schedule):
    print "Parsing schedule -", schedule 

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
  def is_yabm_job(metadata):
    # Jobs containing tool=YABM are managed by YABM
    return re.match("(^|.+,)(tool=YABM)($|,.+)", metadata)
  
  def parse_metadata(self, metadata):
    print "Parsing metadata - " + metadata

  def parse_command(self, command):
    print "Parsing command - " + command

class CronManager:
  """Interface to the functionalities of YABM"""
  def __init__(self):
    self.cron = CronTab(user=True)
    self.configs = []

  def load(self):
    # Load all Configs managed by YABM
    for job in self.cron:
      # Only the jobs managed by YABM should be loaded
      metadata = job.comment
      if Config.is_yabm_job(metadata):
        config = Config()
        config.parse_metadata(metadata)
        config.parse_command(job.command)
        config.schedule = ConfigSchedule()
        config.schedule.parse_schedule("* * * * * (fake schedule 2)")
 
  def save(self):
    pass

  def execute(self):
    pass

