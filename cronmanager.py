from config import Config
from config import ConfigSchedule
from lib.crontab.crontab import CronTab

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
      if Config.is_config(metadata):
        config = Config()
        config.parse_metadata(metadata)
        config.parse_command(job.command)
        config.schedule = ConfigSchedule()
        config.schedule.parse_schedule("* * * * * (fake schedule 2)")
 
  def save(self):
    pass

  def execute(self):
    pass

