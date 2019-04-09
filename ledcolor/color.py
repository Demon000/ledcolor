import random
import colorsys

from tuple_helpers import t_add_w

class Color():
  last_random_hue = 0

  def __init__(self, rgb, into_rgb=None, weight=None):
    if isinstance(rgb, Color):
      rgb = rgb.rgb

    if isinstance(into_rgb, Color):
      into_rgb = into_rgb.rgb

    if into_rgb:
      self._rgb = t_add_w(rgb, into_rgb, weight)
    else:
      self._rgb = rgb

  @property
  def rgb_brightness(self):
    return (self._rgb[0] << 16) | (self._rgb[1] << 8) | (self._rgb[2])

  @property
  def alpha_brightness(self):
    return self._rgb[2]

  @property
  def rgb(self):
      return self._rgb

  @staticmethod
  def random():
    while True:
      hue = random.random()
      if abs(hue - Color.last_random_hue) > 0.2:
        last_random_hue = hue
        break

    r, g, b = [int(256 * i) for i in colorsys.hsv_to_rgb(hue, 1, 0.5)]
    return Color((r, g, b))

class AnimatedColor(Color):
  def __init__(self, on_duration, fade_duration, *args):
    super().__init__(*args)

    self.__on_duration = on_duration
    self.__fade_duration = fade_duration

  @property
  def on_duration(self):
    return self.__on_duration

  @property
  def fade_duration(self):
    return self.__fade_duration
