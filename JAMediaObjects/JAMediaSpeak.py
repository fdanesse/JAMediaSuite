#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWidgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay

# En Base a código de Aleksey Lim.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import subprocess

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gst
from gi.repository import GObject
from gi.repository import GLib

wavpath = "/dev/shm/speak.wav"

GObject.threads_init()
Gst.init([])

class JAMediaSpeak(GObject.GObject):
    """
    Wraper Sencillo para espeak.
    En Base a código de Aleksey Lim.
    Ver Speak.activity.
    """
    
    __gsignals__ = {
        'new-buffer': (GObject.SIGNAL_RUN_FIRST,
        None, [GObject.TYPE_PYOBJECT])}

    def __init__(self):
        
        GObject.GObject.__init__(self)
        
        self.pitch = 50
        self.speed = 170
        self.word_gap = 0
        self.voice = "es"
        
        self.pipeline = False
        self._was_message = False
        
    def speak(self, text):
        """
        Habla text.
        """
        
        self.stop()
        
        subprocess.call(["espeak", "-p%s" % self.pitch,
            "-s%s" % self.speed, "-g%s" % self.word_gap,
            "-w", wavpath, "-v%s" % self.voice,
            ".   %s   ." % text],
            stdout=subprocess.PIPE)
        
        self.setup_init()
        
        self.play()
        
    def stop(self):
        
        if not self.pipeline: return
    
        self.pipeline.set_state(Gst.State.NULL)
        self.emit_buffer('')
    
    def play(self):
        
        self.pipeline.set_state(Gst.State.PLAYING)
        
    def setup_init(self):
        """
        Construye el pipe Gst.
        """
        
        if self.pipeline: del(self.pipeline)
        
        self.pipeline = Gst.Pipeline()
        
        file = Gst.ElementFactory.make("filesrc", "espeak")
        wavparse = Gst.ElementFactory.make("wavparse", "wavparse")
        audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")
        tee = Gst.ElementFactory.make('tee', "tee")
        playsink = Gst.ElementFactory.make("playsink", "playsink")
        queue1 = Gst.ElementFactory.make("queue", "queue1")
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        queue2 = Gst.ElementFactory.make("queue", "queue2")
        
        self.pipeline.add(file)
        self.pipeline.add(wavparse)
        self.pipeline.add(audioconvert)
        self.pipeline.add(tee)
        self.pipeline.add(queue1)
        self.pipeline.add(playsink)
        self.pipeline.add(queue2)
        self.pipeline.add(fakesink)
        
        file.link(wavparse)
        wavparse.link(tee)
        
        tee.link(queue1)
        queue1.link(audioconvert)
        audioconvert.link(playsink)
        
        tee.link(queue2)
        queue2.link(fakesink)
        
        file.set_property("location", wavpath)
        
        fakesink.set_property('signal-handoffs', True)
        fakesink.set_property('dump', True)
        fakesink.connect('handoff', self.on_buffer)
        
        self._was_message = False
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.gstmessage_cb)
    
    def gstmessage_cb(self, bus, message):
        self._was_message = True
        
        if message.type == Gst.MessageType.WARNING:
            def check_after_warnings():
                if not self._was_message:
                    self.stop()
                return True
            
            self._was_message = False
            GLib.timeout_add(500, self.emit_buffer, str(buffer))
            
        elif  message.type == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
            
        elif message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            #print err, debug
            self.stop()
            
    def on_buffer(self, element, buffer, pad):
        GLib.timeout_add(100, self.emit_buffer, str(buffer))
        return True
    
    def emit_buffer(self, buf):
        self.emit("new-buffer", buf)
        return False
    