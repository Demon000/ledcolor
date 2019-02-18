#!/usr/bin/python

import time
from itertools import cycle

import rivalcfg

UPDATE_DELTA = 0.05
WAIT_TIME = 1

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
  if mouse:
    break

  time.sleep(WAIT_TIME)

print("Found mouse: {}".format(mouse))

prev = (0, 0, 0)
for (total_time, color) in cycle(config):
  t = 0
  while t < total_time:
    c = interpolate(t / total_time, prev, color)
    try:
      mouse.set_color(*c)
    except Exception as e:
      print("Could not talk to mouse: {}".format(e))
    t += UPDATE_DELTA
    time.sleep(UPDATE_DELTA)
  prev = color
