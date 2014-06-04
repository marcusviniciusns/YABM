#!/usr/bin/python

from cronmanager import CronManager
from config import Config 

metadata = "tool=YABM,name=My First Job,type=0,mode=0"
command = "rsync -a /home/dummy1/ /home/dummy2/"
schedule = "* * * * *"

def gen_config():
  config = Config()
  config.deserialize(metadata, command, schedule)
  return config 

def assert_config(config):
  assert config.serialize() == metadata
  assert config.command.serialize() == command
  assert config.schedule.serialize() == schedule  

def test_00():
  config = gen_config()
  assert_config(config)

def test_01():
  cm = CronManager()
  config = gen_config()
  original_count = len(cm.configs)

  cm.save(config) 
  cm.save(config)
  cm.save(config)
  assert len(cm.configs) == (original_count + 1)
  
  cm.remove(config)
  cm.remove(config)
  cm.remove(config)
  assert len(cm.configs) == original_count

  cm.remove_all()
  assert len(cm.configs) == 0

  cm.load_all()
  assert len(cm.configs) == 0

def test_02():
  cm = CronManager()
  config = gen_config()
 
  cm.remove_all() 
  cm.save(config)
  assert len(cm.configs) == 1

  cm.load_all()
  assert len(cm.configs) == 1

  config = cm.configs[0]
  assert_config(config)

  cm.remove(config)
  assert len(cm.configs) == 0

def test_03():
  cm = CronManager()
  config1 = gen_config()
  config2 = gen_config()

  cm.save(config1)
  cm.save(config2)
  print(cm)

  cm.remove(config1)
  cm.remove(config2)
  print(cm)

def test_04():
  cm = CronManager()
  config = gen_config()
  cm.save(config)
  assert config.is_valid()
  config.execute()


print "running test_00"
test_00()

print "running test_01"
test_01()

print "running test_02"
test_02()

print "running test_03"
test_03()

print "running test_04"
test_04()

print "done running tests"

