import socket
import sys
import os

from sound_led_controller import SoundLedController
from iterator_led_controller import IteratorLedController
from config import Config
from constants import server_address

class Server():
  def __init__(self, address):
    self.__server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.__server.bind(address)

    self.__leds = {}
    self.__controllers = []

  def __remove_led_control(self, led):
    for controller in self.__controllers:
      controller.remove_led(led)

  # def __find_matching_controller(self, config):
  #   for controller in self.__controllers:
  #     pass

  def __apply_config(self, config):
    if config.name not in self.__leds:
      led = Led(config.name)
      self.__leds[config.name] = led
    else:
      led = self.__leds[config.name]
      self.__remove_led_control(led)

    if config.is_sound:
      controller = SoundLedController([led], config)
    elif config.is_iterator:
      controller = IteratorLedController([led], config)

    self.__controllers.append(controller)
    controller.start()

  def __receive_config(self, connection):
    config_data = b''
    while True:
      data = connection.recv(16)
      if data:
        config_data += data
      else:
        break

    config = Config.deserialize(config_data)
    self.__apply_config(config)

  def __wait_for_connection(self):
    while True:
      connection, _ = self.__server.accept()
      try:
        self.__receive_config(connection)
      finally:
        connection.close()

  def start(self):
    self.__server.listen(1)
    self.__wait_for_connection()

def main():
  try:
    os.unlink(server_address)
  except OSError:
    if os.path.exists(server_address):
      raise

  server = Server(server_address)
  server.start()

if __name__ == "__main__":
  main()
