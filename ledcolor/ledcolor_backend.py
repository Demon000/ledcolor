import socket
import sys
import os

from iterator_color import IteratorColor
from sound_color import SoundColor
from config import Config
from constants import server_address

class Server():
  def __init__(self, address):
    self.__server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.__server.bind(address)

    self.__color_setter = None

  def __apply_config(self, config):
    if self.__color_setter:
      self.__color_setter.stop()

    if config.is_sound:
      self.__color_setter = SoundColor(config)
    elif config.is_iterator:
      self.__color_setter = IteratorColor(config)

    self.__color_setter.start()

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
