import pickle

from parameters.controller_parameters import ControllerParameters
from parameters.led_parameters import LedParameters


class LedControllerParameters:
    def __init__(self, args):
        self.led = LedParameters(args)
        self.controller = ControllerParameters(args)

    def serialize(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialization: bytes) -> 'LedControllerParameters':
        return pickle.loads(serialization)
