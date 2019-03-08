import time

import rivalcfg

from color import AnimatedColor

class Led():
  def __init__(self, config):
    self._update_time = config.update_time

  def _set_color(self, color):
    pass

  def _do_on_color(self, color):
    if color.on_duration == 0:
      return

    self._set_color(color)
    time.sleep(color.on_duration)

  def _do_fade_color(self, color, into_color):
    if color.fade_duration == 0:
      return

    elapsed_time = 0
    while elapsed_time <= color.fade_duration:
      weight = elapsed_time / color.fade_duration

      mixed_color = AnimatedColor(self._update_time, 0, color, into_color, weight)
      self._do_on_color(mixed_color)

      elapsed_time += self._update_time

  def _do_animated_color(self, color, into_color):
    self._do_on_color(color)
    self._do_fade_color(color, into_color)
