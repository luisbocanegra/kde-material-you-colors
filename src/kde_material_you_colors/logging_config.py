from logging.handlers import RotatingFileHandler
import logging
import sys
import os
import re
from . import settings

# Set logging level for pillow
logging.getLogger("PIL").setLevel(logging.WARNING)

# Custom logging format (adapted from https://stackoverflow.com/a/14859558)


class MyLogFormatter(logging.Formatter):
    term_fmt = "{}[%(levelname).1s]{} %(module)s: %(funcName)s: {}%(message)s{}"
    file_fmt = "%(asctime)s.%(msecs)03d [%(levelname).1s] %(module)s: %(funcName)s: %(message)s"
    normal = settings.TERM_STY_NORMAL
    invert = settings.TERM_STY_NORMAL + settings.TERM_STY_INVERT
    bold_white = (
        settings.TERM_STY_INVERT_OFF + settings.TERM_STY_BOLD + settings.TERM_COLOR_WHI
    )
    dbg_fmt = term_fmt.format(
        settings.TERM_COLOR_BLU + invert,
        bold_white,
        normal + settings.TERM_COLOR_BLU,
        settings.TERM_STY_RESET,
    )

    info_fmt = term_fmt.format(
        settings.TERM_COLOR_GRE + invert,
        bold_white,
        normal + settings.TERM_COLOR_GRE,
        settings.TERM_STY_RESET,
    )

    warn_fmt = term_fmt.format(
        settings.TERM_COLOR_YEL + invert,
        bold_white,
        normal + settings.TERM_COLOR_YEL,
        settings.TERM_STY_RESET,
    )

    err_fmt = term_fmt.format(
        settings.TERM_COLOR_RED + invert,
        bold_white,
        normal + settings.TERM_COLOR_RED,
        settings.TERM_STY_RESET,
    )

    def __init__(self, to_file):
        self.to_file = to_file
        super().__init__(
            fmt="%(levelno)d: %(msg)s", datefmt="%Y-%m-%d %H:%M:%S", style="%"
        )

    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if self.to_file is False:
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
        # Remove escape codes if saving to log file
        if self.to_file:
            pattern1 = r"\033\[.*?;1m"
            pattern2 = r"\033\[0m"
            result = re.sub(pattern1, "", result)
            result = re.sub(pattern2, "", result)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result

    @staticmethod
    def set_format():
        # Format for terminal
        term_fmt = MyLogFormatter(to_file=False)
        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.setFormatter(term_fmt)

        # make sure that the folder for log exists
        if not os.path.exists(settings.LOG_FILE_PATH):
            os.makedirs(settings.LOG_FILE_PATH)

        # Format for log file
        file_fmt = MyLogFormatter(to_file=True)
        fh = RotatingFileHandler(
            settings.LOG_FILE_PATH + settings.LOG_FILE_NAME,
            mode="a",
            maxBytes=1 * 1024 * 1024,
            backupCount=1,
            encoding=None,
            delay=False,
        )
        fh.setFormatter(file_fmt)
        logging.root.addHandler(hdlr)
        logging.root.addHandler(fh)
        logging.root.setLevel(logging.DEBUG)
