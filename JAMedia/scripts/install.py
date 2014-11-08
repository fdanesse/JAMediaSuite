import platform

if 'trusty' in platform.platform():
    sudo apt-add-repository ppa:mc3man/trusty-media
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install ffmpeg gstreamer0.10-ffmpeg gstreamer0.10-fluendo-mp3 gstreamer0.10-gnonlin gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly totem-plugins-extra gstreamer-tools ubuntu-restricted-extras libxine1-ffmpeg gxine mencoder mpeg2dec vorbis-tools id3v2 mpg321 mpg123 libflac++6 totem-mozilla icedax tagtool easytag id3tool lame nautilus-script-audio-convert libmad0 libjpeg-progs flac faac faad sox ffmpeg2theora libmpeg2-4 uudeview flac libmpeg3-1 mpeg3-utils mpegdemux liba52-0.7.4-dev libquicktime2
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get autoremove
