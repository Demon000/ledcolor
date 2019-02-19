import time

import rivalcfg

from tuple_helpers import t_add_w

class ColorShift():
  def __init__(self, iterator, update_time, wait_time):
    self.__iterator = iterator
    self.__update_time = update_time
    self.__wait_time = wait_time
    self.__mouse = self.__wait_for_mouse()

  def __wait_for_mouse(self):
    while True:
      mouse = rivalcfg.get_first_mouse()
      if mouse:
        return mouse

      time.sleep(self.__wait_time)

  def __set_color(self, color):
    result = self.__mouse.set_color(*color)
    if result < 0:
      self.__mouse = self.__wait_for_mouse()

    self.__mouse.save()

  def __get_mixed_color(self, color, color_weight):
    return t_add_w(self.__prev_color, color, color_weight)

  def __play_color(self, color_time, color):
    current_color_time = 0
    while current_color_time < color_time:
      color_weight = current_color_time / color_time
      mixed_color = self.__get_mixed_color(color, color_weight)

      self.__set_color(mixed_color)

      current_color_time += self.__update_time
      time.sleep(self.__update_time)

    self.__prev_color = color

  def run(self):
    _, self.__prev_color = next(self.__iterator)
    for color_time, color in self.__iterator:
      self.__play_color(color_time, color)
