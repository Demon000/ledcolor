from itertools import cycle
from typing import Union, List

from utils.color import Color
from utils.helpers import color_from_string, args_to_animated_colors
from utils.string_enum import StringEnum


class ControllerType(StringEnum):
    COLORS = 'colors'
    RANGE_SOUND = 'range_sound'
    MATRIX_SOUND = 'matrix_sound'
    NONE = 'none'


class ControllerParameters:
    def __init__(self, args):
        self.controller_type: str = args.controller_type

        if self.controller_type not in ControllerType.list():
            raise Exception('`{}` is not a valid controller type'.format(self.controller_type))

        self.update_time: float = args.update_time

        self.input_name: Union[str, None] = None
        self.low_color: Union[Color, None] = None
        self.high_color: Union[Color, None] = None
        self.volume_color: Union[Color, None] = None
        self.colors: Union[List[Color], None] = None

        if args.controller_type == ControllerType.RANGE_SOUND:
            self.input_name = args.input_name
            self.low_color = color_from_string(args.low_color_string)
            self.high_color = color_from_string(args.high_color_string)
        elif args.controller_type == ControllerType.MATRIX_SOUND:
            self.input_name = args.input_name
            self.low_color = color_from_string(args.low_color_string)
            self.high_color = color_from_string(args.high_color_string)
            self.volume_color = color_from_string(args.volume_color_string)
        elif args.controller_type == ControllerType.COLORS:
            self.colors = args_to_animated_colors(args.color)

    def __eq__(self, other: 'ControllerParameters') -> bool:
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
