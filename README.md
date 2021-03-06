# KDE Material You Colors
### Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop

This is a Python program that uses the [C# implementation](https://github.com/albi005/MaterialColorUtilities) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) by @albi005, to extract a color from an image and then generate a Material Design 3 color scheme. Which is used to generate both Light and Dark Color Themes for KDE.
<div>
</img>
<img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></img>
<img src=https://img.shields.io/badge/Maintained%3F-yes-green.svg></img>
</div>
<div>
<img src="https://user-images.githubusercontent.com/15076387/163059211-e5e56e10-e841-487e-83ea-60a97497bd6e.png"  alt="Screenshot">
</div>


### Video demo:

https://user-images.githubusercontent.com/15076387/163064257-c3e9c50e-6728-4e9f-b594-83b80436c802.mp4


# Features
- Update automatically on wallpaper change
- Configurarion file
- Support for selecting Wallpaper plugin from seconday monitors (check Configuration section)
- Alternative Material You color selection
- Dark an Light Color schemes
- Dark and Light Icon theme
- Multiple wallpaper plugins supported
- [Pywal](https://github.com/dylanaraps/pywal) support to theme other programs using Material You Colors (Experimental)
- Tint [SierraBreeze](https://github.com/kay0u/SierraBreeze) decoration buttons
- Dynamically update Konsole color scheme (check Configuration section for instructions)

# Installing:
### Arch Linux:
- [AUR](https://aur.archlinux.org/packages/kde-material-you-colors)
### Other distributions
1. Clone/download this repository and cd to it
```sh
git clone https://github.com/luisbocanegra/kde-material-you-colors
cd kde-material-you-colors
```
2. Make the installer executable and run it as root
- For Ubuntu based distros:
```sh
chmod +x install-ubuntu-based.sh
sudo ./install-ubuntu-based.sh
```
- For Fedora based distros:
```sh
chmod +x install-fedora-based.sh
sudo ./install-fedora-based.sh
```
### Optional features
- Install the [Colr](https://pypi.org/project/Colr/) python module to display colored palette and seed colors from terminal
- Install the [pywal](https://pypi.org/project/pywal/) python module to theme other programs using Material You Colors
  - Check [pywal Customization Wiki](https://github.com/dylanaraps/pywal/wiki/Customization) for scripts to theme supported programs 

<span style="color:#ff6568"> **You may need to update to latest Plasma 5.24 due to a BUG related to [this one](https://bugs.kde.org/show_bug.cgi?id=445058) that blocks this program from getting the current wallpaper.** </span>


# Running from terminal
- Run `kde-material-you-colors` from terminal, if you use the default wallpaper plugin on your main screen (0) this should change your Desktop colors right after.


**NOTE:** your wallpaper will be reset to Image Wallpaper Plugin

- If you use a multimonitor setup and want your wallpaper from other screen or use a different wallpaper plugin find your desired configuration by experimenting with the following:

### Options
`--monitor, -m [NUMBER]`&emsp; Monitor to get wallpaper (default is 0) but second one is 6 in my case, play with this to find yours

`--plugin -p [ID]`&emsp; Wallpaper plugin id (default is org.kde.image) you can find them in: /usr/share/plasma/wallpapers/ or /.local/share/plasma/wallpapers

`--file -f [ABSOLUTE_PATH]`&emsp; Text file that contains wallpaper absolute path (Takes precedence over the above options)

`--ncolor -n [NUMBER]`&emsp; Alternative color mode (default is 0), some images return more than one color, this will use either the matched or last one

`--light -l`&emsp; Enable Light mode (default is Dark)

`--dark -d`&emsp; Enable Dark mode (ignores user config)

`--autostart -a`&emsp; Enable (copies) the startup script to automatically start with KDE

`--copyconfig -c`&emsp; Copies the default config to ~/.config/kde-material-you-colors/config.conf

`--iconslight [ICONS-NAME]`&emsp; Icons for Dark scheme

`--iconsdark [ICONS-NAME]`&emsp; Icons for Light scheme

`--pywallight -wall`&emsp; Use pywal Light scheme

`--pywaldark -wald`&emsp; Use pywal Dark scheme

`--lbmultiplier [NUMBER], -lbm [NUMBER]`&emsp; The amount of color for backgrounds in Light mode (value from 0 to 4.0, default is 1)

`--dbmultiplier [NUMBER], -dbm [NUMBER]`&emsp; The amount of color for backgrounds in Dark mode (value from 0 to 4.0, default is 1)

`--on-change-hook [COMMAND]`&emsp; A script/command that will be executed on start or wallpaper/dark/light/settings change

`--sierra-breeze-buttons-color, -sbb`&emsp; Tint Sierra Breeze decoration buttons

`--konsole-profile [KONSOLE_PROFILE], -kp [KONSOLE_PROFILE]`&emsp; The name of your (existing) Konsole profile that is going to be themed, you can check your current profiles with konsole  --list-profiles

`--sbe-titlebar-opacity [OPACITY], -sbeto [OPACITY]`&emsp; Sierra Breeze Enhanced titlebar opacity (value from 0 to 100, default is None)

`--toolbar-opacity [OPACITY], -to [OPACITY]`&emsp; ToolBar opacity, needs Lightly Application Style (value from 0 to 100,
                        default is None)

`--konsole-opacity [OPACITY], -ko [OPACITY]`&emsp; Konsole background opacity (value from 0 to 100, default is None)

# Startup script:

1. Copy the default configuration to ~/.config/kde-material-you-colors/config.conf:

`kde-material-you-colors -c` 

2. Enable script to automatically start with Plasma:

`kde-material-you-colors -a` 

3. Reboot or logout/login to see the changes,

**NOTE:** your wallpaper will be reset to Image Wallpaper Plugin

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

# Configuration:

Open ~/.config/kde-material-you-colors/config.conf


```ini
[CUSTOM]
# INSTRUCTIONS
# Run kde-material-you-colors with no arguments from terminal
# to debug your configuration changing in real time.
# NOTE: 
# Any argument passed from the command line overrides their counterpart here.

# Monitor to get wallpaper from 
# For me main is 0 but second one is 6, play with this to find yours
# Default is 0
monitor = 0

# Wallpaper plugin id you can find them in: /usr/share/plasma/wallpapers/ 
# or /.local/share/plasma/wallpapers for user installed.

# below are some working wallpaper plugins
# Default:                 org.kde.image
# Picture of the day is:   org.kde.potd
# Slideshow:               org.kde.slideshow
# Plain color:             org.kde.color
plugin = org.kde.image

# File containing absolute path of an image (Takes precedence over the above options as they are no longer needed)
# Commented by default
#file = /tmp/000_eDP-1_current_wallpaper

# Enable Light mode
# Accepted values are True or False
# Default is False
# Comment out to follow System Color Setting instead  (MaterialYou schemes only)
light = False

# Alternative color mode (default is 0), some images return more than one color, this will use either the matched or last color
# Default is 0
ncolor = 0

# Light scheme icons 
# Commented by default
#iconslight = Papirus-Light

# Dark scheme icons 
# Commented by default
#iconsdark = Papirus-Dark

# Use pywal to theme other programs using Material You colors
# https://github.com/dylanaraps/pywal/wiki/Customization
# You need to install pywal python module first
# Accepted values are True or False
# Commented by default
#pywal=True

# Force light/dark mode for pywal and/or Konsole
# Accepted values are True or False comment out to dark/light scheme 
# Commented by default (Follows light option above)
# NOTE:
# Theming konsole only doesn't require pywal, just setting konsole_profile below
#pywal_light = False

# The amount of perceptible color for backgrounds in dark mode
# A number between 0 and 4.0 (limited for accessibility purposes)
# Defaults to 1 if not set
#light_blend_multiplier = 1.0

# The amount of perceptible color for backgrounds in dark mode
# A number between 0 and 4.0 (limited for accessibility purposes)
# Defaults to 1 if not set
#dark_blend_multiplier = 1.0

# A script/command that will be executed on start or wallpaper/dark/light/settings change
# example below using https://github.com/vlevit/notify-send.sh to send a desktop notification:
#on_change_hook = notify-send.sh "kde-material-you-colors" "This is a test" -t 2000

# Tint Sierra Breeze decoration buttons https://github.com/kay0u/SierraBreeze
# Accepted values are True or False
# Default is False
# NOTE:
# This WILL OVERWRITE any set colors and reload KWin (screen will blink on x11)
#sierra_breeze_buttons_color = True

# Dynamically updated Konsole color scheme
# Accepted value is the name of your current Konsole profile, except TempMyou and Default profile as is read only
# Default is commented (disabled)
# NOTE:
# This makes a temp profile named TempMyou.profile and MaterialYou/MaterialYouAlt color schemes to switch between them automatically in all open Konsole instances
# You can make direct changes to your profile, but for the color scheme edit MaterialYou one
# WARNING: 
# I recommend you to backup the ~/.local/share/konsole/ folder before trying this because it will edit your profiles 
#konsole_profile = Profile 1

# Konsole background opacity 
# An integer between 0 and 100
# Default is commented (disabled)
#konsole_opacity = 75

# Sierra Breeze Enhanced Title Bar opacity https://github.com/kupiqu/SierraBreezeEnhanced
# An integer between 0 and 100
# Default is commented (disabled)
# NOTE:
# This will reload KWin (screen will blink on x11)
#sbe_titlebar_opacity = 50

# ToolBar opacity needs Lightly Application Style to work https://github.com/Luwx/Lightly
# An integer between 0 and 100
# Default is commented (disabled)
# NOTE:
# kirigami ToolBar opacity is not affected by this option https://github.com/Luwx/Lightly/issues/128
#toolbar_opacity = 75
```

And run `kde-material-you-colors` with no arguments from terminal to test it.

# Removing the autostart script
1. Open `System Settings` > `Startup and Shutdown`
2. Remove `kde-material-you-colors` by clicking on the `-` button.

&emsp;&emsp;**OR** Manually delete ~/.config/autostart/kde-material-you-colors.desktop

3. Logout/Reboot

# Bugs
- As throwaway6560192 pointed out, the `evaluateScript` DBus call doesn't return any output, to get the current wallpaper, I'm using `print()`, but the journal gets spammed by plasmashell with the wallpaper path. If you know a better way of doing this please tell me.
- To update color with `plasma-apply-colorscheme`, the file containing the new color scheme must have a different name than the current one, to workaround this it creates two scheme files with different names, then applies one after the other. As a result you end up with duplicated color schemes and maybe some lag while updating schemes.
- If you encounter a problem (sure there will be) don't hesitate to open an issue.
- This is not a bug but I'm a noob developer, so expect spaggeti code, PRs to improve it are very wellcomed.

# Thanks & Credits
- [@albi005 (Albert Rag??ny-N??meth)](https://github.com/albi005) for the [C# implementation](https://github.com/albi005/MaterialColorUtilities) of Material Color Utilities which I found the easiest to work with.
- [This comment by throwaway6560192 on Reddit](https://www.reddit.com/r/kde/comments/mg6wr4/comment/gssbtqe/?utm_source=share&utm_medium=web2x&context=3) and [@pashazz  (Pavel Borisov) ksetwallpaper](https://github.com/pashazz/ksetwallpaper) for the script to get the current Wallpaper that served me as starting point.
- Everyone that made [material-color-utilities](https://github.com/material-foundation/material-color-utilities) possible.
- [Pywal](https://github.com/dylanaraps/pywal) developers 
