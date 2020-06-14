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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.update_time != other.update_time:
            return False

        if self.is_sound != other.is_sound:
            return False
        elif self.is_sound:
            if self.input_name != other.input_name:
                return False

            if self.low_color != other.low_color:
                return False

            if self.high_color != other.high_color:
                return False

        if self.is_iterator != other.is_iterator:
            return False
        elif self.is_iterator:
            if self.iterator != other.iterator:
                return False

        return True

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialization):
        return pickle.loads(serialization)
