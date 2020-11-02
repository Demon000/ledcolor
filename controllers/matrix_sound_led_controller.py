from controllers.sound_led_controller import SoundLedController
from leds.led import Led
from leds.matrix_led import MatrixLed
from parameters.controller_parameters import ControllerParameters


class MatrixSoundLedController(SoundLedController):
    def __init__(self, config: ControllerParameters):
        super().__init__(config)

    def add_led(self, led: Led):
        if not isinstance(led, MatrixLed):
            raise ValueError('Matrix sound controller can only be used with a matrix led')

        super().add_led(led)

    def _handle_sample(self, data):
        pass
