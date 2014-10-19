#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaBins.py por:
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

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo
from gi.repository import GdkX11

GObject.threads_init()


class JAMedia_Audio_Pipeline(Gst.Pipeline):

    def __init__(self):

        Gst.Pipeline.__init__(self)

        self.set_name('jamedia_audio_pipeline')

        convert = Gst.ElementFactory.make("audioconvert", "convert")
        sink = Gst.ElementFactory.make("autoaudiosink", "sink")

        self.add(convert)
        self.add(sink)

        convert.link(sink)

        pad = convert.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))


class JAMedia_Video_Pipeline(Gst.Pipeline):

    def __init__(self):

        Gst.Pipeline.__init__(self)

        self.set_name('jamedia_video_pipeline')

        self.config = {
            'saturacion': 50.0,
            'contraste': 50.0,
            'brillo': 50.0,
            'hue': 50.0,
            'gamma': 10.0,
            'rotacion': 0}

        convert = Gst.ElementFactory.make('videoconvert', 'convert')
        rate = Gst.ElementFactory.make('videorate', 'rate')
        videobalance = Gst.ElementFactory.make('videobalance', "videobalance")
        gamma = Gst.ElementFactory.make('gamma', "gamma")
        videoflip = Gst.ElementFactory.make('videoflip', "videoflip")
        pantalla = Gst.ElementFactory.make('xvimagesink', "pantalla")
        pantalla.set_property("force-aspect-ratio", True)

        try:  # FIXME: xo no posee esta propiedad
            rate.set_property('max-rate', 30)

        except:
            pass

        self.add(convert)
        self.add(rate)
        self.add(videobalance)
        self.add(gamma)
        self.add(videoflip)
        self.add(pantalla)

        convert.link(rate)
        rate.link(videobalance)
        videobalance.link(gamma)
        gamma.link(videoflip)
        videoflip.link(pantalla)

        pad = convert.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))

    def rotar(self, valor):
        videoflip = self.get_by_name("videoflip")
        rot = videoflip.get_property('method')

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

        videoflip.set_property('method', rot)

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        if brillo:
            self.config['brillo'] = brillo
            valor = (2.0 * brillo / 100.0) - 1.0
            self.get_by_name("videobalance").set_property('brightness', valor)

        if contraste:
            self.config['contraste'] = contraste
            valor = 2.0 * contraste / 100.0
            self.get_by_name("videobalance").set_property('contrast', valor)

        if saturacion:
            self.config['saturacion'] = saturacion
            valor = 2.0 * saturacion / 100.0
            self.get_by_name("videobalance").set_property('saturation', valor)

        if hue:
            self.config['hue'] = hue
            valor = (2.0 * hue / 100.0) - 1.0
            self.get_by_name("videobalance").set_property('hue', valor)

        if gamma:
            self.config['gamma'] = gamma
            valor = (10.0 * gamma / 100.0)
            self.get_by_name("gamma").set_property('gamma', valor)

    def get_balance(self):
        return self.config
