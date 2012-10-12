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

# Se remplaza:
# Depends:
#   python-gst0.10
#   gstreamer0.10-plugins-good
#   gstreamer0.10-plugins-ugly
#   gstreamer0.10-plugins-bad
#   gstreamer0.10-ffmpeg

# Con:
# Depends:
#   python-gi
#   gir1.2-gstreamer-1.0
#   gstreamer1.0-tools
#   gir1.2-gst-plugins-base-1.0
#   gstreamer1.0-plugins-good
#   gstreamer1.0-plugins-ugly
#   gstreamer1.0-plugins-bad
#   gstreamer1.0-libav
    
# https://wiki.ubuntu.com/Novacut/GStreamer1.0#Using_GStreamer_1.0_from_Python
# http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer/html/GstBus.html#gst-bus-create-watch
# http://www.roojs.org/seed/gir-1.1-gtk-2.0/Gst.MessageType.html#expand

import os

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo

GObject.threads_init()
Gst.init([])

PROPIEDADES_PLAYBIN = [
'name',
'parent',
'async-handling',
'message-forward',
'delay',
'auto-flush-bus',
'uri',
'current-uri',
'suburi',
'current-suburi',
'source',
'flags',
'n-video',
'current-video',
'n-audio',
'current-audio',
'n-text',
'current-text',
'subtitle-encoding',
'audio-sink',
'video-sink',
'vis-plugin',
'text-sink',
'volume',
'mute',
'sample',
'subtitle-font-desc',
'connection-speed',
'buffer-size',
'buffer-duration',
'av-offset',
'ring-buffer-max-size',
'force-aspect-ratio']

PROPIEDADES_FILESRC = [
'name',
'parent',
'blocksize',
'num-buffers',
'typefind',
'do-timestamp',
'location']

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
        (GObject.TYPE_FLOAT,))}

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
        
        self.config = {
            'saturacion': 1.0,
            'contraste': 1.0,
            'brillo': 0.0,
            'hue': 0.0,
            'gamma': 1.0
            }
            
        self.set_pipeline()
        
    def set_pipeline(self):
        """Crea el pipe de Gst. (playbin)"""
        
        if self.pipeline: del(self.pipeline)
        
        self.pipeline = Gst.Pipeline()
        
        # http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-playbin2.html
        self.player = Gst.ElementFactory.make("playbin", "player")
        
        self.multi = Gst.ElementFactory.make('tee', "tee")
        self.videobalance = Gst.ElementFactory.make('videobalance', "videobalance")
        self.gamma = Gst.ElementFactory.make('gamma', "gamma")
        self.videoflip = Gst.ElementFactory.make('videoflip', "videoflip")
        self.hilovideoapantalla = Gst.ElementFactory.make('queue', "hilovideoapantalla")
        self.pantalla = Gst.ElementFactory.make('xvimagesink', "pantalla")
        
        self.player.connect("video-changed", self.video_changed)
        self.player.connect("audio-changed", self.audio_changed)
        self.player.connect("about-to-finish", self.about_to_finish)
        self.player.connect("text-changed", self.text_changed)
        self.player.connect("video-tags-changed", self.video_tags_changed)
        self.player.connect("audio-tags-changed", self.audio_tags_changed)
        self.player.connect("text-tags-changed", self.text_tags_changed)
        self.player.connect("source-setup", self.source_setup)
        
        self.pipeline.add(self.player)
        
        self.jamedia_sink = Gst.Bin()
        self.jamedia_sink.add(self.videobalance)
        
        pad = self.videobalance.get_static_pad('sink')
        ghostpad = Gst.GhostPad.new('sink', pad)
        self.jamedia_sink.add_pad(ghostpad)
        
        self.jamedia_sink.add(self.gamma)
        self.jamedia_sink.add(self.videoflip)
        self.jamedia_sink.add(self.multi)
        self.jamedia_sink.add(self.hilovideoapantalla)
        self.jamedia_sink.add(self.pantalla)
        
        self.videobalance.link(self.gamma)
        self.gamma.link(self.videoflip)
        self.videoflip.link(self.multi)
        self.multi.link(self.hilovideoapantalla)
        self.hilovideoapantalla.link(self.pantalla)
        
        self.player.set_property('video-sink', self.jamedia_sink)
        
        self.player.set_window_handle(self.ventana_id)
        
        self.config = {
            'saturacion': 1.0,
            'contraste': 1.0,
            'brillo': 0.0,
            'hue': 0.0,
            'gamma': 1.0
            }
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
    def sync_message(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
        try:
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return
            
        except:
            pass
        
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
                
            elif old == Gst.State.NULL and new == Gst.State.READY:
                pass
            
            elif old == Gst.State.PAUSED and new == Gst.State.READY:
                pass
            
            else:
                return
            
        elif mensaje.type == Gst.MessageType.ASYNC_DONE:
            return
        
        elif mensaje.type == Gst.MessageType.NEW_CLOCK:
            return
        
        elif mensaje.type == Gst.MessageType.STREAM_STATUS:
            return
        
        elif mensaje.type == Gst.MessageType.TAG:
            return
        
        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            #print "***", 'sync_message'
            #print err, debug
            self.new_handle(False)
            return
        
        elif mensaje.type == Gst.MessageType.EOS:
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
            
            return
                
    def on_mensaje(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
        #if mensaje.type == Gst.MessageType.ASYNC_DONE:
        #    print mensaje.get_structure().get_name()
        #elif mensaje.type == Gst.MessageType.NEW_CLOCK:
        #    pass
        
        if mensaje.type == Gst.MessageType.ELEMENT:
            nombre = mensaje.get_structure().get_name()
            
        if mensaje.type == Gst.MessageType.EOS:
            #self.pipeline.seek_simple(Gst.Format.TIME,
            #Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)
            self.new_handle(False)
            self.emit("endfile")
            
        elif mensaje.type == Gst.MessageType.QOS:
            pass
        
        elif mensaje.type == Gst.MessageType.WARNING:
            #print mensaje.get_structure().to_string()
            pass
            
        elif mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            #print "***", 'on_mensaje'
            #print err, debug
            self.new_handle(False)
            #self.stop()
            #self.set_pipeline()
            
        elif mensaje.type == Gst.MessageType.LATENCY:
            pass
        else:
            pass
        
    def load(self, uri):
        """Carga un archivo o stream en el pipe de Gst."""
        
        self.stop()
        self.set_pipeline()
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
        
        self.pipeline.set_state(Gst.State.PLAYING)
        
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
            
        if contraste != None:
            # Double. Range: 0 - 2 Default: 1
            self.config['contraste'] = 2.0 * contraste / 100.0
            
        if brillo != None:
            # Double. Range: -1 - 1 Default: 0
            self.config['brillo'] = (2.0 * brillo / 100.0) - 1.0
            
        if hue != None:
            # Double. Range: -1 - 1 Default: 0
            self.config['hue'] = (2.0 * hue / 100.0) - 1.0
            
        if gamma != None:
            # Double. Range: 0,01 - 10 Default: 1
            self.config['gamma'] = (10.0 * gamma / 100.0)
            
        self.videobalance.set_property('saturation', self.config['saturacion'])
        self.videobalance.set_property('contrast', self.config['contraste'])
        self.videobalance.set_property('brightness', self.config['brillo'])
        self.videobalance.set_property('hue', self.config['hue'])
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
        
    def video_changed(self, player):
        
        #print "\n>>>", "video-changed"
        #print player
        #print "\t", 'name', player.get_property('name')
        #print "\t", 'parent', player.get_property('parent')
        #print "\t", 'source', player.get_property('source')
        #print "\t", 'n-video', player.get_property('n-video')
        #print "\t", 'video-sink', player.get_property('video-sink')
        #print "\t", 'vis-plugin', player.get_property('vis-plugin')
        #print "\t", 'force-aspect-ratio', player.get_property('force-aspect-ratio')
        pass
    
    def audio_changed(self, player):
        
        #print "\n>>>", "audio-changed"
        #print player
        #print "\t", 'name', player.get_property('name')
        #print "\t", 'parent', player.get_property('parent')
        #print "\t", 'source', player.get_property('source')
        #print "\t", 'volume', player.get_property('volume')
        #print "\t", 'n-audio', player.get_property('n-audio')
        #print "\t", 'audio-sink', player.get_property('audio-sink')
        #print "\t", 'sample', player.get_property('sample')
        pass
    
    def about_to_finish(self, player):
        
        #print "\n>>>", "about-to-finish"
        #print "\t", player
        pass
    
    def text_changed(self, player):
        
        #print ">>>", "text-changed"
        pass
        
    def video_tags_changed(self, player, otro):
        
        #print "\n>>>", "video-tags-changed"
        pass
        
    def audio_tags_changed(self, player, otro):
        
        #print "\n>>>", "audio-tags-changed"
        pass
        
    def text_tags_changed(self, player, otro):
        
        #print ">>>", "text-tags-changed"
        pass
        
    def source_setup(self, player, source):
        
        #print "\n>>>", "source-setup"
        #print "\t", player
        #print "\t", filesrc
        #for p in PROPIEDADES_FILESRC:
        #    print "\t", p, source.get_property(p)
        pass
    
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
            
    def new_handle(self, reset):
        """Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if reset:
            self.actualizador = GObject.timeout_add(35, self.handle)
        
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
        self.pipeline.seek_simple(Gst.Format.TIME,
        Gst.SeekFlags.FLUSH, posicion)
    
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
        
        if self.pipeline: del(self.pipeline)
        
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
        