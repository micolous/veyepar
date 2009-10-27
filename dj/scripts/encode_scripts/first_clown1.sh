#!/bin/bash -x

# http://www.firstclown.us/2008/07/01/transcoding-dv-to-widescreen-mp4-in-linux/

# params:
IN=$1
OUT=$2
TEMP=$3

# First Pass
ffmpeg -f dv -i $IN -pass 1 -vcodec libx264 -g 300 -vpre fastfirstpass -mbd 2 -cmp 2 -subcmp 2 -deinterlace -aspect 16:9 -s 640x360 -padtop 4 -padbottom 4 -b 768k -acodec libfaac -y $TEMP

# Second Pass
ffmpeg -f dv -i $IN -pass 2 -vcodec libx264 -vpre h -g 300 -mbd 2 -cmp 2 -subcmp 2 -deinterlace -aspect 16:9 -s 640x360 -padtop 4 -padbottom 4 -b 768k -acodec libfaac -y $TEMP

MP4Box -add $TEMP $OUT  
MP4Box -par 1=1:1 $OUT

