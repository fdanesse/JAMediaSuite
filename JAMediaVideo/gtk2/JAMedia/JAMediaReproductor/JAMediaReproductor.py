#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaReproductor.py por:
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
import gobject
import gst

from JAMediaBins import JAMedia_Audio_Pipeline
from JAMediaBins import JAMedia_Video_Pipeline

gobject.threads_init()

PR = False


class JAMediaReproductor(gobject.GObject):
    """
    Reproductor de Streaming de Radio y Television.
    """

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "newposicion": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    #"video": (gobject.SIGNAL_RUN_CLEANUP,
    #    gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,)),
        }

    # Estados: playing, paused, None

    def __init__(self, ventana_id):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """

        gobject.GObject.__init__(self)

        self.nombre = "JAMediaReproductor"

        self.ventana_id = ventana_id
        self.progressbar = True
        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.player = None
        self.bus = None

        self.player = gst.element_factory_make(
            "playbin2", "player")

        self.audio_bin = JAMedia_Audio_Pipeline()
        self.video_bin = JAMedia_Video_Pipeline()

        self.player.set_property('video-sink', self.video_bin)
        self.player.set_property('audio-sink', self.audio_bin)

        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        elif message.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()

            if self.estado != new:
                self.estado = new

                if new == gst.STATE_PLAYING:
                    self.emit("estado", "playing")
                    self.__new_handle(True)

                elif new == gst.STATE_PAUSED:
                    self.emit("estado", "paused")
                    self.__new_handle(False)

                elif new == gst.STATE_NULL:
                    self.emit("estado", "None")
                    self.__new_handle(False)

                else:
                    self.emit("estado", "paused")
                    self.__new_handle(False)

        elif message.type == gst.MESSAGE_EOS:
            self.__new_handle(False)
            self.emit("endfile")

        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            if PR:
                print "JAMediaReproductor ERROR:"
                print "\t%s" % err
                print "\t%s" % debug
            self.__new_handle(False)

        elif message.type == gst.MESSAGE_LATENCY:
        #    http://cgit.collabora.com/git/farstream.git/
        #       tree/examples/gui/fs-gui.py
        #    print "\n gst.MESSAGE_LATENCY"
            self.player.recalculate_latency()

        #elif message.type == gst.MESSAGE_TAG:
        #    taglist = message.parse_tag()
        #    datos = taglist.keys()

        #    #for dato in datos:
        #    #    print dato, taglist[dato]

        #    if 'audio-codec' in datos and not 'video-codec' in datos:
        #        if self.video_in_stream == True or \
        #            self.video_in_stream == None:

        #            self.video_in_stream = False
        #            self.emit("video", False)
        #            #self.audio_pipeline.agregar_visualizador('monoscope')

        #    elif 'video-codec' in datos:
        #        if self.video_in_stream == False or \
        #            self.video_in_stream == None:

        #            self.video_in_stream = True
        #            self.emit("video", True)
        #            #self.audio_pipeline.quitar_visualizador()

        #else:
        #    print message.type, message.src

        return gst.BUS_PASS

    def __play(self):
        """
        Pone el pipe de gst en gst.STATE_PLAYING
        """

        self.player.set_state(gst.STATE_PLAYING)

    def __pause(self):
        """
        Pone el pipe de gst en gst.STATE_PAUSED
        """

        self.player.set_state(gst.STATE_PAUSED)

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
            self.actualizador = gobject.timeout_add(500, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        if not self.progressbar:
            return True

        valor1 = None
        valor2 = None
        pos = None
        duracion = None

        try:
            valor1, bool1 = self.player.query_duration(gst.FORMAT_TIME)
            valor2, bool2 = self.player.query_position(gst.FORMAT_TIME)

        except:
            if PR:
                print "ERROR en HANDLER"
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

    def pause_play(self):
        """
        Llama a play() o pause()
        segun el estado actual del pipe de gst.
        """

        if self.estado == gst.STATE_PAUSED \
            or self.estado == gst.STATE_NULL \
            or self.estado == gst.STATE_READY:
            self.__play()

        elif self.estado == gst.STATE_PLAYING:
            self.__pause()

    def rotar(self, valor):
        """
        Rota el Video.
        """

        self.video_bin.rotar(valor)

    def set_balance(self, brillo=False, contraste=False,
        saturacion=False, hue=False, gamma=False):
        """
        Seteos de balance en video.
        Recibe % en float y convierte a los valores del filtro.
        """

        self.video_bin.set_balance(brillo=brillo, contraste=contraste,
            saturacion=saturacion, hue=hue, gamma=gamma)

    def get_balance(self):
        """
        Retorna los valores actuales de balance en % float.
        """

        return self.video_bin.get_balance()

    def stop(self):
        """
        Pone el pipe de gst en gst.STATE_NULL
        """

        self.player.set_state(gst.STATE_NULL)
        self.emit("newposicion", 0)

    def load(self, uri):
        """
        Carga un archivo o stream en el pipe de gst.
        """

        if os.path.exists(uri):
            #direccion = gst.filename_to_uri(uri)
            direccion = "file://" + uri
            self.player.set_property("uri", direccion)
            self.progressbar = True
            self.__play()

        else:
            if gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.progressbar = False
                self.__play()

        return False

    def set_position(self, posicion):
        """
        Permite desplazarse por
        la pista que se esta reproduciendo.
        """

        if not self.progressbar:
            return

        if self.duracion < posicion:
            return

        if self.duracion == 0 or posicion == 0:
            return

        posicion = self.duracion * posicion / 100

        # http://pygstdocs.berlios.de/pygst-reference/gst-constants.html
        #self.player.set_state(gst.STATE_PAUSED)
        # http://nullege.com/codes/show/
        #   src@d@b@dbr-HEAD@trunk@src@reproductor.py/72/gst.SEEK_TYPE_SET
        #self.player.seek(
        #    1.0,
        #    gst.FORMAT_TIME,
        #    gst.SEEK_FLAG_FLUSH,
        #    gst.SEEK_TYPE_SET,
        #    posicion,
        #    gst.SEEK_TYPE_SET,
        #    self.duracion)

        # http://nullege.com/codes/show/
        #   src@c@o@congabonga-HEAD@congaplayer@congalib@engines@gstplay.py/
        #   104/gst.SEEK_FLAG_ACCURATE
        event = gst.event_new_seek(
            1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, posicion * 1000000000,
            gst.SEEK_TYPE_NONE, self.duracion * 1000000000)

        self.player.send_event(event)
        #self.player.set_state(gst.STATE_PLAYING)

    def set_volumen(self, volumen):
        """
        Cambia el volúmen de Reproducción. (Recibe float 0.0 - 10.0)
        """

        self.player.set_property('volume', volumen / 10)

    def get_volumen(self):

        return self.player.get_property('volume') * 10
