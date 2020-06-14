class LedController:
    def __init__(self, config):
        self._leds = []
        self.__config = config

    def is_compatible_config(self, config):
        return self.__config == config

    def controls_led(self, led):
        return led in self._leds

    def add_led(self, led):
        if not self.has_leds():
            self.start()

        self._leds.append(led)

    def remove_led(self, led):
        try:
            self._leds.remove(led)
        except ValueError:
            pass

        if not self.has_leds():
            self.stop()

    def has_leds(self):
        return len(self._leds) != 0

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
