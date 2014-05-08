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

import gst
import gobject

gobject.threads_init()


class Efectos_bin(gst.Bin):

    def __init__(self, efectos):

        gst.Bin.__init__(self)

        self.set_name('Efectos_bin')

        queue = gst.element_factory_make(
            'queue', "queue")
        #queue.set_property("max-size-buffers", 0)
        #queue.set_property("max-size-time", 0)
        #queue.set_property("max-size-bytes", 32000)
        #queue.set_property("leaky", 2)

        ffmpegout = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")

        self.add(queue)
        self.add(ffmpegout)

        elementos = []
        cont = 1

        for efecto in efectos:
            ffmpegcolorspaceefecto = gst.element_factory_make(
                'ffmpegcolorspace', "ffmpegcolorspace%s" % cont)

            ef = gst.element_factory_make(
                efecto, efecto)

            elementos.append(ffmpegcolorspaceefecto)
            elementos.append(ef)

            cont += 1

        for elemento in elementos:
            self.add(elemento)
            index = elementos.index(elemento)

            if index > 0:
                elementos[index - 1].link(elementos[index])

        queue.link(elementos[0])
        elementos[-1].link(ffmpegout)

        self.add_pad(gst.GhostPad(
            "sink", queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad(
            "src", ffmpegout.get_static_pad("src")))

    def set_efecto(self, efecto, propiedad, valor):
        """
        Setea propiedades de efectos en el pipe.
        """

        ef = self.get_by_name(efecto)

        if ef:
            ef.set_property(propiedad, valor)


class Camara_ogv_out_bin(gst.Bin):

    def __init__(self, path_archivo):

        gst.Bin.__init__(self)

        self.set_name('ogv_out_bin')

        autoaudiosrc = gst.element_factory_make(
            'autoaudiosrc', "autoaudiosrc")

        vorbisenc = gst.element_factory_make(
            'vorbisenc', 'vorbisenc')

        self.add(autoaudiosrc)
        self.add(vorbisenc)

        autoaudiosrc.link(vorbisenc)

        oggmux = gst.element_factory_make(
            'oggmux', "oggmux")

        archivo = gst.element_factory_make(
            'filesink', "filesink")

        self.add(oggmux)
        self.add(archivo)

        vorbisenc.link(oggmux)
        oggmux.link(archivo)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspacetheora")
        theoraenc = gst.element_factory_make(
            'theoraenc', 'theoraenc')
        theoraenc.set_property("quality", 16)

        self.add(ffmpegcolorspace)
        self.add(theoraenc)

        ffmpegcolorspace.link(theoraenc)
        theoraenc.link(oggmux)

        archivo.set_property(
            "location", path_archivo)

        self.add_pad(gst.GhostPad(
            "sink", ffmpegcolorspace.get_static_pad("sink")))
