from itertools import cycle
import pickle

from helpers import args_to_colors, color_from_string


class Config:
    def __init__(self, options, args):
        self.update_time = options.update_time
        self.name = options.name

        self.is_sound = False
        self.is_iterator = False

        if options.is_sound:
            self.is_sound = True
            self.input_name = options.input_name

            self.low_color = color_from_string(options.low_color_string)
            self.high_color = color_from_string(options.high_color_string)
        elif options.is_colors:
            self.is_iterator = True

            colors = args_to_colors(args)
            self.iterator = cycle(colors)

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialization):
        return pickle.loads(serialization)
