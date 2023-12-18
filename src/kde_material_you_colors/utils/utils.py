import gettext
import logging
import os
import signal
import subprocess
import argparse
import sys
import re
import shutil
import configparser
from .. import settings


def run_hook(hook):
    if hook is not None:
        subprocess.Popen(hook, shell=True)


def kill_existing():
    if os.path.exists(settings.PIDFILE_PATH):
        prev_pid = ""
        with open(settings.PIDFILE_PATH, "r", encoding="utf-8") as pidfile:
            prev_pid = pidfile.readline()

        current_pid = str(os.getpid())
        if prev_pid != current_pid:
            logging.debug(
                f"Found previous process in PID file: '{prev_pid}' killing..."
            )
            try:
                os.kill(int(prev_pid), signal.SIGKILL)
            except ProcessLookupError:
                logging.debug("Process not found, probably ended by someone else")


def copy_user_files(dests):
    for dest in dests:
        if not os.path.exists(dest["dest"]):
            os.makedirs(dest["dest"])

        if not os.path.exists(dest["dest"] + dest["file_dest"]):
            try:
                shutil.copy(
                    dest["origin"] + dest["file"],
                    dest["dest"] + dest["file_dest"],
                )
                logging.info(
                    f'Copied {dest["file"]} -> {dest["dest"] + dest["file_dest"]}'
                )
            except shutil.Error as err:
                logging.error(f"Error: {err}")
                sys.exit(1)
        else:
            logging.warning(
                f'File {dest["file"]} already exists in: {dest["dest"]+dest["file_dest"]}'
            )


def update_desktop_entry():
    if not settings.IN_PATH:
        entries = [
            {
                "dest": settings.USER_APPS_PATH + settings.AUTOSTART_SCRIPT,
                "cmd": settings.PKG_BIN,
            },
            {
                "dest": settings.USER_APPS_PATH + settings.STOP_SCRIPT,
                "cmd": settings.PKG_BIN + " --stop",
            },
            {
                "dest": settings.USER_AUTOSTART_SCRIPT_PATH + settings.AUTOSTART_SCRIPT,
                "cmd": settings.PKG_BIN,
            },
        ]
        for entry in entries:
            if os.path.exists(entry["dest"]):
                logging.debug(f'Updating Exec {entry["dest"]}')
                config = configparser.ConfigParser()
                config.optionxform = str
                config.read(entry["dest"])
                config.set("Desktop Entry", "Exec", entry["cmd"])
                with open(entry["dest"], "w", encoding="utf-8") as f:
                    config.write(f, space_around_delimiters=False)
        # create symbolic link to user PATH

        if not os.path.exists(settings.USER_LOCAL_BIN_PATH):
            os.makedirs(settings.USER_LOCAL_BIN_PATH)
        link_path = settings.USER_LOCAL_BIN_PATH + "kde-material-you-colors"
        if os.path.islink(link_path):
            os.unlink(link_path)
            logging.debug(f"Updating link {settings.PKG_BIN} -> {link_path}")
        else:
            logging.debug(f"Creating link {settings.PKG_BIN} -> {link_path}")
        os.symlink(
            settings.PKG_BIN,
            link_path,
        )


def one_shot_actions(args):
    if args.autostart is True:
        # Autostart desktop entries
        dests = [
            {
                "origin": settings.SAMPLE_AUTOSTART_SCRIPT_PATH,
                "dest": settings.USER_AUTOSTART_SCRIPT_PATH,
                "file": settings.AUTOSTART_SCRIPT,
                "file_dest": settings.AUTOSTART_SCRIPT,
            },
        ]
        copy_user_files(dests)
        update_desktop_entry()

        sys.exit(0)

    if args.copylauncher is True:
        # Start/Stop Desktop entries
        dests = [
            {
                "origin": settings.SAMPLE_AUTOSTART_SCRIPT_PATH,
                "dest": settings.USER_APPS_PATH,
                "file": settings.AUTOSTART_SCRIPT,
                "file_dest": settings.AUTOSTART_SCRIPT,
            },
            {
                "origin": settings.SAMPLE_AUTOSTART_SCRIPT_PATH,
                "dest": settings.USER_APPS_PATH,
                "file": settings.STOP_SCRIPT,
                "file_dest": settings.STOP_SCRIPT,
            },
        ]
        copy_user_files(dests)
        update_desktop_entry()
        sys.exit(0)

    elif args.copyconfig is True:
        dests = [
            {
                "origin": settings.SAMPLE_CONFIG_PATH,
                "dest": settings.USER_CONFIG_PATH,
                "file": settings.SAMPLE_CONFIG_FILE,
                "file_dest": settings.CONFIG_FILE,
            },
        ]

        copy_user_files(dests)
        sys.exit(0)

    elif args.stop is True:
        kill_existing()
        sys.exit(0)

    elif args.version:
        print(settings.__version__)
        sys.exit(0)


class Watcher:
    """A simple class to watch variable changes."""

    def __init__(self, value):
        if isinstance(value, dict):
            self.value = value.copy()
        else:
            self.value = value
        self.changed = False
        self.old_value = value

    def set_value(self, new_value):
        if isinstance(new_value, dict):
            if self.value is None or new_value != self.value:
                # handle the case where self.value is None
                self.old_value = None if self.value is None else self.value.copy()
                self.value = new_value.copy()
                self.changed = True
            else:
                self.changed = False
        else:
            if self.value != new_value:
                self.old_value = self.value
                self.value = new_value
                self.changed = True
            else:
                self.changed = False

    def has_changed(self):
        return self.changed

    def get_old_value(self, prop_name=None):
        if self.old_value is None:
            raise ValueError("No previous value has been set.")
        if prop_name is not None:
            try:
                return self.old_value[prop_name]
            except TypeError as e:
                raise ValueError("The old value is not a subscriptable object.") from e
            except KeyError as e:
                raise ValueError(
                    f"prop_name '{prop_name}' does not exist in the old value."
                ) from e
        return self.old_value

    def get_new_value(self, prop_name=None):
        if self.value is None:
            raise ValueError("No previous value has been set.")
        if prop_name is not None:
            try:
                return self.value[prop_name]
            except TypeError as e:
                raise ValueError("The old value is not a subscriptable object.") from e
            except KeyError as e:
                raise ValueError(
                    f"prop_name '{prop_name}' does not exist in the old value."
                ) from e
        return self.value


def startup_delay(use_startup_delay, delay_conf):
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
            r"([\s-]-{1,2}[a-zA-Z-]+)",
            r"(?<=\[)(-{1,2}[a-zA-Z]+)",
            r"([a-zA-Z]+_[a-zA-Z]+)",
        ]
        line = re.sub(
            "|".join(match_opts),
            rf"{settings.TERM_COLOR_BLU}{settings.TERM_STY_BOLD}\1\2\3{settings.TERM_STY_RESET}",
            line,
        )

        # color argument <meta> values
        match_args = [r"(\<(.*?)\>)"]
        line = re.sub(
            "|".join(match_args),
            rf"{settings.TERM_COLOR_YEL}\1{settings.TERM_STY_RESET}",
            line,
        )

        # color sections usage: , options:\n
        match_sect = [
            r"((\)|^)([a-zA-Z]+):($|)(?!/))",
        ]
        line = re.sub(
            "|".join(match_sect),
            rf"{settings.TERM_COLOR_MAG}{settings.TERM_STY_BOLD}{settings.TERM_STY_INVERT}\1{settings.TERM_STY_RESET}",
            line,
        )

        # programs, commands
        progname = sys.argv[0].split(" ")[0].split("/")[-1]
        match_progname = [
            "(" + progname + ")",
            "( konsole)",
            r"([\s](.*)[a-zA-Z]-[\s][a-zA-Z](.+?)[\s])",
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
        match_progname = ["(ERROR:)"]
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
    formatted_text += settings.TERM_STY_RESET
    return formatted_text


def find_executable(name: str):
    """Find executable path using util-linux `whereis`

    Args:
        name (str): Executable name to find

    Returns:
        (str|None): Executable path or None if wasn't found
    """
    out = (
        subprocess.check_output(
            "whereis " + name,
            shell=True,
            universal_newlines=True,
        )
        .strip()
        .split()
    )

    return None if len(out) == 1 else out[1]
