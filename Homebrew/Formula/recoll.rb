require 'formula'
# Notes:
# - This formula is missing recoll gui, only bulid command line tool

#  copy from https://framagit.org/medoc92/recoll/-/blob/master/packaging/homebrew/recoll.rb
class Recoll < Formula
  desc "Desktop search tool"
  homepage 'http://www.recoll.org'
  url 'https://www.lesbonscomptes.com/recoll/recoll-1.34.6.tar.gz'
  sha256 "e39587d12370df92e4ac951429d0bb805662d7417d4dbcd41e92389b165e9fb8"

  depends_on "xapian"
  depends_on "qt@6"
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
