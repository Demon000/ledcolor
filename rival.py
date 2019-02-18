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

def t_mul(t, s):
  return tuple(x * s for x in t)

def t_add(a, b):
  return tuple(x + y for (x, y) in zip(a, b))

def t_floor(t):
  return tuple(int(x) for x in t)

def interpolate(w, a, b):
  if w > 1:
    w = 1

  if w < 0:
    w = 0

  return t_floor(t_add(t_mul(a, 1 - w), t_mul(b, w)))

def wait_for_mouse():
  while True:
    mouse = rivalcfg.get_first_mouse()
    if mouse:
      print("Found: {}".format(mouse))
      return mouse

    time.sleep(WAIT_TIME)

mouse = wait_for_mouse()

last_color = (0, 0, 0)
for (color_time, color) in cycle(config):
  current_color_time = 0
  while current_color_time < color_time:
    interpolated_color = interpolate(current_color_time / color_time, last_color, color)

    result = mouse.set_color(*interpolated_color)
    if result < 0:
      mouse = wait_for_mouse()

    current_color_time += UPDATE_TIME
    time.sleep(UPDATE_TIME)

  last_color = color
