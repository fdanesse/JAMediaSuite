#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaBins.py por:
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

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo

GObject.threads_init()
Gst.init([])

class JAMedia_Efecto_bin(Gst.Bin):
    """Bin para efecto de video individual."""
    
    def __init__(self, efecto):
        
        Gst.Bin.__init__(self)
        
        self.set_name(efecto)
    
        videoconvert = Gst.ElementFactory.make("videoconvert",
            "videoconvert_%s" % (efecto))
            
        efecto = Gst.ElementFactory.make(efecto, efecto)

        self.add(videoconvert)
        self.add(efecto)

        videoconvert.link(efecto)
    
        self.add_pad(Gst.GhostPad.new("sink", videoconvert.get_static_pad ("sink")))
        self.add_pad(Gst.GhostPad.new("src", efecto.get_static_pad("src")))
        
class JAMedia_Camara_bin(Gst.Bin):
    """Bin para cámara y sus configuraciones
    particulares."""
    
    def __init__(self):
        
        Gst.Bin.__init__(self)
        
        self.set_name('jamedia_camara_bin')
        
        self.camara = Gst.ElementFactory.make("v4l2src", "v4l2src")
        
        caps = Gst.Caps.from_string('video/x-raw,framerate=10/1')
        camerafilter = Gst.ElementFactory.make("capsfilter", "camera_filter")
        camerafilter.set_property("caps", caps)
        
        self.add(self.camara)
        self.add(camerafilter)
        
        self.camara.link(camerafilter)
        
        self.add_pad(Gst.GhostPad.new("src", camerafilter.get_static_pad("src")))
        
class Theoraenc_bin(Gst.Bin):
    """Bin para elementos codificadores
    de video a theoraenc."""
    
    def __init__(self):
        
        Gst.Bin.__init__(self)
        
        self.set_name('video_theoraenc_bin')
        
        que_encode_video = Gst.ElementFactory.make("queue", "que_encode_video")
        que_encode_video.set_property('max-size-buffers', 1000)
        que_encode_video.set_property('max-size-bytes', 0)
        que_encode_video.set_property('max-size-time', 0)
        
        theoraenc = Gst.ElementFactory.make('theoraenc', 'theoraenc')
        theoraenc.set_property("bitrate", 1024) # kbps compresion + resolucion = calidad
        theoraenc.set_property('keyframe-freq', 15)
        theoraenc.set_property('cap-overflow', False)
        theoraenc.set_property('speed-level', 0)
        theoraenc.set_property('cap-underflow', True)
        theoraenc.set_property('vp3-compatible', True)

        self.add(que_encode_video)
        self.add(theoraenc)

        que_encode_video.link(theoraenc)

        pad = que_encode_video.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))
        
        pad = theoraenc.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))
        
class Vorbisenc_bin(Gst.Bin):
    """Bin para elementos codificadores
    de audio a vorbisenc."""
    
    def __init__(self):
        
        Gst.Bin.__init__(self)
        
        self.set_name('audio_vorbisenc_bin')
        
        autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc")
        audiorate = Gst.ElementFactory.make('audiorate', "audiorate")
        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")
        
        self.add(autoaudiosrc)
        self.add(audiorate)
        self.add(audioconvert)
        self.add(vorbisenc)
        
        autoaudiosrc.link(audiorate)
        audiorate.link(audioconvert)
        audioconvert.link(vorbisenc)
        
        pad = vorbisenc.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))


class Foto_bin(Gst.Bin):
    """Bin para tomar fotografías."""
    
    def __init__(self):
        
        Gst.Bin.__init__(self)
        
        self.set_name('foto_bin')
        
        videoconvert = Gst.ElementFactory.make(
            "videoconvert", "videoconvert_gdkpixbuf")
        
        queue = Gst.ElementFactory.make("queue", "queue_foto")
        queue.set_property("leaky", 1)
        queue.set_property("max-size-buffers", 1)
        
        gdkpixbufsink = Gst.ElementFactory.make(
            "gdkpixbufsink", "gdkpixbufsink")
        
        #gdkpixbufsink.set_property('post-messages', False)
        
        self.add(queue)
        self.add(videoconvert)
        self.add(gdkpixbufsink)
        
        queue.link(videoconvert)
        videoconvert.link(gdkpixbufsink)
        
        pad = queue.get_static_pad ("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))
    
    
class Efectos_Video_bin(Gst.Bin):
    """Bin para agregar efectos de video."""
    
    def __init__(self, efectos, config_efectos):
        
        Gst.Bin.__init__(self)
        
        self.set_name('efectos_bin')
        
        self.efectos = efectos
        self.config_efectos = config_efectos
        
        queue = Gst.ElementFactory.make('queue', "queue")
        #queue.set_property('max-size-buffers', 1000)
        #queue.set_property('max-size-bytes', 0)
        #queue.set_property('max-size-time', 0)
        
        videoconvert = Gst.ElementFactory.make(
            'videoconvert',
            "videoconvert_efectos")
        
        self.add(queue)
        
        efectos = []
        for nombre in self.efectos:
            # Crea el efecto
            efecto = JAMedia_Efecto_bin(nombre)
            if efecto and efecto != None:
                efectos.append(efecto)
        
        if efectos:
            for efecto in efectos:
                # Agrega el efecto
                self.add(efecto)
                
            # queue a primer efecto
            queue.link(efectos[0])
            
            for efecto in efectos:
                index = efectos.index(efecto)
                if len(efectos) > index + 1:
                    # Linkea los efectos entre si
                    efecto.link(efectos[efectos.index(efecto) + 1])
                    
            self.add(videoconvert)
            # linkea el ultimo efecto a videoconvert
            efectos[-1].link(videoconvert)
            
        else:
            self.add(videoconvert)
            queue.link(videoconvert)
        
        # Mantener la configuración de cada efecto.
        for efecto in self.config_efectos.keys():
            for property in self.config_efectos[efecto].keys():
                bin_efecto = self.get_by_name(efecto)
                elemento = bin_efecto.get_by_name(efecto)
                elemento.set_property(property, self.config_efectos[efecto][property])
        
        self.add_pad(Gst.GhostPad.new("sink", queue.get_static_pad ("sink")))
        self.add_pad(Gst.GhostPad.new("src", videoconvert.get_static_pad("src")))
        
class Audio_Visualizador_bin(Gst.Bin):
    """Bin visualizador de audio."""
    
    def __init__(self, visualizador):
        
        Gst.Bin.__init__(self)
        
        self.set_name('audio_visualizador_bin')
        
        self.visualizador = visualizador
        
        queue = Gst.ElementFactory.make("queue", "queue")
        
        efecto = Gst.ElementFactory.make(
            self.visualizador,
            self.visualizador)
            
        videoconvert = Gst.ElementFactory.make('videoconvert', "videoconvert")
        
        self.add(queue)
        self.add(efecto)
        self.add(videoconvert)

        queue.link(efecto)
        efecto.link(videoconvert)

        pad = queue.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))
        
        pad = videoconvert.get_static_pad("src")
        self.add_pad(Gst.GhostPad.new("src", pad))
        