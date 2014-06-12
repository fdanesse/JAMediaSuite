#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VideoBins.py por:
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

#gobject.threads_init()


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


class xvimage_bin(gst.Bin):
    """
    Salida de video a pantalla.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('xvimage_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        xvimagesink = gst.element_factory_make(
            'xvimagesink', "xvimagesink")
        xvimagesink.set_property("force-aspect-ratio", True)
        xvimagesink.set_property("sync", False)

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(xvimagesink)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(xvimagesink)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))


class Foto_bin(gst.Bin):

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Foto_bin')

        queue = gst.element_factory_make("queue", "queue")
        queue.set_property("leaky", 1)
        queue.set_property("max-size-buffers", 1)

        ffmpegcolorspace = gst.element_factory_make(
            "ffmpegcolorspace", "ffmpegcolorspace")

        gdkpixbufsink = gst.element_factory_make(
            "gdkpixbufsink", "gdkpixbufsink")

        gdkpixbufsink.set_property("post-messages", False)

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(gdkpixbufsink)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(gdkpixbufsink)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))


class Balance_bin(gst.Bin):
    """
    Bin con brillo, contraste, saturación, hue, gamma y rotación.
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
        videoflip.set_property('method', rot)

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


class Video_Efectos_bin(gst.Bin):
    """
    Bin para efectos de Video.
    """

    def __init__(self, efectos):

        gst.Bin.__init__(self)

        self.set_name('Efectos_bin')

        queue = gst.element_factory_make('queue', "queue")
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


class Theora_bin(gst.Bin):
    """
    Comprime video utilizando theoraenc.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Theora_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
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


class mpeg2_bin(gst.Bin):
    """
    Comprime video utilizando ffenc_mpeg2video.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('mpeg2_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        ffenc_mpeg2video = gst.element_factory_make(
            'ffenc_mpeg2video', 'ffenc_mpeg2video')

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(ffenc_mpeg2video)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(ffenc_mpeg2video)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            ffenc_mpeg2video.get_static_pad("src")))


class Out_lan_smokeenc_bin(gst.Bin):
    """
    Volcado de video a la red lan.
    queue ! ffmpegcolorspace ! smokeenc ! udpsink host=192.168.1.1 port=5000
    """

    def __init__(self, ip):

        gst.Bin.__init__(self)

        self.set_name('out_lan_smokeenc_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")

        smokeenc = gst.element_factory_make(
            'smokeenc', "smokeenc")

        udpsink = gst.element_factory_make(
            'udpsink', "udpsink")

        udpsink.set_property("host", ip)
        udpsink.set_property("port", 5000)

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(smokeenc)
        self.add(udpsink)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(smokeenc)
        smokeenc.link(udpsink)

        self.add_pad(gst.GhostPad(
            "sink", queue.get_static_pad("sink")))


class In_lan_udpsrc_bin(gst.Bin):
    """
    Fuente de video desde red lan.
    udpsrc port=5000 ! queue ! smokedec ! autovideosink
    tcpclientsrc host=192.168.1.5 port=5001 ! queue ! speexdec !
        queue ! autoaudiosink
    """

    def __init__(self, ip):

        gst.Bin.__init__(self)

        self.set_name('in_lan_udpsrc_bin')

        udpsrc = gst.element_factory_make(
            'udpsrc', "udpsrc")
        udpsrc.set_property("port", 5000)

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        smokedec = gst.element_factory_make(
            'smokedec', "smokedec")

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")

        self.add(udpsrc)
        self.add(queue)
        self.add(smokedec)
        self.add(ffmpegcolorspace)

        udpsrc.link(queue)
        queue.link(smokedec)
        smokedec.link(ffmpegcolorspace)

        self.add_pad(gst.GhostPad(
            "src", ffmpegcolorspace.get_static_pad("src")))
