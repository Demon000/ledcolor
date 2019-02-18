#!/usr/bin/python

import time
from itertools import cycle

import rivalcfg.rival_mouse as mouse
import rivalcfg.cli as cli

delta = 0.05

config = [
  (5, (0, 0, 255)),
  (5, (0, 255, 255)),
  (5, (0, 255, 0)),
  (5, (255, 255, 0)),
  (5, (255, 255, 255)),
  (5, (255, 0, 255)),
]

def interpolate(t, a, b):
  if t > 1: t = 1
  if t < 0: t = 0
  return tuple( int((1 - t) * x + t * y) for (x, y) in zip(a, b))

while True:
  profile = cli.get_plugged_mouse_profile()
  if profile is None:
    time.sleep(1)
  else:
    print "Found mouse: " + profile["name"]
    try:
      instance = mouse.RivalMouse(profile)
      prev = (0, 0, 0)
      for (total_time, color) in cycle(config):
         t = 0
         while t < total_time:
           c = interpolate(t / total_time, prev, color)
           instance.set_color(*c)
           t += delta
           time.sleep(delta)
         prev = color
    except Exception, e:
      print "Could not talk to mouse: " + str(e)

