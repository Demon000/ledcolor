import numpy
import soundcard as sc

from color import Color
from constants import *
from thread_led_controller import ThreadLedController


class SoundLedController(ThreadLedController):
    def __init__(self, config):
        super().__init__(self.__work, config)

        self.__chunk_size = int(audio_rate * config.update_time)
        self.__input_name = config.input_name

        self.__low_color = config.low_color
        self.__high_color = config.high_color

        self.__volume_limit = volume_low_limit
        self.__volume_limit_falling = True
        self.__volume_limit_fall = config.update_time / volume_limit_fall_time * (volume_max_limit - volume_low_limit)

    def __normalize_volume(self, volume):
        if self.__volume_limit > volume:
            self.__volume_limit_falling = True

            self.__volume_limit -= self.__volume_limit_fall
            if self.__volume_limit < volume_low_limit:
                self.__volume_limit = volume_low_limit
        else:
            self.__volume_limit_falling = False
            self.__volume_limit = volume

        return volume_max_limit / self.__volume_limit * volume

    def __set_volume(self, volume):
        color = Color(self.__low_color, self.__high_color, volume)

        for led in self._leds:
            led.set_color(color)

    def __get_mic(self):
        if self.__input_name is None:
            return sc.default_microphone()
        else:
            return sc.get_microphone(self.__input_name, True)

    def __work(self):
        mic = self.__get_mic()
        if mic is None:
            raise ValueError("Failed to find default microphone")

        with mic.recorder(audio_rate, channels=audio_channels) as mic_recorder:
            while not self._should_stop_thread:
                data = mic_recorder.record(numframes=self.__chunk_size)
                volume = numpy.max(data)
                volume = self.__normalize_volume(volume)
                self.__set_volume(volume)
