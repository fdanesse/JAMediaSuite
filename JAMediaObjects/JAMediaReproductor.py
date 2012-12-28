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

# Depends:
#   python-gi
#   gir1.2-gstreamer-1.0
#   gstreamer1.0-tools
#   gir1.2-gst-plugins-base-1.0
#   gstreamer1.0-plugins-good
#   gstreamer1.0-plugins-ugly
#   gstreamer1.0-plugins-bad
#   gstreamer1.0-libav

import os

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo

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
        self.pipeline = None
        self.estado = None
        
        self.duracion = 0
        self.posicion = 0
        self.actualizador = None
        
        self.player = None
        self.bus = None
        
        self.videobalance = None
        self.gamma = None
        self.videoflip = None
        self.pantalla = None
        
        self.video_in_stream = None
        
        self.config = {
            'saturacion': 1.0,
            'contraste': 1.0,
            'brillo': 0.0,
            'hue': 0.0,
            'gamma': 1.0
            }
        
        self.set_pipeline()
        
    def set_pipeline(self):
        
        if self.pipeline:
            del(self.pipeline)
            
        self.pipeline = Gst.Pipeline()
        
        self.player = Gst.ElementFactory.make("playbin", "player")
        
        # Elementos configurables permanentes.
        self.videobalance = Gst.ElementFactory.make('videobalance', "videobalance")
        self.gamma = Gst.ElementFactory.make('gamma', "gamma")
        self.videoflip = Gst.ElementFactory.make('videoflip', "videoflip")
        
        self.pantalla = Gst.ElementFactory.make('xvimagesink', "pantalla")
        
        self.player.set_window_handle(self.ventana_id)
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
        # Bin de video
        video_balance_bin = self.get_balance_bin()
        
        self.pipeline.add(self.player)
        self.player.set_property('video-sink', video_balance_bin)
        
        self.video_in_stream = None
        
        # Bin de Audio.
        
        # FIXME:
        # Intento obtener la salida de audio de playbin para poder
        # aplicar efectos sobre la salida de audio.
        # En teoría bastaría con crear un bin y establecer:
        #    self.player.set_property('audio-sink', audio_bin)
        # sin embargo no funciona: Element 'bin5' is not in bin 'abin'
        # Intenté buscando en los hijos de playbin, aunque tampoco puede
        # lograrlo, sin embargo es interesante aprender a estructurar los
        # elementos:
        
        #    La estructura de playbin es:
        #        GstPlaySink
        #            GstStreamSynchronizer (el cual no es accesible)
        
        '''
        audio_bin = self.get_audio_bin()
        
        self.pipeline.add(audio_bin)
        
        self.player.set_property('audio-sink', audio_bin)
        
        # Para imprimir la estructura interna de playbin
        for ele in self.player.children:
            self.print_children(ele)
        
    def print_children(self, elemento):
        
        print "Elemento:", elemento
        
        try:
            for ele in elemento.children:
                print "\tChild:", self.print_children(ele)
                
        except:
            print "\t\tSin hijos:", elemento'''
            
    def get_balance_bin(self):
        """Bin queue + efectos de video + Balance + flip."""
        
        bin = Gst.Bin()
        
        player_queue = Gst.ElementFactory.make("queue", "player_queue")
        
        bin.add(player_queue)
        bin.add(self.videobalance)
        bin.add(self.gamma)
        bin.add(self.videoflip)
        
        player_queue.link(self.videobalance)
        self.videobalance.link(self.gamma)
        self.gamma.link(self.videoflip)
        
        pantalla_bin = self.get_xvimagesink_video_bin()
        bin.add(pantalla_bin)
        self.videoflip.link(pantalla_bin)
        
        bin.add_pad(Gst.GhostPad.new("sink", player_queue.get_static_pad ("sink")))
        
        return bin
    
    def get_xvimagesink_video_bin(self):
        """Bin queue + pantalla para dibujar video."""
        
        bin = Gst.Bin()
        
        xvimage_queue = Gst.ElementFactory.make("queue", "xvimage_queue")
        
        bin.add(xvimage_queue)
        bin.add(self.pantalla)
        
        xvimage_queue.link(self.pantalla)
        
        bin.add_pad(Gst.GhostPad.new("sink", xvimage_queue.get_static_pad ("sink")))
        
        return bin
    
    '''
    def get_audio_bin(self):
        """Salida de audio a sonido."""
        
        bin = Gst.Bin()
    
        audio_queue = Gst.ElementFactory.make("queue", "audio_queue")
        autoaudiosink = Gst.ElementFactory.make("autoaudiosink", "autoaudio_bin")
        
        bin.add(audio_queue)
        bin.add(autoaudiosink)
        
        audio_queue.link(autoaudiosink)
        
        bin.add_pad(Gst.GhostPad.new("sink", audio_queue.get_static_pad ("sink")))
        
        return bin'''
    
    def load(self, uri):
        """Carga un archivo o stream en el pipe de Gst."""
        
        self.stop()
        self.set_pipeline()
        
        if os.path.exists(uri):
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)
            self.play()
            # reconfigurar balance y flip
            
        else:
            # FIXME: Funciona con la radio pero no con la Tv
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.play()
                # reconfigurar balance y flip
        
    def play(self):
        """Pone el pipe de Gst en Gst.State.PLAYING"""
        
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        """Pone el pipe de Gst en Gst.State.NULL"""
        
        self.pipeline.set_state(Gst.State.NULL)
        
    def pause(self):
        """Pone el pipe de Gst en Gst.State.PAUSED"""
        
        self.pipeline.set_state(Gst.State.PAUSED)
        
    def pause_play(self):
        """Llama a play() o pause()
        segun el estado actual del pipe de Gst."""
        
        if self.estado == Gst.State.PAUSED \
            or self.estado == Gst.State.NULL \
            or self.estado == Gst.State.READY:
            self.play()
            
        elif self.estado == Gst.State.PLAYING:
            self.pause()
            
        else:
            print self.estado
        
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
            print taglist
            print datos
            if not 'video-codec' in datos:
                if self.video_in_stream == True or self.video_in_stream == None:
                    self.video_in_stream = False
                    self.emit("video", False)
                    
            if 'video-codec' in datos:
                if self.video_in_stream == False or self.video_in_stream == None:
                    self.video_in_stream = True
                    self.emit("video", True)
                    
            #self.duracion = int(taglist.to_string().split("duration=(guint64)")[1].split(',')[0])
            #Ejemplo:
                # taglist,
                # duration=(guint64)780633000000,
                # video-codec=(string)H.264,
                # audio-codec=(string)"MPEG-4\ AAC"
            return
        
        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "***", 'sync_message'
            print err, debug
            #self.pipeline.set_state(Gst.State.READY)
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
            #self.pipeline.seek_simple(Gst.Format.TIME,
            #Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)
            self.new_handle(False)
            self.emit("endfile")
            
        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "***", 'on_mensaje'
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
        
    def rotar(self, valor):
        """ Rota el Video. """
        
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
        
    def set_balance(self, brillo = None, contraste = None,
        saturacion = None, hue = None, gamma = None):
        """Seteos de balance en la fuente de video.
        Recibe % en float y convierte a los valores del filtro."""
        
        if saturacion != None:
            # Double. Range: 0 - 2 Default: 1
            self.config['saturacion'] = 2.0 * saturacion / 100.0
            self.videobalance.set_property('saturation', self.config['saturacion'])
            
        if contraste != None:
            # Double. Range: 0 - 2 Default: 1
            self.config['contraste'] = 2.0 * contraste / 100.0
            self.videobalance.set_property('contrast', self.config['contraste'])
            
        if brillo != None:
            # Double. Range: -1 - 1 Default: 0
            self.config['brillo'] = (2.0 * brillo / 100.0) - 1.0
            self.videobalance.set_property('brightness', self.config['brillo'])
            
        if hue != None:
            # Double. Range: -1 - 1 Default: 0
            self.config['hue'] = (2.0 * hue / 100.0) - 1.0
            self.videobalance.set_property('hue', self.config['hue'])
            
        if gamma != None:
            # Double. Range: 0,01 - 10 Default: 1
            self.config['gamma'] = (10.0 * gamma / 100.0)
            self.gamma.set_property('gamma', self.config['gamma'])
            
    def get_balance(self):
        """Retorna los valores actuales de balance en % float."""
        
        return {
        'saturacion': self.config['saturacion'] * 100.0 / 2.0,
        'contraste': self.config['contraste'] * 100.0 / 2.0,
        'brillo': (self.config['brillo']+1) * 100.0 / 2.0,
        'hue': (self.config['hue']+1) * 100.0 / 2.0,
        'gamma': self.config['gamma'] * 100.0 / 10.0
        }
        
    def get_balance_default(self):
        """ Retorna los valores por defecto para balance y gamma. """
        
        return {
        'saturacion': 50.0,
        'contraste': 50.0,
        'brillo': 50.0,
        'hue': 50.0,
        'gamma': 10.0
        }
        
    def new_handle(self, reset):
        """Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if reset:
            self.actualizador = GObject.timeout_add(500, self.handle)
        
    def handle(self):
        """Envia los datos de actualizacion para
        la barra de progreso del reproductor."""
        
        bool1, valor1 = self.pipeline.query_duration(Gst.Format.TIME)
        bool2, valor2 = self.pipeline.query_position(Gst.Format.TIME)
        
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
        
        self.pipeline.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH |
            Gst.SeekFlags.KEY_UNIT,
            posicion)
    
    def get_volumen(self):
        """Obtiene el volumen de reproducción.
        Lo hace solo al reproducir el primer archivo
        o streaming y envía el dato para actualizar
        el control de volúmen."""
        pass
        
    def set_volumen(self, valor):
        """Cambia el volúmen de Reproducción."""
        
        self.player.set_property('volume', float(valor/100))
        
class JAMediaGrabador(GObject.GObject):
    """Graba desde un streaming de radio o tv."""
    
    __gsignals__ = {
    "update":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self, uri, archivo):
        
        GObject.GObject.__init__(self)
        
        self.patharchivo = archivo
        self.actualizador = None
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
        
        if self.pipeline:
            del(self.pipeline)
        
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
        
        self.bus = self.pipeline.get_bus()
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
            print "***", 'on_mensaje'
            print err, debug
            self.pipeline.set_state(Gst.State.READY)
            self.new_handle(False)
            
    def new_handle(self, reset):
        """Elimina o reinicia la funcion que
        envia los datos de actualizacion."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
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
        