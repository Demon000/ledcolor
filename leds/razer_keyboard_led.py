from leds.led import Led
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants

class RazerKeyboardLed(Led):
    def __init__(self, led_name):
        device_manager = DeviceManager()
        device_manager.sync_effects = False
