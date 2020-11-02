from controllers.iterator_led_controller import IteratorLedController
from controllers.matrix_sound_led_controller import MatrixSoundLedController
from controllers.range_sound_led_controller import RangeSoundLedController
from parameters.controller_parameters import ControllerType, ControllerParameters


class ControllerFactory:
    @staticmethod
    def build(config: ControllerParameters):
        if config.controller_type == ControllerType.RANGE_SOUND:
            controller = RangeSoundLedController(config)
        elif config.controller_type == ControllerType.MATRIX_SOUND:
            controller = MatrixSoundLedController(config)
        elif config.controller_type == ControllerType.COLORS:
            controller = IteratorLedController(config)
        elif config.controller_type == ControllerType.NONE:
            return None
        else:
            raise ValueError('Unsupported controller type')

        return controller
