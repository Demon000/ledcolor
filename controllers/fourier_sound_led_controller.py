import numpy as np

from config import AUDIO_RATE, AUDIBLE_LOW_FREQ, AUDIBLE_HIGH_FREQ, FREQ_GROUPS_GAMMA, VOLUME_LIMIT_FALL_TIME
from controllers.sound_led_controller import SoundLedController
from leds.led import Led
from leds.matrix_led import MatrixLed
from parameters.controller_parameters import ControllerParameters, FourierValueMode
from utils.color import Color
from utils.value_normalizer import ValueNormalizer


def get_volume_max(amplitudes):
    return np.max(amplitudes)


def get_volume_avg(amplitudes):
    return np.average(amplitudes)


def get_volume_sum(amplitudes):
    s = np.sum(amplitudes)
    if s > 1.0:
        s = 1.0
    return s


class FourierSoundLedController(SoundLedController):
    def __init__(self, config: ControllerParameters):
        super().__init__(config)

        if config.value_mode == FourierValueMode.MAX:
            self.__value_fn = get_volume_max
        elif config.value_mode == FourierValueMode.AVG:
            self.__value_fn = get_volume_avg
        elif config.value_mode == FourierValueMode.SUM:
            self.__value_fn = get_volume_sum

        self.__low_color: Color = config.low_color
        self.__high_color: Color = config.high_color

        freqs = np.fft.fftfreq(self._chunk_size, d=1 / self._chunk_size)
        freqs = freqs[:self._chunk_size // 2]
        freqs = freqs * AUDIO_RATE // self._chunk_size

        self.__audible_index_start = 0
        self.__audible_index_end = 0
        for i, freq in enumerate(freqs):
            if freq < AUDIBLE_LOW_FREQ:
                self.__audible_index_start = i

            if freq > AUDIBLE_HIGH_FREQ:
                self.__audible_index_end = i
                break

        self.__freqs = freqs[self.__audible_index_start:self.__audible_index_end]

        self.__normalizer_samples = int(self._chunks_per_sec * VOLUME_LIMIT_FALL_TIME)
        self.__max_volume_normalizer = ValueNormalizer(self.__normalizer_samples)
        self.__group_volume_normalizers = {}

    def __create_group_normalizers(self, no_groups):
        if no_groups in self.__group_volume_normalizers:
            return

        self.__group_volume_normalizers[no_groups] = \
            [ValueNormalizer(self.__normalizer_samples) for _ in range(no_groups)]

    def __normalize_group_volume(self, group_index, no_groups, volume):
        normalizer = self.__group_volume_normalizers[no_groups][group_index]
        return normalizer.normalize_value(volume)

    def __normalize_max_volume(self, max_volume):
        return self.__max_volume_normalizer.normalize_value(max_volume)

    def __group_amplitudes(self, amplitudes, no_groups=None):
        groups = [[] for _ in range(no_groups)]
        max_freq = self.__freqs[-1]
        for freq, amplitude in zip(self.__freqs, amplitudes):
            group_index = int(((freq / max_freq) ** (1 / FREQ_GROUPS_GAMMA)) * no_groups)
            if group_index >= no_groups:
                group_index = no_groups - 1
            groups[group_index].append(amplitude)

        return groups

    def __set_matrix_volume(self, led, amplitudes):
        height = led.get_height()
        width = led.get_width()

        chunks = self.__group_amplitudes(amplitudes, height)
        color_matrix = []

        self.__create_group_normalizers(height)

        for i, chunk in enumerate(chunks):
            row = []

            volume = self.__value_fn(chunk)
            volume = self.__normalize_group_volume(i, height, volume)

            width_active = int(width * volume)
            for x in range(width):
                if x < width_active:
                    row.append(self.__high_color)
                else:
                    row.append(self.__low_color)

            color_matrix.append(row)

        led.set_color_matrix(color_matrix)

    def __set_simple_volume(self, led, max_amplitude):
        volume = self.__normalize_max_volume(max_amplitude)
        color = Color(self.__low_color, self.__high_color, volume)
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
        amplitudes = amplitudes[self.__audible_index_start:self.__audible_index_end]
        max_amplitude = np.max(amplitudes)

        self.__set_volume(amplitudes, max_amplitude)
