from typing import Union


class ServerError(BaseException):
    ...


class StyleText:
    def __init__(self, present_text: str, style_text: str):
        ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...


class Debugger:
    def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'): ...

