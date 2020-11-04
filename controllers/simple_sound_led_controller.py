import numpy as np

from controllers.sound_led_controller import SoundLedController
from parameters.controller_parameters import ControllerParameters
from utils.volume_normalizer import VolumeNormalizer
from utils.color import Color


class SimpleSoundLedController(SoundLedController):
    def __init__(self, config: ControllerParameters):
        super().__init__(config)

        normalizer_samples = int(self._chunks_per_sec)
        self.__volume_normalizer = VolumeNormalizer(normalizer_samples)
        self.__low_color: Color = config.low_color
        self.__high_color: Color = config.high_color

    def __set_volume(self, volume):
        color = Color(self.__low_color, self.__high_color, volume)

        for led in self._leds:
            led.set_color(color)

    def _handle_sample(self, data):
        volume = np.abs(data)
        volume = np.max(volume)
        volume = self.__volume_normalizer.normalize_volume(volume)
        self.__set_volume(volume)
