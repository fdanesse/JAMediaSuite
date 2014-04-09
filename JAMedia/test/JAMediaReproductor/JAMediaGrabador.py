#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGrabador.py por:
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

gobject.threads_init()


class JAMediaGrabador(gobject.GObject):
    """
    Graba en formato ogg desde un streaming de radio o tv.
    Convierte un archivo de audio o video a ogg.
    """

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "endfile": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, [])}

    def __init__(self, uri, archivo, tipo):

        gobject.GObject.__init__(self)

        self.tipo = tipo

        if not archivo.endswith(".ogg"):
            archivo = "%s%s" % (archivo, ".ogg")
            #archivo = "%s%s" % (archivo, ".mp3")

        self.patharchivo = archivo
        self.actualizador = False
        self.control = 0
        self.tamanio = 0
        self.uri = ""

        self.pipeline = None
        self.player = None
        self.archivo = None
        self.bus = None

        self.__reset()

        print "JAMediaGrabador:" uri

        if os.path.exists(uri):
            # FIXME: Analizar
            #uri = gst.filename_to_uri(uri)
            uri = "file://" + uri

        if gst.uri_is_valid(uri):
            self.archivo.set_property("location", self.patharchivo)
            self.uri = uri
            self.player.set_property("uri", self.uri)
            self.__play()
            self.__new_handle(True, [])

        else:
            self.emit("endfile")

    def __reset(self):
        """
        Crea el pipe de gst. (playbin)
        """

        self.pipeline = gst.Pipeline()

        self.player = gst.element_factory_make(
            "uridecodebin", "uridecodebin")

        self.pipeline.add(self.player)

        # AUDIO
        audioconvert = gst.element_factory_make(
            'audioconvert', 'audioconvert')

        audioresample = gst.element_factory_make(
            'audioresample', 'audioresample')
        audioresample.set_property('quality', 10)

        vorbisenc = gst.element_factory_make(
            'vorbisenc', 'vorbisenc')

        self.pipeline.add(audioconvert)
        self.pipeline.add(audioresample)
        self.pipeline.add(vorbisenc)

        audioconvert.link(audioresample)
        audioresample.link(vorbisenc)

        self.audio_sink = audioconvert.get_static_pad('sink')

        # VIDEO
        videoconvert = gst.element_factory_make(
            'ffmpegcolorspace', 'videoconvert')

        videorate = gst.element_factory_make(
            'videorate', 'videorate')

        try:
            videorate.set_property('max-rate', 30)
        except:
            pass

        theoraenc = gst.element_factory_make(
            'theoraenc', 'theoraenc')

        if self.tipo == "video":
            self.pipeline.add(videoconvert)
            self.pipeline.add(videorate)
            self.pipeline.add(theoraenc)

            videoconvert.link(videorate)
            videorate.link(theoraenc)

        self.video_sink = videoconvert.get_static_pad('sink')

        # MUXOR y ARCHIVO
        oggmux = gst.element_factory_make(
            'oggmux', "oggmux")
        self.archivo = gst.element_factory_make(
            'filesink', "filesink")

        self.pipeline.add(oggmux)
        self.pipeline.add(self.archivo)

        vorbisenc.link(oggmux)

        if self.tipo == "video":
            theoraenc.link(oggmux)

        oggmux.link(self.archivo)

        self.bus = self.pipeline.get_bus()

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        self.player.connect('pad-added', self.__pad_added)
        #self.player.connect("source-setup", self.__source_setup)

    def __pad_added(self, uridecodebin, pad):
        """
        Agregar elementos en forma dinámica según
        sean necesarios. https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """

        caps = pad.get_caps()
        string = caps.to_string()

        if string.startswith('audio'):
            if not self.audio_sink.is_linked():
                pad.link(self.audio_sink)

        elif string.startswith('video'):
            if not self.video_sink.is_linked():
                pad.link(self.video_sink)

    def __play(self, widget=None, event=None):

        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self, widget=None, event=None):
        """
        Detiene y limpia el pipe.
        """

        self.pipeline.set_state(gst.STATE_NULL)
        self.__new_handle(False, [])

        if os.path.exists(self.patharchivo):
            os.chmod(self.patharchivo, 0755)

    def __sync_message(self, bus, message):
        """
        Captura los messages en el bus del pipe gst.
        """

        if message.type == gst.MESSAGE_EOS:
            self.__new_handle(False, [])
            self.emit("endfile")

        elif message.type == gst.MESSAGE_LATENCY:
            self.player.recalculate_latency()

        elif message.type == gst.MESSAGE_ERROR:
            print "\n gst.MESSAGE_ERROR:"
            print message.parse_error()
            self.__new_handle(False, [])

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

        if os.path.exists(self.patharchivo):
            tamanio = os.path.getsize(self.patharchivo)
            tam = int(tamanio) / 1024.0 / 1024.0

            if self.tamanio != tamanio:
                self.control = 0
                self.tamanio = tamanio

                texto = str(self.uri)

                if len(self.uri) > 25:
                    texto = str(self.uri[0:25]) + " . . . "

                info = "Grabando: %s %.2f Mb" % (texto, tam)

                self.emit('update', info)

            else:
                self.control += 1

        if self.control > 60:
            self.stop()
            self.emit("endfile")
            return False

        return True

    #def __source_setup(self, player, source):

    #    self.uri = source.get_property('location')
    #    # print "Grabando:", self.uri

    #def __about_to_finish(self, player):

        #print "\n>>>", "about-to-finish"
    #    pass

    #def __audio_tags_changed(self, player, otro):

        #print "\n>>>", "audio-tags-changed"
    #    pass

'''
    def __mp3_reset(self):
        """
        Grabar audio mp3
        """

        self.player = gst.element_factory_make("playbin", "player")

        audioconvert = gst.element_factory_make('audioconvert', "audioconvert")
        mp3enc = gst.element_factory_make('lamemp3enc', "lamemp3enc")

        self.archivo = gst.element_factory_make('filesink', "archivo")

        jamedia_sink = gst.Bin()
        jamedia_sink.add(audioconvert)

        pad = audioconvert.get_static_pad('sink')
        ghostpad = gst.GhostPad.new('sink', pad)
        jamedia_sink.add_pad(ghostpad)

        jamedia_sink.add(mp3enc)
        jamedia_sink.add(self.archivo)

        audioconvert.link(mp3enc)
        mp3enc.link(self.archivo)

        self.player.set_property('audio-sink', jamedia_sink)

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_message)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        #self.player.connect("about-to-finish", self.__about_to_finish)
        #self.player.connect("audio-tags-changed", self.__audio_tags_changed)
        self.player.connect("source-setup", self.__source_setup)
'''


def update(grabador, datos):
    print datos


def end(grabador):
    import sys
    sys.exit(0)


if __name__ == "__main__":

    import sys

    print "Iniciando Grabador . . ."

    if not len(sys.argv) == 4:
        print "Debes pasar tres parámetros:"
        print "\t Dirección origen, puede ser url o file path."
        print "\t Nombre de archivo final, puede ser path completo o solo el nombre."
        print "\t Tipo de contenido, puede ser audio o video."

        sys.exit(0)

    uri = sys.argv[1]
    archivo = sys.argv[2]
    tipo = sys.argv[3]

    # FIXME: Esto Provoca: Violación de segmento
    grabador = JAMediaGrabador(uri, archivo, tipo)

    grabador.connect('update', update)
    grabador.connect('endfile', end)
