import os
import math
import termios
import sys
import atexit
import tty

_old_term_settings = None

def echo(enable:bool = False):
    fd = sys.stdin.fileno()
    new = termios.tcgetattr(fd)
    if enable:
        new[3] |= termios.ECHO
    else:
        new[3] &= ~termios.ECHO

    termios.tcsetattr(fd, termios.TCSANOW, new)

def wh():
    return os.get_terminal_size()

def mv(x: int, y: int):
    print(f'\x1b[{y};{x}H', end="")

def mvl(y: int, begin: bool = False):
    match (math.copysign(1, y), begin):
        case (-1, False):
            print(f'\x1b[{abs(y)}A', end="")
        case (1, False):
            print(f'\x1b[{y}B', end="")
        case (-1, True):
            print(f'\x1b[{abs(y)}F', end="")
        case (1, True):
            print(f'\x1b[{abs(y)}E', end="")

def sv():
    print("\x1b7", end="")

def ld():
    print("\x1b8", end="")

def ip(x: int, y: int, txt: str):
    sv()
    mv(x,y)
    print(txt, end="", flush=True)
    ld()

def cs():
    rh()
    print('\x1b[2J',end="")

def rh():
    print("\x1b[H",end="")

def border(tl:str="┌", tr:str="┐", bl:str="└", br="┘", m:str="─", s:str="│"):
    x,y = wh()
    sv()
    rh()
    print(f"{tl}{m*(x-2)}{tr}",flush=True)
    for i in range(y-2):
        print(f"{s}",flush=True,end="")
        print(f"\x1b[{x-1}C",flush=True,end="")
        print(f"{s}",flush=True)
    print(f"{bl}{m*(x-2)}{br}",flush=True,end="")
    ld()

def raw(enabled: bool = True):
    global _old_term_settings
    fd = sys.stdin.fileno()
    if enabled:
        _old_term_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
    else:
        if _old_term_settings is not None:
            termios.tcsetattr(fd, termios.TCSADRAIN, _old_term_settings)
            _old_term_settings = None

def getch():
    return sys.stdin.read(1)

atexit.register(echo, True)
atexit.register(cs)
atexit.register(raw, False)

