from collections import deque
from typing import List

import numpy as np


class VolumeNormalizer:
    def __init__(self, max_samples):
        self.__samples = deque(maxlen=max_samples)

    def normalize_volumes(self, volumes: List[float]) -> List[float]:
        self.__samples.extend(volumes)

        min_volume = np.min(self.__samples)
        max_volume = np.max(self.__samples)

        if max_volume - min_volume == 0:
            normalized_volumes = [0.0] * len(volumes)
        else:
            normalized_volumes = (volumes - min_volume) / (max_volume - min_volume)

        return normalized_volumes

    def normalize_volume(self, volume: float) -> float:
        return self.normalize_volumes([volume])[0]
