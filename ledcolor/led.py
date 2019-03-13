import time

from color import AnimatedColor

class Led():

  def __init__(self, name):
    path = '/sys/class/leds/{}/'.format(name)
    self._brightness_path = path + 'brightness'

  def set_color(self, color):
    with open(self._brightness_path, 'w') as file:
      file.write(str(color.rgb_brightness))

  def do_on_color(self, color):
    if color.on_duration == 0:
      return

    self.set_color(color)
    time.sleep(color.on_duration)

  def do_fade_color(self, color, into_color, update_time):
    if color.fade_duration == 0:
      return

    elapsed_time = 0
    while elapsed_time <= color.fade_duration:
      weight = elapsed_time / color.fade_duration

      mixed_color = AnimatedColor(update_time, 0, color, into_color, weight)
      self.do_on_color(mixed_color)

      elapsed_time += update_time

  def do_animated_color(self, color, into_color, update_time):
    self.do_on_color(color)
    self.do_fade_color(color, into_color, update_time)
