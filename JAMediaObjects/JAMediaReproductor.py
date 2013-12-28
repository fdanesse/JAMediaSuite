#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaReproductor.py por:
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

import os

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gst
from gi.repository import GstVideo

#GObject.threads_init()
Gst.init([])

# Guia: http://developer.gnome.org/gstreamer/stable/libgstreamer.html
# Manual: http://gstreamer.freedesktop.org/data/doc/gstreamer/head/manual/html/index.html
# https://wiki.ubuntu.com/Novacut/GStreamer1.0


class JAMediaReproductor(GObject.GObject):
    """
    Reproductor de Audio, Video y Streaming de
    Radio y Television. Implementado sobre:

        python 2.7.3
        Gtk 3
        Gstreamer 1.0
    """

    __gsignals__ = {
    "endfile": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "estado": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "newposicion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,)),
    "volumen": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,)),
    "video": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}

    # Estados: playing, paused, None

    def __init__(self, ventana_id):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """

        GObject.GObject.__init__(self)

        self.name = "JAMediaReproductor"
        self.ventana_id = ventana_id

        self.estado = None
        self.volumen = 0.10
        self.config = {
            'saturacion': 50.0,
            'contraste': 50.0,
            'brillo': 50.0,
            'hue': 50.0,
            'gamma': 10.0,
            'rotacion': 0}

        self.duracion = 0
        self.posicion = 0
        self.actualizador = False

        self.player = None
        self.bus = None

        from JAMediaGstreamer.JAMediaBins import JAMedia_Video_Pipeline
        from JAMediaGstreamer.JAMediaBins import JAMedia_Audio_Pipeline

        # Gestor de la salida de Video del reproductor.
        self.video_pipeline = JAMedia_Video_Pipeline()

        # Gestor de salida de Audio del reproductor.
        self.audio_pipelin = JAMedia_Audio_Pipeline()

        # Debe iniciarse como None (ver señal video)
        self.video_in_stream = None

        self.efectos = []
        #self.config_efectos = {}

        self.__reset()

    def __reset(self):

        # Reproductor.
        self.player = Gst.ElementFactory.make(
            "playbin", "player")
        self.player.set_property(
            'force-aspect-ratio', True)

        # Si no se establecen los valores al original, se produce un error.
        self.video_pipeline.reset_balance()
        self.player.set_property('volume', self.volumen)

        self.player.set_window_handle(self.ventana_id)
        self.player.set_property('video-sink', self.video_pipeline)
        self.player.set_property('audio-sink', self.audio_pipelin)

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        #self.video_in_stream = False

    def load(self, uri):
        """
        Carga un archivo o stream en el pipe de Gst.
        """

        self.stop()
        self.__reset()

        if os.path.exists(uri):
            # Archivo
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)
            self.__play()

        else:
            # Streaming
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.__play()

    def __re_config(self):
        """
        Luego de que está en play,
        recupera los valores configurados para balance y
        rotación y configura con ellos el balance en el pipe.
        """

        self.player.set_property('volume', self.volumen)
        self.video_pipeline.set_rotacion(self.config['rotacion'])
        self.video_pipeline.set_balance(
            brillo=self.config['brillo'],
            contraste=self.config['contraste'],
            saturacion=self.config['saturacion'],
            hue=self.config['hue'],
            gamma=self.config['gamma'])
        self.emit('volumen', self.volumen)

        return False

    def __play(self):
        """
        Pone el pipe de Gst en Gst.State.PLAYING
        """

        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        """
        Pone el pipe de Gst en Gst.State.NULL
        """

        self.player.set_state(Gst.State.NULL)

    def __pause(self):
        """
        Pone el pipe de Gst en Gst.State.PAUSED
        """

        self.player.set_state(Gst.State.PAUSED)

    def pause_play(self):
        """
        Llama a play() o pause()
        segun el estado actual del pipe de Gst.
        """

        if self.estado == Gst.State.PAUSED \
            or self.estado == Gst.State.NULL \
            or self.estado == Gst.State.READY:
            self.__play()

        elif self.estado == Gst.State.PLAYING:
            self.__pause()

    def rotar(self, valor):
        """
        Rota el Video.
        """

        self.video_pipeline.rotar(valor)
        self.config['rotacion'] = self.video_pipeline.get_rotacion()

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        """
        Seteos de balance en video.
        Recibe % en float y convierte a los valores del filtro.
        """

        if brillo:
            self.config['brillo'] = brillo

        if contraste:
            self.config['contraste'] = contraste

        if saturacion:
            self.config['saturacion'] = saturacion

        if hue:
            self.config['hue'] = hue

        if gamma:
            self.config['gamma'] = gamma

        self.video_pipeline.set_balance(
            brillo=brillo,
            contraste=contraste,
            saturacion=saturacion,
            hue=hue,
            gamma=gamma)

    def get_balance(self):
        """
        Retorna los valores actuales de balance en % float.
        """

        # No funciona llamar a los valores reales.
        #return self.video_pipeline.get_balance()
        return self.config

    def __new_handle(self, reset):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = GLib.timeout_add(500, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        bool1, valor1 = self.player.query_duration(Gst.Format.TIME)
        bool2, valor2 = self.player.query_position(Gst.Format.TIME)

        duracion = float(valor1)
        posicion = float(valor2)

        pos = 0
        try:
            pos = int(posicion * 100 / duracion)

        except:
            pass

        if pos < 0 or pos > self.duracion:
            return True

        if self.duracion != duracion:
            self.duracion = duracion

        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)
            # print "***", gst.video_convert_frame(
            #   self.player.get_property("frame"))

        return True

    def set_position(self, posicion):
        """
        Permite desplazarse por
        la pista que se esta reproduciendo.
        """

        if self.duracion < posicion:
            self.emit("newposicion", self.posicion)
            return

        posicion = self.duracion * posicion / 100

        self.player.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH |
            Gst.SeekFlags.KEY_UNIT,
            posicion)

    def set_volumen(self, valor):
        """
        Cambia el volúmen de Reproducción.
        """

        self.volumen = float(valor / 100)
        self.player.set_property('volume', self.volumen)

    def agregar_efecto(self, nombre_efecto):

        self.__new_handle(False)
        self.stop()

        self.efectos.append(nombre_efecto)
        #self.config_efectos[nombre_efecto] = {}
        self.video_pipeline.agregar_efecto(nombre_efecto)

        self.__play()
        self.__new_handle(True)

    def quitar_efecto(self, indice_efecto):

        if type(indice_efecto) == int:
            self.efectos.remove(self.efectos[indice_efecto])
            #if self.efectos[indice_efecto] in self.config_efectos.keys():
            #    del (self.config_efectos[self.efectos[indice_efecto]])

        elif type(indice_efecto) == str:
            for efecto in self.efectos:
                if efecto == indice_efecto:
                    self.efectos.remove(efecto)
                    #if efecto in self.config_efectos.keys():
                    #    del (self.config_efectos[efecto])
                    #break

        self.__new_handle(False)
        self.stop()

        self.video_pipeline.quitar_efecto(indice_efecto)

        self.__play()
        self.__new_handle(True)

    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        """
        Configura un efecto en el pipe.
        """

        self.video_pipeline.configurar_efecto(nombre_efecto, propiedad, valor)

    def __sync_message(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        '''
        # Esto no es necesario si:
        # self.player.set_window_handle(self.ventana_id)
        try:
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

        except:
            pass'''

        if mensaje.type == Gst.MessageType.STATE_CHANGED:
            old, new, pending = mensaje.parse_state_changed()

            if old == Gst.State.PAUSED and new == Gst.State.PLAYING:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "playing")
                    self.__new_handle(True)
                    GLib.idle_add(self.__re_config)
                    return

            elif old == Gst.State.READY and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")
                    self.__new_handle(False)
                    return

            elif old == Gst.State.READY and new == Gst.State.NULL:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "None")
                    self.__new_handle(False)
                    return

            elif old == Gst.State.PLAYING and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")
                    self.__new_handle(False)
                    return
            '''
            elif old == Gst.State.NULL and new == Gst.State.READY:
                pass

            elif old == Gst.State.PAUSED and new == Gst.State.READY:
                pass

            else:
                return'''

        elif mensaje.type == Gst.MessageType.TAG:
            taglist = mensaje.parse_tag()
            datos = taglist.to_string()

            if 'audio-codec' in datos and not 'video-codec' in datos:
                if self.video_in_stream == True or \
                    self.video_in_stream == None:

                    self.video_in_stream = False
                    self.emit("video", False)
                    #self.audio_pipelin.agregar_visualizador('monoscope')

            elif 'video-codec' in datos:
                if self.video_in_stream == False or \
                    self.video_in_stream == None:

                    self.video_in_stream = True
                    self.emit("video", True)
                    #self.audio_pipelin.quitar_visualizador()

            #self.duracion = int(taglist.to_string().split(
            #   "duration=(guint64)")[1].split(',')[0])

            #Ejemplo:
                # taglist,
                # duration=(guint64)780633000000,
                # video-codec=(string)H.264,
                # audio-codec=(string)"MPEG-4\ AAC"

            return

        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug
            self.__new_handle(False)
            return

        '''
        elif mensaje.type == Gst.MessageType.EOS:
            return

        elif mensaje.type == Gst.MessageType.ASYNC_DONE:
            return

        elif mensaje.type == Gst.MessageType.NEW_CLOCK:
            return

        elif mensaje.type == Gst.MessageType.STREAM_STATUS:
            return

        else:
            try:
                nombre = mensaje.get_structure().get_name()

                if nombre == "playbin-stream-changed":
                    pass

                elif nombre == "have-window-handle":
                    pass

                elif nombre == "prepare-window-handle":
                    pass

                else:
                    pass

            except:
                pass

            return'''

    def __on_mensaje(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        if mensaje.type == Gst.MessageType.EOS:
            #self.video_pipeline.seek_simple(Gst.Format.TIME,
            #Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug
            self.__new_handle(False)

        '''
        if mensaje.type == Gst.MessageType.ELEMENT:
            nombre = mensaje.get_structure().get_name()

        if mensaje.type == Gst.MessageType.ASYNC_DONE:
            print mensaje.get_structure().get_name()

        elif mensaje.type == Gst.MessageType.NEW_CLOCK:
            pass

        elif mensaje.type == Gst.MessageType.QOS:
            pass

        elif mensaje.type == Gst.MessageType.WARNING:
            pass

        elif mensaje.type == Gst.MessageType.LATENCY:
            pass

        else:
            pass'''


class JAMediaGrabador(GObject.GObject):
    """
    Graba en formato ogg desde un streaming de radio o tv.
    Convierte un archivo de audio o video a ogg.
    """

    __gsignals__ = {
    "update": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "endfile": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, uri, archivo, tipo):

        GObject.GObject.__init__(self)

        self.tipo = tipo

        if not archivo.endswith(".ogg"):
            archivo = "%s%s" % (archivo, ".ogg")
            #archivo = "%s%s" % (archivo, ".mp3")

        self.patharchivo = archivo
        self.actualizador = False
        self.control = 0
        self.info = ""
        self.uri = ""

        self.pipeline = None
        self.player = None
        self.archivo = None
        self.bus = None

        self.__reset()

        if os.path.exists(uri):
            uri = Gst.filename_to_uri(uri)

        if Gst.uri_is_valid(uri):
            self.archivo.set_property("location", self.patharchivo)
            self.player.set_property("uri", uri)
            self.__play()
            self.__new_handle(True)

        else:
            self.emit("endfile")

    def __reset(self):
        """
        Crea el pipe de Gst. (playbin)
        """

        self.pipeline = Gst.Pipeline()

        self.player = Gst.ElementFactory.make(
            "uridecodebin", "uridecodebin")

        self.pipeline.add(self.player)

        # AUDIO
        audioconvert = Gst.ElementFactory.make(
            'audioconvert', 'audioconvert')

        audioresample = Gst.ElementFactory.make(
            'audioresample', 'audioresample')
        audioresample.set_property('quality', 10)

        vorbisenc = Gst.ElementFactory.make(
            'vorbisenc', 'vorbisenc')

        self.pipeline.add(audioconvert)
        self.pipeline.add(audioresample)
        self.pipeline.add(vorbisenc)

        audioconvert.link(audioresample)
        audioresample.link(vorbisenc)

        self.audio_sink = audioconvert.get_static_pad('sink')

        # VIDEO
        videoconvert = Gst.ElementFactory.make(
            'videoconvert', 'videoconvert')

        videorate = Gst.ElementFactory.make(
            'videorate', 'videorate')
        videorate.set_property('max-rate', 30)

        theoraenc = Gst.ElementFactory.make(
            'theoraenc', 'theoraenc')

        if self.tipo == "video":
            self.pipeline.add(videoconvert)
            self.pipeline.add(videorate)
            self.pipeline.add(theoraenc)

            videoconvert.link(videorate)
            videorate.link(theoraenc)

        self.video_sink = videoconvert.get_static_pad('sink')

        # MUXOR y ARCHIVO
        oggmux = Gst.ElementFactory.make(
            'oggmux', "oggmux")
        self.archivo = Gst.ElementFactory.make(
            'filesink', "filesink")

        self.pipeline.add(oggmux)
        self.pipeline.add(self.archivo)

        vorbisenc.link(oggmux)

        if self.tipo == "video":
            theoraenc.link(oggmux)

        oggmux.link(self.archivo)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        self.player.connect('pad-added', self.__on_pad_added)
        self.player.connect("source-setup", self.__source_setup)

    def __on_pad_added(self, uridecodebin, pad):
        """
        Agregar elementos en forma dinámica según
        sean necesarios. https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """

        string = pad.query_caps(None).to_string()
        # print "Agregando:", string

        if string.startswith('audio/'):
            pad.link(self.audio_sink)

        elif string.startswith('video/'):
            pad.link(self.video_sink)

    def __play(self, widget=None, event=None):

        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self, widget=None, event=None):
        """
        Detiene y limpia el pipe.
        """

        self.pipeline.set_state(Gst.State.PAUSED)
        self.pipeline.set_state(Gst.State.NULL)
        self.__new_handle(False)

        if os.path.exists(self.patharchivo):
            os.chmod(self.patharchivo, 0755)

    def __sync_message(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        #if mensaje.get_structure().get_name() == 'prepare-window-handle':
        #    mensaje.src.set_window_handle(xid)

        pass

    def __on_mensaje(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        if mensaje.type == Gst.MessageType.EOS:
            # self.video_pipeline.seek_simple(Gst.Format.TIME,
            # Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)
            self.__new_handle(False)
            self.emit("endfile")

        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "ERROR:", err, debug
            self.__new_handle(False)
            self.stop()
            self.emit("endfile")

    def __new_handle(self, reset):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion.
        """

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = GLib.timeout_add(
                500, self.__handle)

    def __handle(self):
        """
        Consulta el estado y progreso de
        la grabacion.
        """

        if os.path.exists(self.patharchivo):
            tamanio = int(os.path.getsize(self.patharchivo) / 1024)

            if len(self.uri) > 25:
                texto = str(self.uri[0:25]) + " . . . "

            info = "Grabando: %s %s Kb" % (texto, str(tamanio))

            if self.info != info:
                self.control = 0
                self.info = info
                self.emit('update', self.info)

            else:
                self.control += 1

        if self.control > 60:
            self.stop()
            self.emit("endfile")
            return False

        return True

    def __source_setup(self, player, source):

        self.uri = source.get_property('location')
        # print "Grabando:", self.uri

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

        self.player = Gst.ElementFactory.make("playbin", "player")

        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        mp3enc = Gst.ElementFactory.make('lamemp3enc', "lamemp3enc")

        self.archivo = Gst.ElementFactory.make('filesink', "archivo")

        jamedia_sink = Gst.Bin()
        jamedia_sink.add(audioconvert)

        pad = audioconvert.get_static_pad('sink')
        ghostpad = Gst.GhostPad.new('sink', pad)
        jamedia_sink.add_pad(ghostpad)

        jamedia_sink.add(mp3enc)
        jamedia_sink.add(self.archivo)

        audioconvert.link(mp3enc)
        mp3enc.link(self.archivo)

        self.player.set_property('audio-sink', jamedia_sink)

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)

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
