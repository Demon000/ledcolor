import time

import rivalcfg

from color import TimedColor

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
    if color.on_duration == 0:
      return

    self._set_color(color)
    time.sleep(color.on_duration)

  def _set_fading_color(self, color, into_color):
    self._set_timed_color(color)

    fade_duration = color.fade_duration
    if fade_duration == 0:
      return

    elapsed_time = 0
    while elapsed_time <= fade_duration:
      weight = elapsed_time / fade_duration

      mixed_color = TimedColor(self._update_time, color, into_color, weight)
      self._set_timed_color(mixed_color)

      elapsed_time += self._update_time

  def start(self):
    pass

  def stop(self):
    pass
