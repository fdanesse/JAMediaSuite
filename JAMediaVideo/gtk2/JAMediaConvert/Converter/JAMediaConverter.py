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

gobject.threads_init()


class JAMediaConverter(gst.Pipeline):
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
    "endfile": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "newposicion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "info": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self, origen, codec, dirpath_destino):

        gst.Pipeline.__init__(self)

        self.set_name('jamedia_converter_pipeline')

        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.origen = origen
        self.dirpath_destino = dirpath_destino
        self.codec = codec

        self.bus = self.get_bus()

        if self.codec == "wav":
            self.__run_wav_out()

        elif self.codec == "mp3":
            self.__run_mp3_out()

        filesrc = gst.element_factory_make(
            "filesrc", "filesrc")
        decodebin = gst.element_factory_make(
            "decodebin", "decodebin")

        self.add(filesrc)
        self.add(decodebin)

        filesrc.link(decodebin)

        filesrc.set_property('location', self.origen)
        decodebin.connect('pad-added', self.__on_pad_added)

        self.bus.set_sync_handler(self.__bus_handler)

    def __run_wav_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.add(videoconvert)

        # path de salida
        location = os.path.basename(self.origen)

        if "." in location:
            extension = ".%s" % self.origen.split(".")[-1]
            location = location.replace(extension, ".%s" % self.codec)

        else:
            location = "%s.%s" % (location, self.codec)

        newpath = os.path.join(self.dirpath_destino, location)

        if os.path.exists(newpath):
            fecha = datetime.date.today()
            hora = time.strftime("%H-%M-%S")
            location = "%s_%s_%s" % (fecha, hora, location)
            newpath = os.path.join(self.dirpath_destino, location)

        wavenc = wav_bin(newpath)
        self.add(wavenc)

    def __run_mp3_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.add(videoconvert)

        # path de salida
        location = os.path.basename(self.origen)

        if "." in location:
            extension = ".%s" % self.origen.split(".")[-1]
            location = location.replace(extension, ".%s" % self.codec)

        else:
            location = "%s.%s" % (location, self.codec)

        newpath = os.path.join(self.dirpath_destino, location)

        if os.path.exists(newpath):
            fecha = datetime.date.today()
            hora = time.strftime("%H-%M-%S")
            location = "%s_%s_%s" % (fecha, hora, location)
            newpath = os.path.join(self.dirpath_destino, location)

        lamemp3enc = mp3_bin(newpath)
        self.add(lamemp3enc)

    def __on_pad_added(self, decodebin, pad):
        """
        Agregar elementos en forma dinámica según sean necesarios.
            https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """

        string = str(pad.get_caps())

        #text = "Detectando Capas en la Fuente:"
        #for item in string.split(","):
        #    text = "%s\n\t%s" % (text, item.strip())

        #self.emit("info", text)

        if string.startswith('audio/'):
            audioconvert = self.get_by_name('audio-out')

            if audioconvert:
                sink = audioconvert.get_static_pad('sink')
                pad.link(sink)

        elif string.startswith('video/'):
            videoconvert = self.get_by_name('video-out')

            if videoconvert:
                sink = videoconvert.get_static_pad('sink')
                pad.link(sink)

    def __bus_handler(self, bus, mensaje):

        if mensaje.type == gst.MESSAGE_EOS:
            #self.emit("info", "JAMediaConverter Concluido: %s ==> %s" % (
            #    os.path.basename(self.origen), self.codec))
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == gst.MESSAGE_ERROR:
            err, debug = mensaje.parse_error()
            self.__new_handle(False)
            self.emit("info",
                "JAMediaConverter Error en la Reproducción: %s %s" % (err, debug))
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
                250, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        valor1 = None
        valor2 = None
        pos = None
        duracion = None

        try:
            valor1, bool1 = self.query_duration(gst.FORMAT_TIME)
            valor2, bool2 = self.query_position(gst.FORMAT_TIME)

        except:
            print "JAMediaConverter ERROR en HANDLER"
            return True

        if valor1 != None:
            duracion = valor1 / 1000000000

        if valor2 != None:
            posicion = valor2 / 1000000000

        if duracion == 0 or duracion == None:
            return True

        pos = int(posicion * 100 / duracion)

        if pos < 0 or pos > self.duracion:
            return True

        if self.duracion != duracion:
            self.duracion = duracion

        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)

        return True

    def play(self):
        self.emit("info", "JAMediaConverter Iniciado: %s ==> %s" % (
            os.path.basename(self.origen), self.codec))
        self.set_state(gst.STATE_PLAYING)
        self.__new_handle(True)

    def stop(self):
        self.__new_handle(False)
        self.set_state(gst.STATE_NULL)
        self.emit("info", "JAMediaConverter Detenido: %s" % (
            os.path.basename(self.origen)))
