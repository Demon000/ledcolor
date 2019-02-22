import time

import rivalcfg

from color import AnimatedColor

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

  def _set_animated_color(self, color, into_color):
    self._do_on_color(color)
    self._do_fade_color(color, into_color)

  def start(self):
    pass

  def stop(self):
    pass
