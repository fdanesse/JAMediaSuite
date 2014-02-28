#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Player.py por:
#   Flavio Danesse <fdanesse@gmail.com>

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
from gi.repository import Gst

Gst.init([])
GObject.threads_init()


class MyPlayBin(GObject.Object):

    __gsignals__ = {
    "endfile": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "estado": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    }

    # Estados: playing, paused, None

    def __init__(self, uri, volumen):

        GObject.Object.__init__(self)

        self.estado = "None"

        self.player = Gst.ElementFactory.make(
            "playbin", "player")

        self.bus = self.player.get_bus()

        self.bus.enable_sync_message_emission()
        self.bus.connect(
            'sync-message', self.__sync_message)

        self.__load(uri)
        self.set_volumen(volumen)

    def __sync_message(self, bus, mensaje):

        if mensaje.type == Gst.MessageType.STATE_CHANGED:
            old, new, pending = mensaje.parse_state_changed()

            if old == Gst.State.PAUSED and new == Gst.State.PLAYING:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "playing")

            elif old == Gst.State.READY and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")

            elif old == Gst.State.READY and new == Gst.State.NULL:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "None")

            elif old == Gst.State.PLAYING and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")

        elif mensaje.type == Gst.MessageType.LATENCY:
            self.player.recalculate_latency()

        elif mensaje.type == Gst.MessageType.EOS:
            print "\nGst.MessageType.EOS:"
            self.emit("endfile")

        elif mensaje.type == Gst.MessageType.ERROR:
            print "\nGst.MessageType.ERROR:"
            print mensaje.parse_error()
            self.stop()
            self.emit("endfile")

        return True

    def __load(self, uri):

        if os.path.exists(uri):
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)

        else:
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)

    def set_volumen(self, valor):

        self.player.set_property('volume', valor)

    def stop(self):

        if self.estado == Gst.State.PLAYING:
            self.player.set_state(Gst.State.NULL)

    def play(self):

        if not self.estado == Gst.State.PLAYING:
            self.player.set_state(Gst.State.PLAYING)
