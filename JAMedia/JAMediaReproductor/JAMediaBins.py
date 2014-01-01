#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaBins.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay
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
from gi.repository import GstVideo  # necesario

GObject.threads_init()
Gst.init([])


class JAMedia_Efecto_bin(Gst.Bin):
    """
    Bin para efecto de video individual.
        videoconvert ! efecto
    """

    def __init__(self, efecto):

        Gst.Bin.__init__(self)

        self.set_name(efecto)

        videoconvert = Gst.ElementFactory.make(
            "videoconvert",
            "videoconvert_%s" % (efecto))

        efecto = Gst.ElementFactory.make(efecto, efecto)

        self.add(videoconvert)
        self.add(efecto)

        videoconvert.link(efecto)

        self.add_pad(Gst.GhostPad.new(
            "sink", videoconvert.get_static_pad("sink")))
        self.add_pad(Gst.GhostPad.new(
            "src", efecto.get_static_pad("src")))


class JAMedia_Camara_bin(Gst.Bin):
    """
    Bin para cámara y sus configuraciones
    particulares.
    """

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('jamedia_camara_bin')

        self.camara = Gst.ElementFactory.make("v4l2src", "v4l2src")

        caps = Gst.Caps.from_string('video/x-raw,framerate=10/1')
        camerafilter = Gst.ElementFactory.make("capsfilter", "camera_filter")
        camerafilter.set_property("caps", caps)

        self.add(self.camara)
        self.add(camerafilter)

        self.camara.link(camerafilter)

        self.add_pad(Gst.GhostPad.new(
            "src", camerafilter.get_static_pad("src")))


class Theoraenc_bin(Gst.Bin):
    """
    Bin para elementos codificadores
    de video a theoraenc.
    """

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('video_theoraenc_bin')

        que_encode_video = Gst.ElementFactory.make(
            "queue", "que_encode_video")
        que_encode_video.set_property('max-size-buffers', 1000)
        que_encode_video.set_property('max-size-bytes', 0)
        que_encode_video.set_property('max-size-time', 0)

        theoraenc = Gst.ElementFactory.make('theoraenc', 'theoraenc')
        # kbps compresion + resolucion = calidad
        theoraenc.set_property("bitrate", 1024)
        theoraenc.set_property('keyframe-freq', 15)
        theoraenc.set_property('cap-overflow', False)
        theoraenc.set_property('speed-level', 0)
        theoraenc.set_property('cap-underflow', True)
        theoraenc.set_property('vp3-compatible', True)

        self.add(que_encode_video)
        self.add(theoraenc)

        que_encode_video.link(theoraenc)

        pad = que_encode_video.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))

        pad = theoraenc.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))


class Vorbisenc_bin(Gst.Bin):
    """
    Bin para elementos codificadores
    de audio a vorbisenc.
    """

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('audio_vorbisenc_bin')

        # FIXME: Corregir para no tomar autoaudiosrc
        autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc")
        audiorate = Gst.ElementFactory.make('audiorate', "audiorate")
        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")

        self.add(autoaudiosrc)
        self.add(audiorate)
        self.add(audioconvert)
        self.add(vorbisenc)

        autoaudiosrc.link(audiorate)
        audiorate.link(audioconvert)
        audioconvert.link(vorbisenc)

        pad = vorbisenc.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))


class Foto_bin(Gst.Bin):
    """
    Bin para tomar fotografías.
    """

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('foto_bin')

        videoconvert = Gst.ElementFactory.make(
            "videoconvert", "videoconvert_gdkpixbuf")

        queue = Gst.ElementFactory.make("queue", "queue_foto")
        queue.set_property("leaky", 1)
        queue.set_property("max-size-buffers", 1)

        gdkpixbufsink = Gst.ElementFactory.make(
            "gdkpixbufsink", "gdkpixbufsink")

        #gdkpixbufsink.set_property('post-messages', False)

        self.add(queue)
        self.add(videoconvert)
        self.add(gdkpixbufsink)

        queue.link(videoconvert)
        videoconvert.link(gdkpixbufsink)

        pad = queue.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))


class Efectos_Video_bin(Gst.Bin):
    """
    Bin para agregar efectos de video.
        queue ! [ efecto=videoconvert ! efecto, . . .] ! videoconvert
    """

    def __init__(self, efectos, config_efectos):

        Gst.Bin.__init__(self)

        self.set_name('efectos_bin')

        self.efectos = efectos
        self.config_efectos = config_efectos

        queue = Gst.ElementFactory.make('queue', "queue")
        #queue.set_property('max-size-buffers', 1000)
        #queue.set_property('max-size-bytes', 0)
        #queue.set_property('max-size-time', 0)

        videoconvert = Gst.ElementFactory.make(
            'videoconvert',
            "videoconvert_efectos")

        self.add(queue)

        efectos = []
        for nombre in self.efectos:
            # Crea el efecto
            efecto = JAMedia_Efecto_bin(nombre)
            if efecto and efecto != None:
                efectos.append(efecto)

        if efectos:
            for efecto in efectos:
                # Agrega el efecto
                self.add(efecto)

            # queue a primer efecto
            queue.link(efectos[0])

            for efecto in efectos:
                index = efectos.index(efecto)
                if len(efectos) > index + 1:
                    # Linkea los efectos entre si
                    efecto.link(efectos[efectos.index(efecto) + 1])

            self.add(videoconvert)
            # linkea el ultimo efecto a videoconvert
            efectos[-1].link(videoconvert)

        else:
            self.add(videoconvert)
            queue.link(videoconvert)

        # Mantener la configuración de cada efecto.
        for efecto in self.config_efectos.keys():
            for property in self.config_efectos[efecto].keys():
                bin_efecto = self.get_by_name(efecto)
                elemento = bin_efecto.get_by_name(efecto)
                elemento.set_property(property,
                    self.config_efectos[efecto][property])

        self.add_pad(Gst.GhostPad.new(
            "sink", queue.get_static_pad("sink")))
        self.add_pad(Gst.GhostPad.new(
            "src", videoconvert.get_static_pad("src")))


class Audio_Visualizador_bin(Gst.Bin):
    """
    Bin visualizador de audio.
    """

    def __init__(self, visualizador):

        Gst.Bin.__init__(self)

        self.set_name('audio_visualizador_bin')

        self.visualizador = visualizador

        queue = Gst.ElementFactory.make("queue", "queue")

        efecto = Gst.ElementFactory.make(
            self.visualizador,
            self.visualizador)

        videoconvert = Gst.ElementFactory.make('videoconvert', "videoconvert")

        self.add(queue)
        self.add(efecto)
        self.add(videoconvert)

        queue.link(efecto)
        efecto.link(videoconvert)

        pad = queue.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))

        pad = videoconvert.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))


class Video_Balance_Bin(Gst.Bin):
    """
    Gestor de Video Intermedio para controlar:
        brillo,
        contraste,
        saturación,
        matiz,
        gamma,
        rotación.
    """

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('video_balance_bin')

        self.config_default = {
            'saturacion': 1.0,
            'contraste': 1.0,
            'brillo': 0.0,
            'hue': 0.0,
            'gamma': 1.0,
            }

        self.config = {}
        self.config['saturacion'] = self.config_default['saturacion']
        self.config['contraste'] = self.config_default['contraste']
        self.config['brillo'] = self.config_default['brillo']
        self.config['hue'] = self.config_default['hue']
        self.config['gamma'] = self.config_default['gamma']

        self.videobalance = Gst.ElementFactory.make(
            'videobalance',
            "videobalance")

        self.gamma = Gst.ElementFactory.make(
            'gamma',
            "gamma")

        self.videoflip = Gst.ElementFactory.make(
            'videoflip',
            "videoflip")

        self.add(self.videobalance)
        self.add(self.gamma)
        self.add(self.videoflip)

        self.videobalance.link(self.gamma)
        self.gamma.link(self.videoflip)

        pad = self.videobalance.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))

        pad = self.videoflip.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))

    def reset(self):
        """
        Devuelve balance y rotación al estado original.
        """

        self.config['saturacion'] = self.config_default['saturacion']
        self.config['contraste'] = self.config_default['contraste']
        self.config['brillo'] = self.config_default['brillo']
        self.config['hue'] = self.config_default['hue']
        self.config['gamma'] = self.config_default['gamma']

        self.videobalance.set_property('saturation', self.config['saturacion'])
        self.videobalance.set_property('contrast', self.config['contraste'])
        self.videobalance.set_property('brightness', self.config['brillo'])
        self.videobalance.set_property('hue', self.config['hue'])
        self.gamma.set_property('gamma', self.config['gamma'])

        self.videoflip.set_property('method', 0)

    def set_balance(self, brillo=False, contraste=False,
        saturacion=False, hue=False, gamma=False):
        """
        Seteos de balance en la fuente de video.
        Recibe % en float y convierte a los valores del filtro.
        """

        if saturacion:
            # Double. Range: 0 - 2 Default: 1
            self.config['saturacion'] = 2.0 * saturacion / 100.0
            self.videobalance.set_property(
                'saturation', self.config['saturacion'])

        if contraste:
            # Double. Range: 0 - 2 Default: 1
            self.config['contraste'] = 2.0 * contraste / 100.0
            self.videobalance.set_property(
                'contrast', self.config['contraste'])

        if brillo:
            # Double. Range: -1 - 1 Default: 0
            self.config['brillo'] = (2.0 * brillo / 100.0) - 1.0
            self.videobalance.set_property(
                'brightness', self.config['brillo'])

        if hue:
            # Double. Range: -1 - 1 Default: 0
            self.config['hue'] = (2.0 * hue / 100.0) - 1.0
            self.videobalance.set_property('hue', self.config['hue'])

        if gamma:
            # Double. Range: 0,01 - 10 Default: 1
            self.config['gamma'] = (10.0 * gamma / 100.0)
            self.gamma.set_property('gamma', self.config['gamma'])

    # FIXME: No es correcto si se llama a los valores reales.
    #def get_balance(self):
    #    """
    #    Retorna los valores actuales de balance en % float.
    #    """

    #    return {
    #    'saturacion': self.config['saturacion'] * 100.0 / 2.0,
    #    'contraste': self.config['contraste'] * 100.0 / 2.0,
    #    'brillo': (self.config['brillo']+1) * 100.0 / 2.0,
    #    'hue': (self.config['hue']+1) * 100.0 / 2.0,
    #    'gamma': self.config['gamma'] * 100.0 / 10.0
    #    }

    def rotar(self, valor):
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

    def get_rotacion(self):
        """
        Devuelve el valor configurado para rotacion.
        """

        return self.videoflip.get_property('method')

    def set_rotacion(self, valor):
        """
        Setea la rotacion directamente, recibe un entero.
        """

        return self.videoflip.set_property('method', valor)


class Pantalla_Bin(Gst.Bin):

    def __init__(self):

        Gst.Bin.__init__(self)

        self.set_name('Pantalla_bin')

        self.multi_out_tee = Gst.ElementFactory.make(
            'tee', "multi_out_tee")
        self.multi_out_tee.set_property('pull-mode', 1)

        self.pantalla = Gst.ElementFactory.make(
            'xvimagesink', "pantalla")

        #self.gdkpixbufsink = Gst.ElementFactory.make(
        #    "gdkpixbufsink", "gdkpixbufsink")

        self.add(self.multi_out_tee)
        self.add(self.pantalla)
        #self.add(self.gdkpixbufsink)

        #self.multi_out_tee.link(self.gdkpixbufsink)
        self.multi_out_tee.link(self.pantalla)

        self.add_pad(
            Gst.GhostPad.new(
                "sink",
                self.multi_out_tee.get_static_pad("sink")))


class JAMedia_Audio_Pipeline(Gst.Pipeline):
    """
    Gestor de Audio de JAMedia.
    """

    def __init__(self):

        Gst.Pipeline.__init__(self)

        self.set_name('jamedia_audio_pipeline')

        self.tee_audio = Gst.ElementFactory.make(
            "tee", "tee_audio")

        self.audioconvert = Gst.ElementFactory.make(
            "audioconvert", "audioconvert")

        self.autoaudiosink = Gst.ElementFactory.make(
            "autoaudiosink", "autoaudiosink")

        self.add(self.tee_audio)
        self.add(self.audioconvert)
        self.add(self.autoaudiosink)

        self.tee_audio.link(self.audioconvert)
        self.audioconvert.link(self.autoaudiosink)

        self.add_pad(
            Gst.GhostPad.new(
                "sink",
                self.tee_audio.get_static_pad("sink")))

        self.visualizador_bin = False
        self.xvimagesink = False

    def agregar_visualizador(self, visualizador):

        if not self.visualizador_bin:
            self.visualizador_bin = Audio_Visualizador_bin(visualizador)
            self.xvimagesink = Gst.ElementFactory.make(
                "xvimagesink", "xvimagesink")

            self.add(self.visualizador_bin)
            self.add(self.xvimagesink)

            self.tee_audio.link(self.visualizador_bin)
            self.visualizador_bin.link(self.xvimagesink)

    def quitar_visualizador(self):

        if self.visualizador_bin:
            self.visualizador_bin.unlink(self.xvimagesink)
            self.tee_audio.unlink(self.visualizador_bin)

            self.remove(self.visualizador_bin)
            self.remove(self.xvimagesink)

            del(self.visualizador_bin)
            del(self.xvimagesink)


class JAMedia_Video_Pipeline(Gst.Pipeline):
    """
    Gestor de Video de JAMedia.
    """

    def __init__(self):

        Gst.Pipeline.__init__(self)

        self.set_name('jamedia_video_pipeline')

        self.efectos = []
        self.config_efectos = {}

        self.efectos_bin = Efectos_Video_bin(
            self.efectos, self.config_efectos)
        self.video_balance_bin = Video_Balance_Bin()

        self.pantalla_bin = Pantalla_Bin()

        self.add(self.efectos_bin)
        self.add(self.video_balance_bin)
        self.add(self.pantalla_bin)

        self.efectos_bin.link(self.video_balance_bin)
        self.video_balance_bin.link(self.pantalla_bin)

        self.ghost_pad = Gst.GhostPad.new(
            "sink", self.efectos_bin.get_static_pad("sink"))

        self.ghost_pad.set_target(self.efectos_bin.get_static_pad("sink"))

        self.add_pad(self.ghost_pad)

    def reset_balance(self):

        self.video_balance_bin.reset()

    def set_balance(self, brillo=False, contraste=False,
        saturacion=False, hue=False, gamma=False):
        """
        Seteos de balance en video.
        Recibe % en float y convierte a los valores del filtro.
        """

        self.video_balance_bin.set_balance(brillo,
            contraste, saturacion, hue, gamma)

    def get_balance(self):
        """
        Retorna los valores actuales de balance en % float.
        """

        return self.video_balance_bin.get_balance()

    def rotar(self, valor):
        """
        Rota el Video.
        """

        self.video_balance_bin.rotar(valor)

    def set_rotacion(self, valor):
        """
        Setea la rotacion directamente, recibe un entero.
        """

        return self.video_balance_bin.set_rotacion(valor)

    def get_rotacion(self):
        """
        Devuelve el valor configurado para rotacion.
        """

        return self.video_balance_bin.get_rotacion()

    def agregar_efecto(self, nombre_efecto):
        """
        Agrega un efecto según su nombre.
        """

        self.efectos.append(nombre_efecto)
        self.config_efectos[nombre_efecto] = {}

        self.reconstruir_efectos()

    def quitar_efecto(self, indice_efecto):
        """
        Quita el efecto correspondiente al indice o
        al nombre que recibe.
        """

        if type(indice_efecto) == int:
            self.efectos.remove(self.efectos[indice_efecto])
            if self.efectos[indice_efecto] in self.config_efectos.keys():
                del (self.config_efectos[self.efectos[indice_efecto]])

        elif type(indice_efecto) == str:
            for efecto in self.efectos:
                if efecto == indice_efecto:
                    self.efectos.remove(efecto)
                    if efecto in self.config_efectos.keys():
                        del (self.config_efectos[efecto])
                    break

        self.reconstruir_efectos()

    def reconstruir_efectos(self):

        new_bin = Efectos_Video_bin(
            self.efectos, self.config_efectos)

        self.efectos_bin.unlink(self.video_balance_bin)
        self.remove(self.efectos_bin)
        del(self.efectos_bin)

        self.add(new_bin)
        self.efectos_bin = new_bin

        self.efectos_bin.link(self.video_balance_bin)

        self.ghost_pad.set_target(self.efectos_bin.get_static_pad("sink"))

    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        """
        Configura un efecto en el pipe.
        """

        bin_efecto = self.efectos_bin.get_by_name(nombre_efecto)
        self.config_efectos[nombre_efecto][propiedad] = valor
        bin_efecto.get_by_name(nombre_efecto).set_property(propiedad, valor)
