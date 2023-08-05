import io
from PIL import ImageGrab
from omnitools import b64e, b64d, encryptedsocket_function, key_pair_format
from unencryptedsocket import SS as USS
from encryptedsocket import SS as ESS


class RSESS(ESS):
    def __init__(self, key_pair: key_pair_format) -> None:
        host = "127.199.71.10"
        port = 39293
        functions = dict(take_screenshot=take_screenshot)
        super().__init__(key_pair, functions, host, port)


class RSUSS(USS):
    def __init__(self) -> None:
        host = "127.199.71.10"
        port = 39293
        functions = dict(take_screenshot=take_screenshot)
        super().__init__(functions, host, port)


def take_screenshot():
    tmp = io.BytesIO()
    screenshot = ImageGrab.grab()
    screenshot.save(tmp, format="PNG")
    tmp.seek(0)
    return tmp.read()


