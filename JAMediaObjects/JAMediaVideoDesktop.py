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
    
''' xo 1.75
#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

Model:
    gst-launch-0.10 ximagesrc startx=0 endx=1200 starty=0 endy=900 ! \
    ffmpegcolorspace ! \
    videoscale ! \
    video/x-raw-yuv,width=320,height=240 ! \
    theoraenc ! \
    queue max-size-buffers=10000 max-size-bytes=0 max-size-time=0 ! \
    mux. oggmux name=mux \
    alsasrc ! \
    audio/x-raw-int,width=16,depth=16,rate=8000,channels=1 ! \
    audioconvert ! \
    vorbisenc ! \
    queue max-size-buffers=10000 max-size-bytes=0 max-size-time=0 ! \
    mux. mux. ! \
    filesink location=file.ogg

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
    """Simple Grabador de Escritorio, Versión 2.0
    
    def set_audio_enabled(self, valor)
        Habilita/deshabilita el audio en la grabación.
        
    set_video_quality(self, resolucion)
        Configura calidad de video final.
        
    def record(self, location_path)
        Graba.
        
    def stop(self)
        Detiene la grabación."""

    __gsignals__ = {
        "update":(gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}
    
    def __init__(self):
        
        gtk.Widget.__init__(self)
        
        self.resolution = "video/x-raw-yuv,width=640,height=480" # 800x600 640x480 320x240
        
        self.pipeline = None
        self.update = None
        self.file_path = None
        self.enabled_sound = True
        self.info = None
        
        # Video
        self.ximagesrc = None
        self.ffmpegcolorspace = None
        self.videoscale = None
        self.video_filter = None
        self.theoraenc = None
        self.queue_video = None
        
        # Sound
        self.alsasrc = None
        self.sound_filter = None
        self.audioconvert = None
        self.vorbisenc = None
        self.queue_sound = None
        self.oggmux = None
        self.file = None
        self.bus = None
        
        self.x = 0
        self.y = 0
        self.width = int(gtk.gdk.screen_width())
        self.height = int(gtk.gdk.screen_height())
        
    def set_pipeline(self):
        """Crea el pipe para grabar desde x y autoaudio."""
        
        if self.pipeline:
            del(self.pipeline)
            self.pipeline = None
            
        self.pipeline = gst.Pipeline("player")
        
        # Video
        self.ximagesrc = gst.element_factory_make('ximagesrc', "x11")
        self.ximagesrc.set_property('startx', self.x)
        self.ximagesrc.set_property('endx', self.width)
        self.ximagesrc.set_property('starty', self.y)
        self.ximagesrc.set_property('endy', self.height)
        self.ffmpegcolorspace = gst.element_factory_make('ffmpegcolorspace', "ffmpegcolorspace")
        self.videoscale = gst.element_factory_make("videoscale", "videoscale")
        self.video_filter = gst.element_factory_make("capsfilter", "video_filter")
        video_caps = gst.Caps(self.resolution)
        self.video_filter.set_property("caps", video_caps)
        self.theoraenc = gst.element_factory_make('theoraenc', 'theoraenc')
        self.queue_video = gst.element_factory_make('queue', "queue_video")
        self.queue_video.set_property('max-size-buffers', 10000)
        self.queue_video.set_property('max-size-bytes', 0)
        self.queue_video.set_property('max-size-time', 0)
        
        # Sound
        self.alsasrc = gst.element_factory_make('alsasrc', "alsasrc")
        sound_caps = gst.Caps("audio/x-raw-int,width=16,depth=16,rate=8000,channels=1")
        self.sound_filter = gst.element_factory_make("capsfilter", "sound_filter")
        self.sound_filter.set_property("caps", sound_caps)
        self.audioconvert = gst.element_factory_make('audioconvert', "audioconvert")
        self.vorbisenc = gst.element_factory_make('vorbisenc', "vorbisenc")
        self.queue_sound = gst.element_factory_make('queue', "queue_sound")
        self.queue_sound.set_property('max-size-buffers', 10000)
        self.queue_sound.set_property('max-size-bytes', 0)
        self.queue_sound.set_property('max-size-time', 0)
        
        self.oggmux = gst.element_factory_make('oggmux', "oggmux")
        
        self.file = gst.element_factory_make('filesink', "file")
        self.file.set_property("location", self.file_path)
        
        if self.enabled_sound:
            self.add_todos()
            self.link_todos()
        else:
            self.add_solo_video()
            self.link_solo_video()
            
        self.bus = self.pipeline.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.add_signal_watch()
        self.bus.connect("sync-message::element", self.on_sync_message)
        self.bus.connect("message", self.on_message)
    
    def link_solo_video(self):
        """Linkea solo los elementos de video y archivo, no de audio."""
        
        gst.element_link_many(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_filter,
            self.theoraenc,
            self.queue_video,
            self.oggmux,
            self.file)
            
    def link_todos(self):
        """Linkea todos los elementos del pipe, de audio, video y archivo."""
        
        gst.element_link_many(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_filter,
            self.theoraenc,
            self.queue_video,
            self.oggmux)
            
        gst.element_link_many(
            self.alsasrc,
            self.sound_filter,
            self.audioconvert,
            self.vorbisenc,
            self.queue_sound,
            self.oggmux)
            
        gst.element_link_many(
            self.oggmux,
            self.file)
            
    def add_todos(self):
        """Agrega al pipe todos los elementos, de audio y video."""
        
        self.pipeline.add(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_filter,
            self.theoraenc,
            self.queue_video,
            self.alsasrc,
            self.sound_filter,
            self.audioconvert,
            self.vorbisenc,
            self.queue_sound,
            self.oggmux,
            self.file)
            
    def add_solo_video(self):
        """Agrega al pipe solo los elementos de video pero no de adio."""
        
        self.pipeline.add(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_filter,
            self.theoraenc,
            self.queue_video,
            self.oggmux,
            self.file)
            
    def set_audio_enabled(self, valor):
        """Habilita y desabilita el audio en la grabación."""
        
        self.stop()
        self.enabled_sound = valor
        
    def set_video_quality(self, resolution):
        """Configura la calidad de grabación de video."""
        
        self.stop()
        
        w, h = resolution
        self.resolution = "video/x-raw-yuv,width=%i,height=%i" % (w,h)
        
    def on_sync_message(self, bus, message):
        """Captura mensajes en el bus."""
        
        if message.structure is None: return
    
    def on_message(self, bus, message):
        """Captura mensajes en el bus."""
        
        if message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "ERROR ON_MESSAGE: ", err, debug
            self.pipeline.set_state(gst.STATE_NULL)
            
    def record(self, location_path):
        """Comienza a Grabar."""
        
        self.new_handle(False)
        
        if self.pipeline:
            self.pipeline.set_state(gst.STATE_PAUSED)
            self.pipeline.set_state(gst.STATE_NULL)
        
        dat = datetime.date.today()
        tim = time.strftime("%H-%M-%S")
        self.file_path = os.path.join(location_path,"%s-%s.ogg" % (dat, tim))
        
        self.set_pipeline()
        
        self.pipeline.set_state(gst.STATE_PLAYING)
        
        self.new_handle(True)
        
    def stop(self):
        """Detiene la grabación."""
        
        self.new_handle(False)
        
        if self.pipeline:
            self.pipeline.set_state(gst.STATE_PAUSED)
            self.pipeline.set_state(gst.STATE_NULL)
        
        self.estado = None
        
    def new_handle(self, reset):
        """Reinicia o mata el actualizador."""
        
        if self.update:
            gobject.source_remove(self.update)
            self.update = None
            
        if reset:
            self.update = gobject.timeout_add(1000, self.handle)
            
    def handle(self):
        """Envía información periódicamente."""
        
        if os.path.exists(self.file_path):
            tamanio = int(os.path.getsize(self.file_path)/1024)
            info = "Record: %s - %s Kb." % (str(self.file_path), str(tamanio))
            
            if self.info != info:
                self.info = info
                self.emit('update', self.info)
                print self.info
                
        return True

if __name__=="__main__":
    
    #default_location = os.path.dirname(__file__)
    grabador = DesktopGrab()
    grabador.set_audio_enabled(True)
    if os.path.exists('/home/flavio'):
        path = '/home/flavio'
    else:
        path = '/home/olpc'
    grabador.record(path)
    gtk.main()'''
    
''' en mi notebook
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaDesktopGrab.py por: Flavio Danesse
#   fdanesse@gmail.com - CeibalJAM! - Uruguay

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

class JAMediaDesktopGrab(gtk.Widget):
    """Simple Grabador de Escritorio, Versión 1.0
    
    def set_audio_enabled(self, valor)
        Habilita/deshabilita el audio en la grabación.
        
    set_config_video(self, resolucion, compresion)
        Configura compresión y resolución de video final.
        
    def grabar(self, location_path)
        Graba.
        
    def stop(self)
        Detiene la grabación."""

    __gsignals__ = {
        "update":(gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}
    
    def __init__(self):
        
        gtk.Widget.__init__(self)
        
        self.pipeline = None
        self.bus = None
        self.info = None
        self.resolucion = "video/x-raw-yuv,width=800,height=600" # 800x600 no menor a 640x480
        self.audio_enabled = True
        self.actualizador = None
        self.file_path = None
        
        self.ximagesrc =  None
        self.ffmpegcolorspace = None
        self.videoscale = None
        self.video_capsfilter = None
        self.theoraenc = None
        self.gconfaudiosrc = None
        self.audiorate = None
        self.audio_capsfilter = None
        self.audioconvert = None
        self.vorbisenc = None
        self.oggmux = None
        self.filesink = None
        
        self.x = 0
        self.y = 0
        self.width = int(gtk.gdk.screen_width())
        self.height = int(gtk.gdk.screen_height())
        
    def set_pipeline(self):
        """Crea el pipe para grabar desde x y autoaudio."""
        
        if self.pipeline:
            del(self.pipeline)
            self.pipeline = None
            
        self.pipeline = gst.Pipeline("player")
        
        # Fuente de Video
        self.ximagesrc = gst.element_factory_make('ximagesrc', "ximagesrc")
        self.ximagesrc.set_property('startx', self.x)
        self.ximagesrc.set_property('endx', self.width)
        self.ximagesrc.set_property('starty', self.y)
        self.ximagesrc.set_property('endy', self.height)
        
        self.ffmpegcolorspace = gst.element_factory_make("ffmpegcolorspace", "ffmpegcolorspace")
        
        self.videoscale = gst.element_factory_make("videoscale", "videoscale")
        self.video_capsfilter = gst.element_factory_make("capsfilter", "video_capsfilter")
        scalecaps = gst.Caps(self.resolucion)
        self.video_capsfilter.set_property("caps", scalecaps)
        
        self.theoraenc = gst.element_factory_make('theoraenc', 'theoraenc')
        self.theoraenc.set_property("bitrate", 1024) # kbps compresion + resolucion = calidad
        self.theoraenc.set_property('keyframe-freq', 15)
        self.theoraenc.set_property('cap-overflow', False)
        self.theoraenc.set_property('speed-level', 0)
        self.theoraenc.set_property('cap-underflow', True)
        self.theoraenc.set_property('vp3-compatible', True)
        
        # Fuente de Audio
        self.gconfaudiosrc = gst.element_factory_make('gconfaudiosrc', "gconfaudiosrc")
        self.gconfaudiosrc.set_property("async-handling", True)
        
        self.audiorate = gst.element_factory_make("audiorate", "audiorate")
        self.audiorate.set_property('silent', True)
        self.audiorate.set_property('skip-to-first', True)
        self.audiorate.set_property('tolerance', 1000)
        
        audio_rate = gst.Caps("audio/x-raw-int,endianness=1234,rate=8000,channels=2,width=8,depth=8,signed=False")
        self.audio_capsfilter = gst.element_factory_make("capsfilter", "audio_capsfilter")
        self.audio_capsfilter.set_property("caps", audio_rate)
        
        self.audioconvert = gst.element_factory_make('audioconvert', "audioconvert")
        self.audioconvert.set_property('dithering', 1)
        self.audioconvert.set_property('qos', True)
        
        self.vorbisenc = gst.element_factory_make('vorbisenc', "vorbisenc")
        
        self.oggmux = gst.element_factory_make('oggmux', "oggmux")
        
        self.filesink = gst.element_factory_make('filesink', "filesink")
        self.filesink.set_property("location", self.file_path)
        
        if self.audio_enabled:
            self.add_todos()
            self.link_todos()
        else:
            self.add_solo_video()
            self.link_solo_video()
            
        self.bus = self.pipeline.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.add_signal_watch()
        self.bus.connect("sync-message::element", self.on_sync_message)
        self.bus.connect("message", self.on_message)
    
    def link_solo_video(self):
        """Linkea solo los elementos de video y filesink, no de audio."""
        
        gst.element_link_many(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_capsfilter,
            self.theoraenc,
            #self.hilovideomuxor,
            #self.hiloarchivo,
            self.filesink
            )
            
    def link_todos(self):
        """Linkea todos los elementos del pipe, de audio, video y archivo."""
        
        gst.element_link_many(
            self.gconfaudiosrc,
            self.audiorate,
            self.audio_capsfilter,
            self.audioconvert,
            self.vorbisenc,
            #self.hiloaudiomuxor,
            self.oggmux
            )
            
        gst.element_link_many(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_capsfilter,
            self.theoraenc,
            self.oggmux
            )
            
        gst.element_link_many(
            self.oggmux,
            self.filesink
            )
            
    def add_todos(self):
        """Agrega al pipe todos los elementos, de audio y video."""
        
        self.pipeline.add(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_capsfilter,
            self.theoraenc,
            
            self.gconfaudiosrc,
            self.audiorate,
            self.audio_capsfilter,
            self.audioconvert,
            self.vorbisenc,
            #self.hiloaudiomuxor,
            
            self.oggmux,
            self.filesink
            )
            
    def add_solo_video(self):
        """Agrega al pipe solo los elementos de video pero no de adio."""
        
        self.pipeline.add(
            self.ximagesrc,
            self.ffmpegcolorspace,
            self.videoscale,
            self.video_capsfilter,
            self.hiloencodearvideo,
            self.theoraenc,
            #self.hilovideomuxor,
            self.oggmux,
            #self.hiloarchivo,
            self.filesink
            )
            
    def set_audio_enabled(self, valor):
        """Habilita y desabilita el audio en la grabación."""
        
        self.stop()
        self.audio_enabled = valor
        
    def set_config_video(self, resolucion):
        """Configura la calidad de grabación de video."""
        
        self.stop()
        w, h = resolucion
        self.resolucion = "video/x-raw-yuv,width=%i,height=%i" % (w,h)
        
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
        
        self.pipeline.set_state(gst.STATE_PLAYING)
        
        self.new_handle(True)
        
    def stop(self):
        """Detiene la grabación."""
        
        self.new_handle(False)
        
        if self.pipeline:
            self.pipeline.set_state(gst.STATE_PAUSED)
            self.pipeline.set_state(gst.STATE_NULL)
        
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
    grabador = JAMediaDesktopGrab()
    grabador.set_audio_enabled(True)
    if os.path.exists('/home/flavio'):
        path = '/home/flavio'
    else:
        path = '/home/olpc'
    grabador.grabar(path)
    gtk.main()'''
    
    
