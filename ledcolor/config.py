from itertools import cycle
import pickle

from helpers import text_to_morse, morse_to_colors, args_to_colors, color_from_string

class Config():
  def __init__(self, options, args):
    self.wait_time = options.wait_time
    self.update_time = options.update_time

    self.is_sound = False
    self.is_iterator = False

    if options.is_sound:
      self.is_sound = True
      self.input_name = options.input_name

      self.low_color = color_from_string(options.low_color_string)
      self.high_color = color_from_string(options.high_color_string)
    elif options.is_morse:
      self.is_iterator = True

      text = ' '.join(args)
      morse = text_to_morse(text)
      colors = morse_to_colors(morse, options.update_time)
      self.iterator = cycle(colors)
    else:
      self.is_iterator = True

      colors = args_to_colors(args)
      self.iterator = cycle(colors)

  def serialize(self):
    return pickle.dumps(self)

  @staticmethod
  def deserialize(serialization):
    return pickle.loads(serialization)
