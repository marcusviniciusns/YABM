#!/usr/bin/python

from core import CronManager
import gui

cron_manager = CronManager()

cron_manager.load()
cron_manager.save() 
cron_manager.execute()

# Glue functions will go here

