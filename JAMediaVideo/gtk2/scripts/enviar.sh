gst-launch-0.10 v4l2src ! queue ! ffmpegcolorspace ! smokeenc ! udpsink host=192.168.1.11 port=5000 #autoaudiosrc ! queue ! speexenc ! tcpclientsink host=192.168.1.11 port=5001
