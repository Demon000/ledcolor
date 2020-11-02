from leds.sysfs_linear_led import SysfsLinearLed
from leds.sysfs_rgb_led import SysfsRgbLed
from parameters.led_parameters import LedParameters, LedType


class LedFactory:
    @staticmethod
    def build(config: LedParameters):
        if config.led_type == LedType.SYSFS_RGB:
            return SysfsRgbLed(config.led_name)
        elif config.led_type == LedType.SYSFS_LINEAR:
            return SysfsLinearLed(config.led_name)
        else:
            raise Exception('`{}` is not a valid led type'.format(config.led_type))
