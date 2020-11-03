from typing import Union, Tuple

from utils.tuple_helpers import t_add_w


class Color:
    def __init__(self, rgb: Union['Color', Tuple],
                 into_rgb: Union['Color', Tuple, None] = None,
                 weight: Union[int, None] = None):
        if isinstance(rgb, Color):
            rgb = rgb.rgb

        if isinstance(into_rgb, Color):
            into_rgb = into_rgb.rgb

        if into_rgb:
            self._rgb = t_add_w(rgb, into_rgb, weight)
        else:
            self._rgb = rgb

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if self._rgb != other._rgb:
            return False

        return True

    def __str__(self):
        return 'Color -> r: {}, g: {}, b: {}'.format(*self._rgb)

    @property
    def rgb_brightness(self) -> int:
        return (self._rgb[0] << 16) | (self._rgb[1] << 8) | (self._rgb[2])

    @property
    def alpha_brightness(self) -> int:
        return (self._rgb[0] + self._rgb[1] + self._rgb[2]) / 3

    @property
    def rgb(self) -> Tuple:
        return self._rgb
