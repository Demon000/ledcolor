#!/usr/bin/python

import time
from itertools import cycle

import rivalcfg

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
  mouse = rivalcfg.get_first_mouse()
  if mouse is None:
    time.sleep(1)
  else:
    print("Found mouse: {}".format(mouse))
    try:
      prev = (0, 0, 0)
      for (total_time, color) in cycle(config):
        t = 0
        while t < total_time:
          c = interpolate(t / total_time, prev, color)
          mouse.set_color(*c)
          t += delta
          time.sleep(delta)
        prev = color
    except Exception as e:
      print("Could not talk to mouse: {}".format(e))
