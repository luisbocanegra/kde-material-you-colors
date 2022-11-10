import logging
import os
import subprocess
import globals


def run_hook(hook):
    if hook != None:
        subprocess.Popen(hook, shell=True)


def kill_existing():
    get_pids = subprocess.check_output("ps -e -f | grep [/]usr/bin/kde-material-you-colors | awk '{print $2}'",
                                       shell=True, stderr=subprocess.PIPE, universal_newlines=True).strip().splitlines()
    current_pid = os.getpid()
    for pid in get_pids:
        pid = int(pid)
        if pid != current_pid:
            logging.debug(
                f"Found existing process with PID: '{pid}' killing...")
            subprocess.Popen("kill -9 "+str(pid), shell=True)


def one_shot_actions(args):
    # User may just want to set the startup script / default config, do that only and terminate the script
    if args.autostart == True:
        if not os.path.exists(globals.USER_AUTOSTART_SCRIPT_PATH):
            os.makedirs(globals.USER_AUTOSTART_SCRIPT_PATH)
        if not os.path.exists(globals.USER_AUTOSTART_SCRIPT_PATH+globals.AUTOSTART_SCRIPT):
            try:
                subprocess.check_output("cp "+globals.SAMPLE_AUTOSTART_SCRIPT_PATH+globals.AUTOSTART_SCRIPT+" "+globals.USER_AUTOSTART_SCRIPT_PATH+globals.AUTOSTART_SCRIPT,
                                        shell=True)
                logging.info(
                    f"Autostart script copied to: {globals.USER_AUTOSTART_SCRIPT_PATH+globals.AUTOSTART_SCRIPT}")
            except Exception:
                quit(1)
        else:
            logging.error(
                f"Autostart script already exists in: {globals.USER_AUTOSTART_SCRIPT_PATH+globals.AUTOSTART_SCRIPT}")
        quit(0)
    elif args.copyconfig == True:
        if not os.path.exists(globals.USER_CONFIG_PATH):
            os.makedirs(globals.USER_CONFIG_PATH)
        if not os.path.exists(globals.USER_CONFIG_PATH+globals.CONFIG_FILE):
            try:
                subprocess.check_output("cp "+globals.SAMPLE_CONFIG_PATH+globals.SAMPLE_CONFIG_FILE+" "+globals.USER_CONFIG_PATH+globals.CONFIG_FILE,
                                        shell=True)
                logging.info(
                    f"Config copied to: {globals.USER_CONFIG_PATH+globals.CONFIG_FILE}")
            except Exception:
                quit(1)
        else:
            logging.error(
                f"Config already exists in: {globals.USER_CONFIG_PATH+globals.CONFIG_FILE}")
        quit(0)
    elif args.stop == True:
        kill_existing()
        quit(0)


class Watcher:
    """ A simple class to watch variable changes."""

    def __init__(self, value: any):
        self.value = value
        self.has_changed = False
        self.old_value = None

    def set_value(self, new_value: any) -> None:
        if self.value != new_value:
            self.old_value = self.value
            self.value = new_value
            self.has_changed = True
        else:
            self.has_changed = False

    def has_changed(self):
        return self.has_changed

    def get_old_value(self):
        return self.old_value

    def get_new_value(self):
        return self.value
