gst-launch-0.10 udpsrc port=5000 ! queue ! smokedec ! ffmpegcolorspace ! autovideosink #tcpclientsrc host=192.168.1.11 port=5001 ! queue ! speexdec ! queue ! audioconvert ! autoaudiosink
