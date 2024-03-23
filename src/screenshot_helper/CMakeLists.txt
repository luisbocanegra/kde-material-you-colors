cmake_minimum_required(VERSION 3.16)
set(CMAKE_C_STANDARD 99)

set(PROJECT_NAME "kde-material-you-colors-screenshot-helper")

project("${PROJECT_NAME}" VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(KDE_COMPILERSETTINGS_LEVEL "5.82")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


find_package(Qt6 REQUIRED COMPONENTS DBus Gui)

include(KDEInstallDirs)
include(KDECMakeSettings)

set(PROJECT_SOURCES
    main.cpp
)
add_subdirectory(desktop)

add_executable("${PROJECT_NAME}"
    ${PROJECT_SOURCES}
)

target_link_libraries("${PROJECT_NAME}" PRIVATE Qt6::DBus Qt6::Gui)

install(TARGETS "${PROJECT_NAME}"
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
