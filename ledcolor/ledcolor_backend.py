#!/usr/bin/env python

import socket
import sys
import os

from sound_led_controller import SoundLedController
from iterator_led_controller import IteratorLedController
from led import Led
from config import Config
from constants import server_address

class Server():
  def __init__(self, address):
    self.__server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.__server.bind(address)

    self.__leds = {}
    self.__controllers = []

  def __remove_led_control(self, led):
    found = False
    for controller in self.__controllers:
      if controller.controls_led(led):
        found = True
        break

    if found:
      controller.remove_led(led)
      if not controller.has_leds():
        controller.stop()
        self.__controllers.remove(controller)

  def __create_led_control(self, led, config):
    leds = [led]
    if config.is_sound:
      controller = SoundLedController(leds, config)
    elif config.is_iterator:
      controller = IteratorLedController(leds, config)

    self.__controllers.append(controller)
    controller.start()

  def __create_led(self, name):
    if name in self.__leds:
      return self.__leds[name]

    led = Led(name)
    self.__leds[name] = led

    return led

  def __apply_config(self, config):
    led = self.__create_led(config.name)
    self.__remove_led_control(led)
    self.__create_led_control(led, config)

  def __receive_config(self, connection):
    config_data = b''
    while True:
      data = connection.recv(16)
      if data:
        config_data += data
      else:
        break

    config = Config.deserialize(config_data)
    try:
      self.__apply_config(config)
    except ValueError as ve:
      print(ve)

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
