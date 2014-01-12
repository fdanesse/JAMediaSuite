#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   AudioExtractor.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM! - Uruguay
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

from gi.repository import Gst
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import GstVideo

#GObject.threads_init()
Gst.init([])


class AudioExtractor(Gst.Pipeline):
    """
    * Conversor de formatos para archivos de audio.
    * Extractor de audio de archivos de video.
    """

    __gsignals__ = {
    "endfile": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "estado": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "newposicion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,)),
    #"video": (GObject.SIGNAL_RUN_LAST,
    #    GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))
    "info": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )), }

    def __init__(self, origen, codec):

        Gst.Pipeline.__init__(self)

        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.origen = origen

        self.codec = codec

        self.location = "%s.%s" % (
            self.origen, self.codec)

        if "." in origen:
            extension = ".%s" % self.origen.split(".")[-1]
            self.location = self.origen.replace(
                extension, ".%s" % self.codec)
        '''
        if os.path.exists(self.location):
            print "Este Archivo se Procesó Anteriormente"
            GLib.idle_add(self.emit, "endfile")

        else:
            self.__setup()
        '''

        self.__setup1()

    def __setup1(self):

        # origen
        filesrc = Gst.ElementFactory.make(
            "filesrc", "filesrc")
        decodebin = Gst.ElementFactory.make(
            "decodebin", "decodebin")

        # audio resample
        audioconvert = Gst.ElementFactory.make(
            "audioconvert", "audioconvert")
        audioresample = Gst.ElementFactory.make(
            "audioresample", "audioresample")
        audioresample.set_property('quality', 10)
        audioresample.set_property('quality', 10)

        self.add(filesrc)
        self.add(decodebin)

        self.add(audioconvert)
        self.add(audioresample)

        filesrc.link(decodebin)
        # En __on_pad_added se conecta decodebin a audioconvert
        audioconvert.link(audioresample)

        filesrc.set_property('location', self.origen)
        decodebin.connect('pad-added', self.__on_pad_added)

        self.__setup2()

    def __setup2(self):

        audioresample = self.get_by_name('audioresample')

        if self.codec == 'mp3':
            from Bins import mp3_bin
            lamemp3enc = mp3_bin(self.location)

            self.add(lamemp3enc)
            audioresample.link(lamemp3enc)

        elif self.codec == 'wav':
            from Bins import wav_bin
            wavenc = wav_bin(self.location)

            self.add(wavenc)
            audioresample.link(wavenc)

        elif self.codec == 'ogg':
            from Bins import ogg_bin
            vorbisenc = ogg_bin(self.location)

            self.add(vorbisenc)
            audioresample.link(vorbisenc)

        elif self.codec == 'ogv':
            videoconvert = Gst.ElementFactory.make(
                "videoconvert", "videoconvert")
            videorate = Gst.ElementFactory.make(
                'videorate', 'videorate')
            videorate.set_property('max-rate', 30)

            theoraenc = Gst.ElementFactory.make(
                "theoraenc", "theoraenc")
            oggmux = Gst.ElementFactory.make(
                "oggmux", "oggmux")

            vorbisenc = Gst.ElementFactory.make(
                "vorbisenc", "vorbisenc")

            filesink = Gst.ElementFactory.make(
                "filesink", "filesink")
            filesink.set_property('location',
                self.location)

            self.add(videoconvert)
            self.add(videorate)
            self.add(theoraenc)
            self.add(oggmux)
            self.add(filesink)
            self.add(vorbisenc)

            videoconvert.link(videorate)
            videorate.link(theoraenc)
            theoraenc.link(oggmux)
            oggmux.link(filesink)

            audioresample.link(vorbisenc)
            vorbisenc.link(oggmux)

        self.bus.add_signal_watch()
        self.bus.connect(
            'message', self.__on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect(
            'sync-message', self.__sync_message)

    def play(self):

        self.__play()
        self.__new_handle(True)

    def __on_pad_added(self, decodebin, pad):
        """
        Agregar elementos en forma dinámica según
        sean necesarios. https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """

        string = pad.query_caps(None).to_string()

        text = "Agregando Capas:"
        for item in string.split(","):
            text = "%s\n\t%s" % (text, item.strip())

        self.emit("info", text)

        if string.startswith('audio/'):
            audioconvert = self.get_by_name('audioconvert')

            if audioconvert:
                sink = audioconvert.get_static_pad('sink')
                pad.link(sink)

        elif string.startswith('video/'):
            videoconvert = self.get_by_name('videoconvert')

            if videoconvert:
                sink = videoconvert.get_static_pad('sink')
                pad.link(sink)

    def __sync_message(self, bus, mensaje):
        '''
        if mensaje.get_structure():
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return
        '''
        if mensaje.type == Gst.MessageType.STATE_CHANGED:
            old, new, pending = mensaje.parse_state_changed()

            if old == Gst.State.PAUSED and new == Gst.State.PLAYING:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "playing")
                    self.__new_handle(True)
                    return

            elif old == Gst.State.READY and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")
                    self.__new_handle(False)
                    return

            elif old == Gst.State.READY and new == Gst.State.NULL:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "None")
                    self.__new_handle(False)
                    return

            elif old == Gst.State.PLAYING and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")
                    self.__new_handle(False)
                    return

            #elif old == Gst.State.NULL and new == Gst.State.READY:
            #    pass

            #elif old == Gst.State.PAUSED and new == Gst.State.READY:
            #    pass

            #else:
            #    return

        elif mensaje.type == Gst.MessageType.TAG:
            taglist = mensaje.parse_tag()
            datos = taglist.to_string()

            #if 'audio-codec' in datos and not 'video-codec' in datos:
            #    if self.video_in_stream == True or \
            #        self.video_in_stream == None:

            #        self.video_in_stream = False
            #        self.emit("video", False)

            #elif 'video-codec' in datos:
            #    if self.video_in_stream == False or \
            #        self.video_in_stream == None:

            #        self.video_in_stream = True
            #        self.emit("video", True)

            #self.duracion = int(taglist.to_string().split(
            #   "duration=(guint64)")[1].split(',')[0])

            #Ejemplo:
            #    taglist,
            #    duration=(guint64)780633000000,
            #    video-codec=(string)H.264,
            #    audio-codec=(string)"MPEG-4\ AAC"

            return

        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug
            self.__new_handle(False)
            return

    def __on_mensaje(self, bus, mensaje):

        if mensaje.type == Gst.MessageType.EOS:
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            self.emit("info",
                "Error en la Reproducción: %s %s" % (err, debug))
            print "Error en la Reproducción:", err, debug
            self.__new_handle(False)
            self.emit("endfile")

    def __play(self):

        self.emit("info", "Reproducción Iniciada")
        self.set_state(Gst.State.PLAYING)

    def stop(self):

        self.set_state(Gst.State.NULL)
        self.emit("info", "Reproducción Detenida")

    def __new_handle(self, reset):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = GLib.timeout_add(
                500, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        bool1, valor1 = self.query_duration(Gst.Format.TIME)
        bool2, valor2 = self.query_position(Gst.Format.TIME)

        duracion = int(valor1)
        posicion = int(valor2)

        pos = 0
        try:
            pos = int(posicion * 100 / duracion)

        except:
            pass

        #print pos, posicion, duracion, posicion * 100 / duracion
        #if pos < 0.0 or pos > self.duracion:
        #    print pos, duracion
        #    return True

        if self.duracion != duracion:
            self.duracion = duracion

        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)

        return True
