import os
import math
import sys
if sys.platform != "win32":
    import termios
    import tty
else:
    import msvcrt
    import ctypes
import atexit

_old_term_settings = None

if sys.platform != "win32":
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
else:
    kernel32 = ctypes.windll.kernel32
    hStdin = kernel32.GetStdHandle(-10)

    def echo(enable: bool = False):
        try:
            mode = ctypes.c_uint()
            kernel32.GetConsoleMode(hStdin, ctypes.byref(mode))
            if enable:
                mode.value |= 0x0004
            else:
                mode.value &= ~0x0004
            kernel32.SetConsoleMode(hStdin, mode)
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

if sys.platform != "win32":
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
else:
    STD_INPUT_HANDLE = -10
    ENABLE_ECHO_INPUT = 0x0004
    ENABLE_LINE_INPUT = 0x0002

    _hStdin = kernel32.GetStdHandle(STD_INPUT_HANDLE)

    def raw(enabled: bool = True):
        global _old_term_settings
        try:
            mode = ctypes.c_uint()
            kernel32.GetConsoleMode(_hStdin, ctypes.byref(mode))
            if enabled:
                if _old_term_settings is None:
                    _old_term_settings = mode.value
                new_mode = mode.value & ~(ENABLE_ECHO_INPUT | ENABLE_LINE_INPUT)
                kernel32.SetConsoleMode(_hStdin, new_mode)
            else:
                if _old_term_settings is not None:
                    kernel32.SetConsoleMode(_hStdin, _old_term_settings)
                    _old_term_settings = None
        except:
            pass


if sys.platform == "win32":
    import msvcrt
    def getch():
        ch = msvcrt.getch()
        if isinstance(ch, bytes):
            ch = ch.decode(errors="ignore")
        if ch == "\r":
            return "\n"
        return ch
else:
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
