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
from JAMediaGstreamer.JAMediaBins import Efectos_Video_bin
from JAMediaGstreamer.JAMediaBins import Foto_bin

import JAMediaGlobales as G

GObject.threads_init()
Gst.init([])

CONFIG_DEFAULT = {
    'saturacion': 1.0,
    'contraste': 1.0,
    'brillo': 0.0,
    'hue': 0.0,
    'gamma': 1.0,
    }
    
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
        
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        
        self.player = None
        self.bus = None
        
        self.video_pipeline = None
        self.efectos_bin = None
        self.audio_pipelin = None
        
        self.videobalance = None
        self.gamma = None
        self.videoflip = None
        
        self.video_in_stream = False
        
        self.config = {}
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        self.config['gamma'] = CONFIG_DEFAULT['gamma']
        
        self.efectos = []
        self.config_efectos = {}
        
        self.reset()
        
    def reset(self):
        
        if self.video_pipeline:
            del(self.video_pipeline)
            
        if self.efectos_bin:
            del(self.efectos_bin)
            
        self.video_pipeline = Gst.Pipeline()
        
        self.player = Gst.ElementFactory.make(
            "playbin", "player")
        self.player.set_property(
            'force-aspect-ratio', True)

        self.videobalance = Gst.ElementFactory.make(
            'videobalance', "videobalance")
        
        self.gamma = Gst.ElementFactory.make(
            'gamma', "gamma")
        
        self.videoflip = Gst.ElementFactory.make(
            'videoflip', "videoflip")
        
        self.player.set_window_handle(self.ventana_id)
        
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
        self.multi_out_tee = Gst.ElementFactory.make(
            'tee', "multi_out_tee")
        
        self.efectos_bin = Efectos_Video_bin(
            self.efectos, self.config_efectos)
        
        pantalla = Gst.ElementFactory.make(
            'xvimagesink', "pantalla")
        
        #self.foto_bin = Foto_bin()
        
        self.video_pipeline.add(self.multi_out_tee)
        self.video_pipeline.add(self.efectos_bin)
        self.video_pipeline.add(self.videobalance)
        self.video_pipeline.add(self.gamma)
        self.video_pipeline.add(self.videoflip)
        self.video_pipeline.add(pantalla)
        #self.video_pipeline.add(self.foto_bin)
        
        self.multi_out_tee.link(self.efectos_bin)
        self.efectos_bin.link(self.videobalance)
        self.videobalance.link(self.gamma)
        self.gamma.link(self.videoflip)
        self.videoflip.link(pantalla)
        
        #self.multi_out_tee.link(self.foto_bin)
        
        self.video_pipeline.add_pad(
            Gst.GhostPad.new(
                "sink",
                self.multi_out_tee.get_static_pad ("sink")))
        
        self.player.set_property('video-sink', self.video_pipeline)
        
        # Pipe de Audio
        self.audio_pipelin = Gst.Pipeline()
        
        self.tee_audio = Gst.ElementFactory.make(
            "tee", "tee_audio")
        
        audioconvert = Gst.ElementFactory.make(
            "audioconvert", "audioconvert")
            
        autoaudiosink = Gst.ElementFactory.make(
            "autoaudiosink", "autoaudiosink")
        
        self.audio_pipelin.add(self.tee_audio)
        self.audio_pipelin.add(audioconvert)
        self.audio_pipelin.add(autoaudiosink)
        
        self.tee_audio.link(audioconvert)
        audioconvert.link(autoaudiosink)
        
        self.audio_pipelin.add_pad(
            Gst.GhostPad.new(
                "sink",
                self.tee_audio.get_static_pad ("sink")))
            
        self.player.set_property('audio-sink', self.audio_pipelin)
        
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        self.config['gamma'] = CONFIG_DEFAULT['gamma']
        
        self.videobalance.set_property('saturation', self.config['saturacion'])
        self.videobalance.set_property('contrast', self.config['contraste'])
        self.videobalance.set_property('brightness', self.config['brillo'])
        self.videobalance.set_property('hue', self.config['hue'])
        
        self.gamma.set_property('gamma', self.config['gamma'])
        
        self.videoflip.set_property('method', 0)
        
        self.video_in_stream = False
        
    '''
    def fotografiar(self, widget = None, event = None):
        """Toma una fotografia."""
        
        #foto_bin = self.pipeline.get_by_name("foto_bin")
        gdkpixbufsink = self.foto_bin.get_by_name("gdkpixbufsink")
        
        if gdkpixbufsink and gdkpixbufsink != None:
            pixbuf = gdkpixbufsink.get_property('last-pixbuf')
            
            if pixbuf and pixbuf != None:
                
                fecha = datetime.date.today()
                hora = time.strftime("%H-%M-%S")
                archivo = os.path.join(
                    G.IMAGENES_JAMEDIA_VIDEO,
                    "%s-%s.png" % (fecha, hora))
                
                self.patharchivo = archivo
                
                pixbuf.savev(self.patharchivo, "png", [], [])'''
                
    '''
    def link_visualizador(self):
        
        self.pause()
        
        self.audio_pipelin.add(self.audio_grafico_pipeline)
        self.tee_audio.link(self.audio_grafico_pipeline)
        
        self.play()'''
        
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
    
    def get_volumen(self):
        """Obtiene el volumen de reproducción.
        Lo hace solo al reproducir el primer archivo
        o streaming y envía el dato para actualizar
        el control de volúmen."""
        
        print "Volumen:", self.player.get_property('volume')
        
    def set_volumen(self, valor):
        """Cambia el volúmen de Reproducción."""
        
        self.player.set_property('volume', float(valor/100))
        
    def agregar_efecto(self, nombre_efecto):
        """Agrega un efecto según su nombre."""
        
        self.efectos.append( nombre_efecto )
        self.config_efectos[nombre_efecto] = {}
        
        self.new_handle(False)
        self.reconstruir_efectos()
        self.new_handle(True)
        
    def quitar_efecto(self, indice_efecto):
        """Quita el efecto correspondiente al indice o
        al nombre que recibe."""
        
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
        
        self.new_handle(False)
        self.reconstruir_efectos()
        self.new_handle(True)
        
    def reconstruir_efectos(self):
        
        # FIXME: stream stopped, reason not-negotiated
        """
        uri = self.player.get_property("uri")
        
        if uri and uri != None:
            self.pause()
            
        self.multi_out_tee.unlink(self.efectos_bin)
        self.efectos_bin.unlink(self.videobalance)
        
        self.video_pipeline.remove(self.efectos_bin)
        del(self.efectos_bin)
        
        self.efectos_bin = Efectos_Video_bin(
            self.efectos, self.config_efectos)
        
        self.video_pipeline.add(self.efectos_bin)
        
        self.multi_out_tee.link(self.efectos_bin)
        self.efectos_bin.link(self.videobalance)
        
        self.player.set_property('video-sink', self.video_pipeline)
        
        if uri and uri != None:
            self.play()"""
            
        self.stop()
        
        uri = self.player.get_property("uri")
        
        self.reset()
        
        if uri: self.load(uri)
        
    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        """Configura un efecto en el pipe."""
        
        efectos_bin = self.video_pipeline.get_by_name('efectos_bin')
        bin_efecto = efectos_bin.get_by_name(nombre_efecto)
        self.config_efectos[nombre_efecto][propiedad] = valor
        efectos_bin.config_efectos[nombre_efecto][propiedad] = valor
        bin_efecto.get_by_name(nombre_efecto).set_property(propiedad, valor)
        
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
        