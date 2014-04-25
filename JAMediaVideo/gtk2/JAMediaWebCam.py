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

CONFIG_DEFAULT = {
    'saturacion': 5,
    'contraste': 6,
    'brillo': 8,
    'hue': 0,
    'gamma': 1.0,
    }


class JAMediaWebCam(gobject.GObject):

    __gsignals__ = {
    "estado": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, ventana_id, camara="/dev/video0", formato="ogg"):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """

        gobject.GObject.__init__(self)

        self.ventana_id = ventana_id
        self.config = CONFIG_DEFAULT.copy()

        self.pipeline = gst.Pipeline()

        self.camara = gst.element_factory_make(
            'v4l2src', "camara")
        #self.camara.set_property("device",
        #    self.config["camara"])

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

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        return gst.BUS_PASS

    def rotar(self, valor):

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

    def play(self):

        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):

        self.pipeline.set_state(gst.STATE_NULL)

    def reset(self):
        """
        Re establece la cámara a su estado original.
        """

        self.config = CONFIG_DEFAULT.copy()

        self.camara.set_property(
            'saturation', self.config['saturacion'])
        self.camara.set_property(
            'contrast', self.config['contraste'])
        self.camara.set_property(
            'brightness', self.config['brillo'])
        self.camara.set_property(
            'hue', self.config['hue'])

        self.gamma.set_property(
            'gamma', self.config['gamma'])

        self.videoflip.set_property('method', 0)

        self.stop()

    def set_balance(self, brillo=False, contraste=False,
        saturacion=False, hue=False, gamma=False):
        """
        Seteos de balance en la fuente de video.
        Recibe % en float.
        """

        # Rangos: int. -2147483648 2147483647
        min = 2147483648
        # max = 2147483647
        total = 4294967295

        if saturacion:
            new_valor = int(total * int(saturacion) / 100)
            new_valor -= min
            self.config['saturacion'] = new_valor
            self.camara.set_property(
                'saturation', self.config['saturacion'])

        if contraste:
            new_valor = int(total * int(contraste) / 100)
            new_valor -= min
            self.config['contraste'] = new_valor
            self.camara.set_property(
                'contrast', self.config['contraste'])

        if brillo:
            new_valor = int(total * int(brillo) / 100)
            new_valor -= min
            self.config['brillo'] = new_valor
            self.camara.set_property(
                'brightness', self.config['brillo'])

        if hue:
            new_valor = int(total * int(hue) / 100)
            new_valor -= min
            self.config['hue'] = new_valor
            self.camara.set_property(
                'hue', self.config['hue'])

        if gamma:
            # Double. Range: 0,01 - 10 Default: 1
            self.config['gamma'] = (10.0 * gamma / 100.0)
            self.gamma.set_property(
                'gamma', self.config['gamma'])

    def get_balance(self):
        """
        Retorna los valores actuales de
        balance en %.
        """

        # Rangos: int. -2147483648 2147483647
        min = 2147483648
        #max = 2147483647
        total = 4294967295

        config = {}

        brillo = self.config['brillo'] + min
        config['brillo'] = brillo * 100 / total

        contraste = self.config['contraste'] + min
        config['contraste'] = contraste * 100 / total

        saturacion = self.config['saturacion'] + min
        config['saturacion'] = saturacion * 100 / total

        hue = self.config['hue'] + min
        config['hue'] = hue * 100 / total

        config['gamma'] = self.config['gamma'] * 100.0 / 10.0

        return config
