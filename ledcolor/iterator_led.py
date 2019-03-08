from threading import Thread

from led import Led

class IteratorLed(Led):
  def __init__(self, config):
    super().__init__(config)

    self.__iterator = config.iterator
    self.__thread = Thread(target=self.__animation_work, daemon=True)

  def __animation_work(self):
    color = next(self.__iterator)
    while not self._stopped:
      next_color = next(self.__iterator)
      self._set_animated_color(color, next_color)
      color = next_color

  def start(self):
    self.__thread.start()
