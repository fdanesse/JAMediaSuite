# gst-launch-0.10 v4l2src ! queue ! smokeenc ! udpsink host=192.168.1.2 port=5000
gst-launch-0.10 v4l2src ! queue ! ffmpegcolorspace ! smokeenc ! udpsink clients=192.168.1.2:5000,192.168.1.3:5000
