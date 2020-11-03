import numpy as np

from config import VOLUME_SAMPLE_TIME
from controllers.sound_led_controller import SoundLedController
from leds.led import Led
from leds.matrix_led import MatrixLed
from parameters.controller_parameters import ControllerParameters
from utils.color import Color
from utils.helpers import next_power_of_2
from utils.volume_normalizer import VolumeNormalizer


class MatrixSoundLedController(SoundLedController):
    def __init__(self, config: ControllerParameters):
        super().__init__(config)

        self.__low_color: Color = config.low_color
        self.__high_color: Color = config.high_color
        self.__volume_color: Color = config.volume_color

        self.__fft_size = next_power_of_2(self._chunk_size)
        self.__i = 0

        normalizer_samples = int(VOLUME_SAMPLE_TIME // config.update_time)
        self.__volume_normalizer = VolumeNormalizer(normalizer_samples)

    def add_led(self, led: Led):
        if not isinstance(led, MatrixLed):
            raise ValueError('Matrix sound controller can only be used with a matrix led')

        super().add_led(led)

    def __set_volume(self, volume):
        color = Color(self.__low_color, self.__high_color, volume)

        for led in self._leds:
            led.set_color(color)

    def _handle_sample(self, data):
        data = np.ndarray.flatten(data)
        freqs_amplitude = np.fft.fft(data, n=self.__fft_size)
        freqs = np.fft.fftfreq(self.__fft_size)

        freqs_amplitude = abs(freqs_amplitude[range(self.__fft_size // 2)])
        freqs_amplitude = freqs_amplitude * 2 / (2 * (self.__fft_size // 2))

        freqs = freqs[range(self.__fft_size // 2)]

        max_freq_amplitude = np.max(freqs_amplitude)
        max_freq_amplitude = self.__volume_normalizer.normalize_volume(max_freq_amplitude)

        self.__set_volume(max_freq_amplitude)
