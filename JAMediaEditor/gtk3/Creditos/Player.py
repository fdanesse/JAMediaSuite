#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Player.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
#
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

import os

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gst

GObject.threads_init()
Gst.init([])


class Player(GObject.GObject):

    __gsignals__ = {
    "endfile": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        GObject.GObject.__init__(self)

        self.player = False
        self.bus = False

    def stop(self):
        if self.player:
            self.player.set_state(Gst.State.NULL)
            del(self.player)
            self.player = False

    def load(self, uri):
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.player.set_property('volume', 0.10)
        self.bus = self.player.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)
        GLib.idle_add(self.__load, uri)

    def __play(self):
        self.player.set_state(Gst.State.PLAYING)

    def __sync_message(self, bus, mensaje):
        if mensaje.type == Gst.MessageType.EOS:
            self.emit("endfile")
        elif mensaje.type == Gst.MessageType.ERROR:
            print "\n Gst.MessageType.ERROR:"
            print mensaje.parse_error()
        return True

    def __load(self, uri):
        if os.path.exists(uri):
            # Archivo
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)
            self.__play()
        else:
            # Streaming
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.__play()
