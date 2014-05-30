from lib.crontab.crontab import CronTab
from config import Config
from config import ConfigSchedule

class CronManager:
  """Cron Manager"""
  def __init__(self):
    self.cron = CronTab(user=True)
    self.configs = []

  def load(self):
    # Load all Configs managed by YABM 
    for job in self.cron:
      metadata = job.comment

      # Only jobs which are in the Config format should be loaded
      if Config.is_config(metadata):
        conf = Config()
        conf.parse_metadata(metadata)
        conf.parse_command(job.command)
        conf.schedule = ConfigSchedule()
        conf.schedule.parse_schedule("* * * * * (fake schedule 2)")
 
  def save(self):
    pass

  def execute(self):
    pass

