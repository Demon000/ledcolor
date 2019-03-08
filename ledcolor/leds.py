class Leds():
  def __init__(self, leds):
    self.__leds = leds

  def for_each_led(name, *args, **kwargs):
    for led in self.__leds:
      fn = getattr(led, name):
      return fn(*args, **kwargs)
