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
  
  def parse_schedule(schedule):
    pass

class Config:
  """Represents an YABM Configuration"""
  def __init__(self):
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

  def parse_metadata(metadata):
    pass

class YABM:
  """Interface to the functionalities of YABM"""
  def __init__(self):
    self.cron = CronTab(user=True)
    self.configs = []
  def load(self):
    """Load all Configs managed by YABM"""
    for job in self.cron:
      """We just want to handle jobs managed by YABM. This
         can be told by the tool=YABM key-value pair"""
      if re.match("(^|.+,)(tool=YABM)($|,.+)", job.comment):
        #job.enabled(not job.is_enabled())
        print str(job) + " Enabled = " + str(job.is_enabled())
  def save(selft):
    pass

  def execute(self):
    pass

