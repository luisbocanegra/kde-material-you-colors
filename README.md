<div align="center">

# 🎨 KDE Material You Colors

[![AUR version](https://img.shields.io/aur/version/kde-material-you-colors?logo=archlinux&labelColor=2d333b&style=for-the-badge&color=7ad3ff)](https://aur.archlinux.org/packages/kde-material-you-colors)
[![PyPI - Version](https://img.shields.io/pypi/v/kde-material-you-colors?logo=python&labelColor=2d333b&style=for-the-badge&color=ffde7a)](https://pypi.org/project/kde-material-you-colors/)
[![KDE Store](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fluisbocanegra%2Fkde-material-you-colors%2Fmain%2Fsrc%2Fplasmoid%2Fpackage%2Fmetadata.json&query=KPlugin.Version&logo=kde&label=Plasmoid&labelColor=2d333b&style=for-the-badge&color=7ad3ff)](https://store.kde.org/p/2136963)
[![OBS Fedora 43](https://img.shields.io/badge/dynamic/xml?url=https%3A%2F%2Fapi.opensuse.org%2Fpublic%2Fbuild%2Fhome%3Aluisbocanegra%2FFedora_43%2Fx86_64%2Fkde-material-you-colors%2F_buildinfo&query=%2Fbuildinfo%2Fversrel%2Ftext()&logo=fedora&label=Fedora%2043&labelColor=2d333b&style=for-the-badge&color=7acaff)](https://software.opensuse.org//download.html?project=home%3Aluisbocanegra&package=kde-material-you-colors)
[![OBS Fedora Rawhide](https://img.shields.io/badge/dynamic/xml?url=https%3A%2F%2Fapi.opensuse.org%2Fpublic%2Fbuild%2Fhome%3Aluisbocanegra%2FFedora_Rawhide%2Fx86_64%2Fkde-material-you-colors%2F_buildinfo&query=%2Fbuildinfo%2Fversrel%2Ftext()&logo=fedora&label=Fedora%20Rawhide&labelColor=2d333b&style=for-the-badge&color=7acaff)](https://software.opensuse.org//download.html?project=home%3Aluisbocanegra&package=kde-material-you-colors)
[![OBS openSUSE Tumbleweed](https://img.shields.io/badge/dynamic/xml?url=https%3A%2F%2Fapi.opensuse.org%2Fpublic%2Fbuild%2Fhome%3Aluisbocanegra%2FopenSUSE_Tumbleweed%2Fx86_64%2Fkde-material-you-colors%2F_buildinfo&query=%2Fbuildinfo%2Fversrel%2Ftext()&logo=opensuse&label=openSUSE%20Tumbleweed&labelColor=2d333b&style=for-the-badge&color=c1ff7a)](https://software.opensuse.org//download.html?project=home%3Aluisbocanegra&package=kde-material-you-colors)
[![OBS openSUSE Slowroll](https://img.shields.io/badge/dynamic/xml?url=https%3A%2F%2Fapi.opensuse.org%2Fpublic%2Fbuild%2Fhome%3Aluisbocanegra%2FopenSUSE_Slowroll%2Fx86_64%2Fkde-material-you-colors%2F_buildinfo&query=%2Fbuildinfo%2Fversrel%2Ftext()&logo=opensuse&label=openSUSE%20Slowroll&labelColor=2d333b&style=for-the-badge&color=c1ff7a)](https://software.opensuse.org//download.html?project=home%3Aluisbocanegra&package=kde-material-you-colors)

Automatically generate light/dark color themes for KDE (and pywal if installed) from your current wallpaper, using [@T-Dynamos Python implementation](https://github.com/T-Dynamos/materialyoucolor-python) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities)

</div>

[![Screenshots](https://user-images.githubusercontent.com/15076387/188578458-8171e42b-f36c-44c1-9eb0-506c301d4f16.gif)](https://user-images.githubusercontent.com/15076387/188578458-8171e42b-f36c-44c1-9eb0-506c301d4f16.gif)

If you enjoy using the plugin consider sponsoring or donating so I can dedicate more time to maintain and improve this and [my other projects](https://github.com/luisbocanegra?tab=repositories&q=&type=source&language=&sort=stargazers).

[![GitHub Sponsors](https://img.shields.io/badge/Sponsors-%2329313C?logo=githubsponsors&style=for-the-badge)](https://github.com/sponsors/luisbocanegra)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-supporter?logo=ko-fi&logoColor=%23ffffff&color=%23467BEB&style=for-the-badge)](https://ko-fi.com/luisbocanegra)
[!["Buy Me A Coffee"](https://img.shields.io/badge/Buy%20me%20a%20coffee-supporter?logo=buymeacoffee&logoColor=%23282828&color=%23FF803F&style=for-the-badge)](https://www.buymeacoffee.com/luisbocanegra)
[![PayPal](https://img.shields.io/badge/PayPal-supporter?logo=paypal&logoColor=%23ffffff&color=%23003087&style=for-the-badge)](https://www.paypal.com/donate/?hosted_button_id=Y5TMH3Z4YZRDA)
[![Patreon](https://img.shields.io/badge/Patreon-%23000000?logo=patreon&logoColor=%23ffffff&style=for-the-badge)](https://patreon.com/luisbocanegra?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink)

## Join our Discord / Matrix

[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/ZqD75dzKTe)
[![Discord](https://img.shields.io/badge/Matrix-%23121212.svg?style=for-the-badge&logo=matrix&logoColor=white)](https://matrix.to/#/#kde-plasma-smart-video-wallpaper-reborn:matrix.org)

## Features

### Plasma specific

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

### Themeable programs

- Konsole color scheme
  - opacity & blur control
- Pywal support to theme other programs using Material You Colors
- Basic KSyntaxHighlighting support (Kate, KWrite, KDevelop...)

### Theming options

- Alternative Material You color selection if the wallpaper provides more than one
- Use your favorite color to generate Material You color schemes
- Custom colors list used for konsole/pywal
- Custom amount for colorfulness and brightness of theme
- Color scheme variants from Material You (Vibrant, Monochrome, Neutral...)
- Dark/light Color schemes (Plasma and pywal/konsole independently)
- Set a script that will be executed on start or wallpaper/dark/light/settings change
- Configuration file

## Installing

### Arch Linux

<https://aur.archlinux.org/packages/kde-material-you-colors>

```sh
yay -S kde-material-you-colors
```

### openSUSE Build Service packages (Fedora, openSUSE)

Maintained with @pallaswept and me at <https://build.opensuse.org/package/show/home:luisbocanegra/kde-material-you-colors>

Install instructions: <https://software.opensuse.org//download.html?project=home%3Aluisbocanegra&package=kde-material-you-colors>

### Manual install

1. Install `pipx` system packages from your distribution packages.

2. Install the backend

    **For Plasma 5** this is the last version, development has switched to plasma 6

    ```sh
    pipx install kde-material-you-colors==1.7.1
    pipx inject kde-material-you-colors pywal
    ```

    **For Plasma 6**

    ```sh
    pipx install kde-material-you-colors
    pipx inject kde-material-you-colors pywal16
    # to upgrade to newer version
    pipx upgrade kde-material-you-colors
    ```

    **Note:** You may need to install `gcc python-dbus-dev libglib2.0-dev` system packages or their equivalent for your distribution. Additionally, installing some libraries for Pillow may be necessary, see [Pillow docs](https://pillow.readthedocs.io/en/latest/installation.html#external-libraries)

3. Install the widget from the KDE Store [Plasma 6 version](https://store.kde.org/p/2136963) | [Plasma 5 version](https://www.pling.com/p/2073783/)

   1. **Right click on the Panel** > **Add Widgets** > **Get New Widgets** > **Download New Plasma Widgets**
   2. **Search** for "**KDE Material You Colors**", install & add it to your Panel/Desktop.

4. Install the screenshot helper. **Optional but recommended if you use other than default Image wallpaper plugin**

    **Plasma 6**

    Install `git extra-cmake-modules` system packages or their equivalent for your distribution.

    ```sh
    git clone https://github.com/luisbocanegra/kde-material-you-colors
    cd kde-material-you-colors
    ./install-screenshot-helper.sh
    ```

    **NOTE:** Helper is now installed with `/usr` prefix, reboot if you get `The process is not authorized to take a screenshot` error

    **Plasma 5**

    Install `git extra-cmake-modules` system packages or their equivalent for your distribution.

    ```sh
    git clone https://github.com/luisbocanegra/kde-material-you-colors -b plasma5
    cd kde-material-you-colors
    ./install-screenshot-helper.sh
    ```

To upgrade to a new version repeat these steps.

**Note:** When you upgrade te widget to a newer version it will inform you if it requires a new version of the backend.

## Running

You can Start and change the configuration from the widget.

### From terminal

```sh
kde-material-you-colors
```

Run `kde-material-you-colors -h` to see the list of available options (Flags take precedence over configuration file)

### Starting/Stopping Desktop entries

**If not installed by your package manager**, run `kde-material-you-colors -cl`

- To start the program launch **KDE Material You Colors** from your applications list
- To stop, launch **Stop KDE Material You Colors** from your applications list

### Running on Startup

```sh
kde-material-you-colors -a
```

#### Removing from autostart

1. Open **System Settings** > **Autostart**
2. Remove **kde-material-you-colors** by clicking on the **Trash** button.

## Configuration file

The preferred way to change the configuration is from the widget. If the configuration doesn't exist, it will be automatically created by the widget.

**Editing manually**

The default configuration file can be created by running `kde-material-you-colors -c` the location is `~/.config/kde-material-you-colors/config.conf`

Run `kde-material-you-colors` with no arguments from terminal to test your changes in real time.

Due to Qt limitations, comments are removed from the configuration file by the widget. **You can view the sample configuration file with comments [here](https://github.com/luisbocanegra/kde-material-you-colors/blob/main/src/kde_material_you_colors/data/sample_config.conf)**.

## FAQ

**Q.** How does this different from Plasma's "**Accent Color From Wallpaper**" and "**Tint all colors with accent color**"?

There are some key differences:

- Brighter accent/buttons colors
- Option to choose another color if the wallpaper returns more than one
- Can also apply colors to Konsole and pywal (both from wallpaper and custom ones)
- Colors comparison <https://imgur.com/a/a28uZka> (kde-material-you-colors top, default tint option bottom)

**Q.** Why there are duplicated color schemes in **System Settings**

To update color with `plasma-apply-colorscheme` (utility provided by KDE developers), the file containing the new color scheme must have a different name than the current one, to workaround that, this program creates two color scheme files with different names, then applies one after the other. As a result you end up with duplicated color schemes and maybe some lag while updating schemes.

**Q.** Can't get wallpaper colors of the default wallpaper

If you are using the default Image wallpaper plugin try changing the image to something else at least once first.

**Q.** Slideshow wallpaper (or any other Plugin) doesn't update colors correctly

Try enabling **Only use screenshot method** from the widget **Advanced settings**

**Q.** How does wallpaper detection work and why it fails sometimes?

The wallpaper is obtained in the following order:

- First, uses the [Plasma Desktop Scripting API](https://develop.kde.org/docs/plasma/scripting/api/) to read Wallpaper plugin configuration.
- If the previous fails, the screenshot helper (if installed) is used

The backend uses the [KWin Scripting API](https://develop.kde.org/docs/plasma/kwin/api/) and calls the screenshot helper to take a Screenshot of the Desktop view using the [KWin's Screenshot plugin](https://github.com/KDE/kwin/tree/master/src/plugins/screenshot)

Both methods are somewhat robust but there are edge cases when detection will fail, which are [explained here](https://github.com/luisbocanegra/kde-material-you-colors/issues/187)

**Q.** Broken theming in Qt5 applications [#220](https://github.com/luisbocanegra/kde-material-you-colors/issues/220)

Install `plasma5-integration` or the equivalent from your distribution packages.

## Bug reporting / Feature requests / Contributing

Please read the [Contributing guidelines in this repository](https://github.com/luisbocanegra/kde-material-you-colors/blob/main/CONTRIBUTING.md)

## Acknowledgements

- [materialyoucolor-python](https://github.com/T-Dynamos/materialyoucolor-python) Python Implementation of Material Color Utilities used by this project.
- [Pywal16](https://github.com/eylles/pywal16) to apply material colors to pywal supported software
- [xdg-desktop-portal-kde](https://invent.kde.org/plasma/xdg-desktop-portal-kde) base for desktop screenshot helper.
- [kdotool](https://github.com/jinliu/kdotool) base for getting desktop window id.
- [ksetwallpaper](https://github.com/pashazz/ksetwallpaper) code to get the current Wallpaper that served me as inspiration.
- [Google LLC. / Pictogrammers](https://pictogrammers.com/library/mdi/) widget icon assets.
