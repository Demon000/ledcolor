#!/usr/bin/env python

import socket
import os

from sound_led_controller import SoundLedController
from iterator_led_controller import IteratorLedController
from led import Led
from config import Config, ControllerType
from constants import server_address


class Server:
    def __init__(self, address):
        self.__server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__server.bind(address)

        self.__leds = {}
        self.__controllers = []

    def __find_compatible_controller(self, config):
        for controller in self.__controllers:
            if controller.is_compatible_config(config):
                return controller

        return None

    def __find_led_controller(self, led):
        for controller in self.__controllers:
            if controller.controls_led(led):
                return controller

        return None

    def __remove_led_control(self, led):
        controller = self.__find_led_controller(led)
        if not controller:
            return

        controller.remove_led(led)

    def __add_led_control(self, led, config):
        controller = self.__find_compatible_controller(config)
        if not controller:
            if config.controller_type == ControllerType.SOUND:
                controller = SoundLedController(config)
            elif config.controller_type == ControllerType.COLORS:
                controller = IteratorLedController(config)
            elif config.controller_type == ControllerType.NONE:
                return
            else:
                raise ValueError('Unsupported controller type')

            self.__controllers.append(controller)

        controller.add_led(led)

    def __create_led(self, led_name, led_type):
        if led_name in self.__leds:
            return self.__leds[led_name]

        led = Led(led_name, led_type)
        self.__leds[led_name] = led

        return led

    def __apply_config(self, config):
        led = self.__create_led(config.led_name, config.led_type)
        self.__remove_led_control(led)
        self.__add_led_control(led, config)

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
