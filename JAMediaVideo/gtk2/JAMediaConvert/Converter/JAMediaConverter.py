#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaConverter.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay
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
import time
import datetime
import gst
import gobject

from Bins import wav_bin
from Bins import mp3_bin
from Bins import ogg_bin

def borrar(origen):

    try:
        import os
        import shutil

        if os.path.isdir(origen):
            shutil.rmtree("%s" % (os.path.join(origen)))

        elif os.path.isfile(origen):
            os.remove("%s" % (os.path.join(origen)))

        else:
            return False

        return True

    except:
        print "ERROR Al Intentar Borrar un Archivo"
        return False

PR = True

gobject.threads_init()


class JAMediaConverter(gobject.GObject):
    """
    Recibe un archivo de audio o un archivo de video y un codec de salida:
        Procesa dicho archivo de la siguiente forma:
            Si recibe un archivo de Video:
                Extraer sus imágenes si codec es uno de: ["jpg", "png"]
                Extraer su audio si codec es uno de: ["ogg", "mp3", "wav"]
                Convierte el archivo a uno de: ["ogv", "mpeg", "avi"]

            Si Recibe un archivo de audio:
                Convierte el archivo a uno de: ["ogg", "mp3", "wav"]
    """

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "newposicion": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "info": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self, origen, codec, dirpath_destino):

        gobject.GObject.__init__(self)

        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.timer = 0
        self.tamanio = 0
        self.origen = origen
        self.dirpath_destino = dirpath_destino
        self.codec = codec
        self.newpath = ""

        self.player = gst.element_factory_make(
            "playbin2", "playbin2")

        # path de salida
        location = os.path.basename(self.origen)

        if "." in location:
            extension = ".%s" % self.origen.split(".")[-1]
            location = location.replace(extension, ".%s" % self.codec)

        else:
            location = "%s.%s" % (location, self.codec)

        self.newpath = os.path.join(self.dirpath_destino, location)

        if os.path.exists(self.newpath):
            fecha = datetime.date.today()
            hora = time.strftime("%H-%M-%S")
            location = "%s_%s_%s" % (fecha, hora, location)
            self.newpath = os.path.join(self.dirpath_destino, location)

        # Formato de salida
        if self.codec == "wav":
            self.__run_wav_out()

        elif self.codec == "mp3":
            self.__run_mp3_out()

        elif self.codec == "ogg":
            self.__run_ogg_out()

        elif self.codec == "ogv":
            self.__run_ogv_out()

        elif self.codec == "mpeg":
            self.__run_mpeg_out()

        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __run_wav_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.player.set_property('video-sink', videoconvert)

        wavenc = wav_bin(self.newpath)
        self.player.set_property('audio-sink', wavenc)

        self.player.set_property("uri", "file://" + self.origen)

    def __run_mp3_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.player.set_property('video-sink', videoconvert)

        lamemp3enc = mp3_bin(self.newpath)
        self.player.set_property('audio-sink', lamemp3enc)

        self.player.set_property("uri", "file://" + self.origen)

    def __run_ogg_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.player.set_property('video-sink', videoconvert)

        oggenc = ogg_bin(self.newpath)
        self.player.set_property('audio-sink', oggenc)

        self.player.set_property("uri", "file://" + self.origen)

    def __run_mpeg_out(self):

        # https://github.com/jspiros/hylia-transcoder/
        # blob/master/hylia-transcoder.py

        # Nueva declaración para player
        self.player = gst.Pipeline()

        filesrc = gst.element_factory_make(
            "filesrc", "filesrc")
        decodebin = gst.element_factory_make(
            "decodebin", "decodebin")

        self.player.add(filesrc)
        self.player.add(decodebin)

        filesrc.link(decodebin)

        filesrc.set_property('location', self.origen)
        decodebin.connect('pad-added', self.__on_pad_added)

        # Audio
        queue = gst.element_factory_make(
            "queue", "audio-out")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffenc_mp2 = gst.element_factory_make(
            "ffenc_mp2", "ffenc_mp2")

        self.player.add(queue)
        self.player.add(ffenc_mp2)

        queue.link(ffenc_mp2)

        #Video
        queue = gst.element_factory_make(
            "queue", "video-out")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        videoconvert = gst.element_factory_make(
            "ffmpegcolorspace", "ffmpegcolorspace")
        videorate = gst.element_factory_make(
            'videorate', 'videorate')

        try:
            videorate.set_property('max-rate', 30)
        except:
            pass

        ffenc_mpeg2video = gst.element_factory_make(
            "ffenc_mpeg2video", "ffenc_mpeg2video")

        self.player.add(queue)
        self.player.add(videoconvert)
        self.player.add(videorate)
        self.player.add(ffenc_mpeg2video)

        queue.link(videoconvert)
        videoconvert.link(videorate)
        videorate.link(ffenc_mpeg2video)

        muxor = gst.element_factory_make('mpegtsmux', 'muxor')
        #muxor = gst.element_factory_make("ffmux_mpeg", 'muxor')
        filesink = gst.element_factory_make(
            "filesink", "filesink")

        self.player.add(muxor)
        self.player.add(filesink)

        ffenc_mp2.link(muxor)
        ffenc_mpeg2video.link(muxor)
        muxor.link(filesink)

        filesink.set_property('location', self.newpath)

    def __run_ogv_out(self):

        # Nueva declaración para player
        self.player = gst.Pipeline()

        filesrc = gst.element_factory_make(
            "filesrc", "filesrc")
        decodebin = gst.element_factory_make(
            "decodebin", "decodebin")

        self.player.add(filesrc)
        self.player.add(decodebin)

        filesrc.link(decodebin)

        filesrc.set_property('location', self.origen)
        decodebin.connect('pad-added', self.__on_pad_added)

        # Audio
        queue = gst.element_factory_make(
            "queue", "audio-out")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        audioconvert = gst.element_factory_make(
            "audioconvert", "audioconvert")
        audioresample = gst.element_factory_make(
            "audioresample", "audioresample")
        audioresample.set_property('quality', 10)

        vorbisenc = gst.element_factory_make(
            "vorbisenc", "vorbisenc")
        oggmux = gst.element_factory_make(
            "oggmux", "oggmux")
        filesink = gst.element_factory_make(
            "filesink", "filesink")

        self.player.add(queue)
        self.player.add(audioconvert)
        self.player.add(audioresample)
        self.player.add(vorbisenc)
        self.player.add(oggmux)
        self.player.add(filesink)

        queue.link(audioconvert)
        audioconvert.link(audioresample)
        audioresample.link(vorbisenc)
        vorbisenc.link(oggmux)
        oggmux.link(filesink)

        #Video
        queue = gst.element_factory_make(
            "queue", "video-out")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        videoconvert = gst.element_factory_make(
            "ffmpegcolorspace", "ffmpegcolorspace")
        videorate = gst.element_factory_make(
            'videorate', 'videorate')

        try:
            videorate.set_property('max-rate', 30)
        except:
            pass

        theoraenc = gst.element_factory_make(
            'theoraenc', 'theoraenc')

        self.player.add(queue)
        self.player.add(videoconvert)
        self.player.add(videorate)
        self.player.add(theoraenc)

        queue.link(videoconvert)
        videoconvert.link(videorate)
        videorate.link(theoraenc)
        theoraenc.link(oggmux)

        filesink.set_property('location', self.newpath)

    def __on_pad_added(self, decodebin, pad):
        """
        Agregar elementos en forma dinámica según sean necesarios.
            https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """

        string = str(pad.get_caps())

        #text = "Detectando Capas en la Fuente:"
        #for item in string.split(","):
        #    text = "%s\n\t%s" % (text, item.strip())
        #if PR:
        #    print "Archivo: ", self.origen
        #    print text
        #print text
        if string.startswith('audio/'):
            audioconvert = self.player.get_by_name('audio-out')

            if audioconvert:
                sink = audioconvert.get_static_pad('sink')
                pad.link(sink)

        elif string.startswith('video/'):
            videoconvert = self.player.get_by_name('video-out')

            if videoconvert:
                sink = videoconvert.get_static_pad('sink')
                pad.link(sink)

    def __bus_handler(self, bus, mensaje):

        if mensaje.type == gst.MESSAGE_EOS:
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == gst.MESSAGE_ERROR:
            err, debug = mensaje.parse_error()
            self.__new_handle(False)
            if PR:
                print "JAMediaConverter ERROR:"
                print "\t%s ==> %s" % (self.origen, self.codec)
                print "\t%s" % err
                print "\t%s" % debug
            self.emit("endfile")

        return gst.BUS_PASS

    def __new_handle(self, reset):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(
                500, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        valor1 = None
        valor2 = None
        pos = None
        duracion = None

        # Control de archivo de salida
        if os.path.exists(self.newpath):
            tamanio = os.path.getsize(self.newpath)
            #tam = int(tamanio) / 1024.0 / 1024.0

            if self.tamanio != tamanio:
                self.timer = 0
                self.tamanio = tamanio

            else:
                self.timer += 1

        if self.timer > 60:
            self.stop()
            self.emit("endfile")
            if PR:
                print "JAMediaConverter No Pudo Procesar:", self.newpath
            if os.path.exists(self.newpath):
                borrar(self.newpath)
            return False

        # Control de progreso
        try:
            valor1, bool1 = self.player.query_duration(gst.FORMAT_TIME)
            valor2, bool2 = self.player.query_position(gst.FORMAT_TIME)

        except:
            if PR:
                print "JAMediaConverter ERROR en HANDLER"
            return True

        if valor1 != None:
            duracion = valor1 / 1000000000

        if valor2 != None:
            posicion = valor2 / 1000000000

        if duracion == 0 or duracion == None:
            return True

        pos = int(posicion * 100 / duracion)

        #if pos < 0 or pos > self.duracion:
        #    return True

        if self.duracion != duracion:
            self.duracion = duracion

        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)

        return True

    def play(self):
        self.emit("info", "Procesando ==> %s" % self.codec)

        #if PR:
        #    print "JAMediaConverter Iniciado: %s ==> %s" % (
        #        os.path.basename(self.origen), self.codec)

        self.player.set_state(gst.STATE_PLAYING)
        self.__new_handle(True)

    def stop(self):
        self.__new_handle(False)
        self.player.set_state(gst.STATE_NULL)
        self.emit("info", "  Progreso  ")

        #if PR:
        #    print "JAMediaConverter Detenido: %s" % (
        #        os.path.basename(self.origen))