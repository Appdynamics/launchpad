from yaspin import yaspin


def as_spinner(fn, text):
    with yaspin().bold.blink.bouncingBall as sp:
        sp.text = text
        return fn()
