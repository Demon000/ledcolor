from leds.sysfs_led import SysfsLed


class SysfsRgbLed(SysfsLed):
    def _get_brightness(self, color):
        return color.rgb_brightness
