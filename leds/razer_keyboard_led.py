from openrazer.client import DeviceManager
from openrazer.client.devices.keyboard import RazerKeyboard

from leds.matrix_led import MatrixLed


class RazerKeyboardLed(MatrixLed):
    def __init__(self, config):
        super().__init__(config)

        self.device: RazerKeyboard = self.find_keyboard()

    def find_keyboard(self):
        device_manager = DeviceManager()
        device_manager.sync_effects = False

        for device in device_manager.devices:
            if device.name == self.name:
                return device

        raise ValueError('Keyboard `{}` does not exist'.format(self.name))

    def _get_height(self):
        return self.device.fx.advanced.rows

    def _get_width(self):
        return self.device.fx.advanced.cols

    def _set_color_matrix(self, color_matrix):
        for y in range(self._get_height()):
            for x in range(self._get_width()):
                self.device.fx.advanced.matrix[y, x] = color_matrix[y][x].rgb

        self.device.fx.advanced.draw()

    def _set_color(self, color):
        color_matrix = []
        for y in range(self.get_height()):
            row = []
            for x in range(self.get_width()):
                row.append(color)
            color_matrix.append(row)

        self.set_color_matrix(color_matrix)

    def draw_cells(self):
        self.device.fx.advanced.draw()
