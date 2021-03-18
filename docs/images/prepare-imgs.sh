#!/bin/bash 

r=5

if [ "$2" != "" ] ; then
  r=$2
fi

LIST=`git rev-list --all --objects -- $1 | grep $1 | awk '{print $1;}'`

i=9999;
for rev in $LIST; do
    i=`expr $i - 1`;
    FNAME=`printf "%04d.jpg" $i`;
    git show $rev > tmp/$FNAME;
    echo "wrote to $FNAME"
done

if [ "$3" != "" ] ; then
  i=$3
fi

ffmpeg -framerate $r -start_number $i -i tmp/%04d.jpg -vcodec libx264 -pix_fmt yuv420p -r $r tmp/out.mp4

rm tmp/*.jpg
