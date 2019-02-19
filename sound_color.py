import pyaudio
import numpy

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

    fft = numpy.fft.rfft(data)
    fft = numpy.abs(fft)

    freq = numpy.fft.rfftfreq(self.__chunk_size, 1 / RATE)

    freq_limits = [60, 250, 500, 2000, 4000, 6000]
    freq_groups = [[], [], [], [], [], [], []]

    current_index = 0
    max_index = len(fft)
    while current_index < max_index:
      current_freq = freq[current_index]
      current_amplitude = fft[current_index] / RATE

      limit_index = 0
      max_limit_index = len(freq_limits)
      while limit_index < max_limit_index and \
          current_freq >= freq_limits[limit_index]:
        limit_index += 1

      freq_groups[limit_index].append(current_amplitude)
      current_index += 1

    averages = []
    for group in freq_groups:
      average = numpy.average(group) / 128
      averages.append(average)

    volume = numpy.max(averages).item()
    self.__set_volume(volume)
    return (raw, pyaudio.paContinue)

  def run(self):
    self.__stream = self.__audio.open(format=pyaudio.paInt16, input=True,
        channels=CHANNELS, rate=RATE, frames_per_buffer=self.__chunk_size,
        stream_callback=self.__on_stream_data)

    while True:
      time.sleep(10)
