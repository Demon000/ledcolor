from typing import List

import numpy as np
import soundcard as sc

from parameters.controller_parameters import ControllerParameters
from utils.color import Color
from config import *
from controllers.thread_led_controller import ThreadLedController


class SoundLedController(ThreadLedController):
    def __init__(self, config: ControllerParameters):
        super().__init__(self.__work, config)

        self.__chunk_size: int = int(AUDIO_RATE * config.update_time)
        self.__input_name: str = config.input_name

        self.__low_color: Color = config.low_color
        self.__high_color: Color = config.high_color

        self.__recent_volume_samples: List[float] = [0.0]
        self.__no_recent_volume_samples: int = int(VOLUME_SAMPLE_TIME / config.update_time)

        self.__volume_limit: float = VOLUME_LOW_LIMIT
        self.__volume_limit_falling: bool = True
        self.__volume_limit_fall: float = config.update_time / VOLUME_LIMIT_FALL_TIME * (VOLUME_MAX_LIMIT - VOLUME_LOW_LIMIT)

    def __add_recent_volume(self, volume: float):
        self.__recent_volume_samples.append(volume)
        if len(self.__recent_volume_samples) > self.__no_recent_volume_samples:
            self.__recent_volume_samples.pop(0)

    def __normalize_volume(self, volume) -> float:
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

        with mic.recorder(AUDIO_RATE, channels=AUDIO_CHANNELS) as mic_recorder:
            while not self._should_stop_thread:
                data = mic_recorder.record(numframes=self.__chunk_size)
                volume = np.max(data)
                volume = self.__normalize_volume(volume)
                self.__set_volume(volume)
