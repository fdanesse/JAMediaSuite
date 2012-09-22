#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaVideoDesktop.py por:
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

import sys
import os
import time
import datetime

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo

import JAMediaGlobales as G

GObject.threads_init()
Gdk.threads_init()
Gst.init([])

class JAMediaVideoDesktop(GObject.GObject):
    """Simple Grabador de Escritorio, Versión 1.0"""
    
    __gsignals__ = {"update":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        GObject.GObject.__init__(self)
        
        self.name = "JAMediaVideoDesktop"
        
        self.pipeline = None
        self.estado = None
        
        self.actualizador = None
        self.file_path = None
        
        # config
        # GStreamer-WARNING **: 0.10-style raw video caps are being created. Should be video/x-raw,format=(string).. now.
        self.resolucion = "video/x-raw-yuv,width=800,height=600"
        self.audio = "audio/x-raw-int,rate=16000,channels=1,depth=16"
        
        screen = GdkX11.X11Screen()
        
        self.x = 0
        self.y = 0
        self.width = 640 #int(screen.width())
        self.height = 480 #int(screen.height())
        
        self.calidad_compresion = 16
        
        self.info = None
        
        self.config = {
        'inicioenx': self.x,
        'finenx': self.width,
        'inicioeny': self.y,
        'fineny': self.height,
        'resolucionfinal': self.resolucion,
        'audio': self.audio,
        'compresion': self.calidad_compresion
        }
        
    def set_pipeline(self):
        """Crea el pipe para grabar desde x y autoaudio."""
        
        print "Iniciando pipe gst:"
        #for item in self.config.items():
        #    print item
        
        if self.pipeline:
            del(self.pipeline)
            self.pipeline = None
            
        self.pipeline = Gst.Pipeline()
        
        self.ximagesrc = Gst.ElementFactory.make('ximagesrc', "ximagesrc")
        self.ximagesrc.set_property('use-damage', False)
        self.ximagesrc.set_property('startx', self.x)
        self.ximagesrc.set_property('endx', self.width)
        self.ximagesrc.set_property('starty', self.y)
        self.ximagesrc.set_property('endy', self.height)
        #self.ximagesrc.set_property('parent', self.pipeline)
        
        # Convertir Video
        # Video scaler (required when the autovideosink does not use an X overlay)
        self.videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        self.hiloencodearvideo = Gst.ElementFactory.make('queue', "hiloencodearvideo")
        self.hiloencodearvideo.set_property("leaky", True)
        # Escalar la salida
        '''
        self.escalavideo = Gst.ElementFactory.make("videoscale", "vbscale")
        self.scalecapsfilter = Gst.ElementFactory.make("capsfilter", "scalecaps")
        scalecaps = Gst.Caps()
        scalecaps.from_string(self.resolucion)
        self.scalecapsfilter.set_property("caps", scalecaps)'''
        # Encodear Video
        self.theoraenc = Gst.ElementFactory.make('theoraenc', 'theoraenc')
        self.theoraenc.set_property("quality", self.calidad_compresion) # 48 default
        '''
        # Fuente de Audio
        self.autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc") # autoaudiosrc - pulsesrc - autoaudiosrc
        # Convertir Audio
        self.audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        self.hiloencodearaudio = Gst.ElementFactory.make('queue', "hiloencodearaudio")
        self.hiloencodearaudio.set_property("leaky", True)
        
        # Filtro Audio
        self.audiorate = Gst.ElementFactory.make("audiorate", 'audiorate')
        self.filtroaudio = Gst.ElementFactory.make("capsfilter", "filtroaudio")
        #  GStreamer-WARNING **: 0.10-style raw audio caps are being created. Should be audio/x-raw,format=(string).. now.
        capaaudio = Gst.Caps()
        capaaudio.from_string(self.audio)
        self.filtroaudio.set_property("caps", capaaudio)
        # Encodear Audio
        self.vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")'''
        
        # Muxor - Unión audio y video
        self.hilovideomuxor = Gst.ElementFactory.make('queue', "hilovideomuxor")
        self.hiloaudiomuxor = Gst.ElementFactory.make('queue', "hiloaudiomuxor")
        self.oggmux = Gst.ElementFactory.make('oggmux', "oggmux")
        
        # Archivo - Unión muxor archivo
        self.hiloarchivo = Gst.ElementFactory.make('queue', "hiloarchivo")
        self.hiloarchivo.set_property("leaky", True)
        self.archivo = Gst.ElementFactory.make('filesink', "archivo")
        self.archivo.set_property("location", self.file_path)
        
        
        self.pipeline.add(self.ximagesrc)
        
        self.pipeline.add(self.videoconvert)
        #self.pipeline.add(self.escalavideo)# link_filtered(self.escalavideo, self.scalecapsfilter)
        #self.pipeline.add(self.scalecapsfilter)
        self.pipeline.add(self.hiloencodearvideo)
        self.pipeline.add(self.theoraenc)
        '''
        self.pipeline.add(self.autoaudiosrc)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.audiorate)
        self.pipeline.add(self.filtroaudio)
        self.pipeline.add(self.hiloencodearaudio)
        self.pipeline.add(self.vorbisenc)'''
        
        self.pipeline.add(self.hilovideomuxor)
       # self.pipeline.add(self.hiloaudiomuxor)
        
        self.pipeline.add(self.oggmux)
        
        self.pipeline.add(self.hiloarchivo)
        self.pipeline.add(self.archivo)
        
        
        self.ximagesrc.link(self.videoconvert)
        self.videoconvert.link(self.hiloencodearvideo)
        #self.videoconvert.link(self.escalavideo)
        #self.escalavideo.link(self.scalecapsfilter)
        #self.scalecapsfilter.link(self.hiloencodearvideo)
        self.hiloencodearvideo.link(self.theoraenc)
        
        self.theoraenc.link(self.hilovideomuxor)
        self.hilovideomuxor.link(self.oggmux)
        '''
        self.autoaudiosrc.link(self.audioconvert)
        self.audioconvert.link(self.audiorate)
        self.audiorate.link(self.filtroaudio)
        self.filtroaudio.link(self.hiloencodearaudio)
        self.hiloencodearaudio.link(self.vorbisenc)
        
        self.vorbisenc.link(self.hiloaudiomuxor)
        self.hiloaudiomuxor.link(self.oggmux)
        
        self.oggmux.link(self.hiloarchivo)
        self.hiloarchivo.link(self.archivo)'''
        
        self.bus = self.pipeline.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.add_signal_watch()
        self.bus.connect("sync-message::element", self.on_sync_message)
        self.bus.connect("message", self.on_message)
        
    def set_config(self, resolucion, audiorate,
        audiochannels, audiodepth, compresion):
        """Configura la calidad de grabación de audio y video."""
        
        self.stop()
        
        w, h = resolucion
        self.resolucion = "video/x-raw-yuv,width=%i,height=%i" % (w,h)
        self.audio = "audio/x-raw-int,rate=%i,channels=%i,depth=%i" % (audiorate, audiochannels, audiodepth)
        self.calidad_compresion = compresion
        
        self.set_pipeline()
        
    def on_sync_message(self, bus, message):
        """Captura mensajes en el bus."""
        
        if message.get_structure() is None: return
    
    def on_message(self, bus, message):
        """Captura mensajes en el bus."""
        
        if message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print "ERROR ON_MESSAGE: ", err, debug
            
            #self.pipeline.set_state(Gst.State.NULL)
            
    def grabar(self, location_path):
        """Comienza a Grabar."""
        
        self.new_handle(False)
        '''
        if self.pipeline:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.pipeline.set_state(Gst.State.NULL)'''
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        self.file_path = os.path.join(location_path,"%s-%s.ogg" % (fecha, hora))
        
        self.set_pipeline()
        
        self.estado = "Grabando"
        self.pipeline.set_state(Gst.State.PLAYING)
        
        self.new_handle(True)
        
        for child in self.pipeline.children:
            try:
                print child, child.parent
            except:
                pass
        #sys.exit(0)
        
    def stop(self, widget= None, event= None):
        """Detiene la grabación."""
        
        self.new_handle(False)
        
        if self.pipeline:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.pipeline.set_state(Gst.State.NULL)
        
        self.estado = None
        
    def new_handle(self, reset):
        """Reinicia o mata el actualizador."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if reset:
            self.actualizador = GObject.timeout_add(300, self.handle)
            
    def handle(self):
        """Envía información periódicamente."""
        
        if os.path.exists(self.file_path):
            tamanio = int(os.path.getsize(self.file_path)/1024)
            info = "Grabando: %s - %s Kb Almacenados." % (str(self.file_path), str(tamanio))
            
            if self.info != info:
                self.info = info
                self.emit('update', self.info)
                print self.info
                
        return True
    
if __name__=="__main__":
    
    #default_location = os.path.dirname(__file__)
    grabador = JAMediaVideoDesktop()
    grabador.grabar('/home/flavio')
    Gtk.main()
    
'''
Notas:
     gst-launch-1.0 ximagesrc ! videoconvert ! queue ! theoraenc ! queue ! oggmux ! queue ! filesink location=Prueba.ogg
'''

# gtk 2 + gstreamer 0.10
'''
import sys
import os
import gtk
import gobject
import gst
import pygst
import time
import datetime

gobject.threads_init()
gtk.gdk.threads_init()

class DesktopGrab(gtk.Widget):
    """Simple Grabador de Escritorio, Versión 1.0"""
    
    __gsignals__ = {"update":(gobject.SIGNAL_RUN_FIRST,
    gobject.TYPE_NONE, (gobject.TYPE_STRING,))}
    
    def __init__(self):
        
        gtk.Widget.__init__(self)
        
        self.pipeline = None
        self.estado = None
        
        self.ximagesrc =  None
        
        self.scale = None
        self.scalecapsfilter = None
        self.scalecaps = None
        self.colorspace = None
        
        self.hiloencodearvideo = None
        self.theoraenc = None
        
        self.alsasrc = None
        self.capaaudio = None
        self.filtroaudio = None
        self.hilofiltro = None
        self.audioconvert = None
        
        self.vorbisenc = None
        self.hilovideomuxor = None
        self.hiloaudiomuxor = None
        
        self.oggmux = None
        
        self.hiloarchivo = None
        self.archivo = None
        
        # links
        self.encodearvideo = None
        self.encodearaudio = None
        self.archivar = None
        
        self.actualizador = None
        self.file_path = None
        
        # config
        self.resolucion = "video/x-raw-yuv,width=800,height=600"
        self.audio = "audio/x-raw-int,rate=16000,channels=1,depth=16"
        
        self.x = 0
        self.y = 0
        self.width = int(gtk.gdk.screen_width())
        self.height = int(gtk.gdk.screen_height())
        
        self.calidad_compresion = 16
        
        self.info = None
        
        self.config = {
        'inicioenx': self.x,
        'finenx': self.width,
        'inicioeny': self.y,
        'fineny': self.height,
        'resolucionfinal': self.resolucion,
        'audio': self.audio,
        'compresion': self.calidad_compresion
        }
        
    def set_pipeline(self):
        """Crea el pipe para grabar desde x y autoaudio."""
        
        print "Iniciando pipe gst:"
        for item in self.config.items():
            print item
        
        if self.pipeline:
            del(self.pipeline)
            self.pipeline = None
            
        self.pipeline = gst.Pipeline("player")
        
        self.ximagesrc = gst.element_factory_make('ximagesrc', "x11")
        self.ximagesrc.set_property('startx', self.x)
        self.ximagesrc.set_property('endx', self.width)
        self.ximagesrc.set_property('starty', self.y)
        self.ximagesrc.set_property('endy', self.height)
        
        self.hiloencodearvideo = gst.element_factory_make('queue', "hiloencodearvideo")
        
        self.scale = gst.element_factory_make("videoscale", "vbscale")
        self.scalecapsfilter = gst.element_factory_make("capsfilter", "scalecaps")
        
        self.scalecaps = gst.Caps(self.resolucion)
        self.scalecapsfilter.set_property("caps", self.scalecaps)
        
        # Encodear Video
        self.colorspace = gst.element_factory_make("ffmpegcolorspace", "vbcolorspace")
        self.theoraenc = gst.element_factory_make('theoraenc', 'theoraenc')
        self.theoraenc.set_property("quality", self.calidad_compresion) # 48 default
        
        # Fuente de Audio
        self.alsasrc = gst.element_factory_make('alsasrc', "alsasrc") # alsasrc - pulsesrc - autoaudiosrc
        self.alsasrc.set_property("device", "default")
        self.capaaudio = gst.Caps(self.audio)
        
        self.audiorate = gst.element_factory_make("audiorate")
        
        self.filtroaudio = gst.element_factory_make("capsfilter", "filtroaudio")
        self.filtroaudio.set_property("caps", self.capaaudio)
        
        self.hilofiltro = gst.element_factory_make('queue', "hilofiltro")
        self.hilofiltro.set_property("leaky", True)
        
        # Encodear Audio
        self.audioconvert = gst.element_factory_make('audioconvert', "audioconvert")
        self.vorbisenc = gst.element_factory_make('vorbisenc', "vorbisenc")
        
        # Muxor - Unión audio y video
        self.hilovideomuxor = gst.element_factory_make('queue', "hilovideomuxor")
        self.hiloaudiomuxor = gst.element_factory_make('queue', "hiloaudiomuxor")
        self.oggmux = gst.element_factory_make('oggmux', "oggmux")
        
        # Archivo - Unión muxor archivo
        self.hiloarchivo = gst.element_factory_make('queue', "hiloarchivo")
        self.archivo = gst.element_factory_make('filesink', "archivo")
        self.archivo.set_property("location", self.file_path)
        
        self.pipeline.add(
            self.ximagesrc,
            self.colorspace,
            self.scale,
            self.scalecapsfilter,
            self.hiloencodearvideo,
            self.theoraenc,
            self.hilovideomuxor,
            self.oggmux,
            
            self.alsasrc,
            self.hilofiltro,
            self.audiorate,
            self.filtroaudio,
            self.audioconvert,
            self.vorbisenc,
            self.hiloaudiomuxor,
            
            self.hiloarchivo,
            self.archivo
            )
            
        self.encodearvideo = gst.element_link_many(
            self.ximagesrc,
            self.colorspace,
            self.scale,
            self.scalecapsfilter,
            self.hiloencodearvideo,
            self.theoraenc,
            self.hilovideomuxor,
            self.oggmux
            )
        
        self.encodearaudio = gst.element_link_many(
            self.alsasrc,
            self.hilofiltro,
            self.audiorate,
            self.filtroaudio,
            self.audioconvert,
            self.vorbisenc,
            self.hiloaudiomuxor,
            self.oggmux
            )
            
        self.archivar = gst.element_link_many(
            self.oggmux,
            self.hiloarchivo,
            self.archivo
            )
            
        self.bus = self.pipeline.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.add_signal_watch()
        self.bus.connect("sync-message::element", self.on_sync_message)
        self.bus.connect("message", self.on_message)
        
    def set_config(self, resolucion, audiorate,
        audiochannels, audiodepth, compresion):
        """Configura la calidad de grabación de audio y video."""
        
        self.stop()
        
        w, h = resolucion
        self.resolucion = "video/x-raw-yuv,width=%i,height=%i" % (w,h)
        self.audio = "audio/x-raw-int,rate=%i,channels=%i,depth=%i" % (audiorate, audiochannels, audiodepth)
        self.calidad_compresion = compresion
        
        self.set_pipeline()
        
    def on_sync_message(self, bus, message):
        """Captura mensajes en el bus."""
        
        if message.structure is None: return
    
    def on_message(self, bus, message):
        """Captura mensajes en el bus."""
        
        if message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "ERROR ON_MESSAGE: ", err, debug
            
            self.pipeline.set_state(gst.STATE_NULL)
            
    def grabar(self, location_path):
        """Comienza a Grabar."""
        
        self.new_handle(False)
        
        if self.pipeline:
            self.pipeline.set_state(gst.STATE_PAUSED)
            self.pipeline.set_state(gst.STATE_NULL)
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        self.file_path = os.path.join(location_path,"%s-%s.ogg" % (fecha, hora))
        
        self.set_pipeline()
        
        self.estado = "Grabando"
        self.pipeline.set_state(gst.STATE_PLAYING)
        
        self.new_handle(True)
        
    def stop(self, widget= None, event= None):
        """Detiene la grabación."""
        
        self.new_handle(False)
        
        if self.pipeline:
            self.pipeline.set_state(gst.STATE_PAUSED)
            self.pipeline.set_state(gst.STATE_NULL)
        
        self.estado = None
        
    def new_handle(self, reset):
        """Reinicia o mata el actualizador."""
        
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = None
            
        if reset:
            self.actualizador = gobject.timeout_add(300, self.handle)
            
    def handle(self):
        """Envía información periódicamente."""
        
        if os.path.exists(self.file_path):
            tamanio = int(os.path.getsize(self.file_path)/1024)
            info = "Grabando: %s - %s Kb Almacenados." % (str(self.file_path), str(tamanio))
            
            if self.info != info:
                self.info = info
                self.emit('update', self.info)
                print self.info
                
        return True
    
if __name__=="__main__":
    
    #default_location = os.path.dirname(__file__)
    grabador = DesktopGrab()
    grabador.grabar('/home/flavio')
    gtk.main()'''
    
'''
Notas:
    
    # Bucle Video:
    # gst-launch-0.10 ximagesrc ! ffmpegcolorspace ! autovideosink
    
    # Audio y Video:
    # autoaudiosrc ! queue ! audioconvert ! queue vorbisenc ! queue ! oggmux ! queue ! filesink
    # gst-launch-0.10 ximagesrc ! ffmpegcolorspace ! theoraenc ! queue ! oggmux ! queue ! filesink location=prueba.ogg
'''
