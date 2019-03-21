import os
import time

from color import AnimatedColor

class Led():
  def __init__(self, name):
    color = name.split(':')[1]
    if color == 'rgb':
      self._rgb = True
    else:
      self._rgb = False

    self.__name = name
    self.__path = '/sys/class/leds/{}/'.format(name)
    self.__check_existance()
    self.__read_max_brightness()
    self.__open_brightness()

  def __check_existance(self):
    if not os.path.isdir(self.__path):
      raise ValueError('Led `{}` does not exist.'.format(self.__name))

  def __read_max_brightness(self):
    max_brightness_path = self.__path + 'max_brightness'
    with open(max_brightness_path, 'r') as file:
      self.__max_brightness = int(file.readline())

  def __open_brightness(self):
    brightness_path = self.__path + 'brightness'

    try:
      self.__brightness_file = open(brightness_path, 'w', buffering=1)
      self.__errored = False
    except FileNotFoundError:
      self.__errored = True

  def __write_brightness(self, data):
    if self.__errored:
      self.__open_brightness()

    try:
      self.__brightness_file.write(data)
    except OSError:
      self.__errored = True

  def set_color(self, color):
    if self._rgb:
      brightness = color.rgb_brightness
    else:
      brightness = color.alpha_brightness * self.__max_brightness // 255

    data = str(brightness) + '\n'

    self.__write_brightness(data)

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
