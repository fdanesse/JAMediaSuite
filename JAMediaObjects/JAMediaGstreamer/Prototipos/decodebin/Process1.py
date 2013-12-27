#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reproduce el video y el audio.

Sin:
    from gi.repository import GstVideo

Lo siguiente no funciona:
    def __sync_message(self, bus, mensaje):

        if mensaje.get_structure():
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

Los Objetos no se linkean sin:
    GObject.threads_init()
"""

import os

from gi.repository import Gst
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import GstVideo

GObject.threads_init()
Gst.init([])


class Process(Gst.Pipeline):

    __gsignals__ = {
    "endfile": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "estado": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "newposicion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,)),
    "info": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),}

    def __init__(self, ventana_id):

        Gst.Pipeline.__init__(self)

        self.ventana_id = ventana_id
        self.video_sink = False

        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.estado = False
        self.origen = '/home/flavio/001'

        self.__setup()

    def play(self):
        """
        loop = GObject.MainLoop()
        GObject.threads_init()
        context = loop.get_context()
        context.iteration(True)

        while m.running:
            context.iteration(True)
        """

        GLib.idle_add(self.__play)
        self.__new_handle(True)

    def stop(self):

        self.set_state(Gst.State.NULL)
        self.emit("info", "Reproducción Detenida")
        print "Reproducción Detenida"

    def __setup(self):

        # Origen
        filesrc = Gst.ElementFactory.make(
            "filesrc", "filesrc")
        decodebin = Gst.ElementFactory.make(
            "decodebin", "decodebin")

        self.add(filesrc)
        self.add(decodebin)

        filesrc.link(decodebin)

        # Salida Pantalla
        videoconvert = Gst.ElementFactory.make(
            "videoconvert", "videoconvert")

        xvimagesink = Gst.ElementFactory.make(
            "xvimagesink", "xvimagesink")

        self.add(videoconvert)
        self.add(xvimagesink)

        videoconvert.link(xvimagesink)

        # Salida de Audio
        audioconvert = Gst.ElementFactory.make(
            "audioconvert", "audioconvert")

        autoaudiosink = Gst.ElementFactory.make(
            "autoaudiosink", "autoaudiosink")

        self.add(audioconvert)
        self.add(autoaudiosink)

        audioconvert.link(autoaudiosink)

        # Señales
        decodebin.connect('pad-added', self.__on_pad_added)
        # set_property('video-sink', self.video_pipeline)

        filesrc.set_property('location', self.origen)

        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

    def __on_pad_added(self, uridecodebin, pad):
        """
        Link dinámico.
        """

        string = pad.query_caps(None).to_string()

        text = "Agregando Capas:"
        for item in string.split(","):
            text = "%s\n\t%s" % (text, item.strip())

        self.emit("info", text)
        print text

        if string.startswith('video/'):
            pad.link(self.get_by_name('videoconvert').get_static_pad('sink'))

        elif string.startswith('audio/'):
            pad.link(self.get_by_name('audioconvert').get_static_pad('sink'))

    def __sync_message(self, bus, mensaje):

        if mensaje.get_structure():
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

        if mensaje.type == Gst.MessageType.ERROR:
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
            self.emit("info",
                "Error en la Reproducción: %s %s" % (err, debug))
            print "Error en la Reproducción:", err, debug
            self.__new_handle(False)
            self.emit("endfile")

    def __play(self):

        self.emit("info", "Reproducción Iniciada")
        print "Reproducción Iniciada"
        self.set_state(Gst.State.PLAYING)

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
