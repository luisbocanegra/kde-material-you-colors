import gettext
import logging
import os
import subprocess
from .. import settings
import argparse
import sys
import re


def run_hook(hook):
    if hook != None:
        subprocess.Popen(hook, shell=True)


def kill_existing():
    get_pids = (
        subprocess.check_output(
            "ps -e -f | grep [/]usr/bin/kde-material-you-colors | awk '{print $2}'",
            shell=True,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        .strip()
        .splitlines()
    )
    current_pid = os.getpid()
    for pid in get_pids:
        pid = int(pid)
        if pid != current_pid:
            logging.debug(f"Found existing process with PID: '{pid}' killing...")
            subprocess.Popen("kill -9 " + str(pid), shell=True)


def one_shot_actions(args):
    # User may just want to set the startup script / default config, do that only and terminate the script
    if args.autostart == True:
        if not os.path.exists(settings.USER_AUTOSTART_SCRIPT_PATH):
            os.makedirs(settings.USER_AUTOSTART_SCRIPT_PATH)
        if not os.path.exists(
            settings.USER_AUTOSTART_SCRIPT_PATH + settings.AUTOSTART_SCRIPT
        ):
            try:
                subprocess.check_output(
                    "cp "
                    + settings.SAMPLE_AUTOSTART_SCRIPT_PATH
                    + settings.AUTOSTART_SCRIPT
                    + " "
                    + settings.USER_AUTOSTART_SCRIPT_PATH
                    + settings.AUTOSTART_SCRIPT,
                    shell=True,
                )
                logging.info(
                    f"Autostart script copied to: {settings.USER_AUTOSTART_SCRIPT_PATH+settings.AUTOSTART_SCRIPT}"
                )
            except Exception:
                quit(1)
        else:
            logging.error(
                f"Autostart script already exists in: {settings.USER_AUTOSTART_SCRIPT_PATH+settings.AUTOSTART_SCRIPT}"
            )
        quit(0)
    elif args.copyconfig == True:
        if not os.path.exists(settings.USER_CONFIG_PATH):
            os.makedirs(settings.USER_CONFIG_PATH)
        if not os.path.exists(settings.USER_CONFIG_PATH + settings.CONFIG_FILE):
            try:
                subprocess.check_output(
                    "cp "
                    + settings.SAMPLE_CONFIG_PATH
                    + settings.SAMPLE_CONFIG_FILE
                    + " "
                    + settings.USER_CONFIG_PATH
                    + settings.CONFIG_FILE,
                    shell=True,
                )
                logging.info(
                    f"Config copied to: {settings.USER_CONFIG_PATH+settings.CONFIG_FILE}"
                )
            except Exception:
                quit(1)
        else:
            logging.error(
                f"Config already exists in: {settings.USER_CONFIG_PATH+settings.CONFIG_FILE}"
            )
        quit(0)
    elif args.stop == True:
        kill_existing()
        quit(0)


class Watcher:
    """A simple class to watch variable changes."""

    def __init__(self, value: any):
        self.value = value
        self.changed = False
        self.old_value = None

    def set_value(self, new_value: any) -> None:
        if self.value != new_value:
            self.old_value = self.value
            self.value = new_value
            self.changed = True
        else:
            self.changed = False

    def has_changed(self):
        return self.changed

    def get_old_value(self):
        return self.old_value

    def get_new_value(self):
        return self.value


def startup_delay(use_startup_delay, delay_conf):
    # print(f'use delay:{use_startup_delay}, delay: {delay_conf}')
    if use_startup_delay:
        return delay_conf
    else:
        return 0


class ColoredArgParser(argparse.ArgumentParser):
    """Colored help message for ArgumentParser

    Args:
        argparse (argparse.ArgumentParser): argparse.ArgumentParser
    """

    def _print_message(self, message, file=None):
        if message and message:
            if file is None:
                file = sys.stderr
            else:
                file.write(color_text(message))

    def error(self, message):
        self.print_usage(sys.stderr)
        args = {"prog": self.prog, "message": message}
        self.exit(2, gettext.gettext("%(prog)s: ERROR: %(message)s\n") % args)


def wide_argparse_help(formatter, help_column: int = 30, min_width: int = 100):
    """Return a wider HelpFormatter, if possible.
    Removing help spacing if window is not wide enough.
    Args:
        formatter (argparse.HelpFormatter): Formatter
        help_column (int, optional): Column at which help(right) text starts. Defaults to 30.
        min_width (int optional): Minimun terminal width to remove help padding. Defaults to 100.

    Returns:
        _type_: _description_
    """

    try:
        # https://stackoverflow.com/a/5464440
        # beware: "Only the name of this class is considered a public API."

        # try to get terminal width from interactive shells
        columns = None
        try:
            columns = int(os.popen("stty size", "r").read().split()[1])
            if columns < min_width:
                help_column = 4
        except Exception:
            pass

        kwargs = {"width": columns, "max_help_position": help_column}
        formatter(None, **kwargs)
        return lambda prog: formatter(prog, **kwargs)
    except Exception as e:
        logging.error(f"Warning: Argparse help formatter failed, falling back.{e}")
        return formatter


def color_text(message: str):
    """Color text with regex rules

    Args:
        message (str): text

    Returns:
        str: Colored text
    """
    # # find epilog
    # match_epilog = '((For|Autom)(.*[\s\S][a-zA-Z](.*)[\s\S](.*)){0,6})'
    # re_epilog = re.findall(match_epilog, message)
    # # color them
    # for txt in re_epilog:
    #     # print(txt)
    #     t = txt[0]
    #     message = message.replace(
    #         t.strip(), f'{settings.TERM_COLOR_WHI}{t}{settings.TERM_STY_RESET}')

    # search and color other patterns, line by line
    formatted_text = ""
    for i, line in enumerate(message.splitlines()):
        # find options (--op, -o), config_names
        match_opts = [
            "([\s-]-{1,2}[a-zA-Z-]+)",
            "(?<=\[)(-{1,2}[a-zA-Z]+)",
            "([a-zA-Z]+_[a-zA-Z]+)",
        ]
        line = re.sub(
            "|".join(match_opts),
            rf"{settings.TERM_COLOR_BLU}{settings.TERM_STY_BOLD}\1\2\3{settings.TERM_STY_RESET}",
            line,
        )

        # color argument <meta> values
        match_args = ["(\<(.*?)\>)"]
        line = re.sub(
            "|".join(match_args),
            rf"{settings.TERM_COLOR_YEL}\1{settings.TERM_STY_RESET}",
            line,
        )

        # color sections usage: , options:\n
        match_sect = [
            "((\)|^)([a-zA-Z]+):($|)(?!/))",
        ]
        line = re.sub(
            "|".join(match_sect),
            rf"{settings.TERM_COLOR_MAG}{settings.TERM_STY_BOLD}{settings.TERM_STY_INVERT}\1{settings.TERM_STY_RESET}",
            line,
        )

        # programs, commands
        progname = sys.argv[0].split(" ")[0].split("/")[-1]
        match_progname = [
            f"(" + progname + ")",
            "( konsole)",
            "([\s](.*)[a-zA-Z]-[\s][a-zA-Z](.+?)[\s])",
        ]
        line = re.sub(
            "|".join(match_progname),
            rf"{settings.TERM_COLOR_GRE}{settings.TERM_STY_BOLD}\1\2\3{settings.TERM_STY_RESET}",
            line,
        )

        # uppercase strings
        uppercase_words = ["usage:", "options:"]
        for w in uppercase_words:
            line = line.replace(w, w.upper())

        # Error red
        match_progname = [f"(ERROR:)"]
        line = re.sub(
            "|".join(match_progname),
            rf"{settings.TERM_COLOR_RED}{settings.TERM_STY_BOLD}{settings.TERM_STY_INVERT}\1{settings.TERM_STY_RESET}",
            line,
        )

        # capitalize strings
        cap_words = ["show"]
        for w in cap_words:
            line = line.replace(w, w.capitalize())

        formatted_text += line + "\n"
    formatted_text + settings.TERM_STY_RESET
    return formatted_text
