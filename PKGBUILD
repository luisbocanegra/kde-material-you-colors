# Maintainer: luisbocanegra <luis.bocanegra0 at protonmail dot com>
pkgname=kde-material-you-colors
pkgver=0.8.0
pkgrel=1
pkgdesc="Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop"
arch=('x86_64')
url="https://github.com/luisbocanegra/kde-material-you-colors"
license=('GPL3')
depends=("dbus-python" "python-numpy" "python-pillow" "python-regex" "python-material-color-utilities")
optdepends=('python-colr: colored hex codes printing'
            'python-pywal: theme other programs using Material You Colors'
)
options=('!strip')
source=("${pkgname}-${pkgver}.tar.gz::$url/archive/v${pkgver}.tar.gz")
sha256sums=('72bd590acb3e5132833fabd2991833556fbfb9034dd6b21f09e420b68b9cf4da')

build() {
  cd "${pkgname}-${pkgver}"
  python -m compileall *.py
}

package() {
  cd "${pkgname}-${pkgver}"
  install -Dm644 kde-material-you-colors.desktop ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors.desktop
  install -Dm644 sample_config.conf ${pkgdir}/usr/lib/${pkgname}/sample_config.conf
  install -Dm755 kde-material-you-colors ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors
  find . -type f -name "*.py" -exec install -Dm755 {,${pkgdir}/usr/lib/${pkgname}/}{} \;
  install -dm755 ${pkgdir}/usr/bin
  ln -s /usr/lib/${pkgname}/kde-material-you-colors ${pkgdir}/usr/bin/kde-material-you-colors
  install -Dm644 LICENSE ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
}
