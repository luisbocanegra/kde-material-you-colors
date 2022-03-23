# Maintainer: luisbocanegra <luis.bocanegra0@protonmail.com>
pkgname=kde-material-you-colors
pkgver=0.0.1
pkgrel=1
pkgdesc="Automatic KDE Material You Colors Generator from your wallpaper"
arch=('x86_64')
url="https://github.com/luisbocanegra/kde-material-you-colors"
license=('APACHE')
depends=("skia-sharp" "dbus-python" "python-numpy")
options=('!strip')
source=("${pkgname}-${pkgver}.tar.gz::$url/archive/v${pkgver}.tar.gz")
sha256sums=('20f31708155aec3fe02e4cdd8c4f14fdaa360ae5d3358562f5b18773afc05789')

build() {
  cd "${pkgname}-${pkgver}"
  python -m compileall *.py
}

package() {
  cd "${pkgname}-${pkgver}"
  install -Dm644 kde-material-you-colors.service ${pkgdir}/usr/lib/systemd/user/kde-material-you-colors.service
  install -Dm755 kde-material-you-colors.py ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors.py
  install -Dm755 kde-material-you-colors ${pkgdir}/usr/bin/kde-material-you-colors
  install -Dm755 color_scheme.py ${pkgdir}/usr/lib/${pkgname}/color_scheme.py
  install -Dm755 color_utils.py ${pkgdir}/usr/lib/${pkgname}/color_utils.py
  install -Dm755 schemeconfigs.py ${pkgdir}/usr/lib/${pkgname}/schemeconfigs.py
  install -Dm755 material-color-utility-bin ${pkgdir}/usr/lib/${pkgname}/material-color-utility-bin
  ln -s /usr/lib/${pkgname}/material-color-utility-bin ${pkgdir}/usr/bin/material-color-utility
  install -Dm644 LICENSE ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
}
