from tuple_helpers import t_add_w

class Color():
  def __init__(self, rgb=None, into_rgb=None, weight=None):
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
