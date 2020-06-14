class LedController:
    def __init__(self, leds, config):
        self._leds = leds
        self.__config = config

    def controls_led(self, led):
        return led in self._leds

    def add_led(self, led):
        self._leds.append(led)

    def remove_led(self, led):
        try:
            self._leds.remove(led)
        except:
            pass

    def has_leds(self):
        return len(self._leds)
