from threading import Thread

from controllers.led_controller import LedController


class ThreadLedController(LedController):
    def __init__(self, work, config):
        super().__init__(config)

        self.__work = work
        self.__thread = None
        self._should_stop_thread = False

    def start(self):
        if self.__thread is not None:
            return

        self.__thread = Thread(target=self.__work)
        self._should_stop_thread = False
        self.__thread.start()

    def stop(self):
        if self.__thread is None:
            return

        if self._should_stop_thread is True:
            return

        self._should_stop_thread = True
        self.__thread.join()
        self.__thread = None
