class LedController:
    def __init__(self, leds, config):
        self._leds = leds
        self.__config = config

    def is_compatible_config(self, config):
        return self.__config == config

    def controls_led(self, led):
        return led in self._leds

    def add_led(self, led):
        self._leds.append(led)

    def remove_led(self, led):
        try:
            self._leds.remove(led)
        except ValueError:
            pass

    def has_leds(self):
        return len(self._leds)

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
