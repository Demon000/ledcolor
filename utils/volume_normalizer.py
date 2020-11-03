from typing import List

import numpy as np


class VolumeNormalizer:
    def __init__(self, max_samples, low_limit):
        self.__samples: List[float] = []
        self.__no_max_samples: int = max_samples

        self.__volume_limit: float = low_limit

    def __add_samples(self, volumes: List[float]):
        self.__samples.extend(volumes)
        if len(self.__samples) > self.__no_max_samples:
            self.__samples.pop(0)

    def __add_sample(self, volume: float):
        self.__add_samples([volume])

    def normalize_volumes(self, volumes: List[float]) -> List[float]:
        if not len(self.__samples):
            self.__add_samples(volumes)
            return volumes

        min_volume = np.min(self.__samples)
        max_volume = np.max(self.__samples)

        self.__add_samples(volumes)

        if max_volume - min_volume == 0:
            normalized_volumes = [0.0]
        else:
            normalized_volumes = (volumes - min_volume) / (max_volume - min_volume)

        return normalized_volumes

    def normalize_volume(self, volume: float) -> float:
        return self.normalize_volumes([volume])[0]
