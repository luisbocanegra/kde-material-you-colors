import logging
import schemeconfigs
import globals
from utils import (
    utils,
    file_utils,
    m3_scheme_utils,
    pywal_utils,
    plasma_utils,
    konsole_utils,
    titlebar_utils,
    kwin_utils,
    ksyntax_utils,
)


# TODO: Refactor this into something cleaner


def apply_themes(
    config_watcher: utils.Watcher,
    wallpaper_watcher: utils.Watcher,
    wallpaper_modified: utils.Watcher,
    group1_watcher: utils.Watcher,
    light_mode_watcher: utils.Watcher,
    schemes_watcher: utils.Watcher,
    material_colors: utils.Watcher,
    first_run_watcher: utils.Watcher,
    konsole_profile_modified: utils.Watcher,
):
    # Print new config after change
    if config_watcher.has_changed():
        logging.debug(f"Config: {config_watcher.get_new_value()}")
    needs_kwin_reload = False
    initial_dark_light = False

    group1_watcher.set_value(
        [
            config_watcher.get_new_value()["ncolor"],
            config_watcher.get_new_value()["light_blend_multiplier"],
            config_watcher.get_new_value()["dark_blend_multiplier"],
        ]
    )

    # Get wallpaper type and data
    if (
        wallpaper_watcher.get_new_value() != None
        and wallpaper_watcher.get_new_value()[1] != None
    ):
        wallpaper_new_type = wallpaper_watcher.get_new_value()[0]
        wallpaper_new_data = wallpaper_watcher.get_new_value()[1]

    # if wallpaper is image save time of last modification
    if wallpaper_new_type == "image":
        wallpaper_modified.set_value(
            file_utils.get_last_modification(wallpaper_new_data)
        )
    else:
        wallpaper_modified.set_value(None)

    if config_watcher.get_new_value()["konsole_profile"] != None:
        konsole_profile_modified.set_value(
            file_utils.get_last_modification(
                globals.KONSOLE_DIR
                + config_watcher.get_new_value()["konsole_profile"]
                + ".profile"
            )
        )

    # get dark/light mode
    if config_watcher.get_new_value()["light"] != None:
        light_mode_watcher.set_value(config_watcher.get_new_value()["light"])
    # try to get the initial theme with from hash
    elif first_run_watcher.get_new_value() is True:
        light_mode_watcher.set_value(plasma_utils.get_initial_mode())
        initial_dark_light = light_mode_watcher.get_new_value()
    else:
        light_mode_watcher.set_value(plasma_utils.kde_globals_light())

    dark_light = light_mode_watcher.get_new_value()
    #
    #
    #
    #
    #
    #
    if (
        wallpaper_watcher.has_changed()
        or group1_watcher.has_changed()
        or wallpaper_modified.has_changed()
    ):
        if wallpaper_watcher.has_changed() or wallpaper_modified.has_changed():
            logging.info(f"Using source ({wallpaper_new_type}): {wallpaper_new_data}")
        material_colors.set_value(
            m3_scheme_utils.get_color_schemes(
                wallpaper_watcher.get_new_value(),
                config_watcher.get_new_value()["ncolor"],
            )
        )
        if material_colors.get_new_value() != None:
            # Genrate color schemes from MYou colors
            schemes_watcher.set_value(
                schemeconfigs.ThemeConfig(
                    material_colors.get_new_value(),
                    wallpaper_new_data,
                    config_watcher.get_new_value()["light_blend_multiplier"],
                    config_watcher.get_new_value()["dark_blend_multiplier"],
                    config_watcher.get_new_value()["toolbar_opacity"],
                    config_watcher.get_new_value()["custom_colors_list"],
                )
            )

            # Export generated schemes to output file
            m3_scheme_utils.export_schemes(schemes_watcher.get_new_value())

            # Make plasma color schemes
            plasma_utils.make_scheme(schemes_watcher.get_new_value())

            # light mode may have changed while generating colors, check it again
            if config_watcher.get_new_value()["light"] != None:
                light_mode_watcher.set_value(config_watcher.get_new_value()["light"])
            elif plasma_utils.kde_globals_light() is not None:
                light_mode_watcher.set_value(plasma_utils.kde_globals_light())
                dark_light = light_mode_watcher.get_new_value()
            else:
                dark_light = initial_dark_light

            # skip applying themes if no dark/light mode was specified
            # or found in current user settings
            if dark_light != None:
                logging.info(f"Using light mode for Plasma: {dark_light}")
                # Apply plasma color schemes
                plasma_utils.apply_color_schemes(dark_light)
                ksyntax_utils.export_schemes(schemes_watcher.get_new_value())

                # other UI parts
                plasma_utils.set_icons(
                    config_watcher.get_new_value()["iconslight"],
                    config_watcher.get_new_value()["iconsdark"],
                    dark_light,
                )
                if (
                    config_watcher.get_new_value()["sierra_breeze_buttons_color"]
                    == True
                ):
                    needs_kwin_reload = True
                    titlebar_utils.sierra_breeze_button_colors(
                        schemes_watcher.get_new_value(), dark_light
                    )
                if config_watcher.get_new_value()["klassy_windeco_outline"] == True:
                    needs_kwin_reload = True
                    titlebar_utils.klassy_windeco_outline_color(
                        schemes_watcher.get_new_value(), dark_light
                    )
                if first_run_watcher.get_new_value() == True:
                    if config_watcher.get_new_value()["titlebar_opacity"] != None:
                        needs_kwin_reload = True
                        titlebar_utils.titlebar_opacity(
                            config_watcher.get_new_value()["titlebar_opacity"]
                        )
            else:
                logging.warning(
                    "No default theme found or currently active, skipping Plasma theming"
                )

            # Parts that can follow pywal if enabled
            if dark_light != None or config_watcher.get_new_value()["pywal"]:
                if config_watcher.get_new_value()["pywal_light"] is not None:
                    logging.info(
                        f"Forcing { f'light' if config_watcher.get_new_value()['pywal_light'] else 'dark'} mode for Pywal"
                    )
                # Export and apply color scheme to konsole profile
                if config_watcher.get_new_value()["konsole_profile"] != None:
                    konsole_utils.make_mirror_profile(
                        config_watcher.get_new_value()["konsole_profile"]
                    )
                    konsole_utils.apply_color_scheme(
                        dark_light,
                        config_watcher.get_new_value()["pywal_light"],
                        schemes_watcher.get_new_value(),
                        config_watcher.get_new_value()["konsole_profile"],
                        konsole_opacity=config_watcher.get_new_value()[
                            "konsole_opacity"
                        ],
                    )

                # applications matching titlebar and window color
                if (
                    first_run_watcher.get_new_value() is True
                    or config_watcher.get_new_value()["darker_window_list"] is not None
                ):
                    titlebar_utils.kwin_rule_darker_titlebar(
                        dark_light
                        if config_watcher.get_new_value()["pywal_light"] is None
                        else config_watcher.get_new_value()["pywal_light"],
                        config_watcher.get_new_value()["darker_window_list"],
                    )
                    needs_kwin_reload = True

                # Apply pywal color scheme with MYou colors
                if config_watcher.get_new_value()["pywal"] == True:
                    pywal_utils.apply_schemes(
                        dark_light,
                        use_pywal=config_watcher.get_new_value()["pywal"],
                        pywal_light=config_watcher.get_new_value()["pywal_light"],
                        schemes=schemes_watcher.get_new_value(),
                    )

            if needs_kwin_reload == True:
                kwin_utils.reload()
                needs_kwin_reload = False
            print("---------------------")
        utils.run_hook(config_watcher.get_new_value()["on_change_hook"])
    #
    #
    #
    #
    #
    #
    if first_run_watcher.get_new_value() == False:
        if light_mode_watcher.has_changed():
            if not wallpaper_watcher.has_changed():
                # skip applying themes if no dark/light mode was specified
                # or found in current user settings
                if dark_light != None:
                    logging.info(f"Using light mode for Plasma: {dark_light}")
                    # Apply plasma color schemes
                    # change only if is not currently active
                    if plasma_utils.kde_globals_light() != dark_light:
                        plasma_utils.apply_color_schemes(dark_light)

                    # other UI parts
                    plasma_utils.set_icons(
                        config_watcher.get_new_value()["iconslight"],
                        config_watcher.get_new_value()["iconsdark"],
                        dark_light,
                    )
                    if (
                        config_watcher.get_new_value()["sierra_breeze_buttons_color"]
                        == True
                    ):
                        needs_kwin_reload = True
                        titlebar_utils.sierra_breeze_button_colors(
                            schemes_watcher.get_new_value(), dark_light
                        )
                    if config_watcher.get_new_value()["klassy_windeco_outline"] == True:
                        needs_kwin_reload = True
                        titlebar_utils.klassy_windeco_outline_color(
                            schemes_watcher.get_new_value(), dark_light
                        )
                else:
                    logging.warning(
                        "No default theme found or currently active, skipping Plasma theming"
                    )

                # Parts that can follow pywal if enabled
                if dark_light != None or config_watcher.get_new_value()["pywal"]:
                    if config_watcher.get_new_value()["pywal_light"] is not None:
                        logging.info(
                            f"Forcing { f'light' if config_watcher.get_new_value()['pywal_light'] else 'dark'} mode for Pywal"
                        )
                    # Export and apply color scheme to konsole profile
                    konsole_utils.apply_color_scheme(
                        dark_light,
                        config_watcher.get_new_value()["pywal_light"],
                        schemes_watcher.get_new_value(),
                        config_watcher.get_new_value()["konsole_profile"],
                        konsole_opacity=config_watcher.get_new_value()[
                            "konsole_opacity"
                        ],
                    )
                    # applications matching titlebar and window color
                    if config_watcher.get_new_value()["darker_window_list"] is not None:
                        titlebar_utils.kwin_rule_darker_titlebar(
                            dark_light
                            if config_watcher.get_new_value()["pywal_light"] is None
                            else config_watcher.get_new_value()["pywal_light"],
                            config_watcher.get_new_value()["darker_window_list"],
                        )
                        needs_kwin_reload = True

                    # Apply pywal color scheme with MYou colors
                    if config_watcher.get_new_value()["pywal"] == True:
                        if config_watcher.get_new_value()["pywal_light"] == None:
                            pywal_utils.apply_schemes(
                                dark_light,
                                use_pywal=config_watcher.get_new_value()["pywal"],
                                pywal_light=config_watcher.get_new_value()[
                                    "pywal_light"
                                ],
                                schemes=schemes_watcher.get_new_value(),
                            )

            if needs_kwin_reload == True:
                kwin_utils.reload()
                needs_kwin_reload = False
            print("---------------------")
    #
    #
    #
    #
    #
    #
    #   update copy of konsole profile
    if (
        konsole_profile_modified.has_changed()
        and konsole_profile_modified.get_new_value() != None
        and first_run_watcher.get_new_value() == False
    ):
        konsole_utils.make_mirror_profile(
            config_watcher.get_new_value()["konsole_profile"]
        )

    if (
        config_watcher.has_changed()
        and config_watcher.get_old_value() != None
        and not group1_watcher.has_changed()
    ):
        if dark_light != None:
            # Toolbar opacity changes
            if (
                config_watcher.get_new_value()["toolbar_opacity"]
                != config_watcher.get_old_value()["toolbar_opacity"]
            ):
                if config_watcher.get_new_value()["toolbar_opacity"] != None:
                    material_colors.set_value(
                        m3_scheme_utils.get_color_schemes(
                            wallpaper_watcher.get_new_value(),
                            config_watcher.get_new_value()["ncolor"],
                        )
                    )
                if material_colors.get_new_value() != None:
                    # Genrate color schemes from MYou colors
                    schemes_watcher.set_value(
                        schemeconfigs.ThemeConfig(
                            material_colors.get_new_value(),
                            wallpaper_new_data,
                            config_watcher.get_new_value()["light_blend_multiplier"],
                            config_watcher.get_new_value()["dark_blend_multiplier"],
                            config_watcher.get_new_value()["toolbar_opacity"],
                            config_watcher.get_new_value()["custom_colors_list"],
                        )
                    )
                    # Export generated schemes to output file
                    m3_scheme_utils.export_schemes(schemes_watcher.get_new_value())
                    # Make plasma color schemes
                    plasma_utils.make_scheme(schemes_watcher.get_new_value())
                    # Apply plasma color schemes
                    plasma_utils.apply_color_schemes(dark_light)
                    ksyntax_utils.export_schemes(schemes_watcher.get_new_value())

            # icon changes
            icons_new = [
                config_watcher.get_new_value()["iconslight"],
                config_watcher.get_new_value()["iconsdark"],
            ]
            icons_old = [
                config_watcher.get_old_value()["iconslight"],
                config_watcher.get_old_value()["iconsdark"],
            ]
            if icons_new != icons_old:
                plasma_utils.set_icons(icons_new[0], icons_new[1])

            # titlebar opacity changes
            if (
                config_watcher.get_new_value()["titlebar_opacity"]
                != config_watcher.get_old_value()["titlebar_opacity"]
            ):
                if config_watcher.get_new_value()["titlebar_opacity"] != None:
                    needs_kwin_reload = True
                    titlebar_utils.titlebar_opacity(
                        config_watcher.get_new_value()["titlebar_opacity"]
                    )

            # sbe changes
            if (
                config_watcher.get_new_value()["sierra_breeze_buttons_color"]
                != config_watcher.get_old_value()["sierra_breeze_buttons_color"]
            ):
                if (
                    config_watcher.get_new_value()["sierra_breeze_buttons_color"]
                    == True
                ):
                    needs_kwin_reload = True
                    titlebar_utils.sierra_breeze_button_colors(
                        schemes_watcher.get_new_value(), dark_light
                    )
            # klassy win deco changes
            if (
                config_watcher.get_new_value()["klassy_windeco_outline"]
                != config_watcher.get_old_value()["klassy_windeco_outline"]
            ):
                if config_watcher.get_new_value()["klassy_windeco_outline"] == True:
                    needs_kwin_reload = True
                    titlebar_utils.klassy_windeco_outline_color(
                        schemes_watcher.get_new_value(), dark_light
                    )

        # Parts that can also follow pywal if enabled
        if dark_light != None or config_watcher.get_new_value()["pywal"] != None:
            if (
                config_watcher.get_new_value()["pywal_light"]
                != config_watcher.get_old_value()["pywal_light"]
            ):
                if config_watcher.get_new_value()["pywal_light"] is not None:
                    logging.info(
                        f"Forcing { f'light' if config_watcher.get_new_value()['pywal_light'] else 'dark'} mode for Pywal"
                    )

            # check for changes that affect konsole color scheme
            if (
                config_watcher.get_new_value()["pywal_light"]
                != config_watcher.get_old_value()["pywal_light"]
                or config_watcher.get_new_value()["konsole_opacity"]
                != config_watcher.get_old_value()["konsole_opacity"]
                or config_watcher.get_new_value()["konsole_profile"]
                != config_watcher.get_old_value()["konsole_profile"]
                or config_watcher.get_new_value()["pywal"]
                != config_watcher.get_old_value()["pywal"]
            ):
                konsole_utils.apply_color_scheme(
                    dark_light,
                    config_watcher.get_new_value()["pywal_light"],
                    schemes_watcher.get_new_value(),
                    config_watcher.get_new_value()["konsole_profile"],
                    konsole_opacity=config_watcher.get_new_value()["konsole_opacity"],
                )

            # applications matching titlebar and window color
            if (
                config_watcher.get_new_value()["darker_window_list"]
                != config_watcher.get_old_value()["darker_window_list"]
                or config_watcher.get_new_value()["pywal_light"]
                != config_watcher.get_old_value()["pywal_light"]
            ):
                titlebar_utils.kwin_rule_darker_titlebar(
                    dark_light
                    if config_watcher.get_new_value()["pywal_light"] is None
                    else config_watcher.get_new_value()["pywal_light"],
                    config_watcher.get_new_value()["darker_window_list"],
                )
                needs_kwin_reload = True

            # pywal
            if (
                config_watcher.get_new_value()["pywal_light"]
                != config_watcher.get_old_value()["pywal_light"]
                or config_watcher.get_new_value()["pywal"]
                != config_watcher.get_old_value()["pywal"]
            ):
                pywal_utils.apply_schemes(
                    dark_light,
                    use_pywal=config_watcher.get_new_value()["pywal"],
                    pywal_light=config_watcher.get_new_value()["pywal_light"],
                    schemes=schemes_watcher.get_new_value(),
                )

            # custom color list
            if (
                config_watcher.get_new_value()["custom_colors_list"]
                != config_watcher.get_old_value()["custom_colors_list"]
            ):
                material_colors.set_value(
                    m3_scheme_utils.get_color_schemes(
                        wallpaper_watcher.get_new_value(),
                        config_watcher.get_new_value()["ncolor"],
                    )
                )
                if material_colors.get_new_value() != None:
                    # Genrate color schemes from MYou colors
                    schemes_watcher.set_value(
                        schemeconfigs.ThemeConfig(
                            material_colors.get_new_value(),
                            wallpaper_new_data,
                            config_watcher.get_new_value()["light_blend_multiplier"],
                            config_watcher.get_new_value()["dark_blend_multiplier"],
                            config_watcher.get_new_value()["toolbar_opacity"],
                            config_watcher.get_new_value()["custom_colors_list"],
                        )
                    )
                    # Export generated schemes to output file
                    m3_scheme_utils.export_schemes(schemes_watcher.get_new_value())
                    # Konsole
                    konsole_utils.apply_color_scheme(
                        dark_light,
                        config_watcher.get_new_value()["pywal_light"],
                        schemes_watcher.get_new_value(),
                        config_watcher.get_new_value()["konsole_profile"],
                        konsole_opacity=config_watcher.get_new_value()[
                            "konsole_opacity"
                        ],
                    )
                    # pywal
                    if config_watcher.get_new_value()["pywal"] == True:
                        pywal_utils.apply_schemes(
                            dark_light,
                            use_pywal=config_watcher.get_new_value()["pywal"],
                            pywal_light=config_watcher.get_new_value()["pywal_light"],
                            schemes=schemes_watcher.get_new_value(),
                        )
                        ksyntax_utils.export_schemes(schemes_watcher.get_new_value())

        if needs_kwin_reload == True:
            kwin_utils.reload()
            needs_kwin_reload = False

        utils.run_hook(config_watcher.get_new_value()["on_change_hook"])
    first_run_watcher.set_value(False)
