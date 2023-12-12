import logging
from .color_utils import hex2rgb
from .. import settings
from ..schemeconfigs import ThemeConfig

if settings.USER_HAS_PYWAL:
    import pywal
    from . import pywal_sequences_timeout
if settings.USER_HAS_COLR:
    import colr


def apply_schemes(
    light=None,
    pywal_light=None,
    use_pywal=None,
    schemes: ThemeConfig = None,
    dark_light=None,
):
    if pywal_light is not None:
        mode = pywal_light
    elif light is not None:
        mode = light
    else:
        mode = dark_light

    pywal_colors = (
        schemes.get_wal_light_scheme() if mode else schemes.get_wal_dark_scheme()
    )

    if use_pywal:
        if settings.USER_HAS_PYWAL:
            logging.info("Setting pywal colors...")
            # On very rare occassions pywal will hang, add a timeout to it
            try:
                # Apply the palette to all open terminals.
                # Second argument is a boolean for VTE terminals.
                # Set it to true if the terminal you're using is
                # VTE based. (xfce4-terminal, termite, gnome-terminal.)
                pywal_sequences_timeout.send(pywal_colors, vte_fix=False)
                # Export all template files.
                pywal.export.every(pywal_colors)
                # Reload xrdb, i3 and polybar.
                pywal.reload.env()
            except Exception as e:
                logging.info(f"Failed setting pywal colors:{e}")
        else:
            logging.warning(
                "Pywal option enabled but python module is not installed, ignored"
            )
    # print palette
    print_color_palette(pywal_colors)


def print_color_palette(pywal_colors):
    if settings.USER_HAS_COLR:
        i = 0
        for index, col in pywal_colors["colors"].items():
            if i % 8 == 0 and i != 0:
                print()
            print(f'{colr.color("    ",back=hex2rgb(col))}', end="")
            i += 1
        print(f"{settings.TERM_STY_RESET}")
    else:
        logging.debug(
            "Install colr python module to tint color codes and palette as they update"
        )
        # Print color palette from pywal.colors.palette
        for i in range(0, 16):
            if i % 8 == 0 and i != 0:
                print()

            if i > 7:
                i = "8;5;%s" % i

            print("\033[4%sm%s\033[0m" % (i, " " * (80 // 20)), end="")
        print("\n", end="")
