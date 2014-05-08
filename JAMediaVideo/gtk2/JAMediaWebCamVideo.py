#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWebCamVideo.py por:
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
import time
import gobject
import gst
import pygst
import gtk

from Gstreamer_Bins import Camara_ogv_out_bin
from Gstreamer_Bins import Efectos_bin

gobject.threads_init()
gtk.gdk.threads_init()

class JAMediaWebCamVideo(gobject.GObject):

    __gsignals__ = {
    "estado": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "update": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, ventana_id, device="/dev/video0",
        formato="ogg", efectos=[]):

        gobject.GObject.__init__(self)

        self.actualizador = False
        self.tamanio = 0
        self.estado = None
        self.ventana_id = ventana_id
        self.formato = formato
        self.path_archivo = ""

        self.config = {
            'saturacion': 50.0,
            'contraste': 50.0,
            'brillo': 50.0,
            'hue': 50.0,
            'gamma': 10.0}

        self.pipeline = gst.Pipeline()

        self.camara = gst.element_factory_make(
            'v4l2src', "camara")
        self.camara.set_property("num-buffers", 32000)

        if device == "Estación Remota":
            pass
            # gst-launch-0.10 udpsrc port=5000 !
            # queue ! smokedec ! queue ! autovideosink
            # tcpclientsrc host=192.168.1.5 port=5001 !
            # queue ! speexdec ! queue ! alsasink sync=false

        else:
            self.camara.set_property("device", device)

        videorate = gst.element_factory_make(
            'videorate', 'videorate')
        videorate.set_property("skip-to-first", True)
        #videorate.set_property("drop-only", True)

        try:
            videorate.set_property('max-rate', 24)
        except:
            pass

        self.videobalance = gst.element_factory_make(
            'videobalance', "videobalance")
        self.gamma = gst.element_factory_make(
            'gamma', "gamma")
        self.videoflip = gst.element_factory_make(
            'videoflip', "videoflip")

        self.tee = gst.element_factory_make(
            'tee', "tee")

        queue1 = gst.element_factory_make(
            'queue', "queuexvimage")
        #queue1.set_property("max-size-buffers", 0)
        #queue1.set_property("max-size-time", 0)
        queue1.set_property("max-size-bytes", 32000)
        queue1.set_property("leaky", 2)
        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspacegtk")
        xvimagesink = gst.element_factory_make(
            'xvimagesink', "xvimagesink")
        xvimagesink.set_property(
            "force-aspect-ratio", True)

        self.pipeline.add(self.camara)
        self.pipeline.add(videorate)
        self.pipeline.add(self.videobalance)

        self.camara.link(videorate)

        if efectos:
            efectos_bin = Efectos_bin(efectos)
            self.pipeline.add(efectos_bin)
            videorate.link(efectos_bin)
            efectos_bin.link(self.videobalance)

        else:
            videorate.link(self.videobalance)

        self.pipeline.add(self.gamma)
        self.pipeline.add(self.videoflip)
        self.pipeline.add(self.tee)
        self.pipeline.add(queue1)
        self.pipeline.add(ffmpegcolorspace)
        self.pipeline.add(xvimagesink)

        self.videobalance.link(self.gamma)
        self.gamma.link(self.videoflip)
        self.videoflip.link(self.tee)

        self.tee.link(queue1)
        queue1.link(ffmpegcolorspace)
        ffmpegcolorspace.link(xvimagesink)

        self.bus = self.pipeline.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                gtk.gdk.threads_enter()
                gtk.gdk.display_get_default().sync()
                message.src.set_xwindow_id(self.ventana_id)
                gtk.gdk.threads_leave()

        elif message.type == gst.MESSAGE_EOS:
            #self.__new_handle(False, [])
            #self.emit("endfile")
            print "gst.MESSAGE_EOS"

        elif message.type == gst.MESSAGE_QOS:
            print time.time(), "gst.MESSAGE_QOS"

        elif message.type == gst.MESSAGE_LATENCY:
            print "gst.MESSAGE_LATENCY"
            self.pipeline.recalculate_latency()

        elif message.type == gst.MESSAGE_ERROR:
            print "JAMediaGrabador ERROR:"
            print message.parse_error()
            print
            #self.__new_handle(False, [])

        elif message.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()

            if self.estado != new:
                self.estado = new

                if new == gst.STATE_PLAYING:
                    self.emit("estado", "playing")
                    #print "estado", "playing"
                    #self.__new_handle(True, [old, new])

                elif new == gst.STATE_PAUSED:
                    self.emit("estado", "paused")
                    #print "estado", "paused"
                    #self.__new_handle(False, [old, new])

                elif new == gst.STATE_NULL:
                    self.emit("estado", "None")
                    #print "estado", "None"
                    #self.__new_handle(False, [old, new])

                else:
                    self.emit("estado", "paused")
                    #print "estado", "paused"
                    #self.__new_handle(False, [old, new])

        return gst.BUS_PASS

    def __new_handle(self, reset, data):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion.
        """

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

        if os.path.exists(self.path_archivo):
            tamanio = os.path.getsize(self.path_archivo)
            tam = int(tamanio) / 1024.0 / 1024.0

            if self.tamanio != tamanio:
                self.tamanio = tamanio

                texto = os.path.basename(self.path_archivo)
                info = "Grabando: %s %.2f Mb" % (texto, tam)

                self.emit('update', info)

        return True

    def set_efecto(self, efecto, propiedad, valor):
        """
        Setea propiedades de efectos en el pipe.
        """

        ef = self.pipeline.get_by_name("Efectos_bin")

        if ef:
            ef.set_efecto(efecto, propiedad, valor)

    def rotar(self, valor):
        """
        Rota el video.
        """

        rot = self.videoflip.get_property('method')

        if valor == "Derecha":
            if rot < 3:
                rot += 1

            else:
                rot = 0

        elif valor == "Izquierda":
            if rot > 0:
                rot -= 1

            else:
                rot = 3

        gobject.idle_add(
            self.videoflip.set_property, 'method', rot)

    def play(self):

        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):

        self.__new_handle(False, [])
        self.pipeline.set_state(gst.STATE_NULL)

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        """
        Recibe % en float y convierte a los valores del filtro.
        """

        if brillo:
            self.config['brillo'] = brillo
            valor = (2.0 * brillo / 100.0) - 1.0
            self.videobalance.set_property(
                'brightness', valor)

        if contraste:
            self.config['contraste'] = contraste
            valor = 2.0 * contraste / 100.0
            self.videobalance.set_property(
                'contrast', valor)

        if saturacion:
            self.config['saturacion'] = saturacion
            valor = 2.0 * saturacion / 100.0
            self.videobalance.set_property(
                'saturation', valor)

        if hue:
            self.config['hue'] = hue
            valor = (2.0 * hue / 100.0) - 1.0
            self.videobalance.set_property(
                'hue', valor)

        if gamma:
            self.config['gamma'] = gamma
            valor = (10.0 * gamma / 100.0)
            self.gamma.set_property(
                'gamma', valor)

    def set_formato(self, formato):
        """
        Setea formato de salida [ogv, avi, mpeg, ip]
        """

        self.formato = formato

    def filmar(self, path_archivo):
        """
        Conecta a la salida, sea archivo o ip, para grabar o transmitir.
        """

        self.pipeline.set_state(gst.STATE_PAUSED)
		self.pipeline.set_state(gst.STATE_NULL)

        if self.formato == "ogv" or self.formato == "avi" or self.formato == "mpeg":
            self.path_archivo = u"%s.%s" % (path_archivo, self.formato)

            if self.formato == "ogv":
                out = Camara_ogv_out_bin(self.path_archivo)
                self.pipeline.add(out)
                self.tee.link(out)
                self.play()
                self.__new_handle(True, [])

        else:
            print "JAMediaWebCamVideo => Construir pipe para:", self.formato
