#!/usr/bin/python3

from itertools import cycle
from optparse import OptionParser

from helpers import text_to_morse, morse_to_config, args_to_config
from sound_iterator import SoundIterator
from color_shift import ColorShift

DEFAULT_UPDATE_TIME = 0.05
DEFAULT_WAIT_TIME = 1

description = 'Colors: a list of colors to cycle through, ' + \
    'for example: 1:#ff0000 0.5:ff0000 2:#f00 0.5:f00 3:red'
usage = '%prog [options] [colors]'
parser = OptionParser(usage=usage, description=description)
parser.add_option('-u', '--update-time', dest='update_time', default=DEFAULT_UPDATE_TIME, type=float)
parser.add_option('-w', '--wait-time', dest='wait_time', default=DEFAULT_WAIT_TIME, type=float)
parser.add_option('-m', '--morse', action="store_true", dest='is_morse')
parser.add_option('-s', '--sound', action="store_true", dest='is_sound')

options, args = parser.parse_args()

values = vars(options)

update_time = values['update_time']
wait_time = values['wait_time']
is_morse = values['is_morse']
is_sound = values['is_sound']

if is_morse:
  text = ' '.join(args)
  morse = text_to_morse(text)
  config = morse_to_config(morse, update_time)
  iterator = cycle(config)
elif is_sound:
  iterator = SoundIterator()
else:
  config = args_to_config(args)
  iterator = cycle(config)

color_shift = ColorShift(iterator, update_time, wait_time)
color_shift.run()
