import os
from abc import abstractmethod, ABCMeta

from leds.led import Led
from parameters.led_parameters import LedParameters


class SysfsLed(Led, metaclass=ABCMeta):
    def __init__(self, config: LedParameters):
        super().__init__(config)

        self.__path = '/sys/class/leds/{}/'.format(config.led_name)
        self.__check_existence()
        self.__read_max_brightness()
        self.__open_brightness()

    def __check_existence(self):
        if not os.path.isdir(self.__path):
            raise ValueError('Led `{}` does not exist'.format(self.name))

    def __read_max_brightness(self):
        max_brightness_path = self.__path + 'max_brightness'
        with open(max_brightness_path, 'r') as file:
            self._max_brightness = int(file.readline())

    def __open_brightness(self):
        brightness_path = self.__path + 'brightness'

        try:
            self.__brightness_file = open(brightness_path, 'w', buffering=1)
            self.__errored = False
        except FileNotFoundError:
            self.__errored = True

    def __write_brightness(self, data):
        if self.__errored:
            self.__open_brightness()

        try:
            self.__brightness_file.write(data)
        except OSError:
            self.__errored = True

    @abstractmethod
    def _get_brightness(self, color) -> int:
        pass

    def _set_color(self, color):
        brightness = self._get_brightness(color)
        data = str(brightness) + '\n'
        self.__write_brightness(data)
