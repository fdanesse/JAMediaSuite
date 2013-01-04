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
import time
import datetime

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo

import JAMediaGstreamer
from JAMediaGstreamer.JAMediaBins import JAMedia_Video_Pipeline
from JAMediaGstreamer.JAMediaBins import JAMedia_Audio_Pipeline

import JAMediaGlobales as G

GObject.threads_init()
Gst.init([])
    
# Guia: http://developer.gnome.org/gstreamer/stable/libgstreamer.html

class JAMediaReproductor(GObject.GObject):
    """
    Reproductor de Audio, Video y Streaming de
    Radio y Television. Implementado sobre:
        
        python 2.7.3
        Gtk 3
        Gstreamer 1.0
    """
    
    __gsignals__ = {
    "endfile":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    "estado":(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_STRING,)),
    "newposicion":(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_INT,)),
    "volumen":(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_FLOAT,)),
    "video":(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_BOOLEAN,))}

    # Estados: playing, paused, None
    
    def __init__(self, ventana_id):
        """ Recibe el id de un DrawingArea
        para mostrar el video. """
        
        GObject.GObject.__init__(self)
        
        self.name = "JAMediaReproductor"
        self.ventana_id = ventana_id
        
        self.estado = None
        self.volumen = 0.0
        
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        
        self.player = None              # reproductor
        self.bus = None
        
        # Gestor de la salida de Video del reproductor.
        self.video_pipeline = JAMedia_Video_Pipeline()
        
        # Gestor de salida de Audio del reproductor.
        self.audio_pipelin = JAMedia_Audio_Pipeline()
        
        self.video_in_stream = None # Debe iniciarse como None (ver señal video)
        
        self.efectos = []
        #self.config_efectos = {}
        
        self.reset()
        
    def reset(self):
        
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
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
        #self.video_in_stream = False
        
    def load(self, uri):
        """Carga un archivo o stream en el pipe de Gst."""
        
        self.stop()
        self.reset()
        
        if os.path.exists(uri):
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)
            self.play()
            
        else:
            # FIXME: Funciona con la radio pero no con la Tv
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.play()
        
    def play(self):
        """Pone el pipe de Gst en Gst.State.PLAYING"""
        
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        """Pone el pipe de Gst en Gst.State.NULL"""
        
        self.player.set_state(Gst.State.NULL)
        
    def pause(self):
        """Pone el pipe de Gst en Gst.State.PAUSED"""
        
        self.player.set_state(Gst.State.PAUSED)
        
    def pause_play(self):
        """Llama a play() o pause()
        segun el estado actual del pipe de Gst."""
        
        if self.estado == Gst.State.PAUSED \
            or self.estado == Gst.State.NULL \
            or self.estado == Gst.State.READY:
            self.play()
            
        elif self.estado == Gst.State.PLAYING:
            self.pause()
        
    def rotar(self, valor):
        """ Rota el Video. """
        
        self.video_pipeline.rotar(valor)
        
    def set_balance(self, brillo = None, contraste = None,
        saturacion = None, hue = None, gamma = None):
        """Seteos de balance en video.
        Recibe % en float y convierte a los valores del filtro."""
        
        self.video_pipeline.set_balance(brillo, contraste, saturacion, hue, gamma)
        
    def get_balance(self):
        """Retorna los valores actuales de balance en % float."""
        
        return self.video_pipeline.get_balance()
        
    def new_handle(self, reset):
        """Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = False
            
        if reset:
            self.actualizador = GObject.timeout_add(500, self.handle)
        
    def handle(self):
        """Envia los datos de actualizacion para
        la barra de progreso del reproductor."""
        
        bool1, valor1 = self.player.query_duration(Gst.Format.TIME)
        bool2, valor2 = self.player.query_position(Gst.Format.TIME)
        
        duracion = float(valor1)
        posicion = float(valor2)
        
        pos = 0
        try:
            pos = int(posicion * 100 / duracion)
            
        except:
            pass
        
        if pos < 0 or pos > self.duracion: return True
        
        if self.duracion != duracion: self.duracion = duracion
        
        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)
            # print "***", gst.video_convert_frame(self.player.get_property("frame"))
            
        return True
    
    def set_position(self, posicion):
        """Permite desplazarse por
        la pista que se esta reproduciendo."""
        
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
        """Cambia el volúmen de Reproducción."""
        
        self.volumen = float(valor/100)
        self.player.set_property('volume', self.volumen)
    
    def agregar_efecto(self, nombre_efecto):
        
        self.new_handle(False)
        self.stop()
        
        self.efectos.append( nombre_efecto )
        #self.config_efectos[nombre_efecto] = {}
        self.video_pipeline.agregar_efecto(nombre_efecto)
        
        self.play()
        self.new_handle(True)
        
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
                
        self.new_handle(False)
        self.stop()
        
        self.video_pipeline.quitar_efecto(indice_efecto)
        
        self.play()
        self.new_handle(True)
        
    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        """Configura un efecto en el pipe."""
        
        self.video_pipeline.configurar_efecto(nombre_efecto, propiedad, valor)
        
    def sync_message(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
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
                    self.new_handle(True)
                    GObject.idle_add(
                        self.player.set_property,
                        'volume', self.volumen)
                    return
                
            elif old == Gst.State.READY and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")
                    self.new_handle(False)
                    return
                
            elif old == Gst.State.READY and new == Gst.State.NULL:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "None")
                    self.new_handle(False)
                    return
                
            elif old == Gst.State.PLAYING and new == Gst.State.PAUSED:
                if self.estado != new:
                    self.estado = new
                    self.emit("estado", "paused")
                    self.new_handle(False)
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
                if self.video_in_stream == True or self.video_in_stream == None:
                    self.video_in_stream = False
                    self.emit("video", False)
                    #self.audio_pipelin.agregar_visualizador('monoscope')
                    
            elif 'video-codec' in datos:
                if self.video_in_stream == False or self.video_in_stream == None:
                    self.video_in_stream = True
                    self.emit("video", True)
                    #self.audio_pipelin.quitar_visualizador()
                    
            #self.duracion = int(taglist.to_string().split("duration=(guint64)")[1].split(',')[0])
            #Ejemplo:
                # taglist,
                # duration=(guint64)780633000000,
                # video-codec=(string)H.264,
                # audio-codec=(string)"MPEG-4\ AAC"
            return
        
        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug
            self.new_handle(False)
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
        
    def on_mensaje(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
        if mensaje.type == Gst.MessageType.EOS:
            #self.video_pipeline.seek_simple(Gst.Format.TIME,
            #Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)
            self.new_handle(False)
            self.emit("endfile")
            
        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug
            self.new_handle(False)
            
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
    """Graba desde un streaming de radio o tv."""
    
    __gsignals__ = {
    "update":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self, uri, archivo):
        
        GObject.GObject.__init__(self)
        
        self.patharchivo = archivo
        self.actualizador = False
        self.info = ""
        self.uri = ""
        
        self.pipeline = None
        self.audioconvert = None
        self.mp3enc = None
        self.hiloarchivo = None
        self.archivo = None
        self.jamedia_sink = None
        
        self.player = None
        self.bus = None
        
        self.set_pipeline()
        
        # FIXME: Funciona con la radio pero no con la Tv
        if Gst.uri_is_valid(uri):
            self.archivo.set_property("location", archivo)
            self.player.set_property("uri", uri)
            self.play()
            self.new_handle(True)
        
    def set_pipeline(self):
        """Crea el pipe de Gst. (playbin)"""
        
        if self.video_pipeline:
            del(self.video_pipeline)
        
        self.pipeline = Gst.Pipeline()
        
        self.player = Gst.ElementFactory.make("playbin", "player")
        
        self.pipeline.add(self.player)
        
        self.audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        self.mp3enc = Gst.ElementFactory.make('lamemp3enc', "lamemp3enc")
        
        self.hiloarchivo = Gst.ElementFactory.make('queue', "hiloarchivo")
        self.archivo = Gst.ElementFactory.make('filesink', "archivo")
        
        self.jamedia_sink = Gst.Bin()
        self.jamedia_sink.add(self.audioconvert)
        
        pad = self.audioconvert.get_static_pad('sink')
        ghostpad = Gst.GhostPad.new('sink', pad)
        self.jamedia_sink.add_pad(ghostpad)
        
        self.jamedia_sink.add(self.mp3enc)
        self.jamedia_sink.add(self.hiloarchivo)
        self.jamedia_sink.add(self.archivo)
        
        self.audioconvert.link(self.mp3enc)
        self.mp3enc.link(self.hiloarchivo)
        self.hiloarchivo.link(self.archivo)
        
        self.player.set_property('audio-sink', self.jamedia_sink)
        
        self.bus = self.video_pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
        self.player.connect("about-to-finish", self.about_to_finish)
        self.player.connect("audio-tags-changed", self.audio_tags_changed)
        self.player.connect("source-setup", self.source_setup)
        
    def play(self, widget = None, event = None):
        
        self.pipeline.set_state(Gst.State.PLAYING)
        
    def stop(self, widget= None, event= None):
        """Detiene y limpia el pipe."""
        
        self.pipeline.set_state(Gst.State.PAUSED)
        self.pipeline.set_state(Gst.State.NULL)
        self.new_handle(False)
        
        if os.path.exists(self.patharchivo):
            os.chmod(self.patharchivo, 0755)
        
    def sync_message(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
        #print "A", mensaje.type
        pass
    
    def on_mensaje(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print err, debug
            self.new_handle(False)
            
    def new_handle(self, reset):
        """Elimina o reinicia la funcion que
        envia los datos de actualizacion."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = False
            
        if reset:
            self.actualizador = GObject.timeout_add(500, self.handle)
            
    def handle(self):
        """Consulta el estado y progreso de
        la grabacion."""
        
        if os.path.exists(self.patharchivo):
            tamanio = int(os.path.getsize(self.patharchivo)/1024)
            info = "Grabando: %s - %s Kb Almacenados." % (str(self.uri), str(tamanio))
            
            if self.info != info:
                self.info = info
                self.emit('update', self.info)
                
        return True
    
    def about_to_finish(self, player):
        
        #print "\n>>>", "about-to-finish"
        pass
        
    def audio_tags_changed(self, player, otro):
        
        #print "\n>>>", "audio-tags-changed"
        pass
        
    def source_setup(self, player, source):
        
        self.uri = source.get_property('location')
        