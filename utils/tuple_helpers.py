from typing import Tuple


def t_mul(t: Tuple, s: float) -> Tuple:
    return tuple(x * s for x in t)


def t_add(a: Tuple, b: Tuple) -> Tuple:
    return tuple(x + y for (x, y) in zip(a, b))


def t_int(t: Tuple) -> Tuple:
    return tuple(int(x) for x in t)


def t_add_w(a: Tuple, b: tuple, w: float) -> Tuple:
    if w > 1.0:
        w = 1.0

    if w < 0.0:
        w = 0.0

    return t_int(t_add(t_mul(a, 1 - w), t_mul(b, w)))
