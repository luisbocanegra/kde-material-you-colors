# Maintainer: luisbocanegra <luis.bocanegra0 at protonmail dot com>
pkgname=kde-material-you-colors
pkgver=0.9.0
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
source=("${pkgname}-${pkgver}.tar.gz::$url/releases/download/v${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('7d3c5cd8a92cdab8bad4805cea2953c70af5bde46122d989ab316bd2b30f4992')

build() {
  cd "${pkgname}-${pkgver}"
  python -m compileall *.py
}

package() {
  cd "${pkgname}-${pkgver}"
  install -Dm644 src/kde-material-you-colors.desktop ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors.desktop
  install -Dm644 src/sample_config.conf ${pkgdir}/usr/lib/${pkgname}/sample_config.conf
  install -Dm755 src/kde-material-you-colors ${pkgdir}/usr/lib/${pkgname}/kde-material-you-colors
  find src/ -type f -name "*.py" -exec install -Dm755 {,${pkgdir}/usr/lib/${pkgname}/}{} \;
  install -dm755 ${pkgdir}/usr/bin
  ln -s /usr/lib/${pkgname}/kde-material-you-colors ${pkgdir}/usr/bin/kde-material-you-colors
  install -Dm644 LICENSE ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
}
