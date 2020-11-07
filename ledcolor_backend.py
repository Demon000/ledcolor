#!/usr/bin/env python

import signal
import socket
import os
import sys
from functools import partial
from threading import Thread
from typing import Union, List, Dict

from controllers.controller_factory import ControllerFactory
from controllers.led_controller import LedController
from leds.led import Led
from leds.led_factory import LedFactory
from parameters.controller_parameters import ControllerParameters, ControllerType
from parameters.led_controller_parameters import LedControllerParameters
from config import SERVER_ADDRESS, SERVER_WAIT_TIMEOUT
from parameters.led_parameters import LedParameters


class Server:
    def __init__(self, address):
        self.__server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__server.bind(address)
        self.__server.settimeout(SERVER_WAIT_TIMEOUT)
        self.__thread = Thread(target=self.__wait_for_connection)
        self.__should_stop = False

        self.__controllers: List[LedController] = []

    def __find_compatible_controller(self, config: ControllerParameters) -> Union[LedController, None]:
        for controller in self.__controllers:
            if controller.is_compatible_config(config):
                return controller

        return None

    def __get_compatible_controller(self, config: ControllerParameters) -> LedController:
        controller = self.__find_compatible_controller(config)
        if controller:
            return controller

        controller = ControllerFactory.build(config)
        self.__controllers.append(controller)
        return controller

    def __detach_led(self, name: str):
        for controller in self.__controllers:
            controller.remove_led(name)

    def __apply_config(self, config: LedControllerParameters):
        self.__detach_led(config.led.led_name)
        if config.controller.controller_type == ControllerType.NONE:
            return

        led = LedFactory.build(config.led)
        controller = self.__get_compatible_controller(config.controller)
        controller.add_led(led)

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
        while not self.__should_stop:
            try:
                connection, _ = self.__server.accept()
            except socket.timeout:
                continue

            self.__receive_config(connection)
            connection.close()

    def start(self):
        self.__server.listen(1)
        self.__wait_for_connection()

    def __stop_controllers(self):
        for controller in self.__controllers:
            controller.stop()

    def stop(self):
        self.__should_stop = True
        self.__stop_controllers()


def cleanup(server, signal, frame):
    server.stop()
    sys.exit(0)


def main():
    try:
        os.unlink(SERVER_ADDRESS)
    except OSError:
        if os.path.exists(SERVER_ADDRESS):
            raise

    server = Server(SERVER_ADDRESS)

    signal.signal(signal.SIGINT, partial(cleanup, server))

    server.start()


if __name__ == '__main__':
    main()
