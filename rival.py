#!/usr/bin/python

import time
from itertools import cycle

import rivalcfg

UPDATE_TIME = 0.05
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

last_color = (0, 0, 0)
for (color_time, color) in cycle(config):
  current_color_time = 0
  while current_color_time < color_time:
    interpolated_color = interpolate(current_color_time / color_time, last_color, color)

    try:
      mouse.set_color(*interpolated_color)
    except Exception as e:
      print("Could not talk to mouse: {}".format(e))

    current_color_time += UPDATE_TIME
    time.sleep(UPDATE_TIME)

  last_color = color
