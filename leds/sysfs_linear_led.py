from leds.sysfs_led import SysfsLed


class SysfsLinearLed(SysfsLed):
    def _get_brightness(self, color) -> int:
        return color.alpha_brightness * self._max_brightness // 255
