from color_setter import ColorSetter

class IteratorColor(ColorSetter):
  def __init__(self, iterator, wait_time, update_time):
    super().__init__(wait_time, update_time)

    self.__iterator = iterator

  def start(self):
    color = next(self.__iterator)
    while True:
      next_color = next(self.__iterator)
      self._set_animated_color(color, next_color)
      color = next_color
