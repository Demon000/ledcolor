from utils.color import Color


class AnimatedColor(Color):
    def __init__(self, on_duration, fade_duration, *args):
        super().__init__(*args)

        self.__on_duration: float = on_duration
        self.__fade_duration: float = fade_duration

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if self._rgb != other._rgb:
            return False

        if self.__on_duration != other.__on_duration:
            return False

        if self.__fade_duration != other.__fade_duration:
            return False

        return True

    def __str__(self):
        return "AnimatedColor -> r: {}, g: {}, b: {}, on: {}, fade: {}" \
                .format(*self._rgb, self.__on_duration, self.__fade_duration)

    @property
    def on_duration(self) -> float:
        return self.__on_duration

    @property
    def fade_duration(self) -> float:
        return self.__fade_duration
