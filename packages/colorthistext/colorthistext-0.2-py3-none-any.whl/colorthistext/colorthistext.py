# coding: utf-8


class Foreground:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[39m'


class Background:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
    RESET = '\033[39m'


class Style:
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'


def color(text: str, bg: Background=Background.BLACK, fg: Foreground=None, style: Style=Style.NORMAL):
    if fg == None:
        return '{0}{1}{2}\033[0m'.format(bg, style, text)
    else:
        return '{0}{1}{2}{3}\033[0m'.format(bg, fg, style, text)

