from abc import abstractmethod

import soundcard as sc

from parameters.controller_parameters import ControllerParameters
from controllers.thread_led_controller import ThreadLedController

from config import *


class SoundLedController(ThreadLedController):
    def __init__(self, config: ControllerParameters):
        super().__init__(self.__work, config)

        self._chunk_size: int = int(AUDIO_RATE * config.update_time)
        self.__input_name: str = config.input_name

    @abstractmethod
    def _handle_sample(self, data):
        pass

    def __get_mic(self):
        if self.__input_name is None:
            return sc.default_microphone()
        else:
            return sc.get_microphone(self.__input_name, True)

    def __work(self):
        mic = self.__get_mic()
        if mic is None:
            raise ValueError('Failed to find default microphone')

        with mic.recorder(AUDIO_RATE, channels=AUDIO_CHANNELS) as mic_recorder:
            while not self._should_stop_thread:
                data = mic_recorder.record(numframes=self._chunk_size)
                self._handle_sample(data)
