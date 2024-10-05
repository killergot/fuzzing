from sys import exit

from winappdbg import Debug

def simple_debugger(argv,interactive_swith): 
    debug = Debug()
    try:
        debug.execv(argv)
        if interactive_swith == 1:
            debug.interactive()
        else:
            debug.loop()
    finally:
        debug.stop()
    return