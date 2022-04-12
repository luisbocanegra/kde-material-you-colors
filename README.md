# KDE Material You Colors (beta)
### Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop

This is a Python program that uses the [C# implementation](https://github.com/albi005/MaterialColorUtilities) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) by @albi005, to extract a color from an image and then generate a Material Design 3 color scheme. Which is used to generate both Light and Dark Color Themes for KDE.
<div>
</img>
<img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></img>
<img src=https://img.shields.io/badge/Maintained%3F-yes-green.svg></img>
<img src=https://img.shields.io/badge/Status-beta-red.svg></img>
</div>
<div>
<img src="https://user-images.githubusercontent.com/15076387/162865773-a7e2c4b3-b3a0-4d32-8ac3-8204b7ed0140.png"  alt="Screenshot">
</div>

### Video demo:

https://user-images.githubusercontent.com/15076387/162865563-2784fa53-7cc9-4817-9151-df2df42d957d.mp4


# Features
- Update automatically on wallpaper change
- Configurarion file
- Support for selecting Wallpaper plugin from seconday monitors (check Configuration section)
- Alternative Material You color (mostly random)
- Dark an Light Color schemes
- Dark and Light Icon theme
- Multiple wallpaper plugins supported

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
3. OPTIONAL
- Install the [Colr](https://pypi.org/project/Colr/) python module to display colored seed colors from terminal

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
# Commented out by default
#file = /tmp/000_eDP-1_current_wallpaper

# Enable Light mode
# Default is False
light = False

# Alternative color mode (default is 0), some images return more than one color, this will use either the matched or last color
# Default is 0
ncolor = 0

# Light scheme icons 
#iconslight = Papirus-Light

# Dark scheme icons 
#iconsdark = Papirus-Dark

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
- [@albi005 (Albert Ragány-Németh)](https://github.com/albi005) for the [C# implementation](https://github.com/albi005/MaterialColorUtilities) of Material Color Utilities which I found the easiest to work with.
- [This comment by throwaway6560192 on Reddit](https://www.reddit.com/r/kde/comments/mg6wr4/comment/gssbtqe/?utm_source=share&utm_medium=web2x&context=3) and [@pashazz  (Pavel Borisov) ksetwallpaper](https://github.com/pashazz/ksetwallpaper) for the script to get the current Wallpaper that served me as starting point.
- Everyone that made [material-color-utilities](https://github.com/material-foundation/material-color-utilities) possible.
