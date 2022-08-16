#!/bin/bash
BGreen='\033[1;32m'
clean='\033[0m'
pkgname=kde-material-you-colors

if ! [ $(id -u) = 0 ]; then
    echo "This script must be run as sudo or root, try again..."
    exit 1
fi;

echo -e "${BGreen}Installing dependencies${clean}"
dnf update
dnf install python3 python3-dbus python3-numpy python3-pillow python3-pip

echo -e "${BGreen}Installing python PIP package material_color_utilities_python as user $SUDO_USER ${clean}"

sudo -u $SUDO_USER pip3 install monet/material_color_utilities_python-0.1.0-py3-none-any.whl

echo -e "${BGreen}Installing kde-material-you-colors${clean}"
# Cleanup
rm -rf /usr/lib/${pkgname}

mkdir -p /usr/lib/${pkgname}
cp -f *.{py,conf,desktop} /usr/lib/${pkgname}/
cp -f kde-material-you-colors /usr/lib/${pkgname}/kde-material-you-colors
chmod 755 /usr/lib/${pkgname}/*.py

mkdir -p /usr/share/licenses/kde-material-you-colors/
cp -f LICENSE /usr/share/licenses/${pkgname}/LICENSE
chmod 664 /usr/share/licenses/${pkgname}/LICENSE
chmod 664 /usr/lib/${pkgname}/*.{desktop,conf}

chmod 755 /usr/lib/${pkgname}/kde-material-you-colors
ln -sf /usr/lib/${pkgname}/kde-material-you-colors /usr/bin/kde-material-you-colors

