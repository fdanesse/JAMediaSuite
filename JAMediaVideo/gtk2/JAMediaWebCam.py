#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWebCam.py por:
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


class JAMediaWebCam(gobject.GObject):

    __gsignals__ = {
    "estado": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, ventana_id):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """

        gobject.GObject.__init__(self)

        self.ventana_id = ventana_id

        self.pipeline = gst.Pipeline()

        self.camara = gst.element_factory_make(
            'v4l2src', "camara")
        xvimagesink = gst.element_factory_make(
            'xvimagesink', "xvimagesink")
        xvimagesink.set_property(
            "force-aspect-ratio", True)

        self.gamma = gst.element_factory_make(
            'gamma', "gamma")
        self.videoflip = gst.element_factory_make(
            'videoflip', "videoflip")

        self.pipeline.add(self.camara)
        self.pipeline.add(self.gamma)
        self.pipeline.add(self.videoflip)
        self.pipeline.add(xvimagesink)

        self.camara.link(self.gamma)
        self.gamma.link(self.videoflip)
        self.videoflip.link(xvimagesink)

        self.bus = self.pipeline.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def set_accion(self, accion):

        if accion == "Salir" or accion == "Stop":
            self.stop()

        elif accion == "Filmar":
            # detener
            # linquear para grabar
            # grabar (play)
            pass

        elif accion == "Izquierda" or accion == "Derecha":
            self.__rotar(accion)

        print "Camara:", accion

    def __rotar(self, valor):
        """
        Rota el Video.
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

        self.videoflip.set_property('method', rot)

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        return gst.BUS_PASS

    def play(self):

        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):

        self.pipeline.set_state(gst.STATE_NULL)

    def reset(self):
        """
        Re establece la cámara a su estado original.
        """

        print "Reset"
