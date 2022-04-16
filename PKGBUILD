# Maintainer: luisbocanegra <luis.bocanegra0 at protonmail dot com>
pkgname=kde-material-you-colors
pkgver=0.4.0BETA
pkgrel=1
pkgdesc="Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop"
arch=('x86_64')
url="https://github.com/luisbocanegra/kde-material-you-colors"
license=('APACHE')
depends=("dbus-python" "python-numpy")
optdepends=('python-colr: colored hex codes printing'
            'python-pywal: theme other programs using Material You Colors'
)
options=('!strip')
source=("${pkgname}-${pkgver}.tar.gz::$url/archive/v${pkgver}.tar.gz")
sha256sums=('7e8408dbd92a6ef71de8ce16d0162e35e2650a5853b02aecc033e1047320dec2')

build() {
  cd "${pkgname}-${pkgver}"
  python -m compileall *.py
}

package() {
  cd "${pkgname}-${pkgver}"
  install -Dm644 kde-material-you-colors.desktop ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors.desktop
  install -Dm644 sample_config.conf ${pkgdir}/usr/lib/${pkgname}/sample_config.conf
  install -Dm755 kde-material-you-colors.py ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors.py
  install -Dm755 kde-material-you-colors ${pkgdir}/usr/bin/kde-material-you-colors
  install -Dm755 color_utils.py ${pkgdir}/usr/lib/${pkgname}/color_utils.py
  install -Dm755 utils.py ${pkgdir}/usr/lib/${pkgname}/utils.py
  install -Dm755 schemeconfigs.py ${pkgdir}/usr/lib/${pkgname}/schemeconfigs.py
  install -Dm755 material-color-utility-bin ${pkgdir}/usr/lib/${pkgname}/material-color-utility-bin
  install -Dm755 libSkiaSharp.so ${pkgdir}/usr/lib/${pkgname}/libSkiaSharp.so
  ln -s /usr/lib/${pkgname}/material-color-utility-bin ${pkgdir}/usr/bin/material-color-utility
  install -Dm644 LICENSE ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
}

