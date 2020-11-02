from utils.string_enum import StringEnum


class LedType(StringEnum):
    SYSFS_RGB = 'sysfs_rgb'
    SYSFS_LINEAR = 'sysfs_linear'


class LedParameters:
    def __init__(self, args):
        self.led_name: str = args.led_name
        self.led_type: str = args.led_type

        if self.led_type not in LedType.list():
            raise Exception('`{}` is not a valid led type'.format(self.led_type))
