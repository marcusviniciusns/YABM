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
        config.load(job.command, metadata, job.is_enabled())
        config.schedule = ConfigSchedule(job.minute, job.hour, job.dom, job.month, job.dow)
        config.job = job 
        self.configs.append(config)
 
  def save(self, config):
    if config.job == None:
      config.job = self.cron.new()
    config.job.command = config.serialize_command()
    config.job.comment = config.serialize_metadata()
    config.job.enable(config.active)
    config.job.setall(config.schedule.serialize())
    self.cron.write() 

  def execute(self):
    pass

  def delete(self, config):
    if config.job == None:
      return

    self.cron.remove(config.job)
    config.job = None
    if config in self.configs:
      self.configs.remove(config)

