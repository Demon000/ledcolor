import pyaudio
import numpy
import time
import signal

from color_setter import ColorSetter

from tuple_helpers import t_add_w

CHANNELS = 1
RATE = 44100

class SoundColor(ColorSetter):
  def __init__(self, wait_time, update_time, colors):
    super().__init__(wait_time)

    self.__chunk_size = int(RATE * update_time)
    self.__colors = colors

    self.__audio = pyaudio.PyAudio()
    self.__stream = None

  def __del__(self):
    if self.__stream:
      self.__stream.stop_stream()
      self.__stream.close()

    self.__audio.terminate()

  def __set_volume(self, volume):
    color_index = 0
    max_color_index = len(self.__colors) - 1
    while color_index < max_color_index:
      min_color_volume = color_index / max_color_index
      max_color_volume = (color_index + 1) / max_color_index
      if min_color_volume <= volume <= max_color_volume:
        break

      color_index += 1

    volume_delta = volume - min_color_volume
    first_color = self.__colors[color_index]
    second_color = self.__colors[color_index + 1]

    color = t_add_w(first_color, second_color, volume_delta)
    self._set_color(color, save=False)

  def __on_stream_data(self, raw, frame_count, time_info, status):
    data = numpy.frombuffer(raw, dtype=numpy.int16)
    data = numpy.abs(data)

    volume = numpy.max(data) / 2**15
    self.__set_volume(volume)

    return (raw, pyaudio.paContinue)

  def run(self):
    self.__stream = self.__audio.open(format=pyaudio.paInt16, input=True,
        channels=CHANNELS, rate=RATE, frames_per_buffer=self.__chunk_size,
        stream_callback=self.__on_stream_data)

    signal.pause()
