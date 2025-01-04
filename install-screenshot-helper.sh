#!/bin/sh
if [ -d "build" ]; then
    rm -rf build
fi

# remove local install
rm -f ~/.local/share/applications/kde-material-you-colors-screenshot-helper.desktop ~/.local/bin/kde-material-you-colors-screenshot-helper

cmake -B build -S . -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build
sudo cmake --install build
