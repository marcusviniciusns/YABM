#!/usr/bin/python

from cronmanager import CronManager
from config import Config, ConfigSchedule
from lib.crontab.crontab import CronTab 
import gui

cm = CronManager()
cm.load()

for config in cm.configs:
  print str(config)

def create_new1():
  c = Config()
  c.id = 1
  c.name = "Config"
  c.active = True
  c.source = "/home/marvin/yabm_test/source"
  c.destination = "/home/marvin/yabm_test/destination"
  c.schedule = ConfigSchedule("*","*","*","*","*")
  cm.save(c)

def create_new2():
  cron = CronTab(user=True)
  job = cron.new()
  job.command = "rsync"
  job.setall("* * * * *")
  job.enable = True
  cron.write()

create_new1()

#cron_manager.save() 
#cron_manager.execute()

# Glue functions will go here

