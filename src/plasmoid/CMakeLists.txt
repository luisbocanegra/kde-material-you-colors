set(PROJECT_NAME "plasmoid-kde-material-you")
project(${PROJECT_NAME})
file(READ ${CMAKE_CURRENT_SOURCE_DIR}/package/metadata.json METADATA)

# Get id and version from metadata
string(JSON PLUGIN_ID GET ${METADATA} KPlugin Id)
string(JSON CUR_VERSION GET ${METADATA} KPlugin Version)

# Get version from metadata.
message("Plugin Id: ${PLUGIN_ID}")

# Get version from metadata.
message("Version: ${CUR_VERSION}")

if(INSTALL_PLASMOID)
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
