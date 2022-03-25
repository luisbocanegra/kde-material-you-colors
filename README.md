# KDE Material You Colors (beta)
### Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop

This is a Python program that uses the [C# implementation](https://github.com/albi005/MaterialColorUtilities) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) by @albi005, to extract a color from an image and then generate a Material Design 3 color scheme. Which is used to generate both Light and Dark Color Themes for KDE.
<div>
</img>
<img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></img>
<img src=https://img.shields.io/badge/Maintained%3F-yes-green.svg></img>
<img src=https://img.shields.io/badge/Status-beta-red.svg></img>
<img src="https://img.shields.io/github/repo-size/luisbocanegra/kde-material-you-colors?label=size&style=plasticr"></img>
</div>
<div>
<img src="Screenshot.png"  alt="Screenshot">
</div>

### Video demo:
https://user-images.githubusercontent.com/15076387/159639387-d0a52b1e-ab67-431d-bee0-a7461cdfe408.mp4

# Installing:
### Arch Linux:
```sh 
mkdir kde-material-you-colors 
cd kde-material-you-colors
curl https://raw.githubusercontent.com/luisbocanegra/kde-material-you-colors/main/PKGBUILD --output PKGBUILD
makepkg -si
```
### Ubuntu based:
```sh
git clone https://github.com/luisbocanegra/kde-material-you-colors
cd kde-material-you-colors
chmod +x ubuntu-based-install.sh
sudo ./ubuntu-based-install.sh
```
<span style="color:#ff6568"> **You may need to update to latest Plasma 5.24 due to a BUG related to [this one](https://bugs.kde.org/show_bug.cgi?id=445058) that blocks this program from getting the current wallpaper.** </span>

# Usage:
- Run `kde-material-you-colors` from terminal, if you use the default wallpaper plugin on your main screen (0) this should change your Desktop colors right after.
- If you use a multimonitor setup and want your wallpaper from other screen or use a different wallpaper plugin find your desired configuration by experimenting with the following:

### Options
`--monitor, -m [NUMBER]`&emsp; Monitor to get wallpaper (default is 0) but second one is 6 in my case, play with this to find yours

`--plugin -p [ID]`&emsp; Wallpaper plugin id (default is org.kde.image) you can find them in: /usr/share/plasma/wallpapers/ or /.local/share/plasma/wallpapers

`--file -f [ABSOLUTE_PATH]`&emsp; Text file that contains wallpaper absolute path (Takes precedence over the above options)

`--light -l`&emsp; Enable Light mode (default is Dark)

`--dark -d`&emsp; Enable Dark mode (ignores user config)

`--autostart -a`&emsp; Enable (copies) the startup script to automatically start with KDE

`--copyconfig -c` Copies the default config to ~/.config/kde-material-you-colors/config.conf

# Configuration:
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
# Default is org.kde.image
plugin = org.kde.image

# File containing absolute path of a image (Takes precedence over the above options as they are no longer needed)
# Commented out by default
#file = /absolute/path/of/some/wallpaper

# Enable Light mode
# Default is False
light = False
```
Save the sample configuration to `~/.config/kde-material-you-colors/config.conf`

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
