gst-launch-0.10 udpsrc port=5000 ! queue ! smokedec ! ffmpegcolorspace ! autovideosink
