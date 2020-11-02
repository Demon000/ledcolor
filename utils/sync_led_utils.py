import time

from utils.animated_color import AnimatedColor


class SyncLedUtils:
    @classmethod
    def do_on_color(cls, leds, color):
        if color.on_duration == 0:
            return

        for led in leds:
            led.set_color(color)
        time.sleep(color.on_duration)

    @classmethod
    def do_fade_color(cls, leds, color, into_color, update_time):
        if color.fade_duration == 0:
            return

        elapsed_time = 0
        while elapsed_time <= color.fade_duration:
            weight = elapsed_time / color.fade_duration

            mixed_color = AnimatedColor(update_time, 0, color, into_color, weight)
            cls.do_on_color(leds, mixed_color)

            elapsed_time += update_time

    @classmethod
    def do_animated_color(cls, leds, color, into_color, update_time):
        cls.do_on_color(leds, color)
        cls.do_fade_color(leds, color, into_color, update_time)
