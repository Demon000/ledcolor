from openrazer.client import DeviceManager
from openrazer.client.devices.keyboard import RazerKeyboard

from leds.matrix_led import MatrixLed


class RazerKeyboardLed(MatrixLed):
    def __init__(self, led_name):
        super().__init__(led_name)

        self.device: RazerKeyboard = self.find_keyboard()

    def find_keyboard(self):
        device_manager = DeviceManager()
        device_manager.sync_effects = False

        for device in device_manager.devices:
            if device.name == self.name:
                return device

        raise ValueError('Keyboard `{}` does not exist'.format(self.name))

    def get_height(self):
        return self.device.fx.advanced.rows

    def get_width(self):
        return self.device.fx.advanced.cols

    def set_color_cell(self, x, y, color):
        self.device.fx.advanced.matrix[y, x] = color.rgb

    def draw_cells(self):
        self.device.fx.advanced.draw()

    def _set_color_matrix(self, color_matrix):
        for y in range(self.get_height()):
            for x in range(self.get_width()):
                self.set_color_cell(x, y, color_matrix[y][x])

        self.draw_cells()

    def _set_color(self, color):
        for y in range(self.get_height()):
            for x in range(self.get_width()):
                self.set_color_cell(x, y, color)

        self.draw_cells()
