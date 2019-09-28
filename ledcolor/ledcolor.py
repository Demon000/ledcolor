#!/usr/bin/env python

import socket

from optparse import OptionParser

from config import Config
from constants import *

class Client():
  def __init__(self, address):
    self.__address = address
    self.__client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

  def send_config(self, config):
    config_data = config.serialize()
    self.__client.sendall(config_data)

  def start(self):
    self.__client.connect(self.__address)

  def stop(self):
    self.__client.close()

def main():
  usage = """%prog [options] [colors]

  Colors: a list of colors to cycle through, defined in the following format
    color_string:on_duration:fade_duration

    Where color_string is in one of the following formats:
    #ffffff ffffff #fff fff

    Where on_duration and fade_duration are floating point values representing
    the number of seconds the color stays on and fades out, respectively.
  """

  parser = OptionParser(usage=usage)
  parser.add_option('-u', '--update-time', dest='update_time', default=default_update_time, type=float)
  parser.add_option('-n', '--name', dest='name', type=str)

  parser.add_option('-c', '--colors', action='store_true', dest='is_colors')

  parser.add_option('-s', '--sound', action='store_true', dest='is_sound')
  parser.add_option('-i', '--input', dest='input_name', type=str)
  parser.add_option('-R', '--random', action='store_true', dest='random_color')
  parser.add_option('-L', '--low', dest='low_color_string', default=default_low_color, type=str)
  parser.add_option('-H', '--high', dest='high_color_string', default=default_high_color, type=str)

  options, args = parser.parse_args()
  config = Config(options, args)
  client = Client(server_address)

  client.start()
  client.send_config(config)
  client.stop()

if __name__ == "__main__":
  main()
