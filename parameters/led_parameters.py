from utils.string_enum import StringEnum


class LedType(StringEnum):
    SYSFS_RGB = 'sysfs_rgb'
    SYSFS_LINEAR = 'sysfs_linear'
    RAZER_KEYBOARD = 'razer_keyboard'


class LedParameters:
    def __init__(self, args):
        self.led_name: str = args.led_name
        self.led_type: str = args.led_type
        self.led_matrix_flip: bool = args.led_matrix_flip

        if self.led_type not in LedType.list():
            raise Exception('`{}` is not a valid led type'.format(self.led_type))
