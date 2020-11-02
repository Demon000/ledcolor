from controllers.iterator_led_controller import IteratorLedController
from controllers.sound_led_controller import SoundLedController
from parameters.controller_parameters import ControllerType, ControllerParameters


class ControllerFactory:
    @staticmethod
    def build(config: ControllerParameters):
        if config.controller_type == ControllerType.SOUND:
            controller = SoundLedController(config)
        elif config.controller_type == ControllerType.COLORS:
            controller = IteratorLedController(config)
        elif config.controller_type == ControllerType.NONE:
            return None
        else:
            raise ValueError('Unsupported controller type')

        return controller
