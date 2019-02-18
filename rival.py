#!/usr/bin/python

import time
from itertools import cycle
from optparse import OptionParser

import rivalcfg

from rivalcfg.helpers import is_color, color_string_to_rgb

DEFAULT_UPDATE_TIME = 0.05
DEFAULT_WAIT_TIME = 1

parser = OptionParser()
parser.add_option('-u', '--update-time', dest='update_time', default=DEFAULT_UPDATE_TIME, type=float)
parser.add_option('-w', '--wait-time', dest='wait_time', default=DEFAULT_WAIT_TIME, type=float)

(options, args) = parser.parse_args()

values = vars(options)

update_time = values['update_time']
wait_time = values['wait_time']

config = []
for arg in args:
  duration_string, color_string = arg.split(':')

  try:
    duration = int(duration_string)
  except ValueError:
    print('`{}` is not a valid duration.', )
    exit()

  if not is_color(color_string):
    print('`{}` is not a valid color.'.format(color_string))
    exit()

  color = color_string_to_rgb(color_string)
  config.append((duration, color))

if not config:
  print('No colors have been defined.')
  exit()

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

    time.sleep(wait_time)

mouse = wait_for_mouse()

color_cycle = cycle(config)
last_color = next(color_cycle)[1]
for (color_time, color) in color_cycle:
  current_color_time = 0
  while current_color_time < color_time:
    interpolated_color = interpolate(current_color_time / color_time, last_color, color)

    result = mouse.set_color(*interpolated_color)
    if result < 0:
      mouse = wait_for_mouse()

    mouse.save()

    current_color_time += update_time
    time.sleep(update_time)

  last_color = color
