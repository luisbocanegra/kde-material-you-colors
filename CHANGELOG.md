# Changelog

## [2.0.1](https://github.com/luisbocanegra/kde-material-you-colors/compare/v2.0.0...v2.0.1) (2025-11-30)


### Bug Fixes

* make plain text detection also work with python3-file-magic ([5de370f](https://github.com/luisbocanegra/kde-material-you-colors/commit/5de370f6169ce1b7b6831240d5f1408dd7c9193d))

## [2.0.0](https://github.com/luisbocanegra/kde-material-you-colors/compare/v1.10.1...v2.0.0) (2025-11-07)


### ⚠ BREAKING CHANGES

* Titlebar opacity requires manual enabling ([#272](https://github.com/luisbocanegra/kde-material-you-colors/issues/272))

### Features

* allow passing an image file to 'file' option ([85e3c54](https://github.com/luisbocanegra/kde-material-you-colors/commit/85e3c547ecc1dc38ac9b6d93e4f985f753c828e0))
* rename 'override_titlebar_opacity' to 'titlebar_opacity_override' ([296e00f](https://github.com/luisbocanegra/kde-material-you-colors/commit/296e00fca588aa854ebabc71bc4ad424b9f42aaa))
* Titlebar opacity requires manual enabling ([#272](https://github.com/luisbocanegra/kde-material-you-colors/issues/272)) ([b222ae6](https://github.com/luisbocanegra/kde-material-you-colors/commit/b222ae6f802d488c9731858c25d7a9744af789bc))


### Bug Fixes

* check if running in KDE and handle missing reconfigure method ([f0ee5e1](https://github.com/luisbocanegra/kde-material-you-colors/commit/f0ee5e183339eed8165a122a2e90736f9625e086))
* screenshot method not working in plasma 6.5 and later ([d28cdbd](https://github.com/luisbocanegra/kde-material-you-colors/commit/d28cdbd4a2f87247024990a2afcde89409ac8c8c))

## [1.10.1](https://github.com/luisbocanegra/kde-material-you-colors/compare/v1.10.0...v1.10.1) (2025-05-26)


### Bug Fixes

* switch back to pywal.sequences ([8d0ccba](https://github.com/luisbocanegra/kde-material-you-colors/commit/8d0ccba44be806d104d3f90e9c3abcbd7547b7ea))

## [1.10.0](https://github.com/luisbocanegra/kde-material-you-colors/compare/v1.9.3...v1.10.0) (2025-01-13)


### Features

* add manual color fetch mode ([6563415](https://github.com/luisbocanegra/kde-material-you-colors/commit/65634156efedecc754b6439f4f36ef997e6f6e2a))
* add option to enable konsole blur ([f8840ea](https://github.com/luisbocanegra/kde-material-you-colors/commit/f8840ea2c4c037654e3b09d40957e7d229f68a56))
* add project urls to about section ([682f7e9](https://github.com/luisbocanegra/kde-material-you-colors/commit/682f7e9703c2d7543456b0f5ce60a2c12b5e8eb8))
* Port from qdbus to gdbus command ([19597f6](https://github.com/luisbocanegra/kde-material-you-colors/commit/19597f664ae7f118287a2c46234b90816f6cb746))


### Bug Fixes

* keep last image for screenshot only mode [#229](https://github.com/luisbocanegra/kde-material-you-colors/issues/229) ([a6eb0be](https://github.com/luisbocanegra/kde-material-you-colors/commit/a6eb0be369e51be8315df8c853d5c01a7805da8e))
* make pywal16 export again using empty checksum ([1402a43](https://github.com/luisbocanegra/kde-material-you-colors/commit/1402a4356bac216d9a7778d4455a307d2c26a5af))
* manual fetch using previous wallpaper or running twice ([9a6cd4b](https://github.com/luisbocanegra/kde-material-you-colors/commit/9a6cd4b73c6e0fcaee2d497ff7f12478564697da))
