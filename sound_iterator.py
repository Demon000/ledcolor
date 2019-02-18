import pyaudio
import numpy

from tuple_helpers import t_add_w

CHUNK_SIZE = 2**11
CHANNELS = 1
RATE = 44100
MAX_PEAK = 2**16

LOW = (0, 255, 0)
HIGH = (255, 0, 0)

max_peak = 0

class SoundIterator():
  def __init__(self):
    self.__audio = pyaudio.PyAudio()
    self.__stream = self.__audio.open(format=pyaudio.paInt16, input=True,
        channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK_SIZE,
        stream_callback=self.__on_stream_data)

    self.__current_volume = 0

  def __del__(self):
    self.__stream.stop_stream()
    self.__stream.close()
    self.__audio.terminate()

  def __iter__(self):
    return self

  def __next__(self):
    color = t_add_w(LOW, HIGH, self.__current_volume)
    return (0.1, color)

  def __on_stream_data(self, raw, frame_count, time_info, status):
    data = numpy.frombuffer(raw, dtype=numpy.int16)
    normalized_data = numpy.abs(data)
    peak = numpy.abs(numpy.max(normalized_data) - numpy.min(normalized_data))
    volume = peak * 3 / MAX_PEAK
    self.__current_volume = volume
    return (raw, pyaudio.paContinue)
