from threading import Thread

class IteratorLedController():
  def __init__(self, leds, config):
    self.__leds = leds
    self.__iterator = config.iterator
    self.__update_time = config.update_time

    self.__thread = Thread(target=self.__animation_work, daemon=True)

  def __animation_work(self):
    color = next(self.__iterator)
    while not self.__stopped:
      next_color = next(self.__iterator)
      self.__leds.for_each_led('do_animated_color', color, next_color, self.__update_time)
      color = next_color

  def start(self):
    self.__thread.start()

  def stop(self):
    self.__stopped = True
