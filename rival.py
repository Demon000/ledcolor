#!/usr/bin/python

import time
from itertools import cycle
from optparse import OptionParser

import rivalcfg

from helpers import text_to_morse, morse_to_config, args_to_config

DEFAULT_UPDATE_TIME = 0.05
DEFAULT_WAIT_TIME = 1

description = 'Colors: a list of colors to cycle through, ' + \
    'for example: 1:#ff0000 0.5:ff0000 2:#f00 0.5:f00 3:red'
usage = '%prog [options] [colors]'
parser = OptionParser(usage=usage, description=description)
parser.add_option('-u', '--update-time', dest='update_time', default=DEFAULT_UPDATE_TIME, type=float)
parser.add_option('-w', '--wait-time', dest='wait_time', default=DEFAULT_WAIT_TIME, type=float)
parser.add_option('-t', '--text', dest='text', type=str)

(options, args) = parser.parse_args()

values = vars(options)

update_time = values['update_time']
wait_time = values['wait_time']
text = values['text']

if text:
  morse = text_to_morse(text)
  config = morse_to_config(morse, update_time)
else:
  config = args_to_config(args)

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
