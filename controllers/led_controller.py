from typing import List

from leds.led import Led
from parameters.controller_parameters import ControllerParameters


class LedController:
    def __init__(self, config):
        self._leds: List[Led] = []
        self._config: ControllerParameters = config

    def is_compatible_config(self, config: ControllerParameters) -> bool:
        return self._config == config

    def controls_led(self, led: Led) -> bool:
        return led in self._leds

    def add_led(self, led: Led):
        if not self.has_leds():
            self.start()

        self._leds.append(led)

    def remove_led(self, led: Led):
        try:
            self._leds.remove(led)
        except ValueError:
            pass

        if not self.has_leds():
            self.stop()

    def has_leds(self) -> bool:
        return len(self._leds) != 0

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
