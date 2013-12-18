#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaAudioExtractor.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM! - Uruguay
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
import sys

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gst
from gi.repository import GstVideo
from gi.repository import GObject
from gi.repository import GdkX11
from gi.repository import GLib

GObject.threads_init()
Gst.init([])


class Ventana(Gtk.Window):

    def __init__(self, origen, codec):

        Gtk.Window.__init__(self)

        self.set_title("Mi Aplicación")

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.socket = Gtk.Socket()
        self.add(self.socket)

        self.jamediaaudioextractor = JAMediaAudioExtractor(origen, codec)
        self.socket.add_id(self.jamediaaudioextractor.get_id())

        self.show_all()
        self.realize()

        self.connect("delete-event", self.__exit)

    def __exit(self, widget=None, senial=None):

        if self.jamediaaudioextractor:
            self.jamediaaudioextractor.stop()

        sys.exit(0)

class JAMediaAudioExtractor(Gtk.Plug):

    __gtype_name__ = 'JAMediaAudioExtractor'

    __gsignals__ = {
    "salir": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, origen, codec):
        """
        JAMediaAudioExtractor: Gtk.Plug para embeber en otra aplicacion.
        """

        Gtk.Plug.__init__(self, 0L)

        self.player = None
        self.lista = origen
        self.codec = codec

        vbox = Gtk.VBox()

        from JAMediaWidgets import BarraProgreso

        self.video_widget = Gtk.DrawingArea()
        self.video_widget.modify_bg(0, Gdk.Color(0, 0, 0))
        self.barradeprogreso = BarraProgreso()
        self.barradeprogreso.set_sensitive(False)

        vbox.pack_start(self.video_widget, True, True, 0)
        vbox.pack_start(self.barradeprogreso, False, False, 0)

        self.add(vbox)

        self.show_all()
        self.realize()

        self.connect("embedded", self.__embed_event)

        GLib.idle_add(self.__play)

    def __embed_event(self, widget):
        """
        No hace nada por ahora.
        """

        print "JAMediaAudioExtractor => OK"

    def __play(self):

        if not self.lista:
            #self.__exit()
            return

        origen = self.lista[0]
        self.lista.remove(origen)

        self.player = Extractor(
            self.video_widget.get_property(
            'window').get_xid(), origen, codec)

        self.player.connect('endfile', self.__set_end)
        self.player.connect('estado', self.__set_estado)
        self.player.connect('newposicion', self.__set_posicion)

        self.player.play()

        return False

    def __set_end(self, player):

        GLib.idle_add(self.__play)

    def __set_estado(self, player, estado):

        #print "Estado:", estado
        pass

    def stop(self):

        if self.player:
            self.player.stop()

    def __set_posicion(self, player, posicion):

        self.barradeprogreso.set_progress(float(posicion))
        if float(posicion) == 100.0:
            self.player.stop()
            self.barradeprogreso.set_progress(0.0)
            self.video_widget.modify_bg(0, Gdk.Color(0, 0, 0))
            self.__play()


class Extractor(Gst.Pipeline):
    """
    Extractor de audio de un video y conversor de formatos de audio.

    Si pasas un archivo de audio, lo convierte al formato indicado.
    Si pasas un archivo de video, extrae el audio en el formato indicado.
    Por defecto el archivo resultante es mp3, pero tu puedes indicarle el
    formato de salida (mp3, wav, ogg)

    'gst-launch-1.0 filesrc location=/home/flavio/Documentos/001 ! \
        decodebin name=t ! \
            queue ! audioconvert ! lamemp3enc ! filesink \
                location=/home/flavio/Documentos/002.mp3 \
            t. ! queue ! autovideosink')

    codecs = {
        "MP3": ["lamemp3enc", "mp3"],
        "WAV": ["wavenc", "wav"],
        "OGG": ["vorbisenc ! oggmux", "ogg"],
        }
    """

    __gsignals__ = {
    "endfile": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "estado": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "newposicion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,)),
    #"volumen": (GObject.SIGNAL_RUN_LAST,
    #    GObject.TYPE_NONE, (GObject.TYPE_FLOAT,)),
    #"video": (GObject.SIGNAL_RUN_LAST,
    #    GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))
        }

    def __init__(self, ventana_id, origen, codec):

        Gst.Pipeline.__init__(self)

        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.ventana_id = ventana_id
        self.origen = origen
        self.codec = codec

        print "Iniciando JAMediaExtractor:"
        print "\t Id Video Widget:", self.ventana_id
        print "\t Archivo Original:", self.origen
        print "\t Codec Seleccionado:", self.codec

        filesrc = Gst.ElementFactory.make(
            "filesrc", "filesrc")
        decodebin = Gst.ElementFactory.make(
            "decodebin", "decodebin")

        queue0 = Gst.ElementFactory.make(
            "queue", "queue0")
        audioconvert = Gst.ElementFactory.make(
            "audioconvert", "audioconvert")

        lamemp3enc = Gst.ElementFactory.make(
            "lamemp3enc", "lamemp3enc")
        wavenc = Gst.ElementFactory.make(
            "wavenc", "wavenc")
        vorbisenc = Gst.ElementFactory.make(
            "vorbisenc", "vorbisenc")
        oggmux = Gst.ElementFactory.make(
            "oggmux", "oggmux")

        filesink = Gst.ElementFactory.make(
            "filesink", "filesink")
        queue1 = Gst.ElementFactory.make(
            "queue", "queue1")
        xvimagesink = Gst.ElementFactory.make(
            "xvimagesink", "xvimagesink")

        self.audio_sink = queue0.get_static_pad('sink')
        self.video_sink = queue1.get_static_pad('sink')

        self.add(filesrc)
        self.add(decodebin)
        self.add(queue0)
        self.add(audioconvert)
        self.add(lamemp3enc)
        self.add(wavenc)
        self.add(vorbisenc)
        self.add(oggmux)
        self.add(filesink)
        self.add(queue1)
        self.add(xvimagesink)

        filesrc.link(decodebin)
        queue0.link(audioconvert)

        queue1.link(xvimagesink)

        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        decodebin.connect('pad-added', self.__on_pad_added)

        filesrc.set_property('location', self.origen)
        filesink.set_property(
            'location', "%s.%s" % (self.origen, self.codec))

    def play(self):

        GLib.idle_add(self.__play)
        self.__new_handle(True)

    def __on_pad_added(self, uridecodebin, pad):
        """
        Agregar elementos en forma dinámica según
        sean necesarios. https://wiki.ubuntu.com/Novacut/GStreamer1.0
        """

        string = pad.query_caps(None).to_string()
        print "Agregando:", string

        if string.startswith('audio/'):
            if self.codec == 'mp3':
                self.__set_mp3_codec_bin()

            elif self.codec == 'wav':
                self.__set_wav_codec_bin()

            elif self.codec == 'ogg':
                self.__set_ogg_codec_bin()

            pad.link(self.audio_sink)

        elif string.startswith('video/'):
            pad.link(self.video_sink)

    def __set_mp3_codec_bin(self):
        """
        Construye y Agrega los elementos necesarios
        para extraer el audio en formato mp3.
        """

        print "Construyendo mp3 bin"

        audioconvert = self.get_by_name('audioconvert')
        filesink = self.get_by_name('filesink')
        lamemp3enc = self.get_by_name('lamemp3enc')

        audioconvert.link(lamemp3enc)
        lamemp3enc.link(filesink)

    def __set_wav_codec_bin(self):
        """
        Construye y Agrega los elementos necesarios
        para extraer el audio en formato wav.
        """

        print "Construyendo wav bin"

        audioconvert = self.get_by_name('audioconvert')
        filesink = self.get_by_name('filesink')
        wavenc = self.get_by_name('wavenc')

        audioconvert.link(wavenc)
        wavenc.link(filesink)

    def __set_ogg_codec_bin(self):
        """
        Construye y Agrega los elementos necesarios
        para extraer el audio en formato ogg.
        """

        print "Construyendo ogg bin"

        audioconvert = self.get_by_name('audioconvert')
        filesink = self.get_by_name('filesink')
        vorbisenc = self.get_by_name('vorbisenc')
        oggmux = self.get_by_name('oggmux')

        audioconvert.link(vorbisenc)
        vorbisenc.link(oggmux)
        oggmux.link(filesink)

    def __sync_message(self, bus, mensaje):

        if mensaje.get_structure():
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

        if mensaje.type == Gst.MessageType.STATE_CHANGED:
            old, new, pending = mensaje.parse_state_changed()

            if old == Gst.State.PAUSED and new == Gst.State.PLAYING:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "playing")
                    self.__new_handle(True)
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

            #elif old == Gst.State.NULL and new == Gst.State.READY:
            #    pass

            #elif old == Gst.State.PAUSED and new == Gst.State.READY:
            #    pass

            #else:
            #    return

        elif mensaje.type == Gst.MessageType.TAG:
            taglist = mensaje.parse_tag()
            datos = taglist.to_string()

            #if 'audio-codec' in datos and not 'video-codec' in datos:
            #    if self.video_in_stream == True or \
            #        self.video_in_stream == None:

            #        self.video_in_stream = False
            #        self.emit("video", False)

            #elif 'video-codec' in datos:
            #    if self.video_in_stream == False or \
            #        self.video_in_stream == None:

            #        self.video_in_stream = True
            #        self.emit("video", True)

            #self.duracion = int(taglist.to_string().split(
            #   "duration=(guint64)")[1].split(',')[0])

            #Ejemplo:
            #    taglist,
            #    duration=(guint64)780633000000,
            #    video-codec=(string)H.264,
            #    audio-codec=(string)"MPEG-4\ AAC"

            return

        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug
            self.__new_handle(False)
            return

    def __on_mensaje(self, bus, mensaje):

        if mensaje.type == Gst.MessageType.EOS:
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "Error en la Reproducción:", err, debug
            self.__new_handle(False)
            self.emit("endfile")

    def __play(self):

        print "Reproducción Iniciada"
        self.set_state(Gst.State.PLAYING)

    def stop(self):

        self.set_state(Gst.State.NULL)
        print "Reproducción Detenida"

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
            self.actualizador = GLib.timeout_add(
                500, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        bool1, valor1 = self.query_duration(Gst.Format.TIME)
        bool2, valor2 = self.query_position(Gst.Format.TIME)

        duracion = int(valor1)
        posicion = int(valor2)

        pos = 0
        try:
            pos = int(posicion * 100 / duracion)

        except:
            pass

        #print pos, posicion, duracion, posicion * 100 / duracion
        #if pos < 0.0 or pos > self.duracion:
        #    print pos, duracion
        #    return True

        if self.duracion != duracion:
            self.duracion = duracion

        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)

        return True


def get_data(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    """

    import commands

    datos = commands.getoutput(
        'file -ik %s%s%s' % ("\"", archivo, "\""))

    retorno = ""

    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)

    return retorno


if __name__ == "__main__":

    origen = False

    if len(sys.argv) > 1:
        origen = sys.argv[1]

    codec = "mp3"
    lista = []

    if len(sys.argv) > 2:
        codec = str(sys.argv[2]).lower()

    if origen:
        # Directorio
        if os.path.isdir(origen):
            for archivo in os.listdir(origen):
                arch = os.path.join(origen, archivo)

                if "video" in get_data(arch):
                    lista.append(arch)

        # Archivo
        elif os.path.isfile(origen):
            if "video" in get_data(origen):
                lista.append(origen)

    Ventana(lista, codec)
    Gtk.main()
