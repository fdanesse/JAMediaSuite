#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaReproductor.py por:
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


class JAMediaReproductor(gobject.GObject):
    """
    Reproductor de Audio, Video y Streaming de
    Radio y Television. Implementado sobre:

        python 2.7.3
        Gtk 3
        gstreamer 1.0
    """

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "newposicion": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "volumen": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,)),
    "video": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    # Estados: playing, paused, None

    def __init__(self, ventana_id):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """

        gobject.GObject.__init__(self)

        self.nombre = "JAMediaReproductor"
        self.ventana_id = ventana_id

        self.progressbar = True
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

        from JAMediaBins import JAMedia_Video_Pipeline
        from JAMediaBins import JAMedia_Audio_Pipeline

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

        self.posicion = 0
        self.duracion = 0

        self.__new_handle(False, [self.__reset])
        self.progressbar = True

        if self.player:
            del(self.player)

        # Reproductor.
        self.player = gst.element_factory_make(
            "playbin2", "player")

        # Si no se establecen los valores al original, se produce un error.
        self.video_pipeline.reset_balance()
        self.player.set_property('volume', self.volumen)

        self.player.set_property('video-sink', self.video_pipeline)
        self.player.set_property('audio-sink', self.audio_pipelin)

        self.bus = self.player.get_bus()

        #self.bus.add_signal_watch()
        #self.bus.enable_sync_message_emission()
        #self.bus.connect('sync-message', self.__sync_message)

        self.bus.set_sync_handler(self.__bus_handler)

        #self.video_in_stream = False

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        elif message.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()

            if self.estado != new:
                self.estado = new

                if new == gst.STATE_PLAYING:
                    self.emit("estado", "playing")
                    self.__new_handle(True, [old, new])

                    # FIXME: Si se llama enseguida falla.
                    gobject.idle_add(self.__re_config)

                elif new == gst.STATE_PAUSED:
                    self.emit("estado", "paused")
                    self.__new_handle(False, [old, new])

                elif new == gst.STATE_NULL:
                    self.emit("estado", "None")
                    self.__new_handle(False, [old, new])

                else:
                    self.emit("estado", "paused")
                    self.__new_handle(False, [old, new])

        elif message.type == gst.MESSAGE_EOS:
            self.__new_handle(False, [gst.MESSAGE_EOS])
            self.emit("endfile")

        elif message.type == gst.MESSAGE_ERROR:
            print "\n gst.MESSAGE_ERROR:"
            print message.parse_error()
            self.__new_handle(False, [gst.MESSAGE_ERROR])

        elif message.type == gst.MESSAGE_LATENCY:
        #    # http://cgit.collabora.com/git/farstream.git/tree/examples/gui/fs-gui.py
        #    print "\n gst.MESSAGE_LATENCY"
            self.player.recalculate_latency()

        elif message.type == gst.MESSAGE_TAG:
            taglist = message.parse_tag()
            datos = taglist.keys()

            #for dato in datos:
            #    print dato, taglist[dato]

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

        #else:
        #    print message.type, message.src

        return gst.BUS_PASS

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
        Pone el pipe de gst en gst.STATE_PLAYING
        """

        self.player.set_state(gst.STATE_PLAYING)

    def __pause(self):
        """
        Pone el pipe de gst en gst.STATE_PAUSED
        """

        self.player.set_state(gst.STATE_PAUSED)

    def __new_handle(self, reset, func):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        #print time.time(), reset, func

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(150, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        if not self.progressbar:
            return True

        valor1 = None
        valor2 = None
        pos = None
        duracion = None

        #import time
        #print time.time(), self.duracion, self.posicion

        try:
            valor1, bool1 = self.player.query_duration(gst.FORMAT_TIME)
            valor2, bool2 = self.player.query_position(gst.FORMAT_TIME)

        except:
            print "ERROR en HANDLER"
            return True

        if valor1 != None:
            duracion = valor1 / 1000000000

        if valor2 != None:
            posicion = valor2 / 1000000000

        if duracion == 0 or duracion == None:
            return True

        pos = int(posicion * 100 / duracion)

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

    def pause_play(self):
        """
        Llama a play() o pause()
        segun el estado actual del pipe de gst.
        """

        if self.estado == gst.STATE_PAUSED \
            or self.estado == gst.STATE_NULL \
            or self.estado == gst.STATE_READY:
            self.__play()

        elif self.estado == gst.STATE_PLAYING:
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

    def stop(self):
        """
        Pone el pipe de gst en gst.STATE_NULL
        """

        self.player.set_state(gst.STATE_NULL)

    def load(self, uri):
        """
        Carga un archivo o stream en el pipe de gst.
        """

        self.stop()
        self.__reset()

        gobject.idle_add(self.__load, uri)

    def __load(self, uri):

        if os.path.exists(uri):
            # Archivo
            #direccion = gst.filename_to_uri(uri)
            direccion = "file://" + uri
            self.player.set_property("uri", direccion)
            self.progressbar = True
            self.__play()

        else:
            # Streaming
            if gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.progressbar = False
                self.__play()

        return False

    def set_position(self, posicion):
        """
        Permite desplazarse por
        la pista que se esta reproduciendo.
        """

        if self.duracion < posicion:
            #self.emit("newposicion", self.posicion)
            print "Duracion menor que posicion", self.duracion, posicion
            return

        if self.duracion == 0 or posicion == 0:
            return

        posicion = self.duracion * posicion / 100

        # http://pygstdocs.berlios.de/pygst-reference/gst-constants.html
        #self.player.set_state(gst.STATE_PAUSED)
        # http://nullege.com/codes/show/src@d@b@dbr-HEAD@trunk@src@reproductor.py/72/gst.SEEK_TYPE_SET
        #self.player.seek(
        #    1.0,
        #    gst.FORMAT_TIME,
        #    gst.SEEK_FLAG_FLUSH,
        #    gst.SEEK_TYPE_SET,
        #    posicion,
        #    gst.SEEK_TYPE_SET,
        #    self.duracion)

        # http://nullege.com/codes/show/src@c@o@congabonga-HEAD@congaplayer@congalib@engines@gstplay.py/104/gst.SEEK_FLAG_ACCURATE
        event = gst.event_new_seek(
            1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, posicion * 1000000000,
            gst.SEEK_TYPE_NONE, self.duracion * 1000000000)

        self.player.send_event(event)
        #self.player.set_state(gst.STATE_PLAYING)

    def set_volumen(self, valor):
        """
        Cambia el volúmen de Reproducción.
        """

        self.volumen = float(valor / 100)
        self.player.set_property('volume', self.volumen)

    def agregar_efecto(self, nombre_efecto):

        self.__new_handle(False, [])
        self.stop()

        self.efectos.append(nombre_efecto)
        #self.config_efectos[nombre_efecto] = {}
        self.video_pipeline.agregar_efecto(nombre_efecto)

        self.__play()
        # FIXME: Verificar. self.__new_handle(True) solo debiera
        # estar en los messages del bus.
        self.__new_handle(True, [])

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

        self.__new_handle(False, [])
        self.stop()

        self.video_pipeline.quitar_efecto(indice_efecto)

        self.__play()
        self.__new_handle(True, [])

    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        """
        Configura un efecto en el pipe.
        """

        self.video_pipeline.configurar_efecto(nombre_efecto, propiedad, valor)


class JAMediaGrabador(gobject.GObject):
    """
    Graba en formato ogg desde un streaming de radio o tv.
    Convierte un archivo de audio o video a ogg.
    """

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "endfile": (gobject.SIGNAL_RUN_LAST,
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
        videorate.set_property('max-rate', 30)

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
            # self.video_pipeline.seek_simple(gst.FORMAT_TIME,
            # gst.SeekFlags.FLUSH | gst.SeekFlags.KEY_UNIT, 0)
            print "\n gst.MESSAGE_EOS:"
            self.__new_handle(False, [])
            self.stop()
            self.emit("endfile")

        #elif message.type == gst.MESSAGE_LATENCY:
        #    # http://cgit.collabora.com/git/farstream.git/tree/examples/gui/fs-gui.py
        #    print "\n gst.MESSAGE_LATENCY"
        #    self.player.recalculate_latency()

        elif message.type == gst.MESSAGE_ERROR:
            print "\n gst.MESSAGE_ERROR:"
            print message.parse_error()
            self.__new_handle(False, [])
            self.stop()
            self.emit("endfile")

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
