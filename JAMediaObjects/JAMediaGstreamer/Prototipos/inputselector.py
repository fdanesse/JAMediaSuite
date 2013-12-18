#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from gi.repository import Gtk
from gi.repository import Gst
from gi.repository import GstVideo
from gi.repository import GObject
from gi.repository import GdkX11

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
        self.combo_box.append_text("camara")

        vbox.pack_start(self.video_widget, True, True, 0)
        vbox.pack_end(self.combo_box, False, False, 0)

        self.add(vbox)

        self.show_all()
        self.realize()

        self.connect("delete-event", self.__exit)

        ventana_id = self.video_widget.get_property('window').get_xid()
        self.player = SwitchTest(ventana_id)

        self.combo_box.connect("changed", self.__seleccion_en_combo)

        self.combo_box.set_active(0)

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

        videotest0 = Gst.ElementFactory.make("videotestsrc", "videotestsrc0")
        videotest0.set_property('pattern', 0)
        queue0 = Gst.ElementFactory.make("queue", "queue0")

        videotest1 = Gst.ElementFactory.make("videotestsrc", "videotestsrc1")
        videotest1.set_property('pattern', 1)
        queue1 = Gst.ElementFactory.make("queue", "queue1")

        videotest2 = Gst.ElementFactory.make("v4l2src", "camara")
        #videotest1.set_property('pattern', 1)
        queue2 = Gst.ElementFactory.make("queue", "queue2")

        videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")

        input_selector = Gst.ElementFactory.make("input-selector", "input-selector")
        videosink = Gst.ElementFactory.make("xvimagesink", "videosink")

        self.pipeline.add(videotest0)
        self.pipeline.add(queue0)
        self.pipeline.add(videotest1)
        self.pipeline.add(queue1)
        self.pipeline.add(videotest2)
        self.pipeline.add(queue2)
        self.pipeline.add(input_selector)
        self.pipeline.add(videoconvert)
        self.pipeline.add(videosink)

        videotest0.link(queue0)
        videotest1.link(queue1)
        videotest2.link(queue2)

        queue0.link(input_selector)
        queue1.link(input_selector)
        queue2.link(input_selector)

        input_selector.link(videoconvert)
        videoconvert.link(videosink)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        self.__play()

    def __sync_message(self, bus, mensaje):

        if mensaje.get_structure():
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

    def __on_mensaje(self, bus, mensaje):

        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            #print err, debug

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

        elif opcion == "camara":
            input_selector.set_property('active-pad',input_selector.pads[3])

Ventana()
Gtk.main()
