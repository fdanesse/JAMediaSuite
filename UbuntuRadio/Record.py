#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Record.py por:
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

from gi.repository import GLib
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
    "update": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    }

    # Estados: playing, paused, None

    def __init__(self, uri, formato):

        GObject.Object.__init__(self)

        self.estado = "None"
        self.formato = formato

        self.patharchivo = None
        self.actualizador = False
        self.control = 0
        self.info = ""
        self.uri = uri

        #-> Pipeline
        self.pipeline = Gst.Pipeline()

        self.player = Gst.ElementFactory.make(
            "uridecodebin", "uridecodebin")

        self.pipeline.add(self.player)

        audioconvert = Gst.ElementFactory.make(
            'audioconvert', 'audioconvert')
        audioresample = Gst.ElementFactory.make(
            'audioresample', 'audioresample')
        audioresample.set_property('quality', 10)

        # si se quiere ogg
        vorbisenc = Gst.ElementFactory.make(
            'vorbisenc', 'vorbisenc')

        self.pipeline.add(audioconvert)
        self.pipeline.add(audioresample)
        self.pipeline.add(vorbisenc)

        audioconvert.link(audioresample)
        audioresample.link(vorbisenc)

        self.audio_sink = audioconvert.get_static_pad('sink')

        # si se quiere ogg
        oggmux = Gst.ElementFactory.make(
            'oggmux', "oggmux")
        self.archivo = Gst.ElementFactory.make(
            'filesink', "filesink")

        self.pipeline.add(oggmux)
        self.pipeline.add(self.archivo)

        vorbisenc.link(oggmux)
        oggmux.link(self.archivo)

        self.bus = self.player.get_bus()

        self.bus.enable_sync_message_emission()
        self.bus.connect(
            'sync-message', self.__sync_message)

        self.player.connect(
            'pad-added', self.__on_pad_added)

        self.__load(self.uri)

    def __on_pad_added(self, uridecodebin, pad):
        """
        Agregar elementos en forma dinámica según
        sean necesarios. https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """

        string = pad.query_caps(None).to_string()
        # print "Agregando:", string

        if string.startswith('audio/'):
            pad.link(self.audio_sink)

    def __sync_message(self, bus, mensaje):

        '''
        # FIXME: Nunca se Produce esta señal
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
        '''
        if mensaje.type == Gst.MessageType.LATENCY:
            self.player.recalculate_latency()

        elif mensaje.type == Gst.MessageType.EOS:
            print "\nGst.MessageType.EOS:"
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == Gst.MessageType.ERROR:
            print "\nGst.MessageType.ERROR:"
            print mensaje.parse_error()
            self.__new_handle(False)
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

    def __new_handle(self, reset):

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = GLib.timeout_add(
                500, self.__handle)

    def __handle(self):
        """
        Consulta el estado y progreso de
        la grabacion.
        """

        if os.path.exists(self.patharchivo):
            tamanio = float(os.path.getsize(
                self.patharchivo) / 1024.0 / 1024.0)

            texto = str(self.uri)

            if len(self.uri) > 25:
                texto = str(self.uri[0:25]) + " . . . "

            info = "Grabando: %s %.2f Mb" % (
                texto, tamanio)

            if self.info != info:
                self.control = 0
                self.info = info
                self.emit('update', self.info)

            else:
                self.control += 1

        if self.control > 60:
            self.stop()
            #self.emit("endfile")
            return False

        return True

    def stop(self):

        if self.estado == Gst.State.PLAYING:
            self.estado = Gst.State.NULL
            self.emit("estado", "None")
            self.pipeline.set_state(Gst.State.NULL)

        self.__new_handle(False)

        if os.path.exists(self.patharchivo):
            os.chmod(self.patharchivo, 0755)

    def play(self, name):

        import time
        import datetime

        hora = time.strftime("%H-%M-%S")
        fecha = str(datetime.date.today())

        from Globales import get_my_files_directory

        archivo = "%s-%s-%s.%s" % (
            name.replace(" ", "_"),
            fecha, hora, self.formato)
        self.patharchivo = os.path.join(
            get_my_files_directory(), archivo)

        self.archivo.set_property(
            "location", self.patharchivo)

        if not self.estado == Gst.State.PLAYING:
            self.estado = Gst.State.PLAYING
            self.emit("estado", "playing")
            self.pipeline.set_state(Gst.State.PLAYING)

        self.__new_handle(True)
