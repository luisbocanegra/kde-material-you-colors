# install the .desktop and rc files in the correct place
set(ENTRY_FNAME "kde-material-you-colors-screenshot-helper")
configure_file(${ENTRY_FNAME}.cmake ${CMAKE_CURRENT_BINARY_DIR}/${ENTRY_FNAME}.desktop)
install(
    PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/${ENTRY_FNAME}.desktop
    DESTINATION ${KDE_INSTALL_APPDIR}
)
