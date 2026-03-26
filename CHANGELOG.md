# Changelog

## [2.2.0](https://github.com/luisbocanegra/kde-material-you-colors/compare/v2.1.0...v2.2.0) (2026-03-26)


### Features

* tint KDE Rounded Corners effect window outline ([ba906b4](https://github.com/luisbocanegra/kde-material-you-colors/commit/ba906b4de9d1f8b82a8de50ab357c45b72e376d6))


### Bug Fixes

* use correct default contrast values ([a6d1c2d](https://github.com/luisbocanegra/kde-material-you-colors/commit/a6d1c2d513bf4cc4d85eb4eec130cac69edf8452))
* widget doesn't create configuration file ([652a55a](https://github.com/luisbocanegra/kde-material-you-colors/commit/652a55a95b39e1e0c3f909ceed184c7a821397f7))

## [2.1.0](https://github.com/luisbocanegra/kde-material-you-colors/compare/v2.0.2...v2.1.0) (2026-03-23)


### Features

* add wallpaper and config to json file ([b947110](https://github.com/luisbocanegra/kde-material-you-colors/commit/b94711066c796b1c6d12d2cac5261bb52f51fbb0))
* colors preview in widget ([f9ff715](https://github.com/luisbocanegra/kde-material-you-colors/commit/f9ff715ba8fdf81810fd85285d01875f8a4e4a5e))
* contrast level ([a8a9ec4](https://github.com/luisbocanegra/kde-material-you-colors/commit/a8a9ec495bc4637fa9e86b1e3353edae8f2ed47f))
* frames and outlines contrast ([55ba059](https://github.com/luisbocanegra/kde-material-you-colors/commit/55ba059cf4566be97101041a674396e1c5beb1f3))
* material specification version configuration ([e27f1fa](https://github.com/luisbocanegra/kde-material-you-colors/commit/e27f1fa6e8bff4de37bce32c05b7d434b939c77f))
* update klassy decoration outline color ([c354ba7](https://github.com/luisbocanegra/kde-material-you-colors/commit/c354ba7c5fbfa901d153831dee8bb820a434d661))


### Bug Fixes

* backend running check with long user names ([5064335](https://github.com/luisbocanegra/kde-material-you-colors/commit/5064335c2b1a584936d23622bd85d048f66b3882))
* duplicate custom colors in json output ([679c68e](https://github.com/luisbocanegra/kde-material-you-colors/commit/679c68ea2b1391937bb64028d2d06a0c42be8c5f))
* ensure sections exist in klassy configuration ([006d5ef](https://github.com/luisbocanegra/kde-material-you-colors/commit/006d5ef9d155b1ffaaf13589cd6a167f57f3675f))
* klassy 6.5 decoration outline color ([02617bd](https://github.com/luisbocanegra/kde-material-you-colors/commit/02617bd1aaf3ee0b15503691bf39d62dc382f95b))
* port away from deprecated Qt.labs.settings ([0c79646](https://github.com/luisbocanegra/kde-material-you-colors/commit/0c79646331bc12f8b39772a119d1100e79e27c45))

## [2.0.2](https://github.com/luisbocanegra/kde-material-you-colors/compare/v2.0.1...v2.0.2) (2025-11-30)


### Bug Fixes

* remove debug prints ([330cf0a](https://github.com/luisbocanegra/kde-material-you-colors/commit/330cf0aa0439048914d857620a1938a0e454024f))

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
