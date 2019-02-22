import pyaudio
import numpy
import signal

from color_setter import ColorSetter
from color import Color

CHANNELS = 1
RATE = 48000

class SoundColor(ColorSetter):
  def __init__(self, low_color, high_color, input_name, wait_time, update_time):
    super().__init__(wait_time, update_time)

    self.__chunk_size = int(RATE * update_time)
    self.__low_color = low_color
    self.__high_color = high_color
    self.__input_name = input_name

  def __set_volume(self, volume):
    color = Color(self.__low_color.rgb, self.__high_color.rgb, volume)
    self._set_color(color)

  def __on_stream_data(self, raw, frame_count, time_info, status):
    data = numpy.frombuffer(raw, dtype=numpy.int16)
    data = numpy.abs(data)

    volume = numpy.max(data) / 2**15
    self.__set_volume(volume)

    return (raw, pyaudio.paContinue)

  def __find_input_index(self):
    info = self.__audio.get_default_host_api_info()

    devices_count = info.get('deviceCount')
    for device_index in range(devices_count):
      device = self.__audio.get_device_info_by_host_api_device_index(0, device_index)
      if device['name'] == self.__input_name:
        return device['index']

    return None

  def start(self):
    self.__audio = pyaudio.PyAudio()
    input_index = self.__find_input_index()
    self.__stream = self.__audio.open(format=pyaudio.paInt16,
        input=True, input_device_index=input_index,
        channels=CHANNELS, rate=RATE, frames_per_buffer=self.__chunk_size,
        stream_callback=self.__on_stream_data)

  def stop(self):
    self.__audio.terminate()
    self.__stream.stop_stream()
    self.__stream.close()
