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
dnf install python3 python3-dbus python3-numpy python3-pillow python3-pip python3-regex

echo -e "${BGreen}Installing python PIP package material-color-utilities-python as user $SUDO_USER ${clean}"

pip3 install material-color-utilities-python

echo -e "${BGreen}Installing kde-material-you-colors${clean}"
# Cleanup
rm -rf /usr/lib/${pkgname}

mkdir -p /usr/lib/${pkgname}
cp -f src/*.{py,conf,desktop} /usr/lib/${pkgname}/
cp -f src/*.desktop /usr/share/applications/
cp -f src/kde-material-you-colors /usr/lib/${pkgname}/kde-material-you-colors
chmod 755 /usr/lib/${pkgname}/*.py

mkdir -p /usr/share/licenses/kde-material-you-colors/
cp -f LICENSE /usr/share/licenses/${pkgname}/LICENSE
chmod 664 /usr/share/licenses/${pkgname}/LICENSE
chmod 664 /usr/lib/${pkgname}/*.{desktop,conf}

chmod 755 /usr/lib/${pkgname}/kde-material-you-colors
ln -sf /usr/lib/${pkgname}/kde-material-you-colors /usr/bin/kde-material-you-colors

