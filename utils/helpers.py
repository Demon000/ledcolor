from typing import Tuple, List

from utils.color import Color
from utils.animated_color import AnimatedColor


def duration_from_string(duration_string) -> float:
    try:
        duration = float(duration_string)
    except ValueError:
        raise Exception('`{}` is not a valid duration'.format(duration_string))

    return duration


def rgb_from_string(string) -> Tuple:
    # #f00 or #ff0000 -> f00 or ff0000
    if string.startswith("#"):
        string = string[1:]

    # f00 -> ff0000
    if len(string) == 3:
        string = string[0] * 2 + string[1] * 2 + string[2] * 2

    # ff0000 -> (255, 0, 0)
    if len(string) == 6:
        return tuple(int(string[i:i + 2], 16) for i in range(0, 6, 2))

    raise Exception('`{}` is not a valid color'.format(string))


def color_from_string(string) -> Color:
    rgb = rgb_from_string(string)
    return Color(rgb)


def args_to_colors(args) -> List[Color]:
    colors = []
    for arg in args:
        color_string, on_duration_string, fade_duration_string = arg.split(':')

        rgb = rgb_from_string(color_string)
        on_duration = duration_from_string(on_duration_string)
        fade_duration = duration_from_string(fade_duration_string)

        color = AnimatedColor(on_duration, fade_duration, rgb)
        colors.append(color)

    if not len(colors):
        raise Exception('No colors have been supplied')

    return colors
