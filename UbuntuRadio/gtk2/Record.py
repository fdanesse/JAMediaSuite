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
import gobject
import gst

gobject.threads_init()


class MyPlayBin(gobject.GObject):

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "update": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    }

    # Estados: playing, paused, None

    def __init__(self, uri, formato):

        gobject.GObject.__init__(self)

        self.estado = "None"
        self.formato = formato

        self.patharchivo = None
        self.actualizador = False
        self.control = 0
        self.info = ""
        self.uri = uri

        #-> Pipeline
        self.pipeline = gst.Pipeline()

        self.player = gst.element_factory_make(
            "uridecodebin", "uridecodebin")

        self.pipeline.add(self.player)

        audioconvert = gst.element_factory_make(
            'audioconvert', 'audioconvert')
        audioresample = gst.element_factory_make(
            'audioresample', 'audioresample')
        audioresample.set_property('quality', 10)

        self.pipeline.add(audioconvert)
        self.pipeline.add(audioresample)

        audioconvert.link(audioresample)

        self.audio_sink = audioconvert

        self.archivo = gst.element_factory_make(
            'filesink', "filesink")
        self.pipeline.add(self.archivo)

        if self.formato == "ogg":
            vorbisenc = gst.element_factory_make(
                'vorbisenc', 'vorbisenc')
            oggmux = gst.element_factory_make(
                'oggmux', "oggmux")

            self.pipeline.add(vorbisenc)
            self.pipeline.add(oggmux)

            audioresample.link(vorbisenc)
            vorbisenc.link(oggmux)
            oggmux.link(self.archivo)

        elif self.formato == "mp3":
            lamemp3enc = gst.element_factory_make(
                "lamemp3enc", "lamemp3enc")

            self.pipeline.add(lamemp3enc)

            audioresample.link(lamemp3enc)
            lamemp3enc.link(self.archivo)

        elif self.formato == "wav":
            wavenc = gst.element_factory_make(
                "wavenc", "wavenc")

            self.pipeline.add(wavenc)

            audioresample.link(wavenc)
            wavenc.link(self.archivo)

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

        tpad = self.audio_sink.get_compatible_pad(pad)
        if tpad:
            pad.link(tpad)

    def __sync_message(self, bus, mensaje):

        if mensaje.type == gst.MESSAGE_LATENCY:
            self.player.recalculate_latency()

        elif mensaje.type == gst.MESSAGE_EOS:
            print "\ngst.MessageType.EOS:"
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == gst.MESSAGE_ERROR:
            print "\ngst.MessageType.ERROR:"
            print mensaje.parse_error()
            self.__new_handle(False)
            self.stop()
            self.emit("endfile")

        return True

    def __load(self, uri):

        self.player.set_property("uri", uri)

    def __new_handle(self, reset):

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(
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

        if self.estado == gst.STATE_PLAYING:
            self.estado = gst.STATE_NULL
            self.emit("estado", "None")
            self.pipeline.set_state(gst.STATE_NULL)

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

        if not self.estado == gst.STATE_PLAYING:
            self.estado = gst.STATE_PLAYING
            self.emit("estado", "playing")
            self.pipeline.set_state(gst.STATE_PLAYING)

        self.__new_handle(True)
