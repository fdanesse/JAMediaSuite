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

import gobject
import gst

CONFIG_DEFAULT = {
    'saturacion': (50.0, 5),
    'contraste': (50.0, 6),
    'brillo': (50.0, 8),
    'hue': (50.0, 0),
    'gamma': (10.0, 1.0),
    }


class JAMediaWebCamVideo(gobject.GObject):

    __gsignals__ = {
    "estado": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, ventana_id, device="/dev/video0",
        formato="ogg", efectos=[]):
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

        if device == "Estación Remota":
            pass
            # gst-launch-0.10 udpsrc port=5000 !
            # queue ! smokedec ! queue ! autovideosink
            # tcpclientsrc host=192.168.1.5 port=5001 !
            # queue ! speexdec ! queue ! alsasink sync=false

        else:
            self.camara.set_property("device", device)

        xvimagesink = gst.element_factory_make(
            'xvimagesink', "xvimagesink")
        xvimagesink.set_property(
            "force-aspect-ratio", True)

        self.gamma = gst.element_factory_make(
            'gamma', "gamma")
        self.videoflip = gst.element_factory_make(
            'videoflip', "videoflip")

        self.tee = gst.element_factory_make(
            'tee', "tee")

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")

        self.pipeline.add(self.camara)
        self.pipeline.add(self.gamma)
        self.pipeline.add(self.videoflip)
        self.pipeline.add(self.tee)
        self.pipeline.add(ffmpegcolorspace)
        self.pipeline.add(xvimagesink)

        self.camara.link(self.gamma)
        self.gamma.link(self.videoflip)

        self.tee.link(ffmpegcolorspace)
        ffmpegcolorspace.link(xvimagesink)

        if efectos:
            queue = gst.element_factory_make(
                'queue', "queue")

            self.pipeline.add(queue)

            self.videoflip.link(queue)

            elementos = []
            cont = 1

            for efecto in efectos:
                ffmpegcolorspace = gst.element_factory_make(
                    'ffmpegcolorspace', "ffmpegcolorspace%s" % cont)

                ef = gst.element_factory_make(
                    efecto, efecto)

                elementos.append(ffmpegcolorspace)
                elementos.append(ef)

                cont += 1

            for elemento in elementos:
                self.pipeline.add(elemento)
                index = elementos.index(elemento)

                if index > 0:
                    elementos[index-1].link(elementos[index])

            queue.link(elementos[0])
            elementos[-1].link(self.tee)

        else:
            self.videoflip.link(self.tee)

        self.bus = self.pipeline.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        return gst.BUS_PASS

    def set_efecto(self, efecto, propiedad, valor):

        ef = self.pipeline.get_by_name(efecto)
        ef.set_property(propiedad, valor)

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

        gobject.idle_add(
            self.videoflip.set_property, 'method', rot)

    def play(self):

        self.pipeline.set_state(gst.STATE_PLAYING)

        print "brightness", self.camara.get_property('brightness')
        print "contrast", self.camara.get_property('contrast')
        print "saturation", self.camara.get_property('saturation')
        print "hue", self.camara.get_property('hue')
        print "gamma", self.gamma.get_property('gamma')

    def stop(self):

        self.pipeline.set_state(gst.STATE_NULL)

    def reset(self):
        """
        Re establece la cámara a su estado original.
        """

        self.config = CONFIG_DEFAULT.copy()

        self.camara.set_property(
            'saturation', self.config['saturacion'][1])
        self.camara.set_property(
            'contrast', self.config['contraste'][1])
        self.camara.set_property(
            'brightness', self.config['brillo'][1])
        self.camara.set_property(
            'hue', self.config['hue'][1])

        self.gamma.set_property(
            'gamma', self.config['gamma'][1])

        self.videoflip.set_property('method', 0)

        self.stop()

    def set_balance(self, brillo=False, contraste=False,
        saturacion=False, hue=False, gamma=False):
        """
        Seteos de balance en la fuente de video.
        Recibe % en float.
        """

        # Rangos: int. -2147483648 2147483647
        total = 2147483648*2

        if saturacion != False:
            new_valor = long(total * long(saturacion) / long(100))
            self.config['saturacion'] = (
                saturacion, new_valor - (total / 2))

            gobject.idle_add(self.camara.set_property,
                'saturation', self.config['saturacion'][1])

        if contraste != False:
            new_valor = long(total * long(contraste) / long(100))
            self.config['contraste'] = (
                contraste, new_valor - (total / 2))

            gobject.idle_add(self.camara.set_property,
                'contrast', self.config['contraste'][1])

        if brillo != False:
            new_valor = long(total * long(brillo) / long(100))
            self.config['brillo'] = (
                brillo, new_valor - (total / 2))

            gobject.idle_add(self.camara.set_property,
                'brightness', self.config['brillo'][1])

        if hue != False:
            new_valor = long(total * long(hue) / long(100))
            self.config['hue'] = (
                hue, new_valor - (total / 2))

            gobject.idle_add(self.camara.set_property,
                'hue', self.config['hue'][1])

        if gamma != False:
            # Double. Range: 0,01 - 10 Default: 1
            self.config['gamma'] = (
                gamma, (10.0 * gamma / 100.0))

            gobject.idle_add(self.gamma.set_property,
                'gamma', self.config['gamma'][1])
