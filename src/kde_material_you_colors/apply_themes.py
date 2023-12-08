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

    schemes = schemeconfigs.ThemeConfig(
        material_colors,
        wallpaper.data,
        config.read("light_blend_multiplier"),
        config.read("dark_blend_multiplier"),
        config.read("toolbar_opacity"),
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
    if config.read("titlebar_opacity"):
        titlebar_utils.titlebar_opacity(config.read("titlebar_opacity"))
        needs_kwin_reload = True
    if config.read("konsole_profile"):
        konsole_utils.make_mirror_profile(config.read("konsole_profile"))
        konsole_utils.apply_color_scheme(
            dark_light,
            config.read("pywal_light"),
            schemes,
            config.read("konsole_profile"),
            konsole_opacity=config.read("konsole_opacity"),
        )
    if config.read("darker_window_list"):
        titlebar_utils.kwin_rule_darker_titlebar(
            dark_light
            if config.read("pywal_light") is None
            else config.read("pywal_light"),
            config.read("darker_window_list"),
        )
    if config.read("pywal"):
        pywal_utils.apply_schemes(
            dark_light,
            use_pywal=config.read("pywal"),
            pywal_light=config.read("pywal_light"),
            schemes=schemes,
        )
    if needs_kwin_reload is True:
        kwin_utils.reload()
    utils.run_hook(config.read("on_change_hook"))
