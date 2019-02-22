from tuple_helpers import t_add_w

class Color():
  def __init__(self, rgb, into_rgb=None, weight=None):
    if type(rgb) is Color:
      rgb = rgb.rgb

    if type(into_rgb) is Color:
      into_rgb = into_rgb.rgb

    if into_rgb:
      self._rgb = t_add_w(rgb, into_rgb, weight)
    else:
      self._rgb = rgb

  @property
  def rgb(self):
      return self._rgb

class TimedColor(Color):
  def __init__(self, on, *args):
    super().__init__(*args)

    self._on = on

  @property
  def on_duration(self):
      return self._on

class FadingColor(TimedColor):
  def __init__(self, fade, *args):
    super().__init__(*args)

    self.__fade = fade

  @property
  def fade_duration(self):
    return self.__fade
