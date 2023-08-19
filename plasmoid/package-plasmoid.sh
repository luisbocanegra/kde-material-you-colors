#!/bin/sh

# Remove the build directory if it exists
if [ -d "build" ]; then
    rm -rf build
fi

# Create a new build directory
mkdir build
cd build

# skip building/installing
cmake -DINSTALL_PLASMOID=OFF -DCMAKE_BUILD_TYPE=Release ..

# package the plasmoid file
make plasmoid
