import sys


class Color:
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELOW = '\033[1;33m'
    BLUE = '\033[1;34m'
    PINK = '\033[1;35m'
    PINKBACK_WHITEFONT = '\033[45;37m'
    GREEN_LIGHTNING = '\033[32m \033[05m'
    END = '\033[0m'


def _log(color: str, content: str, exit: bool = False):
    output = color
    output += content
    output += Color.END
    print(output)

    if exit:
        sys.exit(0)


def _alert(content: str):
    color = Color.GREEN
    _log(color, content)


def _wraning(content: str):
    color = Color.YELOW
    _log(color, content)


def _error(content: str):
    color = Color.RED
    _log(color, content, True)