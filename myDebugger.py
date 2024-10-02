from sys import exit

from winappdbg import Debug

def simple_debugger(argv): 
    debug = Debug()
    try:
        debug.execv(argv)
        debug.interactive()
    finally:
        debug.stop()
    return



