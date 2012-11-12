#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWebCam.py por:
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

# Depends: python-gi,
#    gir1.2-gstreamer-1.0,
#    gir1.2-gst-plugins-base-1.0,
#    gstreamer1.0-plugins-good,
#    gstreamer1.0-plugins-ugly,
#    gstreamer1.0-plugins-bad,
#    gstreamer1.0-libav

# brightness    Integer. Range: -2147483648 - 2147483647 Default: 0
# contrast      Integer. Range: -2147483648 - 2147483647 Default: 0
# saturation    Integer. Range: -2147483648 - 2147483647 Default: 0
# hue           Integer. Range: -2147483648 - 2147483647 Default: 0

# http://wiki.oz9aec.net/index.php/Gstreamer_cheat_sheet
# http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-libs/html/index.html
# http://fossies.org/unix/privat/gst-plugins-base-0.11.93.tar.gz:a/gst-plugins-base-0.11.93/docs/plugins/html/index.html

import os
import time
import datetime

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo

import JAMediaGlobales as G
   
GObject.threads_init()
Gst.init([])

CONFIG_DEFAULT = {
    'device': "/dev/video0",
    'saturacion': 5,
    'contraste': 6,
    'brillo': 8,
    'hue': 0,
    }

class JAMediaWebCam(GObject.GObject):
    """Interfaz para Webcam, en base a Gstreamer 1.0."""
    
    def __init__(self, ventana_id):
        """ Recibe el id de un DrawingArea
        para mostrar el video. """
        
        GObject.GObject.__init__(self)
        
        self.name = "JAMediaWebCam"
        self.ventana_id = ventana_id
        self.pipeline = None
        self.estado = None
        self.patharchivo = None
        
        # Camara Base
        self.camara = None
        self.multi = None
        self.hilovideoapantalla = None
        self.pantalla = None
        
        # Video
        self.hiloencodearvideo = None
        self.videoconvert = None
        self.theoraenc = None
        self.hilovideomuxor = None
        self.oggmux = None
        
        # Audio
        self.autoaudiosrc = None
        self.audioconvert = None
        self.vorbisenc = None
        self.hiloaudiomuxor = None
        
        # Solo audio
        self.mp3enc = None
        
        # Archivo
        self.archivo = None
        
        # Imagenes
        self.pngenc = None
        
        self.elementos_base = []
        self.elementos_grabacion = []
        self.elementos_grabacion_solo_audio = []
        self.elementos_fotografia = []
        
        self.config = {}
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        
        self.setup_init()
        
    def setup_init(self):
        """Crea todos los elementos a utilizar en el pipe.
        Linkea solo desde fuente de video a la pantalla."""
        
        self.pipeline = Gst.Pipeline()
        
        # Fuente de Video
        self.camara = Gst.ElementFactory.make('v4l2src', "webcam")
        
        # Enlace doble desde fuente de video.
        self.multi = Gst.ElementFactory.make('tee', "tee")
        
        # Salida de Video 1 (a la pantalla)
        self.hilovideoapantalla = Gst.ElementFactory.make('queue', "hilovideoapantalla")
        
        self.pantalla = Gst.ElementFactory.make('xvimagesink', "pantalla") # autovideosink o xvimagesink
        
        # Salida de Video 2 (a theoraenc)
        self.hiloencodearvideo = Gst.ElementFactory.make('queue', "hiloencodearvideo")
        self.hiloencodearvideo.set_property('max-size-buffers', 1000)
        self.hiloencodearvideo.set_property('max-size-bytes', 0)
        self.hiloencodearvideo.set_property('max-size-time', 0)
        
        self.videoconvert = Gst.ElementFactory.make('videoconvert', "videoconvert")
        self.theoraenc = Gst.ElementFactory.make('theoraenc', 'theoraenc')
        self.theoraenc.set_property("bitrate", 1024) # kbps compresion + resolucion = calidad
        self.theoraenc.set_property('keyframe-freq', 15)
        self.theoraenc.set_property('cap-overflow', False)
        self.theoraenc.set_property('speed-level', 0)
        self.theoraenc.set_property('cap-underflow', True)
        self.theoraenc.set_property('vp3-compatible', True)
        
        # Para fotografiar
        self.pngenc = Gst.ElementFactory.make('pngenc', "pngenc")
        
        # Fuente de Audio a vorbisenc.
        self.autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc")
        
        self.audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        self.vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")
        
        # Solo audio
        self.mp3enc = Gst.ElementFactory.make('lamemp3enc', "lamemp3enc")
        
        # Muxor - Unión audio y video en oggmux.
        self.hilovideomuxor = Gst.ElementFactory.make('queue', "hilovideomuxor")
        self.hilovideomuxor.set_property('max-size-buffers', 12000)
        self.hilovideomuxor.set_property('max-size-bytes', 0)
        self.hilovideomuxor.set_property('max-size-time', 0)
        
        self.hiloaudiomuxor = Gst.ElementFactory.make('queue', "hiloaudiomuxor")
        self.hiloaudiomuxor.set_property('max-size-buffers', 5000)
        self.hiloaudiomuxor.set_property('max-size-bytes', 0)
        self.hiloaudiomuxor.set_property('max-size-time', 0)
        
        self.oggmux = Gst.ElementFactory.make('oggmux', "oggmux")
        
        # Archivo - Salida de oggmux a un archivo.
        self.archivo = Gst.ElementFactory.make('filesink', "archivo")
        
        self.elementos_base = [
            self.camara,
            self.multi,
            self.hilovideoapantalla,
            self.pantalla]
            
        self.elementos_grabacion = [
            self.hiloencodearvideo,
            self.videoconvert,
            self.theoraenc,
            self.hilovideomuxor,
            self.oggmux,
            self.autoaudiosrc,
            self.audioconvert,
            self.vorbisenc,
            self.hiloaudiomuxor,
            self.archivo]
            
        self.elementos_grabacion_solo_audio = [
            self.autoaudiosrc,
            self.audioconvert,
            self.mp3enc,
            self.archivo]
            
        self.elementos_fotografia = [
            self.hiloencodearvideo,
            self.videoconvert,
            self.pngenc,
            self.archivo]
            
        self.set_camara()
        self.get_base_pipe()
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
    def set_camara(self, device = None):
        """Setea una cámara fuente de video."""
        
        if device != None:
            self.config['device'] = device
            self.camara.set_property("device", self.config['device'])
        
    def set_balance(self, brillo = None, contraste = None,
        saturacion = None, hue = None):
        """Seteos de balance en la fuente de video."""
        
        # Rangos: int. -2147483648 2147483647
        #valor = 2147483647 - (-2147483648)
        valor = 100 -(-100)
        if saturacion != None:
            self.config['saturacion'] = int((valor * int(saturacion) / 100) - valor/2)
            self.camara.set_property('saturation', self.config['saturacion'])
            
        if contraste != None:
            self.config['contraste'] = int((valor * int(contraste) / 100) - valor/2)
            self.camara.set_property('contrast', self.config['contraste'])
            
        if brillo != None:
            self.config['brillo'] = int( (valor * int(brillo) / 100) - (valor/2))
            self.camara.set_property('brightness', self.config['brillo'])
            
        if hue != None:
            self.config['hue'] = int( (valor * int(hue) / 100) - (valor/2) )
            self.camara.set_property('hue', self.config['hue'])
        
    def get_balance(self):
        """Retorna los valores actuales de balance en % float."""
        
        #valor = 2147483647 - (-2147483648) # 4294967295
        config = {}
        valor = 100 -(-100)
        config['brillo'] = float( (self.camara.get_property('brightness') + (valor/2)) * 100 / valor)
        config['contraste'] = float( (self.camara.get_property('contrast') + (valor/2)) * 100 / valor)
        config['saturacion'] = float( (self.camara.get_property('saturation') + (valor/2)) * 100 / valor)
        config['hue'] = float( (self.camara.get_property('hue') + (valor/2)) * 100 / valor)
        
        return config
    
    def reset(self):
        """Re establece el pipe al estado
        original (sólo camara a pantalla)."""
        
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        
        self.camara.set_property('saturation', self.config['saturacion'])
        self.camara.set_property('contrast', self.config['contraste'])
        self.camara.set_property('brightness', self.config['brillo'])
        self.camara.set_property('hue', self.config['hue'])
        
        self.stop()
        self.get_base_pipe()
        self.play()
        
    def get_base_pipe(self):
        """Linkea los elementos base."""
        
        map(self.agregar, self.elementos_base)
        
        self.camara.link(self.multi)
        self.multi.link(self.hilovideoapantalla)
        self.hilovideoapantalla.link(self.pantalla)
        
    def get_foto_pipe(self):
        """linkea elementos fotograficos."""
        
        map(self.agregar, self.elementos_fotografia)
        
        self.multi.link(self.hiloencodearvideo)
        self.hiloencodearvideo.link(self.videoconvert)
        self.videoconvert.link(self.pngenc)
        
        self.pngenc.link(self.archivo)
        
    def get_audio_video_pipe(self):
        """Linkea elementos de filmación."""
        
        map(self.agregar, self.elementos_grabacion)
        
        self.multi.link(self.hiloencodearvideo)
        self.hiloencodearvideo.link(self.videoconvert)
        self.videoconvert.link(self.theoraenc)
        self.theoraenc.link(self.hilovideomuxor)
        self.hilovideomuxor.link(self.oggmux)
        
        self.autoaudiosrc.link(self.audioconvert)
        self.audioconvert.link(self.vorbisenc)
        self.vorbisenc.link(self.hiloaudiomuxor)
        self.hiloaudiomuxor.link(self.oggmux)
        
        self.oggmux.link(self.archivo)
        
    def get_solo_audio_pipe(self):
        """Linkea elementos para grabar solamente audio."""
        
        map(self.agregar, self.elementos_grabacion_solo_audio)
        
        self.autoaudiosrc.link(self.audioconvert)
        self.audioconvert.link(self.mp3enc)
        
        self.mp3enc.link(self.archivo)
        
    def pause(self, widget = None, event = None):
        
        self.pipeline.set_state(Gst.State.PAUSED)
        self.estado = "paused"
        
    def play(self, widget = None, event = None):
        
        self.pipeline.set_state(Gst.State.PLAYING)
        self.estado = "playing"
        
    def stop(self, widget= None, event= None):
        """Detiene y limpia el pipe."""
        
        self.pipeline.set_state(Gst.State.PAUSED)
        self.pipeline.set_state(Gst.State.NULL)
        
        try:
            if os.path.exists(self.patharchivo):
                os.chmod(self.patharchivo, 0755)
                
        except:
            pass
        
        map(self.remover, self.pipeline.children)
        
        self.estado = "stoped"
        
    def remover(self, objeto):
        """Para remover objetos en el pipe."""
        
        if objeto in self.pipeline.children: self.pipeline.remove(objeto)
        
    def agregar(self, objeto):
        """Para agregar objetos al pipe."""
        
        if not objeto in self.pipeline.children: self.pipeline.add(objeto)
        
    def grabar(self, widget= None, event= None):
        """ Graba Audio y Video desde la webcam. """
        
        self.stop()
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(G.VIDEO_JAMEDIA_VIDEO,"%s-%s.ogg" % (fecha, hora))
        self.patharchivo = archivo
        self.archivo.set_property("location", archivo)
        
        self.get_base_pipe()
        self.get_audio_video_pipe()
        
        self.play()
        self.estado = "GrabandoAudioVideoWebCam"
        
    def grabarsoloaudio(self, widget = None, event = None):
        """Grabar solo audio."""
        
        self.stop()
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(G.AUDIO_JAMEDIA_VIDEO,"%s-%s.mp3" % (fecha, hora))
        self.patharchivo = archivo
        self.archivo.set_property("location", archivo)
        
        self.get_base_pipe()
        self.get_solo_audio_pipe()
        
        self.play()
        self.estado = "GrabandoAudioPulsersc"
        
    def fotografiar(self, widget = None, event = None):
        """Toma una fotografia."""
        
        self.stop()
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(G.IMAGENES_JAMEDIA_VIDEO,"%s-%s.png" % (fecha, hora))
        self.patharchivo = archivo
        self.archivo.set_property("location", archivo)
        
        self.get_base_pipe()
        self.get_foto_pipe()
        
        self.play()
        self.estado = "FotografiandoWebCam"
        
    def sync_message(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
        try:
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return
            
        except:
            pass
    
    def on_mensaje(self, bus, mensaje):
        """Captura los mensajes en el bus del pipe Gst."""
        
        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "***", 'on_mensaje'
            print err, debug
            self.pipeline.set_state(Gst.State.READY)
            