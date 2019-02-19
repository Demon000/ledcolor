#!/usr/bin/python3

from itertools import cycle
from optparse import OptionParser

from helpers import text_to_morse, morse_to_config, args_to_config, args_to_colors
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

options, args = parser.parse_args()
wait_time = options.wait_time
update_time = options.update_time

if options.is_sound:
  colors = args_to_colors(args)
  color_setter = SoundColor(wait_time, update_time, colors)
else:
  if options.is_morse:
    text = ' '.join(args)
    morse = text_to_morse(text)
    config = morse_to_config(morse, update_time)
  else:
    config = args_to_config(args)

  iterator = cycle(config)
  color_setter = IteratorColor(iterator, wait_time, update_time)

color_setter.run()
