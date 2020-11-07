from collections import deque
from typing import List

import numpy as np


class ValueNormalizer:
    def __init__(self, max_samples):
        self.__samples = deque(maxlen=max_samples)

    def normalize_values(self, values: List[float]) -> List[float]:
        self.__samples.extend(values)

        min_value = np.min(self.__samples)
        max_value = np.max(self.__samples)

        if max_value - min_value == 0:
            normalized_values = [0.0] * len(values)
        else:
            normalized_values = (values - min_value) / (max_value - min_value)

        return normalized_values

    def normalize_value(self, value: float) -> float:
        return self.normalize_values([value])[0]
