#!/usr/bin/env python

import socket
from argparse import ArgumentParser

from parameters.led_controller_parameters import LedControllerParameters
from parameters.controller_parameters import ControllerType
from parameters.led_parameters import LedType
from config import *


class Client:
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
    parser = ArgumentParser()

    parser.add_argument('led_name', type=str, help="""
    Name of the LED device
    """)

    parser.add_argument('led_type', choices=LedType.list(), help="""
    Type of the LED device, available types:
    {}
    """.format(', '.join(LedType.list())))

    parser.add_argument('controller_type', choices=ControllerType.list(), help="""
    Controller type to use, available types:
    {}
    """.format(', '.join(ControllerType.list())))

    parser.add_argument('color', type=str, nargs='*', help="""
    Multiple colors to cycle through when in colors mode, defined in the following format
    color_string:on_duration:fade_duration.
    color_string is in one of the following formats: #ffffff ffffff #fff fff
    """)

    parser.add_argument('-u', '--update-time', dest='update_time', default=DEFAULT_OUTPUT_TIME, type=float, help="""
    Number of seconds to pass (floating point value) between color updates
    """)

    parser.add_argument('-i', '--input', dest='input_name', type=str, help="""
    Name of the input device to use when in sound mode, can be found by doing `pacmd list-sources`.
    Uses the default system microphone by default
    """)

    parser.add_argument('-L', '--low', dest='low_color_string', default=DEFAULT_LOW_COLOR, type=str, help="""
    Low volume color string to use when in sound mode, specified in one of the following formats:
    #ffffff ffffff #fff fff
    """)

    parser.add_argument('-H', '--high', dest='high_color_string', default=DEFAULT_HIGH_COLOR, type=str, help="""
    High volume color string to use when in sound mode, specified in one of the following formats:
    #ffffff ffffff #fff fff
    """)

    args = parser.parse_args()
    config = LedControllerParameters(args)
    client = Client(SERVER_ADDRESS)

    client.start()
    client.send_config(config)
    client.stop()


if __name__ == '__main__':
    main()
