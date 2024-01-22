cmake_minimum_required(VERSION 3.16)
set(CMAKE_C_STANDARD 99)

set(PROJECT_NAME "kde-material-you-colors-screenshot-helper")

project("${PROJECT_NAME}" VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(QT_MIN_VERSION "5.15.2")
set(KF5_MIN_VERSION "5.102.0")
set(KDE_COMPILERSETTINGS_LEVEL "5.82")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ECM ${KF5_MIN_VERSION} REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

find_package(Qt5 REQUIRED COMPONENTS DBus)
find_package(KF5WindowSystem REQUIRED)

include(KDEInstallDirs)
include(KDECMakeSettings)

set(PROJECT_SOURCES
    src/screenshot_helper/main.cpp
)
add_subdirectory(src/screenshot_helper/desktop)

add_executable("${PROJECT_NAME}"
    ${PROJECT_SOURCES}
)

target_link_libraries("${PROJECT_NAME}" PRIVATE Qt5::DBus KF5::WindowSystem)

install(TARGETS "${PROJECT_NAME}"
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
