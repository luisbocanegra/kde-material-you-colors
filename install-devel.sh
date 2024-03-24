python3 -m build
pipx install dist/kde_material_you_colors-1.8.0-py3-none-any.whl

cmake -B build -S . -DCMAKE_INSTALL_PREFIX=~/.local -DINSTALL_PLASMOID=ON -DPACKAGE_PLASMOID=OFF && cmake --build build && cmake --install build
systemctl --user restart plasma-plasmashell.service
