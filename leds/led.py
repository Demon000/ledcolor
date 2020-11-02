from abc import ABC, abstractmethod


class Led(ABC):
    def __init__(self, led_name):
        self.name = led_name

        self.__last_color = None

    @abstractmethod
    def _set_color(self, color):
        pass

    def set_color(self, color):
        if self.__last_color == color:
            return

        self.__last_color = color
        self._set_color(color)
