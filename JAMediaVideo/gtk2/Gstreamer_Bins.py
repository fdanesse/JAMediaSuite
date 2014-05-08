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
        queue.set_property("max-size-buffers", 32000)
        queue.set_property("min-threshold-buffers", 0)
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

        audiorate = gst.element_factory_make(
            'audiorate', "audiorate")

        capaaudio = gst.Caps(
            "audio/x-raw-int,rate=16000,channels=2,depth=16")
        filtroaudio = gst.element_factory_make(
            "capsfilter", "filtroaudio")
        filtroaudio.set_property("caps", capaaudio)

        queueaudio = gst.element_factory_make(
            'queue', "queueaudio")
        queueaudio.set_property("max-size-buffers", 32000)
        queueaudio.set_property("min-threshold-buffers", 0)

        audioconvert = gst.element_factory_make(
            'audioconvert', "audioconvert")

        vorbisenc = gst.element_factory_make(
            'vorbisenc', 'vorbisenc')

        self.add(autoaudiosrc)
        self.add(audiorate)
        self.add(filtroaudio)
        self.add(queueaudio)
        self.add(audioconvert)
        self.add(vorbisenc)

        autoaudiosrc.link(audiorate)
        audiorate.link(filtroaudio)
        filtroaudio.link(queueaudio)
        queueaudio.link(audioconvert)
        audioconvert.link(vorbisenc)

        queueaudiomuxor = gst.element_factory_make(
            'queue', "queueaudiomuxor")
        queueaudiomuxor.set_property("max-size-buffers", 32000)
        queueaudiomuxor.set_property("min-threshold-buffers", 0)
        oggmux = gst.element_factory_make(
            'oggmux', "oggmux")
        archivo = gst.element_factory_make(
            'filesink', "filesink")

        self.add(queueaudiomuxor)
        self.add(oggmux)
        self.add(archivo)

        vorbisenc.link(queueaudiomuxor)
        queueaudiomuxor.link(oggmux)

        queuevideo = gst.element_factory_make(
            'queue', "queuevideo")
        queuevideo.set_property("max-size-buffers", 32000)
        queuevideo.set_property("min-threshold-buffers", 0)

        #scale = gst.element_factory_make("videoscale", "vbscale")
        #scalecapsfilter = gst.element_factory_make("capsfilter", "scalecaps")
        #scalecaps = gst.Caps("video/x-raw-yuv,width=160,height=120")
        # 'video/x-raw-yuv,width=320,height=240''video/x-raw-yuv,width=160,height=120'
        #scalecapsfilter.set_property("caps", scalecaps)

        self.add(queuevideo)
        #self.add(scale)
        #self.add(scalecapsfilter)

        #queue.link(scale)
        #scale.link(scalecapsfilter)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspacetheora")
        theoraenc = gst.element_factory_make(
            'theoraenc', 'theoraenc')
        theoraenc.set_property("quality", 16)
        queuevideomuxor = gst.element_factory_make(
            'queue', "queuevideomuxor")
        queuevideomuxor.set_property("max-size-buffers", 32000)
        queuevideomuxor.set_property("min-threshold-buffers", 0)

        self.add(ffmpegcolorspace)
        self.add(theoraenc)
        self.add(queuevideomuxor)

        queuevideo.link(ffmpegcolorspace)
        #scalecapsfilter.link(ffmpegcolorspace)
        ffmpegcolorspace.link(theoraenc)
        theoraenc.link(queuevideomuxor)
        queuevideomuxor.link(oggmux)

        queuearchivo = gst.element_factory_make(
            'queue', "queuearchivo")
        queuearchivo.set_property("max-size-buffers", 32000)
        queuearchivo.set_property("min-threshold-buffers", 0)

        self.add(queuearchivo)

        oggmux.link(queuearchivo)
        queuearchivo.link(archivo)

        archivo.set_property(
            "location", path_archivo)

        self.add_pad(gst.GhostPad(
            "sink", queuevideo.get_static_pad("sink")))
