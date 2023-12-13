from . import schemeconfigs
from .config import Configs
from .utils.wallpaper_utils import WallpaperReader
from .utils import (
    utils,
    m3_scheme_utils,
    pywal_utils,
    plasma_utils,
    konsole_utils,
    titlebar_utils,
    kwin_utils,
    ksyntax_utils,
)


def apply(config: Configs, wallpaper: WallpaperReader, dark_light):
    needs_kwin_reload = False
    material_colors = m3_scheme_utils.get_color_schemes(
        wallpaper,
        config.read("ncolor"),
    )
    if material_colors is None:
        return
    schemes = schemeconfigs.ThemeConfig(
        material_colors,
        wallpaper.source,
        config.read("light_blend_multiplier"),
        config.read("dark_blend_multiplier"),
        config.read("toolbar_opacity"),
        config.read("toolbar_opacity_dark"),
        config.read("custom_colors_list"),
    )

    # Export generated schemes to output file
    m3_scheme_utils.export_schemes(schemes)

    # Make plasma color schemes
    plasma_utils.make_scheme(schemes)
    plasma_utils.apply_color_schemes(dark_light)
    ksyntax_utils.export_schemes(schemes)
    plasma_utils.set_icons(
        config.read("iconslight"),
        config.read("iconsdark"),
        dark_light,
    )
    if config.read("sierra_breeze_buttons_color"):
        titlebar_utils.sierra_breeze_button_colors(schemes, dark_light)
        needs_kwin_reload = True
    if config.read("klassy_windeco_outline"):
        titlebar_utils.klassy_windeco_outline_color(schemes, dark_light)
        needs_kwin_reload = True
    if config.read("titlebar_opacity") or config.read("titlebar_opacity_dark"):
        titlebar_utils.titlebar_opacity(
            config.read("titlebar_opacity"),
            config.read("titlebar_opacity_dark"),
            dark_light,
        )
        needs_kwin_reload = True
    konsole_utils.export_scheme(
        light=config.read("light"),
        pywal_light=config.read("pywal_light"),
        schemes=schemes,
        konsole_opacity=config.read("konsole_opacity"),
        konsole_opacity_dark=config.read("konsole_opacity_dark"),
        dark_light=dark_light,
    )
    if config.read("disable_konsole") is not True:
        konsole_utils.apply_color_scheme()
    if config.read("darker_window_list"):
        titlebar_utils.kwin_rule_darker_titlebar(
            dark_light
            if config.read("pywal_light") is None
            else config.read("pywal_light"),
            config.read("darker_window_list"),
        )
    if config.read("pywal"):
        pywal_utils.apply_schemes(
            light=config.read("light"),
            use_pywal=config.read("pywal"),
            pywal_light=config.read("pywal_light"),
            schemes=schemes,
            dark_light=dark_light,
        )
    if needs_kwin_reload is True:
        kwin_utils.reload()
    pywal_utils.print_color_palette(
        light=config.read("light"),
        pywal_light=config.read("pywal_light"),
        schemes=schemes,
        dark_light=dark_light,
    )
    utils.run_hook(config.read("on_change_hook"))
