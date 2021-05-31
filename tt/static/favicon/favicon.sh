#!/bin/bash
# Hello Internet, I'm too lazy to hide this file, so enjoy!

cd $(dirname "$0")

convert logo.png -thumbnail '256x256>' -gravity center -background transparent -extent 256x256 256.png
optipng -clobber -quiet 256.png
for s in 196 180 64 48 32 24 16; do
  convert 256.png -resize x$s $s.png
  optipng -clobber -quiet $s.png
done
convert 256.png -define icon:auto-resize=64,48,32,24,16 -colors 256 ../favicon.ico
