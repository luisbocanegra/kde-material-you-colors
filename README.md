<div align="center">

# 🎨 KDE Material You Colors

<img src="https://github.com/luisbocanegra/kde-material-you-colors/assets/15076387/6bd4e04a-48a7-48bc-8dd1-3a75524cd10e" alt="Screenshot" height="250px">

Automatically generate light/dark color themes for KDE (and pywal if installed) from your current wallpaper, using [Python implementation](https://github.com/avanishsubbiah/material-color-utilities-python) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities)

[![AUR version](https://img.shields.io/aur/version/kde-material-you-colors?style=for-the-badge&logo=archlinux&labelColor=2d333b&color=1f425f)](https://aur.archlinux.org/packages/kde-material-you-colors)
[![PyPI - Version](https://img.shields.io/pypi/v/kde-material-you-colors?style=for-the-badge&logo=python&labelColor=2d333b&color=1f425f)](https://pypi.org/project/kde-material-you-colors/)
[![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fluisbocanegra%2Fkde-material-you-colors%2Fmain%2Fsrc%2Fplasmoid%2Fpackage%2Fmetadata.json&query=KPlugin.Version&style=for-the-badge&color=1f425f&labelColor=2d333b&logo=kde&label=Plasmoid)](https://store.kde.org/p/2136963)

</div>

[![Screenshots](https://user-images.githubusercontent.com/15076387/188578458-8171e42b-f36c-44c1-9eb0-506c301d4f16.gif)](https://user-images.githubusercontent.com/15076387/188578458-8171e42b-f36c-44c1-9eb0-506c301d4f16.gif)

# Features

## Plasma specific

- [Plasma Widget](https://store.kde.org/p/2136963) (Plasma 6 version)
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
- Set a script that will be executed on start or wallpaper/dark/light/settings change
- Configuration file

# Installing

## 1. Backend

Using pypi with `pipx` (recommended) using this command,
```sh
pipx install kde-material-you-colors
# Optional
# pywal to theme other programs using Material You Colors
pipx inject kde-material-you-colors pywal
```

or `pip` using this command
```sh
pip install kde-material-you-colors
# Optional
# pywal to theme other programs using Material You Colors
pip install pywal
```

> [!IMPORTANT]
> You may need to install `gcc python-dbus-dev libglib2.0-dev` system packages or their equivalent for your distribution. Additionally, installing some libraries for Pillow may be necessary, see [Pillow docs](https://pillow.readthedocs.io/en/latest/installation.html#external-libraries)

## 2. Plasma widget and desktop screenshot helper (support for all wallpaper plugins)

Install `extra-cmake-modules libplasma plasma5support` system packages or their equivalent for your distribution.

### User install

```sh
cmake -B build -S . -DCMAKE_INSTALL_PREFIX=~/.local -DINSTALL_PLASMOID=ON
cmake --build build
cmake --install build
```

### System-wide install

```sh
cmake -B build -S . -DCMAKE_INSTALL_PREFIX=/usr -DINSTALL_PLASMOID=ON
cmake --build build
sudo cmake --install build
```

> [!NOTE]
> You can also install the widget from the KDE Store [Plasma 6 version](https://store.kde.org/p/2136963) and set `-DINSTALL_PLASMOID=OFF` in the command above
>
> 1. Right click on panel > Add Widgets > Get New Widgets > Download New Plasma Widgets
> 2. Search for "KDE Material You Colors"

### Arch Linux

- [AUR](https://aur.archlinux.org/packages/kde-material-you-colors) use your preferred AUR helper

### Optional features

- Install the [pywal](https://pypi.org/project/pywal/) python module to theme other programs using Material You Colors
  - Check [pywal Customization Wiki](https://github.com/dylanaraps/pywal/wiki/Customization) to theme supported programs

# Running from terminal to debug your configuration

- Run `kde-material-you-colors`

- Flags take precedence over configuration file, run `kde-material-you-colors -h` to see the list of available options

## Starting/Stopping Desktop entries

> [!NOTE]
> **If not installed by your package manager**, run `kde-material-you-colors -cl` to copy desktop entries to ~/.local/share/applications/

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

- To update color with `plasma-apply-colorscheme` (utility provided by KDE developers), the file containing the new color scheme must have a different name than the current one, to workaround this the program creates two scheme files with different names, then applies one after the other. As a result you end up with duplicated color schemes and maybe some lag while updating schemes.

- The wallpaper is obtained in the following order:

  - First, uses the [Plasma Desktop Scripting API](https://develop.kde.org/docs/plasma/scripting/api/) to read Wallpaper plugin configuration.
  - If the previous fails, the screenshot helper (if installed) is used

    The backend uses the [KWin Scripting API](https://develop.kde.org/docs/plasma/kwin/api/) and calls the screenshot helper to take a Screenshot of the Desktop view using the [KWin's Screenshot plugin](https://github.com/KDE/kwin/tree/master/src/plugins/screenshot)

## Bug reporting / Feature requests / Contributing

Please read the [Contributing guidelines in this repository](CONTRIBUTING.md)

# Credits

- [Python Implementation](https://github.com/avanishsubbiah/material-color-utilities-python) of Material Color Utilities used by this project.
- [Material Color Utilities](https://github.com/material-foundation/material-color-utilities)
- [Pywal](https://github.com/dylanaraps/pywal) used to apply material colors to pywal supported software
- [MaterialColorUtilities (C#)](https://github.com/albi005/MaterialColorUtilities) (used until v0.8.0).
- [xdg-desktop-portal-kde](https://invent.kde.org/plasma/xdg-desktop-portal-kde) base for desktop screenshot helper.
- [kdotool](https://github.com/jinliu/kdotool) base for getting desktop window id.
- [Google LLC. / Pictogrammers](https://pictogrammers.com/library/mdi/) for the widget icon.
- [This comment on Reddit](https://www.reddit.com/r/kde/comments/mg6wr4/comment/gssbtqe/?utm_source=share&utm_medium=web2x&context=3) and [ksetwallpaper](https://github.com/pashazz/ksetwallpaper) for the code to get the current Wallpaper that served me as inspiration.
