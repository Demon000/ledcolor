import time

from color import AnimatedColor

class Led():
  def __init__(self, name):
    color = name.split(':')[1]
    if color == 'rgb':
      self._rgb = True
    else:
      self._rgb = False

    path = '/sys/class/leds/{}/'.format(name)
    brightness_path = path + 'brightness'
    self._brightness_file = open(brightness_path, 'w', buffering=1)

    max_brightness_path = path + 'max_brightness'
    with open(max_brightness_path, 'r') as file:
      self._max_brightness = int(file.readline())

  def set_color(self, color):
    if self._rgb:
      brightness = color.rgb_brightness
    else:
      brightness = color.alpha_brightness * self._max_brightness // 255

    data = str(brightness) + '\n'

    self._brightness_file.write(data)

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
