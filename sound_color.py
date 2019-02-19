import pyaudio
import numpy
import time

from color_setter import ColorSetter

from tuple_helpers import t_add_w

CHANNELS = 1
RATE = 44100
LOW = (0, 255, 0)
HIGH = (255, 0, 0)

class SoundColor(ColorSetter):
  def __init__(self, wait_time, update_time):
    super().__init__(wait_time)

    self.__chunk_size = int(RATE * update_time)
    self.__audio = pyaudio.PyAudio()
    self.__stream = None

  def __del__(self):
    if self.__stream:
      self.__stream.stop_stream()
      self.__stream.close()

    self.__audio.terminate()

  def __set_volume(self, volume):
    color = t_add_w(LOW, HIGH, volume)
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

    while True:
      time.sleep(10)
