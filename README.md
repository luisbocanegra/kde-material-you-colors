# KDE Material You Colors
### Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop

This is a Python program that uses the [C# implementation](https://github.com/material-foundation/material-color-utilities) of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) by @albi005, to extract a color from an image and then generate a Material Design 3 color scheme. Which is used to Generate both Light and Dark Color Themes for KDE.
<div>
</img>
<img src="https://img.shields.io/badge/Made%20with-Ptython-1f425f.svg"></img>
<img src=https://img.shields.io/badge/Maintained%3F-yes-green.svg></img>
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
git clone https://github.com/luisbocanegra/kde-material-you-colors
cd kde-material-you-colors
makepkg -si
```
### Building instructions:
`Soon™`

# Usage:
Run `kde-material-you-colors` from terminal
### Options
`--monitor, -m`&emsp; Monitor to get wallpaper (default is 0)

`--light -l`&emsp; Enable Light mode (default is Dark)

`--dark -d`&emsp; Enable Dark mode (override user config)

`--plugin -p`&emsp; Wallpaper plugin id (default is org.kde.image) you can find them in: /usr/share/plasma/wallpapers/ or /.local/share/plasma/wallpapers
`--file -f`&emsp; Text file that contains wallpaper absolute path (Takes precedence over all the other options)

# Configuration:
```ini
[CUSTOM]
# File containing absolute path (Takes precedance over all the other as they are not needed)
#file = /tmp/000_eDP-1_current_wallpaper

# Use light scheme (True or False)
light = False

# Screen? containment number (Integer)
monitor = 1

# Wallpaper plugin id (string)
plugin = org.kde.images
```
Save the sample configuration to `/home/luis/.config/kde-material-you-colors/config.conf`

And `kde-material-you-colors` with no arguments from terminal to test it.

# Start on login with systemd
After testing your configuration you can enable the user service to start on login:
``systemctl enable --user kde-material-you-colors.service``