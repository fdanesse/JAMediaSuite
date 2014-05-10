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


class Theora_bin(gst.Bin):
    """
    Comprime video utilizando theoraenc.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Theora_bin')

        queue = gst.element_factory_make(
            'queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        #scale = gst.element_factory_make("videoscale", "vbscale")
        #scalecapsfilter = gst.element_factory_make(
        #   "capsfilter", "scalecaps")
        #scalecaps = gst.Caps("video/x-raw-yuv,width=160,height=120")
        #   'video/x-raw-yuv,width=320,height=240''video/x-raw-yuv,
        #   width=160,height=120'
        #scalecapsfilter.set_property("caps", scalecaps)

        #self.add(scale)
        #self.add(scalecapsfilter)

        #queue.link(scale)
        #scale.link(scalecapsfilter)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspacetheora")
        theoraenc = gst.element_factory_make(
            'theoraenc', 'theoraenc')
        theoraenc.set_property("quality", 16)

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(theoraenc)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(theoraenc)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            theoraenc.get_static_pad("src")))


class Vorbis_bin(gst.Bin):
    """
    Comprime Audio utilizando vorbisenc.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Vorbis_bin')

        autoaudiosrc = gst.element_factory_make(
            'autoaudiosrc', "autoaudiosrc")
        audiorate = gst.element_factory_make(
            'audiorate', "audiorate")

        capaaudio = gst.Caps(
            "audio/x-raw-int,rate=16000,channels=2,depth=16")
        filtroaudio = gst.element_factory_make(
            "capsfilter", "filtroaudio")
        filtroaudio.set_property("caps", capaaudio)

        audioconvert = gst.element_factory_make(
            'audioconvert', "audioconvert")

        vorbisenc = gst.element_factory_make(
            'vorbisenc', 'vorbisenc')

        self.add(autoaudiosrc)
        self.add(audiorate)
        self.add(filtroaudio)
        self.add(audioconvert)
        self.add(vorbisenc)

        autoaudiosrc.link(audiorate)
        audiorate.link(filtroaudio)
        filtroaudio.link(audioconvert)
        audioconvert.link(vorbisenc)

        self.add_pad(gst.GhostPad("src",
            vorbisenc.get_static_pad("src")))


# FIXME: Por algún motivo no linkea
class Xvimage_bin(gst.Bin):
    """
    Salida de Video a pantalla utilizando xvimagesink.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Xvimage_bin')

        queue = gst.element_factory_make(
            'queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspacegtk")
        xvimagesink = gst.element_factory_make(
            'xvimagesink', "xvimagesink")
        xvimagesink.set_property(
            "force-aspect-ratio", True)

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(xvimagesink)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(xvimagesink)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))


class Balance_bin(gst.Bin):
    """
    Bin con brillo, contraste, saturación, hue y rotación.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Balance_bin')

        self.config = {
            'saturacion': 50.0,
            'contraste': 50.0,
            'brillo': 50.0,
            'hue': 50.0,
            'gamma': 10.0}

        videobalance = gst.element_factory_make(
            "videobalance", "videobalance")
        gamma = gst.element_factory_make(
            "gamma", "gamma")
        videoflip = gst.element_factory_make(
            "videoflip", "videoflip")

        self.add(videobalance)
        self.add(gamma)
        self.add(videoflip)

        videobalance.link(gamma)
        gamma.link(videoflip)

        self.add_pad(gst.GhostPad("sink",
            videobalance.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            videoflip.get_static_pad("src")))

    def rotar(self, valor):
        """
        Rota el video.
        """

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

        gobject.idle_add(videoflip.set_property,
            'method', rot)

    def set_rotacion(self, rot):

        videoflip = self.get_by_name("videoflip")
        videoflip.set_property(
            'method', rot)

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        """
        Recibe % en float y convierte a los valores del filtro.
        """

        balance = self.get_by_name("videobalance")
        gammabin = self.get_by_name("gamma")

        if brillo:
            self.config['brillo'] = brillo
            valor = (2.0 * brillo / 100.0) - 1.0
            balance.set_property(
                'brightness', valor)

        if contraste:
            self.config['contraste'] = contraste
            valor = 2.0 * contraste / 100.0
            balance.set_property(
                'contrast', valor)

        if saturacion:
            self.config['saturacion'] = saturacion
            valor = 2.0 * saturacion / 100.0
            balance.set_property(
                'saturation', valor)

        if hue:
            self.config['hue'] = hue
            valor = (2.0 * hue / 100.0) - 1.0
            balance.set_property(
                'hue', valor)

        if gamma:
            self.config['gamma'] = gamma
            valor = (10.0 * gamma / 100.0)
            gammabin.set_property(
                'gamma', valor)

    def get_config(self):

        return self.config.copy()

    def get_rotacion(self):

        videoflip = self.get_by_name("videoflip")
        return videoflip.get_property('method')


class v4l2src_bin(gst.Bin):
    """
    Bin de entrada de camara v4l2src.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('jamedia_camara_bin')

        camara = gst.element_factory_make(
            "v4l2src", "v4l2src")

        caps = gst.Caps('video/x-raw-rgb,framerate=30/1')
        camerafilter = gst.element_factory_make(
            "capsfilter", "camera_filter")
        camerafilter.set_property("caps", caps)

        self.add(camara)
        self.add(camerafilter)

        camara.link(camerafilter)

        self.add_pad(gst.GhostPad("src",
            camerafilter.get_static_pad("src")))

    def set_device(self, device):

        camara = self.get_by_name("v4l2src")
        camara.set_property("device", device)


class Video_Efectos_bin(gst.Bin):
    """
    Bin para efectos de Video.
    """

    def __init__(self, efectos):

        gst.Bin.__init__(self)

        self.set_name('Efectos_bin')

        queue = gst.element_factory_make(
            'queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

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
    """
    Toma el audio desde autoaudio en vorbisbin.
    Recibe fuente de video y la pasa por theorabin.
        Graba Audio y Video en Formato ogv.
    """

    def __init__(self, path_archivo):

        gst.Bin.__init__(self)

        self.set_name('ogv_out_bin')

        vorbisbin = Vorbis_bin()
        theorabin = Theora_bin()

        oggmux = gst.element_factory_make(
            'oggmux', "oggmux")

        queue = gst.element_factory_make(
            'queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        archivo = gst.element_factory_make(
            'filesink', "filesink")

        self.add(vorbisbin)
        self.add(theorabin)
        self.add(oggmux)
        self.add(queue)
        self.add(archivo)

        vorbisbin.link(oggmux)
        theorabin.link(oggmux)
        oggmux.link(queue)
        queue.link(archivo)

        archivo.set_property(
            "location", path_archivo)

        self.add_pad(gst.GhostPad(
            "sink", theorabin.get_static_pad("sink")))
