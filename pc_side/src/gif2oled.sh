#!/bin/bash

SRC=$1
DEST_IMG=${1%.*}
DEST_OLED=${2=.}/${DEST_IMG}_oled



val=0
bash gif2img.sh $SRC

mkdir $DEST_OLED

for img in `find $DEST_IMG -name '*.png'` 
do
	echo $img
	name=${img%.*}.oled
	name=${name##*/}
	#name=`printf "%04d.oled" $val`
	python img2oled.py "$img" "$DEST_OLED/$name" 170
	val=$((val+1))
done


