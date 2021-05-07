#!/bin/bash
SRC=$1
DEST=${1%.*}

mkdir $DEST
ffmpeg -i $SRC -f image2 $DEST/%4d.png
exit 0

