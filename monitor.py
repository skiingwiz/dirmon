#!/usr/bin/env python3
from pathlib import Path
from configparser import ConfigParser
from subprocess import Popen
import re
import shlex

def running(to_match):
  import os
  count = 0
  exp = re.compile(to_match)

  pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

  for pid in pids:
    try:
      cmdline = str(open(os.path.join('/proc', pid, 'cmdline'), 'rb').read())
      if exp.search(cmdline):
        count += 1
    except IOError: # proc has already terminated
      continue

  return count


config = ConfigParser()
config.read_file(open('monitor.cfg'))

for section in config.sections():
  c = config[section]
  p = Path(c['path'])
  endings = c['endings'].split(',')
  exclude_endings = c['excluded_endings'].split(',')

  to_match = c['process_match']
  max_p = int(c['max_processes'])
  num_run = running(to_match)
  if num_run >= max_p:
    print("[%s] Not running because there are already %s running" % (section, num_run)) 
    continue

  for e in endings:
    for f in p.rglob("*." + e):
      exclude = False
      for ee in exclude_endings:
        #excluded ending tacked on to full file name
        f1 = Path(str(f) + "." + ee)
        #excluded ending replacing suffix
        f2 = Path(re.sub(f.suffix + "$", "." + ee, str(f)))
        if f1.exists():
          #print("[%s] Skipping because %s exists" % (section, f1))
          exclude = True
        elif f2.exists():
          #print("[%s] Skipping because %s exists" % (section, f2))
          exclude = True

      if not exclude: 
          to_run = c['exec']
          # TODO more variable substitution?
          to_run = to_run.replace('!p', str(f))
          print("[%s] Running %s" % (section, to_run))
          args = shlex.split(to_run)
          Popen(args)
