#!/usr/bin/python3
import os
import time
import argparse
import logging
from . import settings
from .utils import utils
from .logging_config import MyLogFormatter


logger = MyLogFormatter.set_format()


def main():
    parser = utils.ColoredArgParser(
        description="Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop and more, powered by python-material-color-utilities with pywal support. Any argument passed here overrides their counterpart in the configuration file (if any).",
        epilog="For more information, issues, feature requests and updates check the project page https://github.com/luisbocanegra/kde-material-you-colors",
        formatter_class=utils.wide_argparse_help(
            argparse.HelpFormatter, help_column=50, min_width=120
        ),
    )

    parser.add_argument(
        "--monitor",
        "-m",
        type=int,
        help="Monitor to get wallpaper (default is 0) but second one is 6 in my case, play with this to find yours",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--color",
        "-col",
        type=str,
        help="Custom color (hex or rgb) used to generate M3 color scheme Takes precedence over automatic wallpaper detection",
        default=None,
        metavar="<color>",
    )

    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Text file that contains wallpaper absolute path (Takes precedence over automatic wallpaper detection and --color options)",
        default=None,
        metavar="<filename>",
    )

    parser.add_argument(
        "--ncolor",
        "-n",
        type=int,
        help="Alternative color mode (default is 0), some images return more than one color, this will use either the matched or last one",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--custom-colors-list",
        "-ccl",
        type=str,
        help="List of 7 space separated colors (hex or rgb) to be used for text in pywal/konsole/KSyntaxHighlighting instead of wallpaper ones",
        default=None,
        metavar="<colors>",
    )

    parser.add_argument(
        "--light", "-l", action="store_true", help="Enable Light mode", default=None
    )

    parser.add_argument(
        "--dark", "-d", action="store_true", help="Enable Dark mode", default=None
    )

    parser.add_argument(
        "--autostart",
        "-a",
        action="store_true",
        help="Enable (copy) the startup script to automatically start with KDE",
    )

    parser.add_argument(
        "--copyconfig",
        "-c",
        action="store_true",
        help="Copies the default config to ~/.config/kde-material-you-colors/config.conf",
    )

    parser.add_argument(
        "--copylauncher",
        "-cl",
        action="store_true",
        help="Copies desktop entries to ~/.local/share/applications/. Use only if they were not installed by a package manager",
    )

    parser.add_argument(
        "--iconslight",
        type=str,
        help="Icons theme for Dark scheme",
        default=None,
        metavar="<icon-theme-name>",
    )

    parser.add_argument(
        "--iconsdark",
        type=str,
        help="Icons theme for Light scheme",
        default=None,
        metavar="<icon-theme-name>",
    )

    parser.add_argument(
        "--pywal",
        "-wal",
        action="store_true",
        help="Use pywal to theme other apps with Material You",
        default=None,
    )

    parser.add_argument(
        "--pywallight",
        "-wall",
        action="store_true",
        help="Use Light mode for pywal controlled apps",
        default=None,
    )

    parser.add_argument(
        "--pywaldark",
        "-wald",
        action="store_true",
        help="Use Dark mode for pywal controlled apps",
        default=None,
    )

    parser.add_argument(
        "--lbmultiplier",
        "-lbm",
        type=float,
        help="The amount of color for backgrounds in Light mode (value from 0 to 4.0, default is 1)",
        default=None,
        metavar="<float>",
    )

    parser.add_argument(
        "--dbmultiplier",
        "-dbm",
        type=float,
        help="The amount of color for backgrounds in Dark mode (value from 0 to 4.0, default is 1)",
        default=None,
        metavar="<float>",
    )

    parser.add_argument(
        "--on-change-hook",
        type=str,
        help="A script/command that will be executed on start or wallpaper/dark/light/settings change (absolute path)",
        default=None,
        metavar="<script or command>",
    )

    parser.add_argument(
        "--sierra-breeze-buttons-color",
        "-sbb",
        action="store_true",
        help="Tint Sierra Breeze decoration buttons",
        default=None,
    )

    parser.add_argument(
        "--disable-konsole",
        "-dk",
        action="store_true",
        help="Disable Konsole automatic theming (color schemes are still generated)",
        default=None,
    )

    parser.add_argument(
        "--titlebar-opacity",
        "-tio",
        type=int,
        help="Titlebar opacity in normal mode (value from 0 to 100, default is 100)",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--titlebar-opacity-dark",
        "-tiod",
        type=int,
        help="Titlebar opacity in dark mode (value from 0 to 100, default is 100)",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--toolbar-opacity",
        "-too",
        type=int,
        help="ToolBar opacity in normal mode, needs Lightly Application Style (value from 0 to 100, default is 100)",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--toolbar-opacity-dark",
        "-tood",
        type=int,
        help="ToolBar opacity in dark mode, needs Lightly Application Style (value from 0 to 100, default is 100)",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--konsole-opacity",
        "-ko",
        type=int,
        help="Konsole background opacity in normal mode (value from 0 to 100, default is 100)",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--konsole-opacity-dark",
        "-kod",
        type=int,
        help="Konsole background opacity in dark mode (value from 0 to 100, default is 100)",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--stop",
        action="store_true",
        help="Kill an existing instance of kde-material-you-colors and exit",
    )

    parser.add_argument(
        "--klassy-windeco-outline",
        "-kwo",
        action="store_true",
        help="Tint Klassy Window Decoration window outline",
        default=None,
    )

    parser.add_argument(
        "--darker-window-list",
        "-dwl",
        type=str,
        help="List of space separated window class names to apply a darker titlebar to, useful for terminal or code editors and other programs themed by pywal (will create a window rule)",
        default=None,
        metavar="<names>",
    )

    parser.add_argument(
        "--use-startup-delay",
        action="store_true",
        help="Enable the startup delay, disabled by default, requires --startup-delay option",
        default=None,
    )

    parser.add_argument(
        "--startup-delay",
        "-sd",
        type=int,
        help="Add a startup delay (in seconds) before doing anything, useful for waiting for other utilities that may change themes on boot (default is 0), requires --use-startup-delay option",
        default=None,
        metavar="<integer>",
    )

    parser.add_argument(
        "--main-loop-delay",
        "-mld",
        type=float,
        help="Main loop delay (in seconds), useful for decreasing unnecessary detections or save a bit of power (default is 1)",
        default=None,
        metavar="<float>",
    )

    parser.add_argument(
        "--screenshot-delay",
        "-scd",
        type=float,
        help="Delay after taking screenshot (in seconds), useful for live wallpapers that display a constant transition based on time or other circumstances, which would trigger colors generation too often (default is 900 seconds which is 15 minutes), must be bigger than --main-loop-delay",
        default=None,
        metavar="<float>",
    )

    parser.add_argument(
        "--once-after-change",
        "-ofc",
        action="store_true",
        help="Apply colors from screenshot only after wallpaper plugin changes, useful for animated looped wallpapers that would trigger color generation indefinitely but unnecessarily",
        default=None,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Print version information",
    )

    # Get commandline arguments
    args = parser.parse_args()
    # Check for one shot arguments
    utils.one_shot_actions(args)
    # Kill existing instance if found
    utils.kill_existing()

    # Make oneshot actions take less cpu
    # pylint: disable=import-outside-toplevel
    from .config import Configs
    from .utils import wallpaper_utils
    from .utils import file_utils
    from .utils import notify
    from .utils import plasma_utils
    from . import apply_themes

    logging.info("###### STARTED NEW SESSION ######")
    logging.debug(f"Installed in {settings.PKG_INSTALL_DIR}")

    with open(settings.PIDFILE_PATH, "w", encoding="utf-8") as pidfile:
        pidfile.write(str(os.getpid()))
        pidfile.close()

    config = Configs(args, settings.USER_CONFIG_PATH + settings.CONFIG_FILE)

    # startup delay
    time.sleep(
        utils.startup_delay(
            config.options["use_startup_delay"], config.options["startup_delay"]
        )
    )

    # set initial state so first apply is done
    config_file = settings.USER_CONFIG_PATH + settings.CONFIG_FILE
    first_run = True
    apply = False
    stop_apply = False
    config_watcher = utils.Watcher(config.options)
    wallpaper_watcher = utils.Watcher(None)
    light_mode_watcher = utils.Watcher(None)
    config_modified = utils.Watcher(file_utils.get_file_sha1(config_file))
    wallpaper = wallpaper_utils.WallpaperReader(config)
    wallpaper_modified = utils.Watcher(file_utils.get_file_sha1(wallpaper.source))
    plugin_watcher = utils.Watcher(wallpaper.plugin)
    source_watcher = utils.Watcher(wallpaper.source)
    pause_watcher = utils.Watcher(config.read("pause_mode"))
    if pause_watcher.value:
        msg = "Pause mode enabled" if pause_watcher.value else "Pause mode disabled"
        logging.warning(msg)
    if wallpaper.type == "screenshot":
        head = "Screenshot mode enabled"
        cont = f"Waiting {config.read('screenshot_delay')}s between updates"
        notify.send_notification(head, cont)
        logging.warning("%s, %s", head, cont)
    if wallpaper.error:
        notify.send_notification("Could not get wallpaper", str(wallpaper.error))
        logging.error(f"Could not get wallpaper {str(wallpaper.error)}")

    counter = 0

    logging.debug(config.options)

    while True:
        config_modified.set_value(file_utils.get_file_sha1(config_file))

        # Get config from file and compare it with passed args
        if config_modified.changed:
            config.update_config()
            logging.debug(config.options)
        pause_watcher.set_value(config.read("pause_mode"))

        # Get current options, pass to watcher
        config_watcher.set_value(config.options)

        if pause_watcher.has_changed():
            msg = "Pause mode enabled" if pause_watcher.value else "Pause mode disabled"
            logging.warning(msg)

        if config.read("pause_mode"):
            time.sleep(1)
            # toggle first run if we sarted paused so it doesnt apply twice
            first_run = False if first_run else True
            continue

        #
        #
        #
        #
        # update wallpaper
        wallpaper.update(config)
        wallpaper_watcher.set_value(wallpaper.current)

        target_cycles = config.read("screenshot_delay") / (
            config.read("main_loop_delay") or 1
        )

        # Monitor file for changes (image and screenshot only)
        if wallpaper.is_image() or wallpaper.is_screenshot():
            wallpaper_modified.set_value(file_utils.get_file_sha1(wallpaper.source))

        # Update plugin name
        if wallpaper.plugin is not None:
            plugin_watcher.set_value(wallpaper.plugin)

        # Update source name (colors source)
        if wallpaper.source is not None:
            source_watcher.set_value(wallpaper.source)

        # Update light mode
        light_mode_watcher = plasma_utils.update_light_mode(
            config, light_mode_watcher, first_run
        )

        group1 = (
            plugin_watcher.changed
            or source_watcher.changed
            or wallpaper_modified.changed
        )

        # stop applying theme until plugin changes (for screenshot)
        if wallpaper.is_screenshot():
            stop_apply = config.read("once_after_change")

        if apply and wallpaper.source and stop_apply is False or first_run:
            if counter == 0:
                logging.info(f"{wallpaper}")
                apply_themes.apply(config, wallpaper, light_mode_watcher.value)
                apply = False

        if group1:
            if wallpaper.error:
                notify.send_notification(
                    "Could not get wallpaper", str(wallpaper.error)
                )
                logging.error(f"Could not get wallpaper {str(wallpaper.error)}")
            if plugin_watcher.changed and wallpaper.type == "screenshot":
                head = "Screenshot mode enabled"
                cont = f"Waiting {config.read('screenshot_delay')}s between updates"
                notify.send_notification(head, cont)
                logging.warning("%s, %s", head, cont)
            if wallpaper.source:
                apply = True

        if plugin_watcher.changed or config_watcher.changed:
            apply = False
            stop_apply = False
            logging.info(f"{wallpaper}")
            apply_themes.apply(config, wallpaper, light_mode_watcher.value)
            counter = 0

        if wallpaper.is_screenshot():
            if target_cycles > counter:
                counter += 1
            else:
                counter = 0

        # print("counter:", counter)

        time.sleep(config.read("main_loop_delay"))
        first_run = False


main()
