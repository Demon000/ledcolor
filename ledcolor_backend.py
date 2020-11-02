#!/usr/bin/env python

import socket
import os
from typing import Union

from controllers.controller_factory import ControllerFactory
from controllers.led_controller import LedController
from leds.led import Led
from leds.led_factory import LedFactory
from parameters.controller_parameters import ControllerParameters
from parameters.led_controller_parameters import LedControllerParameters
from config import SERVER_ADDRESS


class Server:
    def __init__(self, address):
        self.__server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__server.bind(address)

        self.__leds = {}
        self.__controllers = []

    def __find_compatible_controller(self, config: ControllerParameters) -> Union[LedController, None]:
        for controller in self.__controllers:
            if controller.is_compatible_config(config):
                return controller

        return None

    def __find_led_controller(self, led) -> Union[LedController, None]:
        for controller in self.__controllers:
            if controller.controls_led(led):
                return controller

        return None

    def __remove_led_control(self, led):
        controller = self.__find_led_controller(led)
        if not controller:
            return

        controller.remove_led(led)

    def __add_led_control(self, led, config: ControllerParameters):
        controller = self.__find_compatible_controller(config)
        if not controller:
            controller = ControllerFactory.build(config)
            self.__controllers.append(controller)

        if not controller:
            return

        controller.add_led(led)

    def __create_led(self, config) -> Led:
        if config.led_name in self.__leds:
            return self.__leds[config.led_name]

        led = LedFactory.build(config)
        self.__leds[config.led_name] = led

        return led

    def __apply_config(self, config):
        led = self.__create_led(config.led)
        self.__remove_led_control(led)
        self.__add_led_control(led, config.controller)

    def __receive_config(self, connection):
        config_data = b''
        while True:
            data = connection.recv(16)
            if data:
                config_data += data
            else:
                break

        config = LedControllerParameters.deserialize(config_data)
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
        os.unlink(SERVER_ADDRESS)
    except OSError:
        if os.path.exists(SERVER_ADDRESS):
            raise

    server = Server(SERVER_ADDRESS)
    server.start()


if __name__ == '__main__':
    main()
