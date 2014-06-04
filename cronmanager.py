from lib.crontab.crontab import CronTab
from config import * 

class CronManager:
  """Cron Manager"""
  def __init__(self):
    self.cron = CronTab(user=True)
    self.configs = None
    self.load_all()

  def __str__(self):
    ret = ""
    for config in self.configs:
      ret += str(config) + "\n\n"
    return ret

  def load_all(self):
    self.configs = []
    for job in self.cron:
      metadata = job.comment

      # Only jobs which are in the Config format should be loaded
      if Config.is_config(metadata):
        config = Config()
        config.deserialize(metadata, job.command, str(job.slices))
        config.enabled = job.is_enabled()
        config.job = job 
        self.configs.append(config)
 
  def save(self, config):
    if config == None:
      return

    if not config.job == None:
      # ensures that the previous job is removed before we
      # create a new one
      self.cron.remove(config.job)

    config.job = self.cron.new(command = config.command.serialize())
    config.job.setall(config.schedule.serialize())
    config.job.comment = config.serialize()
    config.job.enable(config.enabled)
    if not config in self.configs:
      self.configs.append(config)

    self.cron.write()

  def remove(self, config):
    if config == None:
      return

    if not config.job == None:
      self.cron.remove(config.job)
      self.cron.write()
      config.job = None
   
    if config in self.configs: 
      self.configs.remove(config)

  def remove_all(self):
    self.load_all()
    for config in self.configs:
      self.remove(config)

