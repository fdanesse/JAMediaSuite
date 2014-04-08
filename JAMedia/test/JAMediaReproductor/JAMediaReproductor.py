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


class JAMediaReproductor(gst.Pipeline):
    """
    Reproductor de Audio, Video y Streaming de
    Radio y Television. Implementado sobre:

        python 2.7.3
        Gtk 3
        gstreamer 1.0
    """

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "newposicion": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    #"video": (gobject.SIGNAL_RUN_CLEANUP,
    #    gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,)),
        }

    # Estados: playing, paused, None

    def __init__(self, ventana_id):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """

        gst.Pipeline.__init__(self)

        self.set_name('JAMediaReproductor')
        self.nombre = 'JAMediaReproductor'  #FIXME: para hacer switch

        self.config = {
            'saturacion': 50.0,
            'contraste': 50.0,
            'brillo': 50.0,
            'hue': 50.0,
            'gamma': 10.0,
            'rotacion': 0}

        self.ventana_id = ventana_id
        self.progressbar = True
        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.player = None
        self.bus = None

        # BIN
        player = gst.element_factory_make(
            "uridecodebin", "uridecodebin")

        # AUDIO
        audioconvert = gst.element_factory_make(
            'audioconvert', 'audioconvert')
        audioresample = gst.element_factory_make(
            'audioresample', 'audioresample')
        audioresample.set_property('quality', 10)
        volume = gst.element_factory_make(
            'volume', 'volume')
        autoaudiosink = gst.element_factory_make(
            "autoaudiosink", "autoaudiosink")

        # Video
        videoconvert = gst.element_factory_make(
            'ffmpegcolorspace', 'videoconvert')
        videorate = gst.element_factory_make(
            'videorate', 'videorate')
        videobalance = gst.element_factory_make(
            'videobalance', "videobalance")
        gamma = gst.element_factory_make(
            'gamma', "gamma")
        videoflip = gst.element_factory_make(
            'videoflip', "videoflip")
        pantalla = gst.element_factory_make(
            'xvimagesink', "pantalla")
        pantalla.set_property(
            "force-aspect-ratio", True)

        self.add(player)
        self.add(audioconvert)
        self.add(audioresample)
        self.add(volume)
        self.add(autoaudiosink)
        self.add(videoconvert)
        self.add(videorate)
        self.add(videobalance)
        self.add(gamma)
        self.add(videoflip)
        self.add(pantalla)

        audioconvert.link(audioresample)
        audioresample.link(volume)
        volume.link(autoaudiosink)

        videoconvert.link(videorate)
        videorate.link(videobalance)
        videobalance.link(gamma)
        gamma.link(videoflip)
        videoflip.link(pantalla)

        self.audio_sink = audioconvert.get_static_pad('sink')
        self.video_sink = videoconvert.get_static_pad('sink')

        self.bus = self.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

        player.connect('pad-added', self.__pad_added)

        try: # FIXME: xo no posee esta propiedad
            self.videorate.set_property('max-rate', 30)
        except:
            pass

        #self.video_in_stream = False

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
            self.stop()
            self.__new_handle(False, [gst.MESSAGE_ERROR])

        elif message.type == gst.MESSAGE_LATENCY:
        #    # http://cgit.collabora.com/git/farstream.git/tree/examples/gui/fs-gui.py
        #    print "\n gst.MESSAGE_LATENCY"
            self.recalculate_latency()

        #elif message.type == gst.MESSAGE_TAG:
        #    taglist = message.parse_tag()
        #    datos = taglist.keys()

        #    #for dato in datos:
        #    #    print dato, taglist[dato]

        #    if 'audio-codec' in datos and not 'video-codec' in datos:
        #        if self.video_in_stream == True or \
        #            self.video_in_stream == None:

        #            self.video_in_stream = False
        #            self.emit("video", False)
        #            #self.audio_pipeline.agregar_visualizador('monoscope')

        #    elif 'video-codec' in datos:
        #        if self.video_in_stream == False or \
        #            self.video_in_stream == None:

        #            self.video_in_stream = True
        #            self.emit("video", True)
        #            #self.audio_pipeline.quitar_visualizador()

        #else:
        #    print message.type, message.src

        return gst.BUS_PASS

    def __play(self):
        """
        Pone el pipe de gst en gst.STATE_PLAYING
        """

        self.set_state(gst.STATE_PLAYING)

    def __pause(self):
        """
        Pone el pipe de gst en gst.STATE_PAUSED
        """

        self.set_state(gst.STATE_PAUSED)

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
            self.actualizador = gobject.timeout_add(500, self.__handle)

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

        try:
            valor1, bool1 = self.query_duration(gst.FORMAT_TIME)
            valor2, bool2 = self.query_position(gst.FORMAT_TIME)

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
        """
        Seteos de balance en video.
        Recibe % en float y convierte a los valores del filtro.
        """

        if brillo:
            self.config['brillo'] = brillo
            valor = (2.0 * brillo / 100.0) - 1.0
            self.get_by_name("videobalance").set_property(
                'brightness', valor)

        if contraste:
            self.config['contraste'] = contraste
            valor = 2.0 * contraste / 100.0
            self.get_by_name("videobalance").set_property(
                'contrast', valor)

        if saturacion:
            self.config['saturacion'] = saturacion
            valor = 2.0 * saturacion / 100.0
            self.get_by_name("videobalance").set_property(
                'saturation', valor)

        if hue:
            self.config['hue'] = hue
            valor = (2.0 * hue / 100.0) - 1.0
            self.get_by_name("videobalance").set_property(
                'hue', valor)

        if gamma:
            self.config['gamma'] = gamma
            valor = (10.0 * gamma / 100.0)
            self.get_by_name("gamma").set_property(
                'gamma', valor)

    def get_balance(self):
        """
        Retorna los valores actuales de balance en % float.
        """

        return self.config

    def stop(self):
        """
        Pone el pipe de gst en gst.STATE_NULL
        """

        self.set_state(gst.STATE_NULL)
        self.emit("newposicion", 0)

    def load(self, uri):
        """
        Carga un archivo o stream en el pipe de gst.
        """

        if os.path.exists(uri):
            #direccion = gst.filename_to_uri(uri)
            direccion = "file://" + uri
            self.get_by_name("uridecodebin").set_property("uri", direccion)
            self.progressbar = True
            self.__play()

        else:
            if gst.uri_is_valid(uri):
                self.get_by_name("uridecodebin").set_property("uri", uri)
                self.progressbar = False
                self.__play()

        return False

    def set_position(self, posicion):
        """
        Permite desplazarse por
        la pista que se esta reproduciendo.
        """

        if self.duracion < posicion:
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

        self.send_event(event)
        #self.player.set_state(gst.STATE_PLAYING)

    def set_volumen(self, volumen):
        """
        Cambia el volúmen de Reproducción.
        """

        self.get_by_name("volume").set_property('volume', volumen)

    def get_volumen(self):

        return self.get_by_name("volume").get_property('volume')


def exit(win=False, event=False):
    import sys
    gtk.main_quit()
    sys.exit(0)


def print_status(player, uno=False, dos=False):
    print uno, dos


if __name__ == "__main__":
    import gtk

    win = gtk.Window()
    drawing = gtk.DrawingArea()
    win.add(drawing)

    win.show_all()

    win.connect("delete-event", exit)
    xid = drawing.get_property('window').xid
    player = JAMediaReproductor(xid)

    player.connect("endfile", print_status)
    player.connect("estado", print_status)
    player.connect("newposicion", print_status)
    player.connect("volumen", print_status)
    player.connect("video", print_status)

    player.load("/home/flavio/Lorde/Lorde - Tennis Court")

    gtk.main()
