import os
import getpass
import tempfile
from pathlib import Path
import importlib.util
import importlib.metadata
import shutil
import sysconfig
from kde_material_you_colors.utils.utils import find_executable

__version__ = importlib.metadata.version("kde_material_you_colors")
USERNAME = getpass.getuser()
USER_HAS_PYWAL = importlib.util.find_spec("pywal") is not None
HOME = str(Path.home())
TEMPDIR = tempfile.gettempdir()
PKG_INSTALL_DIR = os.path.dirname(__file__)
scheme = (
    "rpm_prefix"
    if "rpm_prefix" in sysconfig.get_scheme_names()
    else sysconfig.get_default_scheme()
)
PKG_BIN = sysconfig.get_path("scripts", scheme) + "/kde-material-you-colors"
SAMPLE_CONFIG_FILE = "sample_config.conf"
CONFIG_FILE = "config.conf"
SAMPLE_CONFIG_PATH = PKG_INSTALL_DIR + "/data/"
USER_CONFIG_PATH = HOME + "/.config/kde-material-you-colors/"
USER_APPS_PATH = HOME + "/.local/share/applications/"
USER_SCHEMES_PATH = HOME + "/.local/share/color-schemes"
THEME_LIGHT_PATH = USER_SCHEMES_PATH + "/MaterialYouLight"
THEME_DARK_PATH = USER_SCHEMES_PATH + "/MaterialYouDark"
AUTOSTART_SCRIPT = "kde-material-you-colors.desktop"
STOP_SCRIPT = "kde-material-you-colors-stop.desktop"
SAMPLE_AUTOSTART_SCRIPT_PATH = PKG_INSTALL_DIR + "/data/"
USER_AUTOSTART_SCRIPT_PATH = HOME + "/.config/autostart/"
PICTURE_OF_DAY_PLUGIN = "org.kde.potd"
PLAIN_COLOR_PLUGIN = "org.kde.color"
PICTURE_OF_DAY_PLUGIN_CACHE_DIR = HOME + "/.cache/plasma_engine_potd/"
PICTURE_OF_DAY_UNSPLASH_PROVIDER = "unsplash"
PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY = "1065976"
PICTURE_OF_DAY_DEFAULT_PROVIDER = "apod"  # astronomy picture of the day
PICTURE_OF_DAY_BING_PROVIDER = "bing"
KDE_GLOBALS = HOME + "/.config/kdeglobals"
BREEZE_RC = HOME + "/.config/breezerc"
SBE_RC = HOME + "/.config/sierrabreezeenhancedrc"
KLASSY_RC = HOME + "/.config/klassy/klassyrc"
KONSOLE_DIR = HOME + "/.local/share/konsole/"
KONSOLE_COLOR_SCHEME_PATH = KONSOLE_DIR + "MaterialYou.colorscheme"
KONSOLE_COLOR_SCHEME_ALT_PATH = KONSOLE_DIR + "MaterialYouAlt.colorscheme"
KONSOLE_TEMP_PROFILE = KONSOLE_DIR + "TempMyou.profile"
KONSOLE_DEFAULT_THEMED_PROFILE = "Profile 1"
KONSOLE_RC = HOME + "/.config/konsolerc"
KSYNTAX_THEMES_DIR = HOME + "/.local/share/org.kde.syntax-highlighting/themes/"
LOG_FILE_PATH = HOME + "/.local/share/kde-material-you-colors/"
LOG_FILE_NAME = "kde-material-you-colors.log"
MATERIAL_YOU_COLORS_JSON = f"{TEMPDIR}/kde-material-you-colors-" + USERNAME + ".json"
KWIN_RULES_RC = HOME + "/.config/kwinrulesrc"
PIDFILE_PATH = f"{TEMPDIR}/kde-material-you-colors-{USERNAME}.pid"
SCREENSHOT_PATH = f"{TEMPDIR}/kde-material-you-colors-desktop-screenshot-{USERNAME}.png"
KWIN_DESKTOP_ID_JSCRIPT = (
    f"{TEMPDIR}/kde-material-you-colors-desktop-win-id-{USERNAME}.js"
)
KONSOLE_ACTIVE_PROFILE_NAME = (
    f"{TEMPDIR}/kde-material-you-colors-konsole-profile-{USERNAME}"
)
# PLASMA_WORKSPACE_ENV_FILE = "kde-material-you-colors-set-path.sh"
# PLASMA_WORKSPACE_ENV_PATH = PKG_INSTALL_DIR + "/data/"
# USER_PLASMA_WORKSPACE_ENV_PATH = HOME + "/.config/plasma-workspace/env/"
USER_LOCAL_BIN_PATH = HOME + "/.local/bin/"
IN_PATH = bool(shutil.which("kde-material-you-colors"))
CHANGE_ICONS_PROGRAM = "plasma-changeicons"
PLASMA_CHANGEICONS_PATH = find_executable(CHANGE_ICONS_PROGRAM)

SCREENSHOT_HELPER = "kde-material-you-colors-screenshot-helper"
SCREENSHOT_HELPER_PATH = find_executable(SCREENSHOT_HELPER)

TERM_COLOR_RED = "\033[31m"
TERM_COLOR_GRE = "\033[32m"
TERM_COLOR_YEL = "\033[33m"
TERM_COLOR_BLU = "\033[34m"
TERM_COLOR_MAG = "\033[35m"
TERM_COLOR_CYA = "\033[36m"
TERM_COLOR_WHI = "\033[37m"
TERM_COLOR_DEF = "\033[39m"

TERM_STY_BOLD = "\033[1m"
TERM_STY_NORMAL = "\033[22m"
TERM_STY_BOLD = "\033[1m"
TERM_STY_FAINT = "\033[2m"
TERM_STY_RESET = "\033[0m"
TERM_STY_INVERT = "\033[7m"
TERM_STY_INVERT_OFF = "\033[27m"
