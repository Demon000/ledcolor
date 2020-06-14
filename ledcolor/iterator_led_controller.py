from led_controller import LedController
from threading import Thread


class IteratorLedController(LedController):
    def __init__(self, leds, config):
        super().__init__(leds, config)

        self.__stopped = False
        self.__iterator = config.iterator
        self.__update_time = config.update_time

        self.__thread = Thread(target=self.__animation_work, daemon=True)

    def __animation_work(self):
        color = next(self.__iterator)
        while not self.__stopped:
            next_color = next(self.__iterator)
            for led in self._leds:
                led.do_animated_color(color, next_color, self.__update_time)
            color = next_color

    def start(self):
        self.__thread.start()

    def stop(self):
        self.__stopped = True
