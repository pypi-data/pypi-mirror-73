from colorama import Fore, Style


class CursorMove:

    @classmethod
    def up(cls, count: int) -> str:
        return f'\033[{count}A'

    @classmethod
    def down(cls, count: int) -> str:
        return f'\033[{count}B'

    @classmethod
    def right(cls, count: int) -> str:
        return f'\033[{count}C'

    @classmethod
    def left(cls, count: int) -> str:
        return f'\033[{count}D'

    @classmethod
    def bol(cls, count: int) -> str:
        return f'\033[{count}E'

    @classmethod
    def eol(cls, count: int) -> str:
        return f'\033[{count}F'


def green(s: str) -> str:
    return '{}{}{}'.format(
        Fore.GREEN,
        s,
        Style.RESET_ALL,
    )


def blue(s: str) -> str:
    return '{}{}{}'.format(
        Fore.BLUE,
        s,
        Style.RESET_ALL,
    )


def yellow(s: str) -> str:
    return '{}{}{}'.format(
        Fore.YELLOW,
        s,
        Style.RESET_ALL,
    )


def red(s: str) -> str:
    return '{}{}{}'.format(
        Fore.RED,
        s,
        Style.RESET_ALL,
    )
