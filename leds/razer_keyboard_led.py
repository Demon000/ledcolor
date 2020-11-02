from openrazer.client import DeviceManager
from openrazer.client.devices.keyboard import RazerKeyboard

from leds.led import Led


class RazerKeyboardLed(Led):
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

    def _set_color(self, color):
        no_rows = self.device.fx.advanced.rows
        no_cols = self.device.fx.advanced.cols

        for r in range(no_rows):
            for c in range(no_cols):
                self.device.fx.advanced.matrix[r, c] = color.rgb

        self.device.fx.advanced.draw()
