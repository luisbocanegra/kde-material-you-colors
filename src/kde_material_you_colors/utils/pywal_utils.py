import logging
from kde_material_you_colors.utils.color_utils import hex2rgb
from kde_material_you_colors import settings
from kde_material_you_colors.schemeconfigs import ThemeConfig

if settings.USER_HAS_PYWAL:
    import pywal


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
                pywal.sequences.send(pywal_colors, vte_fix=False)
                # Export all template files.
                pywal.export.every(pywal_colors)
                # Reload xrdb, i3 and polybar.
                pywal.reload.env()
            except Exception as e:
                logging.exception(f"Failed setting pywal colors:{e}")
        else:
            logging.warning(
                "Pywal option enabled but python module is not installed, ignored"
            )


def print_color_palette(
    light=None,
    pywal_light=None,
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

    for i, (name, color) in enumerate(pywal_colors["colors"].items()):
        fg = "30"
        if i == 0:
            fg = "39"
        if i % 8 == 0 and i != 0:
            print()
        rgb = hex2rgb(color)
        print(f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]};{fg}m {color} \033[0m", end="")
    print(f"{settings.TERM_STY_RESET}")
