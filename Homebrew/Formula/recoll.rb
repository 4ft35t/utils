require 'formula'
# Notes:
# - This formula is missing recoll gui, only bulid command line tool

#  copy from https://framagit.org/medoc92/recoll/-/blob/master/packaging/homebrew/recoll.rb
class Recoll < Formula
  desc "Desktop search tool"
  homepage 'http://www.recoll.org'
  url 'https://www.lesbonscomptes.com/recoll/recoll-1.35.0.tar.gz'
  sha256 "e66b0478709dae93d2d1530256885836595a14925d5d19fc95a63a04d06df941"

  depends_on "xapian"
  # depends_on "qt@6" # disable for no gui
  depends_on "antiword"
  depends_on "poppler"
  depends_on "unrtf"
  depends_on "aspell"
  depends_on "exiftool"
  depends_on "chmlib"

  def install
    system "./configure", "--enable-recollq",
                          "--disable-qtgui",
                          "--prefix=#{prefix}"
    system "make", "install"
    # bin.install "#{buildpath}/qtgui/recoll.app/Contents/MacOS/recoll"
  end

  test do
    system "#{bin}/recollindex", "-h"
  end
end
