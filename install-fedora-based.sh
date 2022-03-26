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
dnf install python3 python3-dbus python3-numpy

echo -e "${BGreen}Installing kde-material-you-colors${clean}"
mkdir -p /usr/lib/${pkgname}
cp -f *.{py,conf,desktop} /usr/lib/${pkgname}/
cp -f kde-material-you-colors /usr/bin/kde-material-you-colors
cp -f material-color-utility-bin /usr/lib/${pkgname}/material-color-utility-bin
cp -f libSkiaSharp.so /usr/lib/${pkgname}/libSkiaSharp.so
chmod 755 /usr/lib/${pkgname}/*.py

mkdir -p /usr/share/licenses/kde-material-you-colors/
cp -f LICENSE /usr/share/licenses/${pkgname}/LICENSE
chmod 664 /usr/share/licenses/${pkgname}/LICENSE
chmod 664 /usr/lib/${pkgname}/*.{desktop,conf}

chmod 755 /usr/bin/kde-material-you-colors
chmod 755 /usr/lib/${pkgname}/material-color-utility-bin
chmod 755 /usr/lib/${pkgname}/libSkiaSharp.so
ln -sf /usr/lib/${pkgname}/material-color-utility-bin /usr/bin/material-color-utility
