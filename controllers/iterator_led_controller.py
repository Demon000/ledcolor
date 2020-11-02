from controllers.thread_led_controller import ThreadLedController


class IteratorLedController(ThreadLedController):
    def __init__(self, config):
        super().__init__(self.__work, config)

        self.__colors = config.colors
        self.__update_time = config.update_time

    def __work(self):
        colors = []
        while not self._should_stop_thread:
            if not colors:
                colors = self.__colors[::-1]

            next_color = colors.pop()
            for led in self._leds:
                led.do_animated_color(color, next_color, self.__update_time)
            color = next_color
