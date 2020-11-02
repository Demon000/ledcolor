import numpy as np
import soundcard as sc

from color import Color
from constants import *
from controllers.thread_led_controller import ThreadLedController


class SoundLedController(ThreadLedController):
    def __init__(self, config):
        super().__init__(self.__work, config)

        self.__chunk_size = int(audio_rate * config.update_time)
        self.__input_name = config.input_name

        self.__low_color = config.low_color
        self.__high_color = config.high_color

        self.__recent_volume_samples = [0]
        self.__no_recent_volume_samples = int(volume_sample_time / config.update_time)

        self.__volume_limit = volume_low_limit
        self.__volume_limit_falling = True
        self.__volume_limit_fall = config.update_time / volume_limit_fall_time * (volume_max_limit - volume_low_limit)

    def __add_recent_volume(self, volume):
        self.__recent_volume_samples.append(volume)
        if len(self.__recent_volume_samples) > self.__no_recent_volume_samples:
            self.__recent_volume_samples.pop(0)

    def __normalize_volume(self, volume):
        min_volume = np.min(self.__recent_volume_samples)
        max_volume = np.max(self.__recent_volume_samples)

        if max_volume - min_volume == 0:
            normalized_volume = 0
        else:
            normalized_volume = (volume - min_volume) / (max_volume - min_volume)

        self.__add_recent_volume(volume)

        return normalized_volume

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
                volume = np.max(data)
                volume = self.__normalize_volume(volume)
                self.__set_volume(volume)
