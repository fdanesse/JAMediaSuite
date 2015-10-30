#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from gi.repository import Gtk
from gi.repository import Gst
from gi.repository import GstVideo
from gi.repository import GObject
from gi.repository import GdkX11
from gi.repository import GLib

GObject.threads_init()
Gst.init([])

class Ventana(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("Mi Aplicación")

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.VBox()

        self.video_widget = Gtk.DrawingArea()
        self.combo_box = Gtk.ComboBoxText()

        self.combo_box.append_text("sink0")
        self.combo_box.append_text("sink1")

        vbox.pack_start(self.video_widget, True, True, 0)
        vbox.pack_end(self.combo_box, False, False, 0)

        self.add(vbox)

        self.show_all()
        self.realize()

        self.connect("delete-event", self.__exit)

        ventana_id = self.video_widget.get_property('window').get_xid()
        self.player = SwitchTest(ventana_id)

        self.combo_box.connect("changed", self.__seleccion_en_combo)

        #self.combo_box.set_active(0)

    def __seleccion_en_combo(self, widget):

        self.player.switch(widget.get_active_text())

    def __exit(self, widget, senial):

        self.player.stop()
        sys.exit(0)


class SwitchTest(GObject.GObject):

    def __init__(self, ventana_id):

        GObject.GObject.__init__(self)

        self.ventana_id = ventana_id

        self.pipeline = Gst.Pipeline()

        ### Camara 1
        camara0 = Gst.ElementFactory.make(
            "v4l2src", "v4l2src0")
        camara0.set_property(
            'device', '/dev/video0')
        videoconvert0 = Gst.ElementFactory.make(
            "videoconvert", "videoconvert0")

        ### Camara 2
        camara1 = Gst.ElementFactory.make(
            "v4l2src", "v4l2src1")
        camara1.set_property(
            'device', '/dev/video1')
        videoconvert1 = Gst.ElementFactory.make(
            "videoconvert", "videoconvert1")

        input_selector = Gst.ElementFactory.make(
            "input-selector", "input-selector")
        tee = Gst.ElementFactory.make(
            "tee", "tee")

        videoconvert2 = Gst.ElementFactory.make(
            "videoconvert", "videoconvert2")
        pantalla = Gst.ElementFactory.make(
            'xvimagesink', "xvimagesink")

        #oggmux = Gst.ElementFactory.make(
        #    'oggmux', "oggmux")
        #filesink = Gst.ElementFactory.make(
        #    'filesink', "filesink")

        #video_bin = Theoraenc_bin()
        #audio_bin = Vorbisenc_bin()

        self.pipeline.add(camara0)
        self.pipeline.add(videoconvert0)

        self.pipeline.add(camara1)
        self.pipeline.add(videoconvert1)

        self.pipeline.add(input_selector)
        self.pipeline.add(tee)

        self.pipeline.add(videoconvert2)
        self.pipeline.add(pantalla)

        #self.pipeline.add(video_bin)
        #self.pipeline.add(audio_bin)
        #self.pipeline.add(oggmux)
        #self.pipeline.add(filesink)

        camara0.link(videoconvert0)
        videoconvert0.link(input_selector)

        camara1.link(videoconvert1)
        videoconvert1.link(input_selector)

        input_selector.link(tee)
        tee.link(videoconvert2)
        videoconvert2.link(pantalla)

        #tee.link(video_bin)
        #video_bin.link(oggmux)
        #audio_bin.link(oggmux)
        #oggmux.link(filesink)

        #filesink.set_property("location", "/home/flavio/prueba.ogg")

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        GLib.idle_add(self.__play)

    def __sync_message(self, bus, mensaje):

        if mensaje.get_structure():
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

    def __on_mensaje(self, bus, mensaje):

        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug

    def __play(self):

        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):

        self.pipeline.set_state(Gst.State.NULL)

    def switch(self, opcion):

        input_selector = self.pipeline.get_by_name('input-selector')

        if opcion == "sink0":
            input_selector.set_property('active-pad',input_selector.pads[1])

        elif opcion == "sink1":
            input_selector.set_property('active-pad',input_selector.pads[2])


class Theoraenc_bin(Gst.Bin):
    """
    Bin para elementos codificadores
    de video a theoraenc.
    """

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('video_theoraenc_bin')

        que_encode_video = Gst.ElementFactory.make(
            "queue", "que_encode_video")
        que_encode_video.set_property('max-size-buffers', 1000)
        que_encode_video.set_property('max-size-bytes', 0)
        que_encode_video.set_property('max-size-time', 0)

        theoraenc = Gst.ElementFactory.make('theoraenc', 'theoraenc')
        # kbps compresion + resolucion = calidad
        theoraenc.set_property("bitrate", 1024)
        theoraenc.set_property('keyframe-freq', 15)
        theoraenc.set_property('cap-overflow', False)
        theoraenc.set_property('speed-level', 0)
        theoraenc.set_property('cap-underflow', True)
        theoraenc.set_property('vp3-compatible', True)

        self.add(que_encode_video)
        self.add(theoraenc)

        que_encode_video.link(theoraenc)

        pad = que_encode_video.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))

        pad = theoraenc.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))


class Vorbisenc_bin(Gst.Bin):
    """
    Bin para elementos codificadores
    de audio a vorbisenc.
    """

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('audio_vorbisenc_bin')

        # FIXME: Corregir para no tomar autoaudiosrc
        autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc")
        audiorate = Gst.ElementFactory.make('audiorate', "audiorate")
        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")

        self.add(autoaudiosrc)
        self.add(audiorate)
        self.add(audioconvert)
        self.add(vorbisenc)

        autoaudiosrc.link(audiorate)
        audiorate.link(audioconvert)
        audioconvert.link(vorbisenc)

        pad = vorbisenc.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))

Ventana()
Gtk.main()
