import time

from color_setter import ColorSetter

from tuple_helpers import t_add_w

class IteratorColor(ColorSetter):
  def __init__(self, iterator, wait_time, update_time):
    super().__init__(wait_time)

    self.__update_time = update_time
    self.__prev_color = next(iterator)[1]
    self.__iterator = iterator

  def __get_mixed_color(self, prev_color, color, color_weight):
    return t_add_w(prev_color, color, color_weight)

  def __shift_color(self, color_time, color):
    current_color_time = 0
    while current_color_time < color_time:
      color_weight = current_color_time / color_time
      mixed_color = self.__get_mixed_color(self.__prev_color, color, color_weight)

      self._set_color(mixed_color)

      current_color_time += self.__update_time
      time.sleep(self.__update_time)

    self.__prev_color = color

  def start(self):
    for color_time, color in self.__iterator:
      self.__shift_color(color_time, color)
