#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
import gobject
import pygst
pygst.require("0.10")
import gst

class Main():

    def __init__(self):

        src1 = gst.element_factory_make("filesrc")
        src2 = gst.element_factory_make("filesrc")

        src1.set_property("location", "/home/flavio/001")
        src2.set_property("location", "/home/flavio/002")

        dec1 = gst.element_factory_make("decodebin2")
        dec2 = gst.element_factory_make("decodebin2")

        alpha1 = gst.element_factory_make("alpha")
        alpha2 = gst.element_factory_make("alpha")

        self.controller = gst.Controller(alpha2, "alpha")
        self.controller.set_interpolation_mode(
            "alpha", gst.INTERPOLATE_LINEAR)
        self.controller.set("alpha", 0, 0.0)
        #self.controller.set("alpha", 5*gst.SECOND, 0.5)
        self.controller.set("alpha", 0.0, 0.5)

        mixer = gst.element_factory_make("videomixer")

        queue = gst.element_factory_make("queue")
        color = gst.element_factory_make("ffmpegcolorspace")
        sink  = gst.element_factory_make("xvimagesink")

        pipeline = gst.Pipeline("pipeline")

        pipeline.add(
            src1, src2, dec1, dec2,
            alpha1, alpha2, mixer,
            queue, color, sink)

        def on_pad(comp, pad, data, element):
            #padname = pad.get_name()
            caps = pad.get_caps()
            name = caps[0].get_name()

            if 'video/x-raw-yuv' in name:
                sinkpad = element.get_compatible_pad(pad, pad.get_caps())
                #sinkpad = element.get_pad('sink')
                pad.link(sinkpad)

            else:
                pass

        dec1.connect("new-decoded-pad", on_pad, alpha1)
        dec2.connect("new-decoded-pad", on_pad, alpha2)

        src1.link(dec1)
        src2.link(dec2)

        alpha1.link(mixer)
        alpha2.link(mixer)

        mixer.link(queue)
        queue.link(color)
        color.link(sink)

        self.pipeline = pipeline

    def start(self):

        self.running = True
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        self.pipeline.set_state(gst.STATE_PLAYING)

    def on_exit(self, *args):

        self.pipeline.set_state(gst.STATE_NULL)
        self.running = False

    def on_message(self, bus, message):
        t = message.type

	if t == gst.MESSAGE_EOS:
            self.on_exit()

	elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()

	    print "Error: %s" % err, debug
            self.on_exit()

loop = gobject.MainLoop()
gobject.threads_init()
context = loop.get_context()

m = Main()
m.start()

while m.running:
    context.iteration(True)
