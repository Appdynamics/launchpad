import types

from yaspin import yaspin


def as_spinner(fn: types.LambdaType, text: str):
    with yaspin().bold.blink.bouncingBall as sp:
        sp.text = text
        return fn()
