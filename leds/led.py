from abc import ABC, abstractmethod

from parameters.led_parameters import LedParameters


class Led(ABC):
    def __init__(self, config: LedParameters):
        self.name = config.led_name

        self.__last_color = None

    @abstractmethod
    def _set_color(self, color):
        pass

    def set_color(self, color):
        if self.__last_color == color:
            return

        self.__last_color = color
        self._set_color(color)
