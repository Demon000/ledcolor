#!/usr/bin/python3

import signal

from itertools import cycle
from optparse import OptionParser

from helpers import text_to_morse, morse_to_config, args_to_config, color_from_string
from iterator_color import IteratorColor
from sound_color import SoundColor

description = 'Colors: a list of colors to cycle through, ' + \
    'for example: 1:#ff0000 0.5:ff0000 2:#f00 0.5:f00 3:red'
usage = '%prog [options] [colors]'
parser = OptionParser(usage=usage, description=description)
parser.add_option('-u', '--update-time', dest='update_time', default=0.05, type=float)
parser.add_option('-w', '--wait-time', dest='wait_time', default=1, type=float)
parser.add_option('-m', '--morse', action="store_true", dest='is_morse')
parser.add_option('-s', '--sound', action="store_true", dest='is_sound')
parser.add_option('-L', '--low', dest='low_color_string', default='#00ff00', type=str)
parser.add_option('-H', '--high', dest='high_color_string', default='#ff0000', type=str)
parser.add_option('-i', '--input', dest='input_index', type=int)

options, args = parser.parse_args()
wait_time = options.wait_time
update_time = options.update_time

if options.is_sound:
  low_color = color_from_string(options.low_color_string)
  high_color = color_from_string(options.high_color_string)
  color_setter = SoundColor(wait_time, update_time, low_color, high_color, options.input_index)
else:
  if options.is_morse:
    text = ' '.join(args)
    morse = text_to_morse(text)
    config = morse_to_config(morse, update_time)
  else:
    config = args_to_config(args)

  iterator = cycle(config)
  color_setter = IteratorColor(iterator, wait_time, update_time)

color_setter.start()

def stop(*args):
  color_setter.stop()

for type_ in (signal.SIGABRT, signal.SIGINT, signal.SIGTERM):
    signal.signal(type_, stop)

signal.pause()
