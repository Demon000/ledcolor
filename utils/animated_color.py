from utils.color import Color


class AnimatedColor(Color):
    def __init__(self, on_duration, fade_duration, *args):
        super().__init__(*args)

        self.__on_duration: float = on_duration
        self.__fade_duration: float = fade_duration

    @property
    def on_duration(self) -> float:
        return self.__on_duration

    @property
    def fade_duration(self) -> float:
        return self.__fade_duration
