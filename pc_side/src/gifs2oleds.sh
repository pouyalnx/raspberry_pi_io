#!/bin/bash

SRC=$1
DEST=${SRC}_oled

mkdir $DEST
for gif in `find $SRC -name "*.gif"`
do
	bash gif2oled.sh $gif $DEST
done
