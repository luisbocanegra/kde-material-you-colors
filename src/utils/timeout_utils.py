import logging
import sys
import signal

# Current function name from https://stackoverflow.com/a/31615605
# for current func name, specify 0 or no argument.
# for name of caller of current func, specify 1.
# for name of caller of caller of current func, specify 2. etc.


def currentFuncName(n=0):
    return sys._getframe(n + 1).f_code.co_name


def timeout_handler(signum, frame):  # Register a timeout handler
    logging.error(
        f"{currentFuncName(1)}: took too much time, aborted, reboot if the problem persists"
    )
    raise TimeoutError


def timeout_set(time_s=3):
    # Register the signal handler
    signal.signal(signal.SIGALRM, timeout_handler)
    # Define a timeout for the function
    signal.alarm(time_s)


def timeout_reset():
    signal.alarm(0)
