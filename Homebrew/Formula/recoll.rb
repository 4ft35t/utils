require 'formula'

# Notes:
# - This formula is missing python-libxml2 and python-libxslt deps
#   which recoll needs for indexing many formats (e.g. libreoffice,
#   openxml). Homebrew does not include these packages.
#   So the user needs to install them with pip because I don't understand how
#   the "Resource" homebrew thing works.
# Still a bit of work then, but I did not investigate, because the macports
# version was an easier target.

class Recoll < Formula
  desc "Desktop search tool"
  homepage 'http://www.recoll.org'
  url 'https://www.lesbonscomptes.com/recoll/recoll-1.31.2.tar.gz'
  sha256 "d3edb28fa76f2bb15e6555f82ef74e9151a2271535d3fdeb5f34012b1c2c3c54"

  depends_on "xapian"
  depends_on "qt@5"
  depends_on "antiword"
  depends_on "poppler"
  depends_on "unrtf"

  def install
    # homebrew has webengine, not webkit and we're not ready for this yet
    system "./configure", "--disable-python-module",
                          "--disable-webkit",
                          "--disable-python-chm",
                          "--enable-recollq",
                          "QMAKE=/usr/local/opt/qt@5/bin/qmake",
                          "--prefix=#{prefix}"
    system "make", "install"
    bin.install "#{buildpath}/qtgui/recoll.app/Contents/MacOS/recoll"
  end

  test do
    system "#{bin}/recollindex", "-h"
  end
end
