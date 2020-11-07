from abc import abstractmethod, ABCMeta

from leds.led import Led
from parameters.led_parameters import LedParameters
from utils.helpers import flip_2d_list


class MatrixLed(Led, metaclass=ABCMeta):
    def __init__(self, config: LedParameters):
        super().__init__(config)

        self.__flipped = config.led_matrix_flip

    @abstractmethod
    def _get_width(self):
        pass

    @abstractmethod
    def _get_height(self):
        pass

    def get_width(self):
        if self.__flipped:
            return self._get_height()
        else:
            return self._get_width()

    def get_height(self):
        if self.__flipped:
            return self._get_width()
        else:
            return self._get_height()

    @abstractmethod
    def _set_color_matrix(self, color_matrix):
        pass

    def set_color_matrix(self, color_matrix):
        if len(color_matrix) != self.get_height():
            raise ValueError("Color matrix height doesn't match")

        if len(color_matrix[0]) != self.get_width():
            raise ValueError("Color matrix width doesn't match")

        if self.__flipped:
            color_matrix = flip_2d_list(color_matrix)

        self._set_color_matrix(color_matrix)
