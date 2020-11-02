from leds.sysfs_led import SysfsLed


class SysfsLinearLed(SysfsLed):
    def _get_brightness(self, color):
        return color.alpha_brightness * self.__max_brightness // 255
