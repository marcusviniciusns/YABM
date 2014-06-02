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
    self.configs = []

    for job in self.cron:
      metadata = job.comment

      # Only jobs which are in the Config format should be loaded
      if Config.is_config(metadata):
        config = Config()
        config.parse_metadata(metadata)
        config.parse_command(job.command)
        config.schedule = ConfigSchedule()
        config.schedule.parse_schedule("* * * * * (fake schedule 2)")
        config.job = job 
        self.configs.append(config)
 
  def save(self, config):
    pass

  def execute(self):
    pass

  def delete(self, config):
    if config.job == None:
      return

    self.cron.remove(config.job)
    config.job = None
    if config in self.configs:
      self.configs.remove(config)

