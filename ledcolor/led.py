import os
import time

from color import AnimatedColor
from config import LedType


class Led:
    def __init__(self, led_name, led_type):
        self.__last_color = None
        self.__name = led_name
        self.__type = led_type

        if led_type == LedType.SYSFS_RGB or \
                led_type == LedType.SYSFS_LINEAR:
            self.__path = '/sys/class/leds/{}/'.format(led_name)

        self.__check_existence()
        self.__read_max_brightness()
        self.__open_brightness()

    def __check_existence(self):
        if not os.path.isdir(self.__path):
            raise ValueError('Led `{}` does not exist.'.format(self.__name))

    def __read_max_brightness(self):
        max_brightness_path = self.__path + 'max_brightness'
        with open(max_brightness_path, 'r') as file:
            self.__max_brightness = int(file.readline())

    def __open_brightness(self):
        brightness_path = self.__path + 'brightness'

        try:
            self.__brightness_file = open(brightness_path, 'w', buffering=1)
            self.__errored = False
        except FileNotFoundError:
            self.__errored = True

    def __write_brightness(self, data):
        if self.__errored:
            self.__open_brightness()

        try:
            self.__brightness_file.write(data)
        except OSError:
            self.__errored = True

    def set_color(self, color):
        if self.__last_color is not None and self.__last_color == color:
            return

        self.__last_color = color
        if self.__type == LedType.SYSFS_RGB:
            brightness = color.rgb_brightness
        elif self.__type == LedType.SYSFS_LINEAR:
            brightness = color.alpha_brightness * self.__max_brightness // 255
        else:
            raise Exception('`{}` is not a valid led type'.format(self.__type))

        data = str(brightness) + '\n'
        self.__write_brightness(data)

    def do_on_color(self, color):
        if color.on_duration == 0:
            return

        self.set_color(color)
        time.sleep(color.on_duration)

    def do_fade_color(self, color, into_color, update_time):
        if color.fade_duration == 0:
            return

        elapsed_time = 0
        while elapsed_time <= color.fade_duration:
            weight = elapsed_time / color.fade_duration

            mixed_color = AnimatedColor(update_time, 0, color, into_color, weight)
            self.do_on_color(mixed_color)

            elapsed_time += update_time

    def do_animated_color(self, color, into_color, update_time):
        self.do_on_color(color)
        self.do_fade_color(color, into_color, update_time)
