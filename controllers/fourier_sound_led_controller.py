import numpy as np
from more_itertools import pairwise

from config import AUDIO_RATE, AUDIBLE_LOW_FREQ, AUDIBLE_HIGH_FREQ, AUDIBLE_RANGES_HIGH_FREQ
from controllers.sound_led_controller import SoundLedController
from leds.led import Led
from leds.matrix_led import MatrixLed
from parameters.controller_parameters import ControllerParameters
from utils.color import Color
from utils.volume_normalizer import VolumeNormalizer


class FourierSoundLedController(SoundLedController):
    def __init__(self, config: ControllerParameters):
        super().__init__(config)

        self.__low_color: Color = config.low_color
        self.__high_color: Color = config.high_color

        freqs = np.fft.fftfreq(self._chunk_size, d=1 / self._chunk_size)
        freqs = freqs[:self._chunk_size // 2]
        freqs = freqs * AUDIO_RATE // self._chunk_size

        self.__audible_ranges = []
        audible_range_index = 0
        start_audible_index = 0
        end_audible_index = 0
        for i, freq in enumerate(freqs):
            if audible_range_index < len(AUDIBLE_RANGES_HIGH_FREQ) and \
                    freq > AUDIBLE_RANGES_HIGH_FREQ[audible_range_index]:
                self.__audible_ranges.append(i)
                audible_range_index += 1

            if freq < AUDIBLE_LOW_FREQ:
                start_audible_index = i

            if freq > AUDIBLE_HIGH_FREQ:
                end_audible_index = i
                break

        self.__audible_ranges.insert(0, start_audible_index)
        self.__audible_ranges.append(end_audible_index)

        self.__freqs = freqs[start_audible_index:end_audible_index]

        normalizer_samples = int(self._chunks_per_sec * self._chunk_size)
        self.__volume_normalizer = VolumeNormalizer(normalizer_samples)

    def __group_amplitudes(self, amplitudes, no_groups=None):
        groups = []

        for i, (start, end) in enumerate(pairwise(self.__audible_ranges)):
            if not no_groups or i + 1 < no_groups:
                groups.append(amplitudes[start:end])
            else:
                end = self.__audible_ranges[-1]
                groups.append(amplitudes[start:end])
                break

        return groups

    def __set_matrix_volume(self, led, amplitudes):
        height = led.get_height()
        width = led.get_width()

        chunks = self.__group_amplitudes(amplitudes, height)

        for i, chunk in enumerate(chunks):
            average_volume = np.max(chunk)

            width_active = int(width * average_volume)
            width_inactive = int(width * (1 - average_volume))

            for j in range(width_active):
                led.set_color_cell(j, i, self.__high_color)

            for j in range(width_inactive):
                led.set_color_cell(width_active + j, i, self.__low_color)

        led.draw_cells()

    def __set_simple_volume(self, led, max_amplitude):
        color = Color(self.__low_color, self.__high_color, max_amplitude)
        led.set_color(color)

    def __set_volume(self, amplitudes, max_amplitude):
        for led in self._leds:
            if isinstance(led, MatrixLed):
                self.__set_matrix_volume(led, amplitudes)
            elif isinstance(led, Led):
                self.__set_simple_volume(led, max_amplitude)

    def _handle_sample(self, data):
        data = np.ndarray.flatten(data)
        amplitudes = np.fft.fft(data)
        amplitudes = amplitudes[:self._chunk_size // 2]
        amplitudes = abs(amplitudes)

        amplitudes = self.__volume_normalizer.normalize_volumes(amplitudes)
        audible_amplitudes = self.__group_amplitudes(amplitudes, 1)[0]
        max_amplitude = np.max(audible_amplitudes)

        self.__set_volume(amplitudes, max_amplitude)
