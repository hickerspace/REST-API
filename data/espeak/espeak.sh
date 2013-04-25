#!/bin/bash

cd "$(dirname "$0")"

if [ "$1" != "en" ] && [ "$1" != "de" ]
then
	echo "Please specify either 'en' or 'de' as your language of choice."
	exit 1
fi

# create wav from text
espeak "$2" -v$1 -s130 -w espeak-$$.wav

# prepend intro gong
sox psa.wav espeak-$$.wav announce-$$.wav

# encode mp3
lame -S -V0 -h -b 160 --vbr-new announce-$$.wav announce-$$.mp3

# move mp3 to final destination
mv announce-$$.mp3 $(mktemp --tmpdir="$(dirname "$0")/../announces/ --suffix=.mp3)

# cleanup
rm espeak-$$.wav
rm announce-$$.wav
