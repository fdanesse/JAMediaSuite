#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaVideoEscritorio.py por:
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
from gi.repository import GLib
from gi.repository import Gst
from gi.repository import GstVideo

GObject.threads_init()
#Gdk.threads_init()
Gst.init([])

class JAMediaVideoEscritorio(GObject.GObject):
    """Simple Grabador de Escritorio, Versión 1.0"""
    
    __gsignals__ = {
    "update":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        GObject.GObject.__init__(self)
        
        self.name = "JAMediaVideoDesktop"
        
        self.pipeline = False
        self.bus = False
        self.info = False
        #self.resolucion = "video/x-raw-yuv,width=640,height=480" # 800x600 no menor a 640x480
        self.audio_enabled = True
        self.actualizador = False
        self.file_path = False
        
        self.ximagesrc =  False
        self.videoconvert = False
        self.videoscale = False
        self.video_capsfilter = False
        self.theoraenc = False
        self.gconfaudiosrc = False
        self.audiorate = False
        self.audio_capsfilter = False
        self.audioconvert = False
        self.vorbisenc = False
        self.hilovideomuxor = False
        self.hiloaudiomuxor = False
        self.oggmux = False
        self.filesink = False
        
        self.screen = GdkX11.X11Screen()
        
        self.x = 0
        self.y = 0
        self.width = int(self.screen.width())
        self.height = int(self.screen.height())
        
    def set_pipeline(self):
        """
        Crea el pipe para grabar desde x y autoaudio.
        """
        
        if self.pipeline:
            del(self.pipeline)
            
        self.pipeline = Gst.Pipeline()
        
        screen = GdkX11.X11Screen()
        width = int(screen.width())
        height = int(screen.height())
        
        # >>> Video
        print "Grabando un Escritorio de:", "%sx%s" % (width, height)
        
        ximagesrc = Gst.ElementFactory.make('ximagesrc', "ximagesrc")
        #self.ximagesrc.set_property("screen-num", self.screen.get_screen_number())
        #self.ximagesrc.set_property('use-damage', False)
        ximagesrc.set_property('startx', 0)
        ximagesrc.set_property('endx', 200)#ximagesrc.set_property('endx', width)
        ximagesrc.set_property('starty', 0)
        ximagesrc.set_property('endy', 100)#ximagesrc.set_property('endy', height)
        
        que_encode_video = Gst.ElementFactory.make("queue", "que_encode_video")
        '''
        que_encode_video.set_property('max-size-buffers', 1000)
        que_encode_video.set_property('max-size-bytes', 0)
        que_encode_video.set_property('max-size-time', 0)'''
        
        videoscale = Gst.ElementFactory.make('videoscale', 'videoscale')
        video_capsfilter = Gst.ElementFactory.make("capsfilter", "scalecaps")
        scalecaps = Gst.Caps()
        scalecaps.from_string("video/x-raw-yuv,width=640,height=480")
        video_capsfilter.set_property("caps", scalecaps)
        
        videoconvert = Gst.ElementFactory.make('videoconvert', 'videoconvert')
        
        theoraenc = Gst.ElementFactory.make('theoraenc', 'theoraenc')
        '''
        theoraenc.set_property("bitrate", 1024) # kbps compresion + resolucion = calidad
        theoraenc.set_property('keyframe-freq', 15)
        theoraenc.set_property('cap-overflow', False)
        theoraenc.set_property('speed-level', 0)
        theoraenc.set_property('cap-underflow', True)
        theoraenc.set_property('vp3-compatible', True)'''
        
        que_video_mux = Gst.ElementFactory.make('queue', "que_video_mux")
        '''
        que_video_mux.set_property('max-size-buffers', 12000)
        que_video_mux.set_property('max-size-bytes', 0)
        que_video_mux.set_property('max-size-time', 0)'''

        videobin = Gst.Bin()

        videobin.add(ximagesrc)
        videobin.add(videoconvert)
        videobin.add(videoscale)
        videobin.add(video_capsfilter)
        #videobin.add(que_encode_video)
        videobin.add(theoraenc)
        #videobin.add(que_video_mux)

        ximagesrc.link(videoconvert)
        videoconvert.link(videoscale)
        videoscale.link(video_capsfilter)
        #video_capsfilter.link(que_encode_video)
        video_capsfilter.link(theoraenc)
        #theoraenc.link(que_video_mux)

        #pad = que_encode_video.get_static_pad("sink")
        #videobin.add_pad(Gst.GhostPad.new("sink", pad))
        pad = theoraenc.get_static_pad("src")
        videobin.add_pad(Gst.GhostPad.new("src", pad))
        print "\tvideobin:"
        print videobin.children
    # <<< Video
        
    # >>> Audio
        autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc")
        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")
        
        que_audio_mux = Gst.ElementFactory.make('queue', "que_audio_mux")
        '''
        que_audio_mux.set_property('max-size-buffers', 5000)
        que_audio_mux.set_property('max-size-bytes', 0)
        que_audio_mux.set_property('max-size-time', 0)'''
        
        audiobin = Gst.Bin()
        
        audiobin.add(autoaudiosrc)
        audiobin.add(audioconvert)
        audiobin.add(vorbisenc)
        audiobin.add(que_audio_mux)
        
        autoaudiosrc.link(audioconvert)
        audioconvert.link(vorbisenc)
        vorbisenc.link(que_audio_mux)
        
        pad = que_audio_mux.get_static_pad("src")
        audiobin.add_pad(Gst.GhostPad.new("src", pad))
        print "\taudiobin:"
        print audiobin.children
    # <<< Audio
    
        oggmux = Gst.ElementFactory.make('oggmux', "oggmux")
        oggmux.set_property("skeleton", True)
        
        sink = Gst.ElementFactory.make('filesink', "archivo")
        sink.set_property("location", self.file_path)
        
        self.pipeline.add(videobin)
        self.pipeline.add(audiobin)
        self.pipeline.add(oggmux)
        self.pipeline.add(sink)
        
        audiobin.link(oggmux)
        videobin.link(oggmux)
        oggmux.link(sink)
        
        print "\tself.pipeline:"
        print self.pipeline.children
        
        '''
        fakesink = Gst.ElementFactory.make('fakesink', "fakesink")
        self.pipeline.add(videobin)
        self.pipeline.add(fakesink)
        videobin.link(fakesink)'''
        
        self.bus = self.pipeline.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.add_signal_watch()
        
        self.bus.connect("sync-message::element", self.on_sync_message)
        self.bus.connect("message", self.on_message)
        
    '''
    def set_audio_enabled(self, valor):
        """Habilita y desabilita el audio en la grabación."""
        
        self.stop()
        self.audio_enabled = valor
        
    def set_config_video(self, resolucion):
        """Configura la calidad de grabación de video."""
        
        self.stop()
        w, h = resolucion
        self.resolucion = "video/x-raw-yuv,width=%i,height=%i" % (w,h)'''
        
    def on_sync_message(self, bus, message):
        """
        Captura mensajes en el bus.
        """
        
        if message.get_structure() is None: return
    
        try:
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                #mensaje.src.set_window_handle(0)
                return
            
        except:
            pass
        
    def on_message(self, bus, message):
        """
        Captura mensajes en el bus.
        """
        
        if message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print "ERROR ON_MESSAGE: ", err, debug
            self.new_handle(False)
            
    def grabar(self, location_path):
        """
        Comienza a Grabar.
        """
        
        self.stop()
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        self.file_path = os.path.join(location_path,"%s-%s.ogg" % (fecha, hora))
        
        self.set_pipeline()
        
        self.play()
        
    def play(self, widget = False, event = False):
        
        self.pipeline.set_state(Gst.State.PLAYING)
        self.new_handle(True)
        
    def stop(self, widget = False, event = False):
        
        self.new_handle(False)
        
        if self.pipeline:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.pipeline.set_state(Gst.State.NULL)
        
        try:
            if os.path.exists(self.patharchivo):
                os.chmod(self.patharchivo, 0755)
                
        except:
            pass
        
    def new_handle(self, reset):
        """
        Reinicia o mata el actualizador.
        """
        
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
            
        if reset:
            self.actualizador = GLib.timeout_add(300, self.handle)
            
    def handle(self):
        """
        Envía información periódicamente.
        """
        
        if os.path.exists(self.file_path):
            tamanio = int(os.path.getsize(self.file_path)/1024)
            info = "Grabando: %s - %s Kb Almacenados." % (str(self.file_path), str(tamanio))
            
            if self.info != info:
                self.info = info
                self.emit('update', self.info)
                print self.info
                
        return True
    
if __name__=="__main__":
    
    grabador = JAMediaVideoEscritorio()
    #grabador.set_audio_enabled(False)
    
    if os.path.exists('/home/flavio'):
        path = '/home/flavio'
        
    else:
        path = '/home/olpc'
        
    grabador.grabar(path)
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
