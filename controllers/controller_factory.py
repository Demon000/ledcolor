from controllers.iterator_led_controller import IteratorLedController
from controllers.fourier_sound_led_controller import FourierSoundLedController
from controllers.simple_sound_led_controller import SimpleSoundLedController
from parameters.controller_parameters import ControllerType, ControllerParameters


class ControllerFactory:
    @staticmethod
    def build(config: ControllerParameters):
        if config.controller_type == ControllerType.SIMPLE_SOUND:
            controller = SimpleSoundLedController(config)
        elif config.controller_type == ControllerType.FOURIER_SOUND:
            controller = FourierSoundLedController(config)
        elif config.controller_type == ControllerType.COLORS:
            controller = IteratorLedController(config)
        elif config.controller_type == ControllerType.NONE:
            return None
        else:
            raise ValueError('Unsupported controller type')

        return controller
