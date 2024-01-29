cmake_minimum_required(VERSION 3.16)
set(PROJECT_NAME "plasmoid-kde-material-you")
project(${PROJECT_NAME})
option(INSTALL_PLASMOID "Install the plasmoid" ON)

# Use Extra CMake Modules (ECM) for common functionality.
# See http://api.kde.org/ecm/manual/ecm.7.html
# and http://api.kde.org/ecm/manual/ecm-kde-modules.7.html
find_package(ECM REQUIRED NO_MODULE)

# Needed by find_package(KF5Plasma) below.
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR} ${CMAKE_MODULE_PATH})

file(READ ${CMAKE_CURRENT_SOURCE_DIR}/package/metadata.json METADATA)

# Get id and version from metadata
string(JSON PLUGIN_ID GET ${METADATA} KPlugin Id)
string(JSON CUR_VERSION GET ${METADATA} KPlugin Version)

# Get version from metadata.
message("Plugin Id: ${PLUGIN_ID}")

# Get version from metadata.
message("Version: ${CUR_VERSION}")

# Locate plasma_install_package macro.
if(INSTALL_PLASMOID)
    find_package(KF5Plasma REQUIRED)
    plasma_install_package(package ${PLUGIN_ID})
endif()

if(PACKAGE_PLASMOID)
    # Genreate plasmoid file
    set(PLASMOID_FILE "${CMAKE_BINARY_DIR}/${PROJECT_NAME}-v${CUR_VERSION}.plasmoid")
    add_custom_target(plasmoid ALL
        COMMAND rm -rf "${PLASMOID_FILE}"
        COMMAND ${CMAKE_COMMAND} -E chdir ${CMAKE_CURRENT_SOURCE_DIR}/package zip -r ${PLASMOID_FILE} ./
        COMMENT "Generating ${PLASMOID_FILE}"
    )
endif()
