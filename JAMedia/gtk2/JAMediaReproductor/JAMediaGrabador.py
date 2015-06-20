#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGrabador.py por:
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
import sys
import gobject
import gst
from multiprocessing import Process
gobject.threads_init()


class JAMediaGrabador(gobject.GObject, Process):

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "endfile": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self, uri, archivo, tipo):

        gobject.GObject.__init__(self)
        Process.__init__(self)

        self.tipo = tipo

        if not archivo.endswith(".ogg"):
            archivo = "%s%s" % (archivo, ".ogg")

        self.patharchivo = archivo
        self.actualizador = False
        self.estado = None
        self.control = 0
        self.tamanio = 0
        self.uri = ""

        self.pipeline = None
        self.player = None
        self.archivo = None
        self.bus = None

        self.pipeline = gst.Pipeline()

        self.player = gst.element_factory_make("uridecodebin", "uridecodebin")
        self.player.set_property("buffer-size", 40000)
        self.player.set_property("download", True)

        self.pipeline.add(self.player)

        # AUDIO
        audioconvert = gst.element_factory_make('audioconvert', 'audioconvert')
        audioresample = gst.element_factory_make(
            'audioresample', 'audioresample')
        audioresample.set_property('quality', 10)
        vorbisenc = gst.element_factory_make('vorbisenc', 'vorbisenc')

        self.pipeline.add(audioconvert)
        self.pipeline.add(audioresample)
        self.pipeline.add(vorbisenc)

        audioconvert.link(audioresample)
        audioresample.link(vorbisenc)

        self.audio_sink = audioconvert.get_static_pad('sink')

        # VIDEO
        videoconvert = gst.element_factory_make(
            'ffmpegcolorspace', 'videoconvert')
        videorate = gst.element_factory_make('videorate', 'videorate')

        try:
            videorate.set_property('max-rate', 30)
        except:
            pass

        theoraenc = gst.element_factory_make('theoraenc', 'theoraenc')

        if self.tipo == "video":
            self.pipeline.add(videoconvert)
            self.pipeline.add(videorate)
            self.pipeline.add(theoraenc)

            videoconvert.link(videorate)
            videorate.link(theoraenc)

        self.video_sink = videoconvert.get_static_pad('sink')

        # MUXOR y ARCHIVO
        oggmux = gst.element_factory_make('oggmux', "oggmux")
        self.archivo = gst.element_factory_make('filesink', "filesink")

        self.pipeline.add(oggmux)
        self.pipeline.add(self.archivo)

        vorbisenc.link(oggmux)

        if self.tipo == "video":
            theoraenc.link(oggmux)

        oggmux.link(self.archivo)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        self.player.connect('pad-added', self.__pad_added)

        self.load(uri)

    def __on_mensaje(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            self.__new_handle(False)
            self.emit("endfile")
        elif message.type == gst.MESSAGE_BUFFERING:
            buf = int(message.structure["buffer-percent"])
            if buf < 100 and self.estado == gst.STATE_PLAYING:
                #self.emit("loading-buffer", buf)
                self.__pause()
            elif buf > 99 and self.estado != gst.STATE_PLAYING:
                #self.emit("loading-buffer", buf)
                self.play()
        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "JAMediaGrabador ERROR:"
            print "\t%s" % err
            print "\t%s" % debug
            self.__new_handle(False)

    def __sync_message(self, bus, message):
        if message.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()
            if self.estado != new:
                self.estado = new
        elif message.type == gst.MESSAGE_LATENCY:
            self.player.recalculate_latency()
        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "JAMediaGrabador ERROR:"
            print "\t%s" % err
            print "\t%s" % debug
            self.__new_handle(False)

    def __pad_added(self, uridecodebin, pad):
        """
        Agregar elementos en forma dinámica:
            https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """
        caps = pad.get_caps()
        string = caps.to_string()
        if string.startswith('audio'):
            if not self.audio_sink.is_linked():
                pad.link(self.audio_sink)
        elif string.startswith('video'):
            if not self.video_sink.is_linked():
                pad.link(self.video_sink)

    def __pause(self):
        self.player.set_state(gst.STATE_PAUSED)

    def __new_handle(self, reset):
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False
        if reset:
            self.actualizador = gobject.timeout_add(
                500, self.__handle)

    def __handle(self):
        if os.path.exists(self.patharchivo):
            tamanio = os.path.getsize(self.patharchivo)
            tam = int(tamanio) / 1024.0 / 1024.0
            if self.tamanio != tamanio:
                self.control = 0
                self.tamanio = tamanio
                texto = str(self.uri)
                if len(self.uri) > 25:
                    texto = str(self.uri[0:25]) + " . . . "
                info = "Grabando: %s %.2f Mb" % (texto, tam)
                self.emit('update', info)
            else:
                self.control += 1
        if self.control > 60:
            self.stop()
            self.emit("endfile")
            return False
        return True

    def play(self):
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.__new_handle(True)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)
        self.__new_handle(False)
        if os.path.exists(self.patharchivo):
            os.chmod(self.patharchivo, 0755)

    def load(self, uri):
        print "JAMediaGrabador:", uri
        if gst.uri_is_valid(uri):
            self.archivo.set_property("location", self.patharchivo)
            self.uri = uri
            self.player.set_property("uri", self.uri)
        else:
            print "JAMediaGrabador: uri inválida:", uri
            self.emit("endfile")
        return False


def update(grabador, datos):
    print datos


def end(grabador):
    sys.exit(0)


if __name__ == "__main__":
    print "Iniciando Grabador . . ."

    if not len(sys.argv) == 4:
        print "Debes pasar tres parámetros:"
        print "\t Dirección origen, puede ser url o file path."
        print "\t Nombre de archivo final, puede ser path completo o solo el nombre."
        print "\t Tipo de contenido, puede ser audio o video."

        sys.exit(0)

    uri = sys.argv[1]
    archivo = sys.argv[2]
    tipo = sys.argv[3]

    # FIXME: Esto Provoca: Violación de segmento
    grabador = JAMediaGrabador(uri, archivo, tipo)

    grabador.connect('update', update)
    grabador.connect('endfile', end)
