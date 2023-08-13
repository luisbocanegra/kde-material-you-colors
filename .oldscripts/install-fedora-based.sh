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

install -dm755 ${pkgdir}/usr/lib/${pkgname}/utils
install -dm755 ${pkgdir}/usr/share/applications/

install -Dm644 src/*.{py,conf} ${pkgdir}/usr/lib/${pkgname}/
install -Dm644 src/utils/*.py ${pkgdir}/usr/lib/${pkgname}/utils/
install -Dm644 src/*.desktop ${pkgdir}/usr/share/applications/
install -Dm755 src/kde-material-you-colors ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors
install -dm755 ${pkgdir}/usr/bin

ln -sf /usr/lib/${pkgname}/kde-material-you-colors ${pkgdir}/usr/bin/kde-material-you-colors
install -Dm644 LICENSE ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
