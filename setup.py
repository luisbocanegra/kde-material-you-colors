import setuptools

DESC = (
    "Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop"
)
LDESC = open("README.md").read()

setuptools.setup(
    name="kde-material-you-colors",
    version="1.5.1",
    description=DESC,
    long_description=LDESC,
    long_description_content_type="text/markdown",
    author="Luis Bocanegra",
    author_email="luisbocanegra17b@gmail.com",
    url="https://github.com/luisbocanegra/kde-material-you-colors",
    project_urls={
        "Bug Tracker": "https://github.com/luisbocanegra/kde-material-you-colors/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes",
        "Environment :: X11 Applications :: KDE",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "dbus-python>=1.3.2",
        "numpy>=1.20",
        "material-color-utilities-python>=0.1.5",
    ],
    extras_require={"cli": ["Colr>=0.9.1", "pywal>=3.3.0"]},
    entry_points={
        "console_scripts": [
            "kde-material-you-colors=kde_material_you_colors.main:main",
        ],
    },
)
