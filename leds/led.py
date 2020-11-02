import time
from abc import ABC, abstractmethod
from threading import Condition, Thread

from utils.animated_color import AnimatedColor


class Led(ABC):
    def __init__(self, led_name):
        self.name = led_name

        self.__last_color = None

    @abstractmethod
    def _set_color(self, color):
        pass

    def set_color(self, color):
        if self.__last_color == color:
            return

        self.__last_color = color
        self._set_color(color)

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
