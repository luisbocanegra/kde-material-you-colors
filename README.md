<div align="center">

# 🎨 KDE Material You Colors

![plasmoid screenshot](https://github.com/luisbocanegra/kde-material-you-colors/assets/15076387/6bd4e04a-48a7-48bc-8dd1-3a75524cd10e)

Automatically generate Light/Dark Color Themes for KDE (and pywal if installed) from your current wallpaper, using [Python implementation](https://github.com/avanishsubbiah/material-color-utilities-python) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities)

![made with python badge](https://img.shields.io/static/v1?style=for-the-badge&label=Made%20with&message=Python&color=1f425f&logo=python&labelColor=2d333b)
![latest version badge](https://img.shields.io/github/v/release/luisbocanegra/kde-material-you-colors?include_prereleases&style=for-the-badge&color=1f425f&labelColor=2d333b)
</div>

![Screenshots](https://user-images.githubusercontent.com/15076387/188578458-8171e42b-f36c-44c1-9eb0-506c301d4f16.gif)

# Features

## Plasma specific

- [Plasma Widget](https://store.kde.org/p/2073783)
- Support for all Wallpaper plugins (color, image, slideshows, animated, Plasma 5.26+ dark wallpaper variants)
- Update automatically on wallpaper change
- Change icon themes
- Start automatically on login
- Make titlebar darker to match specified applications like terminals, code editors and other programs themed by pywal
- Follow Plasma Material You Dark/Light change to work with theme schedulers like [Koi](https://github.com/baduhai/Koi)
- **Plasma addons**
  - Tint [SierraBreeze](https://github.com/kay0u/SierraBreeze) window decoration buttons
  - TitleBar opacity control for [Klassy](https://github.com/paulmcauley/klassy) and [SierraBreezeEnhanced](https://github.com/kupiqu/SierraBreezeEnhanced) window decorations
  - ToolBar opacity control for [Lightly](https://github.com/Luwx/Lightly) Application style
  - Tint [Klassy](https://github.com/paulmcauley/klassy) window decoration outline

## Themeable programs

- Konsole color scheme
  - opacity control
- **[Pywal](https://github.com/dylanaraps/pywal) support to theme other programs using Material You Colors**
- Basic KSyntaxHighlighting support (Kate, KWrite, KDevelop...)

## Theming options

- Alternative Material You color selection if the wallpaper provides more than one
- Use your favorite color to generate Material You color schemes
- Custom colors list used for konsole/pywal
- Custom amount for background color tint
- Dark/light Color schemes (Plasma and pywal/konsole independently)
- Set a script/command that will be executed on start or wallpaper/dark/light/settings change
- Configuration file

# Installing

## Plasma widget

Install from the [KDE Store](https://store.kde.org/p/2073783)

1. Right click on panel > Add Widgets > Get New Widgets > Download New Plasma Widgets
2. Search for "KDE Material You Colors"

## Backend (MANDATORY)

### Using pypi with `pipx` (recommended) or `pip`

```sh
pipx install kde-material-you-colors
# Optional
# pywal to theme other programs using Material You Colors
pipx install pywal
```

### Arch Linux

- [AUR](https://aur.archlinux.org/packages/kde-material-you-colors) use your preferred AUR helper

### Optional features

- Install the [pywal](https://pypi.org/project/pywal/) python module to theme other programs using Material You Colors
  - Check [pywal Customization Wiki](https://github.com/dylanaraps/pywal/wiki/Customization) to theme supported programs

# Running from terminal to debug your configuration

- Run `kde-material-you-colors`

- Flags take precedence over configuration file, run `kde-material-you-colors -h` to see the list of available options

## Starting/Stopping Desktop entries

**If not installed by your package manager**, run `kde-material-you-colors -cl` to copy desktop entries to ~/.local/share/applications/

- To start the program launch **KDE Material You Colors** from your applications list
- To stop it launch **Stop KDE Material You Colors** from your applications list

# Running on Startup

After finishing the setup, you can make it run automatically on boot

1. Copy the default configuration to ~/.config/kde-material-you-colors/config.conf:

    `kde-material-you-colors -c`

2. Set the program to automatically start with Plasma:

    `kde-material-you-colors -a`

3. Reboot or logout/login and test the changes

## Removing from autostart

1. Open `System Settings` > `Startup and Shutdown`
2. Remove `kde-material-you-colors` by clicking on the `-` button.

# Configuration file

- Copy default configuration: run `kde-material-you-colors -c`
- Edit ~/.config/kde-material-you-colors/config.conf
- Run `kde-material-you-colors` with no arguments from terminal to test it.
- **You can view the sample configuration file [here](https://github.com/luisbocanegra/kde-material-you-colors/blob/main/src/kde_material_you_colors/data/sample_config.conf)**

# Notes

- To update color with `plasma-apply-colorscheme` (utility provided by plasma developers), the file containing the new color scheme must have a different name than the current one, to workaround this the program creates two scheme files with different names, then applies one after the other. As a result you end up with duplicated color schemes and maybe some lag while updating schemes.

- The wallpaper is obtained in the following order:

  - First, uses the [Plasma Desktop Scripting API](https://develop.kde.org/docs/plasma/scripting/api/) to read Wallpaper plugin configuration.

  - If the previous fails it uses the [KWin Scripting API](https://develop.kde.org/docs/plasma/kwin/api/) and [KWin's Screenshot plugin](https://github.com/KDE/kwin/tree/master/src/plugins/screenshot) to take a Screenshot of the Desktop view

## Bug reporting / Feature requests / Contributing

Please read the [Contributing guidelines in this repository](CONTRIBUTING.md)

# Thanks & Credits

- [Avanish Subbiah](https://github.com/avanishsubbiah) for the [Python implementation](https://github.com/avanishsubbiah/material-color-utilities-python) of Material Color Utilities required by this project.
- [This comment by throwaway6560192 on Reddit](https://www.reddit.com/r/kde/comments/mg6wr4/comment/gssbtqe/?utm_source=share&utm_medium=web2x&context=3) and [@pashazz (Pavel Borisov) ksetwallpaper](https://github.com/pashazz/ksetwallpaper) for the script to get the current Wallpaper that served me as starting point.
- Everyone that made [material-color-utilities](https://github.com/material-foundation/material-color-utilities) possible.
- [Pywal](https://github.com/dylanaraps/pywal) developers
- [Albert Ragány-Németh](https://github.com/albi005) for the [C# implementation](https://github.com/albi005/MaterialColorUtilities) of Material Color Utilities (used until v0.8.0).
[Google LLC. / Pictogrammers](https://pictogrammers.com/library/mdi/) for the widget icon
