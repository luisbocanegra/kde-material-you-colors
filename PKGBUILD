# Maintainer: luisbocanegra <luis.bocanegra0 at protonmail dot com>
pkgname=kde-material-you-colors
pkgver=1.5.1
pkgrel=1
pkgdesc="Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop"
arch=('x86_64')
url="https://github.com/luisbocanegra/kde-material-you-colors"
license=('GPL3')
depends=("dbus-python" "python-numpy" "python-material-color-utilities")
optdepends=('python-colr: colored hex codes printing'
            'python-pywal: theme other programs using Material You Colors'
)

source=("${pkgname}-${pkgver}.zip::$url/releases/download/v${pkgver}/${pkgname}-${pkgver}.zip")
sha256sums=('bfa3438b434a66ad6b48a024e408a9208edc82a9435fa0190b8324977ad8feed')

package() {
  cd "${pkgname}-${pkgver}"
  install -dm755 ${pkgdir}/usr/lib/${pkgname}/utils
  install -dm755 ${pkgdir}/usr/share/applications/

  install -Dm644 src/*.{py,conf} ${pkgdir}/usr/lib/${pkgname}/
  install -Dm644 src/utils/*.py ${pkgdir}/usr/lib/${pkgname}/utils
  install -Dm644 src/*.desktop ${pkgdir}/usr/share/applications/
  install -Dm755 src/kde-material-you-colors ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors
  install -dm755 ${pkgdir}/usr/bin

  ln -s /usr/lib/${pkgname}/kde-material-you-colors ${pkgdir}/usr/bin/kde-material-you-colors
  install -Dm644 LICENSE ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
}
