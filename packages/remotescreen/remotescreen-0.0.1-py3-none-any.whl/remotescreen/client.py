from omnitools import b64e, b64d, encryptedsocket_function, key_pair_format, args
from unencryptedsocket import SC as USC
from encryptedsocket import SC as ESC


class RSESC(ESC):
    def __init__(self, host: str = "127.199.71.10", port: int = 39293) -> None:
        super().__init__(host, port)

    def get_screenshot(self):
        return super().request(command="take_screenshot", data=args())


class RSUSC(USC):
    def __init__(self, host: str = "127.199.71.10", port: int = 39293) -> None:
        super().__init__(host, port)

    def get_screenshot(self):
        return super().request(command="take_screenshot", data=args())


