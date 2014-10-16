#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import gobject
import pygst
import gst
import gtk


class X11_Stream(gobject.GObject):

    def __init__(self, ip='192.168.5.52'):

        gobject.GObject.__init__(self)

        self.pipeline = gst.Pipeline()

        desktop = ximagesrc_bin()
        video_out = Out_lan_smokeenc_bin(ip)

        self.pipeline.add(desktop)
        self.pipeline.add(video_out)

        desktop.link(video_out)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        self.pipeline.set_state(gst.STATE_PLAYING)

    def __sync_message(self, bus, message):
        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                #gtk.gdk.threads_enter()
                #gtk.gdk.display_get_default().sync()
                #message.src.set_xwindow_id(self.ventana_id)
                #gtk.gdk.threads_leave()
                pass

        elif message.type == gst.MESSAGE_LATENCY:
            self.pipeline.recalculate_latency()

        elif message.type == gst.MESSAGE_ERROR:
            print "X11_Stream ERROR:"
            print message.parse_error()

        elif message.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()
            #if self.estado != new:
            #    self.estado = new

    def __on_mensaje(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            #self.emit("endfile")
            pass

        elif message.type == gst.MESSAGE_ERROR:
            print "X11_Stream ERROR:"
            print message.parse_error()

    def stop(self):
        self.__new_handle(False)
        self.player.set_state(gst.STATE_NULL)


class ximagesrc_bin(gst.Bin):

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('ximagesrc_bin')

        x = 0
        y = 0
        import gtk
        width = int(gtk.gdk.screen_width())
        height = int(gtk.gdk.screen_height())
        resolution = "video/x-raw-yuv,width=640,height=480"  #"video/x-raw-yuv,width=600,height=450"

        ximagesrc = gst.element_factory_make("ximagesrc", "ximagesrc")
        ximagesrc.set_property('startx', x)
        ximagesrc.set_property('endx', width)
        ximagesrc.set_property('starty', y)
        ximagesrc.set_property('endy', height)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        videoscale = gst.element_factory_make("videoscale", "videoscale")
        video_filter = gst.element_factory_make("capsfilter", "video_filter")
        video_caps = gst.Caps(resolution)
        video_filter.set_property("caps", video_caps)

        self.add(ximagesrc)
        self.add(ffmpegcolorspace)
        self.add(videoscale)
        self.add(video_filter)

        ximagesrc.link(ffmpegcolorspace)
        ffmpegcolorspace.link(videoscale)
        videoscale.link(video_filter)

        self.add_pad(gst.GhostPad("src", video_filter.get_static_pad("src")))


class Out_lan_smokeenc_bin(gst.Bin):

    def __init__(self, ip):

        gst.Bin.__init__(self)

        self.set_name('out_lan_smokeenc_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        videorate = gst.element_factory_make('videorate', "videorate")

        try:
            videorate.set_property("max-rate", 30)

        except:
            pass

        smokeenc = gst.element_factory_make('smokeenc', "smokeenc")
        udpsink = gst.element_factory_make('udpsink', "udpsink")

        udpsink.set_property("host", ip)
        udpsink.set_property("port", 5000)

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(videorate)
        self.add(smokeenc)
        self.add(udpsink)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(videorate)
        videorate.link(smokeenc)
        smokeenc.link(udpsink)

        self.add_pad(gst.GhostPad("sink", queue.get_static_pad("sink")))


if __name__ == "__main__":
    X11_Stream('192.168.5.52')
    gobject.MainLoop()
