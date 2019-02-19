import time

from color_setter import ColorSetter

from tuple_helpers import t_add_w

class IteratorColor(ColorSetter):
  def __init__(self, iterator, wait_time, update_time):
    super().__init__(wait_time)

    self.__update_time = update_time
    self.__iterator = iterator

  def __get_mixed_color(self, prev_color, color, color_weight):
    return t_add_w(prev_color, color, color_weight)

  def __play_color(self, color, duration):
    self._set_color(color)
    time.sleep(duration)

  def __fade_color(self, old_color, new_color, duration):
    left_duration = duration
    while left_duration >= 0:
      color_weight = left_duration / duration
      mixed_color = self.__get_mixed_color(new_color, old_color, color_weight)

      self._set_color(mixed_color)

      left_duration -= self.__update_time
      time.sleep(self.__update_time)


  def start(self):
    current_item = next(self.__iterator)
    while True:
      next_item = next(self.__iterator)

      self.__play_color(current_item[0], current_item[1])
      self.__fade_color(current_item[0], next_item[0], current_item[2])

      current_item = next_item
