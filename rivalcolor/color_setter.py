import time

import rivalcfg

from color import MixedTimedColor

class ColorSetter():
  def __init__(self, wait_time, update_time):
    self._wait_time = wait_time
    self._update_time = update_time
    self._mouse = self._wait_for_mouse()

  def _wait_for_mouse(self):
    while True:
      try:
        mouse = rivalcfg.get_first_mouse()
      except OSError:
        mouse = None

      if mouse:
        return mouse

      time.sleep(self._wait_time)

  def _set_color(self, color):
    result = self._mouse.set_color(*color.rgb)
    if result < 0:
      self._mouse = self._wait_for_mouse()

  def _set_timed_color(self, color):
    self._set_color(color)
    time.sleep(color.on_duration)

  def _set_fading_color(self, color, into_color):
    self._set_timed_color(color)

    left_duration = color.fade_duration
    while left_duration >= 0:
      if color.fade_duration:
        color_weight = 1 - left_duration / color.fade_duration
      else:
        color_weight = 0

      mixed_color = MixedTimedColor(self._update_time, color, into_color, color_weight)

      left_duration -= self._update_time
      self._set_timed_color(mixed_color)

  def start(self):
    pass

  def stop(self):
    pass
