from abc import ABC, abstractmethod
from typing import List, Union

from leds.led import Led
from parameters.controller_parameters import ControllerParameters


class LedController(ABC):
    def __init__(self, config):
        self._leds: List[Led] = []
        self._config: ControllerParameters = config

    def is_compatible_config(self, config: ControllerParameters) -> bool:
        return self._config == config

    def controls_led(self, *args, **kwargs) -> bool:
        return self.find_led(*args, **kwargs) is not None

    def add_led(self, led: Led):
        if not self.has_leds():
            self.start()

        self._leds.append(led)

    def find_led(self, name: str) -> Union[Led, None]:
        for searched_led in self._leds:
            if searched_led.name == name:
                return searched_led

        return None

    def remove_led(self, *args, **kwargs):
        led = self.find_led(*args, **kwargs)
        if not led:
            return

        try:
            self._leds.remove(led)
        except ValueError:
            pass

        if not self.has_leds():
            self.stop()

    def has_leds(self) -> bool:
        return len(self._leds) != 0

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
