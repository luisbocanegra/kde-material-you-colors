cmake_minimum_required(VERSION 3.16)
set(PROJECT_NAME "kde-material-you-colors")
project(${PROJECT_NAME})
option(INSTALL_PLASMOID "Install plasmoid" OFF)
option(PACKAGE_PLASMOID "Package plasmoid" OFF)

set(PROJECT_DEP_VERSION "6.0.0")
set(QT_MIN_VERSION "6.6.0")
set(KF6_MIN_VERSION "6.0.0")
set(KDE_COMPILERSETTINGS_LEVEL "5.85")

find_package(ECM ${KF6_MIN_VERSION} REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)

if(INSTALL_PLASMOID)
    find_package(Plasma5Support ${PROJECT_DEP_VERSION} REQUIRED)
    find_package(Plasma ${PROJECT_DEP_VERSION} REQUIRED)
endif()

add_subdirectory(src/screenshot_helper)
add_subdirectory(src/plasmoid)
