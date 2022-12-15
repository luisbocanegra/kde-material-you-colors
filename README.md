<div align="center">

# 🎨 KDE Material You Colors

### Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop

This is a Python program that uses the [Python implementation](https://github.com/avanishsubbiah/material-color-utilities-python) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) to generate a Material Design 3 color scheme.
Which is used to generate Light and Dark Color Themes for KDE (and pywal if installed) from your current wallpaper, automatically.

![](https://img.shields.io/static/v1?style=for-the-badge&label=Made%20with&message=Python&color=1f425f&logo=python&labelColor=2d333b)
![](https://img.shields.io/static/v1?style=for-the-badge&label=Maintained&message=yes&color=1f425f&eColor=181818&labelColor=2d333b)
![](https://img.shields.io/github/v/release/luisbocanegra/kde-material-you-colors?include_prereleases&style=for-the-badge&color=1f425f&labelColor=2d333b)
</div>

<div>
<img src="https://user-images.githubusercontent.com/15076387/188578458-8171e42b-f36c-44c1-9eb0-506c301d4f16.gif"  alt="Screenshot">
</div>

Table of Contents
=================

- [Features](#features)
  - [Plasma specific](#plasma-specific)
  - [Themeable addons/programs](#themeable-addonsprograms)
  - [Theming options](#theming-options)
- [Installing](#installing)
  - [Arch Linux](#arch-linux)
  - [Other distributions](#other-distributions)
    - [Updating](#updating)
  - [Optional features](#optional-features)
- [Running](#running)
    - [From terminal to debug your configuration](#from-terminal-to-debug-your-configuration)
    - [Options](#options)
    - [Desktop entries](#desktop-entries)
- [Startup script](#startup-script)
  - [Removing the autostart script](#removing-the-autostart-script)
- [Changing Current Wallpaper plugin](#changing-current-wallpaper-plugin)
- [Working Wallpaper plugins](#working-wallpaper-plugins)
- [Configuration file](#configuration-file)
- [Notes](#notes)
  - [Bug reporting / Feature requests / Contributing](#bug-reporting--feature-requests--contributing)
- [Thanks \& Credits](#thanks--credits)

# Features
## Plasma specific
- Update automatically on wallpaper change
- Multiple wallpaper [plugins supported](#working-wallpaper-plugins)
- Support for selecting Wallpaper plugin from secondary monitors
- Dark and Light Icon theme
- Support Plasma 5.26+ dark wallpaper variants
- Start automatically on login
- Make titlebar darker to match specified applications like terminals, code editors and other programs themed by pywal
- Follow Plasma Material You Dark/Light change to work with theme schedulers like [Koi](https://github.com/baduhai/Koi)

## Themeable addons/programs
- Konsole color scheme support
  - opacity control
- **[Pywal](https://github.com/dylanaraps/pywal) support to theme other programs using Material You Colors**
- Basic KSyntaxHighlighting support (Kate, KWrite, KDevelop...)
- **Plasma addons**
  - Tint [SierraBreeze](https://github.com/kay0u/SierraBreeze) window decoration buttons
  - TitleBar opacity control for [Klassy](https://github.com/paulmcauley/klassy) and [SierraBreezeEnhanced](https://github.com/kupiqu/SierraBreezeEnhanced) window decorations
  - ToolBar opacity control for [Lightly](https://github.com/Luwx/Lightly) Application style
  - Tint [Klassy](https://github.com/paulmcauley/klassy) window decoration outline

## Theming options
- Alternative Material You color selection if the wallpaper provides more than one
- Use your favorite color to generate Material You color schemes
- Custom colors list used for konsole/pywal
- Custom amount for background color tint
- Dark an Light Color schemes (Plasma and pywal/konsole independently)
- Set a script/command that will be executed on start or wallpaper/dark/light/settings change
- Configurarion file


# Installing
## Arch Linux
- [AUR](https://aur.archlinux.org/packages/kde-material-you-colors)
## Other distributions
1. Clone/download this repository and cd to it
```sh
git clone https://github.com/luisbocanegra/kde-material-you-colors --branch main
cd kde-material-you-colors
```
2. Make the installer executable and run it as root

For Ubuntu based distros:
```sh
chmod +x install-ubuntu-based.sh
sudo ./install-ubuntu-based.sh
```
For Fedora based distros:
```sh
chmod +x install-fedora-based.sh
sudo ./install-fedora-based.sh
```
### Updating

Fetch latest changes:

```sh
cd kde-material-you-colors
git pull
```

Repeat step 2

## Optional features
- Install the [Colr](https://pypi.org/project/Colr/) python module to display colored palette and seed colors from terminal
- Install the [pywal](https://pypi.org/project/pywal/) python module to theme other programs using Material You Colors
  - Check [pywal Customization Wiki](https://github.com/dylanaraps/pywal/wiki/Customization) to theme supported programs

# Running
### From terminal to debug your configuration
- Run `kde-material-you-colors` from terminal, this should change your Desktop colors right after.

**NOTE:** Without any configuration/arguments your wallpaper will be reset to Image Wallpaper Plugin

### Options
- Run `kde-material-you-colors -h` to see the list of available options

### Desktop entries
- To start/restart the program launch **KDE Material You Colors** from your applications list
- To stop it launch **Stop KDE Material You Colors** from your applications list

# Startup script
After finishing the setup, you can make it run automatically on boot

1. Copy the default configuration to ~/.config/kde-material-you-colors/config.conf:

`kde-material-you-colors -c` 

2. Set the program to automatically start with Plasma:

`kde-material-you-colors -a` 

3. Reboot or logout/login and test the changes,

**NOTE:** your wallpaper will be reset to Image Wallpaper Plugin

## Removing the autostart script
1. Open `System Settings` > `Startup and Shutdown`
2. Remove `kde-material-you-colors` by clicking on the `-` button.

# Changing Current Wallpaper plugin

<span style="color:#ff6568"> **Use the configuration file !!** </span>

Using Plasma Wallpaper Settings may Crash Plasmashell and will set again the plugin from Configuration file

# Working Wallpaper plugins
This is a list of compatible Plasma Wallpaper Plugins

| Name        | ID          |
| ----------- | ----------- |
| Image (default)      | `org.kde.image`  |
| Picture of the day | `org.kde.potd` |
| Slideshow | `org.kde.slideshow` |
| Plain color | `org.kde.color` |

# Configuration file

- Copy default configuration: run `kde-material-you-colors -c`
- Edit ~/.config/kde-material-you-colors/config.conf
- Run `kde-material-you-colors` with no arguments from terminal to test it.
- **You can view the sample configuration file [here](https://github.com/luisbocanegra/kde-material-you-colors/blob/main/src/sample_config.conf)**

# Notes
- To update color with `plasma-apply-colorscheme` (utility provided by plasma developers), the file containing the new color scheme must have a different name than the current one, to workaround this the program creates two scheme files with different names, then applies one after the other. As a result you end up with duplicated color schemes and maybe some lag while updating schemes.

## Bug reporting / Feature requests / Contributing
Please read the [Contributing guidelines in this repository](CONTRIBUTING.md)

# Thanks & Credits
- [Avanish Subbiah](https://github.com/avanishsubbiah) for the [Python implementation](https://github.com/avanishsubbiah/material-color-utilities-python) of Material Color Utilities required by this project.
- [This comment by throwaway6560192 on Reddit](https://www.reddit.com/r/kde/comments/mg6wr4/comment/gssbtqe/?utm_source=share&utm_medium=web2x&context=3) and [@pashazz  (Pavel Borisov) ksetwallpaper](https://github.com/pashazz/ksetwallpaper) for the script to get the current Wallpaper that served me as starting point.
- Everyone that made [material-color-utilities](https://github.com/material-foundation/material-color-utilities) possible.
- [Pywal](https://github.com/dylanaraps/pywal) developers 
- [Albert Ragány-Németh](https://github.com/albi005) for the [C# implementation](https://github.com/albi005/MaterialColorUtilities) of Material Color Utilities (used until v0.8.0).
