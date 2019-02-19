import time

import rivalcfg

class ColorSetter():
  def __init__(self, wait_time):
    self._wait_time = wait_time
    self._mouse = self._wait_for_mouse()

  def _wait_for_mouse(self):
    while True:
      mouse = rivalcfg.get_first_mouse()
      if mouse:
        return mouse

      time.sleep(self._wait_time)

  def _set_color(self, color, save=False):
    result = self._mouse.set_color(*color)
    if result < 0:
      self._mouse = self._wait_for_mouse()

    if save:
      self._mouse.save()
