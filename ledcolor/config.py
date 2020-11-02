from enum import Enum
from itertools import cycle
import pickle

from helpers import args_to_colors, color_from_string


class StringEnum(str, Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class LedType(StringEnum):
    SYSFS_RGB = 'sysfs_rgb'
    SYSFS_LINEAR = 'sysfs_linear'


class ControllerType(StringEnum):
    COLORS = 'colors'
    SOUND = 'sound'
    NONE = 'none'


class Config:
    def __init__(self, args):
        self.led_name = args.led_name
        self.led_type = args.led_type
        self.controller_type = args.controller_type
        self.update_time = args.update_time

        if self.led_type not in LedType.list():
            raise Exception('`{}` is not a valid led type'.format(self.led_type))

        if self.controller_type not in ControllerType.list():
            raise Exception('`{}` is not a valid controller type'.format(self.led_type))

        self.input_name = None
        self.low_color = None
        self.high_color = None
        self.colors = None

        if args.controller_type == ControllerType.SOUND:
            self.input_name = args.input_name

            self.low_color = color_from_string(args.low_color_string)
            self.high_color = color_from_string(args.high_color_string)
        elif args.controller_type == ControllerType.COLORS:
            self.colors = cycle(args_to_colors(args.color))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.controller_type != other.controller_type:
            return False

        if self.update_time != other.update_time:
            return False

        if self.input_name != other.input_name:
            return False

        if self.low_color != other.low_color:
            return False

        if self.high_color != other.high_color:
            return False

        if self.colors != other.colors:
            return False

        return True

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialization):
        return pickle.loads(serialization)
