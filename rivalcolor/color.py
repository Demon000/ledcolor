from tuple_helpers import t_add_w

class Color():
  def __init__(self, r, g, b):
    self._rgb = (r, g, b)

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

class MixedColor(Color):
  def __init__(self, color, into_color, weight):
    r, g, b = t_add_w(color.rgb, into_color.rgb, weight)

    super().__init__(r, g, b)

class MixedTimedColor(TimedColor):
  def __init__(self, on, color, into_color, weight):
    r, g, b = t_add_w(color.rgb, into_color.rgb, weight)

    super().__init__(on, r, g, b)

class FadingColor(TimedColor):
  def __init__(self, fade, *args):
    super().__init__(*args)

    self.__fade = fade

  @property
  def fade_duration(self):
    return self.__fade
