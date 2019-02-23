from threading import Thread

from color_setter import ColorSetter

class IteratorColor(ColorSetter):
  def __init__(self, iterator, wait_time, update_time):
    super().__init__(wait_time, update_time)

    self.__iterator = iterator
    self.__stopped = False
    self.__thread = Thread(target=self.__animation_work, daemon=True)

  def __animation_work(self):
    color = next(self.__iterator)
    while not self.__stopped:
      next_color = next(self.__iterator)
      self._set_animated_color(color, next_color)
      color = next_color

  def start(self):
    self.__thread.start()

  def stop(self):
    self.__stopped = True
