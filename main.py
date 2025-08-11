import os
import math
import termios
import sys
import atexit
import tty

_old_term_settings = None

def echo(enable:bool = False):
    try:
        fd = sys.stdin.fileno()
        new = termios.tcgetattr(fd)
        if enable:
            new[3] |= termios.ECHO
        else:
            new[3] &= ~termios.ECHO

        termios.tcsetattr(fd, termios.TCSANOW, new)
    except:
        pass

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

def border(tl:str="┌", tr:str="┐", bl:str="└", br="┘", m:str="─", s:str="│", x:int=1, y:int=1, w:int=None, h:int=None):
    if w == None:
        w = wh()[0]
    if h == None:
        h = wh()[1]
    sv()
    mv(x,y)
    print(f"{tl}{m*(w-2)}{tr}",flush=True)
    mv(x,y+2)
    for i in range(h-1):
        print(f"{s}",flush=True,end="")
        print(f"\x1b[{w-2}C",flush=True,end="")
        print(f"{s}",flush=True,end="")
        mv(x,y+i+1)
    print(f"{bl}{m*(w-2)}{br}",flush=True,end="")
    ld()

def raw(enabled: bool = True):
    try:
        global _old_term_settings
        fd = sys.stdin.fileno()
        if enabled:
            _old_term_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
        else:
            if _old_term_settings is not None:
                termios.tcsetattr(fd, termios.TCSADRAIN, _old_term_settings)
                _old_term_settings = None
    except:
        pass

def getch():
    return sys.stdin.read(1)

def hide(enabled: bool = True):
    if enabled:
        print("\033[?25l",end="")
    else:
        print("\033[?25h",end="")

atexit.register(echo, True)
atexit.register(raw, False)
atexit.register(rh)
atexit.register(cs)
atexit.register(hide,False)
