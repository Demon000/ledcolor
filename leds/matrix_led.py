from abc import abstractmethod, ABCMeta

from leds.led import Led


class MatrixLed(Led, metaclass=ABCMeta):
    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def _set_color_matrix(self, color_matrix):
        pass

    @abstractmethod
    def set_color_cell(self, x, y, color):
        pass

    @abstractmethod
    def draw_cells(self):
        pass

    def set_color_matrix(self, color_matrix):
        if len(color_matrix) != self.get_height():
            raise ValueError("Color matrix height doesn't match")

        if len(color_matrix[0]) != self.get_width():
            raise ValueError("Color matrix width doesn't match")

        self._set_color_matrix(color_matrix)
