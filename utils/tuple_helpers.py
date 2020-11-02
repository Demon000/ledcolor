from typing import Tuple


def t_mul(t, s) -> Tuple:
    return tuple(x * s for x in t)


def t_add(a, b) -> Tuple:
    return tuple(x + y for (x, y) in zip(a, b))


def t_int(t) -> Tuple:
    return tuple(int(x) for x in t)


def t_add_w(a, b, w) -> Tuple:
    if w > 1:
        w = 1

    if w < 0:
        w = 0

    return t_int(t_add(t_mul(a, 1 - w), t_mul(b, w)))
