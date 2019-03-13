class LedController():
  def __init__(self, leds, config):
    self.__leds = leds
    self.__config = config

  def for_each_led(self, name, *args, **kwargs):
    for led in self.__leds:
      fn = getattr(led, name)
      return fn(*args, **kwargs)

  def controls_led(self, led):
    return led in self.__leds

  def add_led(self, led):
    self.__leds.append(led)

  def remove_led(self, led):
    try:
      self.__leds.remove(led)
    except:
      pass

  # def uses_config(self, config):
  #   return self.__config == config
