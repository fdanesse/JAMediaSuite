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

import gobject
import gst

gobject.threads_init()


class MyPlayBin(gobject.GObject):

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    }

    # Estados: playing, paused, None

    def __init__(self, uri, volumen):

        gobject.GObject.__init__(self)

        self.estado = "None"

        self.player = gst.element_factory_make(
            "playbin2", "player")

        self.bus = self.player.get_bus()

        self.bus.enable_sync_message_emission()
        self.bus.connect(
            'sync-message', self.__sync_message)

        self.__load(uri)
        self.set_volumen(volumen)

    def __sync_message(self, bus, mensaje):

        if mensaje.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = mensaje.parse_state_changed()

            if old == gst.STATE_PAUSED and new == gst.STATE_PLAYING:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "playing")

            elif old == gst.STATE_READY and new == gst.STATE_PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")

            elif old == gst.STATE_READY and new == gst.STATE_NULL:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "None")

            elif old == gst.STATE_PLAYING and new == gst.STATE_PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")

        elif mensaje.type == gst.MESSAGE_LATENCY:
            self.player.recalculate_latency()

        elif mensaje.type == gst.MESSAGE_EOS:
            print "\ngst.MessageType.EOS:"
            self.emit("endfile")

        elif mensaje.type == gst.MESSAGE_ERROR:
            print "\ngst.MessageType.ERROR:"
            print mensaje.parse_error()
            self.stop()
            self.emit("endfile")

        return True

    def __load(self, uri):

        self.player.set_property("uri", uri)

    def set_volumen(self, valor):

        self.player.set_property('volume', valor)

    def stop(self):

        if self.estado == gst.STATE_PLAYING:
            self.player.set_state(gst.STATE_NULL)

    def play(self):

        if not self.estado == gst.STATE_PLAYING:
            self.player.set_state(gst.STATE_PLAYING)
