from logging.handlers import RotatingFileHandler
import logging
import sys
import os
import globals

# Set logging level for pillow
logging.getLogger('PIL').setLevel(logging.WARNING)

# Custom logging format (adapted from https://stackoverflow.com/a/14859558)


class MyLogFormatter(logging.Formatter):

    term_fmt = '{}[%(levelname).1s]{} %(module)s: %(funcName)s: {}%(message)s'
    file_fmt = '%(asctime)s.%(msecs)03d [%(levelname).1s] %(module)s: %(funcName)s: %(message)s'
    dbg_fmt = term_fmt.format(
        globals.TERM_COLOR_BLU+globals.TERM_STY_NORMAL+globals.TERM_STY_INVERT,
        globals.TERM_STY_INVERT_OFF+globals.TERM_STY_BOLD+globals.TERM_COLOR_WHI,
        globals.TERM_STY_NORMAL+globals.TERM_COLOR_BLU)

    info_fmt = term_fmt.format(
        globals.TERM_COLOR_GRE+globals.TERM_STY_NORMAL+globals.TERM_STY_INVERT,
        globals.TERM_STY_INVERT_OFF+globals.TERM_STY_BOLD+globals.TERM_COLOR_WHI,
        globals.TERM_STY_NORMAL + globals.TERM_COLOR_GRE)

    warn_fmt = term_fmt.format(
        globals.TERM_COLOR_YEL+globals.TERM_STY_NORMAL+globals.TERM_STY_INVERT,
        globals.TERM_STY_INVERT_OFF+globals.TERM_STY_BOLD+globals.TERM_COLOR_WHI,
        globals.TERM_STY_NORMAL + globals.TERM_COLOR_YEL)

    err_fmt = term_fmt.format(
        globals.TERM_COLOR_RED+globals.TERM_STY_NORMAL+globals.TERM_STY_INVERT,
        globals.TERM_STY_INVERT_OFF+globals.TERM_STY_BOLD+globals.TERM_COLOR_WHI,
        globals.TERM_STY_NORMAL + globals.TERM_COLOR_RED)

    def __init__(self, to_file):
        self.to_file = to_file
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt="%Y-%m-%d %H:%M:%S", style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if self.to_file == False:
            if record.levelno == logging.DEBUG:
                self._style._fmt = MyLogFormatter.dbg_fmt

            elif record.levelno == logging.INFO:
                self._style._fmt = MyLogFormatter.info_fmt

            elif record.levelno == logging.WARNING:
                self._style._fmt = MyLogFormatter.warn_fmt

            elif record.levelno == logging.ERROR:
                self._style._fmt = MyLogFormatter.err_fmt
        else:
            self._style._fmt = MyLogFormatter.file_fmt
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result

    def set_format():
        # Format for terminal
        term_fmt = MyLogFormatter(to_file=False)
        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.setFormatter(term_fmt)

        # make sure that the folder for log exists
        if not os.path.exists(globals.LOG_FILE_PATH):
            os.makedirs(globals.LOG_FILE_PATH)

        # Format for log file
        file_fmt = MyLogFormatter(to_file=True)
        fh = RotatingFileHandler(
            globals.LOG_FILE_PATH+globals.LOG_FILE_NAME,
            mode='a',
            maxBytes=1*1024*1024,
            backupCount=1,
            encoding=None,
            delay=0)
        fh.setFormatter(file_fmt)
        logging.root.addHandler(hdlr)
        logging.root.addHandler(fh)
        logging.root.setLevel(logging.DEBUG)
