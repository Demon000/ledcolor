from leds.led import Led
from leds.razer_keyboard_led import RazerKeyboardLed
from leds.sysfs_linear_led import SysfsLinearLed
from leds.sysfs_rgb_led import SysfsRgbLed
from parameters.led_parameters import LedParameters, LedType


class LedFactory:
    @staticmethod
    def build(config: LedParameters) -> Led:
        if config.led_type == LedType.SYSFS_RGB:
            return SysfsRgbLed(config)
        elif config.led_type == LedType.SYSFS_LINEAR:
            return SysfsLinearLed(config)
        elif config.led_type == LedType.RAZER_KEYBOARD:
            return RazerKeyboardLed(config)
        else:
            raise Exception('`{}` is not a valid led type'.format(config.led_type))
