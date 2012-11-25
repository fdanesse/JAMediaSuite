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

import os
import time
import datetime

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo
from gi.repository import GdkPixbuf

from JAMediaObjects import JAMediaGlobales as G

GObject.threads_init()
Gst.init([])

# Notas:
#   Actualmente, las imágenes y el video se toman
#   Al tamaño y framerate en el que sale de la cámara
#   640x480 en mi caso. Una fotografía ocupa 2.5 Mb
#   En xo, en video, probablemente lo mejor sea escalar a
#   320x240 o 160x120, en ambos casos la calidad no es mala.

CONFIG_DEFAULT = {
    'device': "/dev/video0",
    'saturacion': 5,
    'contraste': 6,
    'brillo': 8,
    'hue': 0,
    }

def get_efecto(efecto):
    """Crea un bin con efecto para agregar al pipe."""
    
    efectobin = Gst.Bin()# Gst.ElementFactory.make("bin")
    
    queue = Gst.ElementFactory.make("queue", "queue")
    queue.set_property('max-size-buffers', 1000)
    queue.set_property('max-size-bytes', 0)
    queue.set_property('max-size-time', 0)
    videoconvert1 = Gst.ElementFactory.make("videoconvert", "videoconvert1")
    efecto = Gst.ElementFactory.make(efecto, efecto)
    videoconvert2 = Gst.ElementFactory.make("videoconvert", "videoconvert2")
    
    efectobin.add(queue)
    efectobin.add(videoconvert1)
    efectobin.add(efecto)
    efectobin.add(videoconvert2)
    
    queue.link(videoconvert1)
    videoconvert1.link(efecto)
    efecto.link(videoconvert2)
    
    efectobin.add_pad(Gst.GhostPad.new("sink", queue.get_static_pad ("sink")))
    efectobin.add_pad(Gst.GhostPad.new("src", videoconvert2.get_static_pad("src")))
    
    return efectobin

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
        
        self.elementos_base = []
        
        self.config = {}
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        
        self.efectos = []
        
        self.setup_init()
        
    def setup_init(self):
        """Crea todos los elementos a utilizar en el pipe.
        Linkea solo desde fuente de video a la pantalla."""
        
        self.pipeline = Gst.Pipeline()
        
        # Fuente de Video
        self.camara = Gst.ElementFactory.make('v4l2src', "webcam")
        
        # Rotación
        self.videoflip = Gst.ElementFactory.make('videoflip', "videoflip")
        
        # Enlace doble desde fuente de video.
        self.multi = Gst.ElementFactory.make('tee', "tee")
        
        # Salida de Video 1 (a la pantalla)
        self.hilovideoapantalla = Gst.ElementFactory.make('queue', "hilovideoapantalla")
        self.hilovideoapantalla.set_property('max-size-buffers', 1000)
        self.hilovideoapantalla.set_property('max-size-bytes', 0)
        self.hilovideoapantalla.set_property('max-size-time', 0)
        
        self.pantalla = Gst.ElementFactory.make('xvimagesink', "pantalla") # autovideosink o xvimagesink
        
        self.elementos_base = [
            self.camara,
            self.videoflip,
            self.multi,
            self.hilovideoapantalla,
            self.pantalla]
        
        self.set_camara()
        self.get_base_pipe()
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
    def rotar(self, valor):
        """ Rota el Video. """
        
        self.pause()
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
        GObject.idle_add(self.play)
        
    def set_camara(self, device = None):
        """Setea una cámara fuente de video."""
        
        if device != None:
            self.config['device'] = device
            self.camara.set_property("device", self.config['device'])
        
    def set_balance(self, brillo = None, contraste = None,
        saturacion = None, hue = None):
        """Seteos de balance en la fuente de video.
        Recibe % en float."""
        
        # Rangos: int. -2147483648 2147483647
        min	= 2147483648
        #max = 2147483647
        total = 4294967295
        
        if saturacion != None:
            new_valor = int (total * int(saturacion) / 100)
            new_valor -= min
            self.config['saturacion'] = new_valor
            self.camara.set_property('saturation', self.config['saturacion'])
            
        if contraste != None:
            new_valor = int (total * int(contraste) / 100)
            new_valor -= min
            self.config['contraste'] = new_valor
            self.camara.set_property('contrast', self.config['contraste'])
            
        if brillo != None:
            new_valor = int (total * int(brillo) / 100)
            new_valor -= min
            self.config['brillo'] = new_valor
            self.camara.set_property('brightness', self.config['brillo'])
            
        if hue != None:
            new_valor = int (total * int(hue) / 100)
            new_valor -= min
            self.config['hue'] = new_valor
            self.camara.set_property('hue', self.config['hue'])
        
    def get_balance(self):
        """Retorna los valores actuales de balance en %."""
        
        # Rangos: int. -2147483648 2147483647
        min	= 2147483648
        #max = 2147483647
        total = 4294967295
        
        config = {}
        
        brillo = self.config['brillo'] + min
        config['brillo'] = brillo * 100 / total
        
        contraste = self.config['contraste'] + min
        config['contraste'] = contraste * 100 / total
        
        saturacion = self.config['saturacion'] + min
        config['saturacion'] = saturacion * 100 / total
        
        hue = self.config['hue'] + min
        config['hue'] = hue * 100 / total
        
        return config
    
    def reset(self):
        """Re establece el pipe al estado
        original (sólo camara a pantalla y sin efectos)."""
        
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        
        self.camara.set_property('saturation', self.config['saturacion'])
        self.camara.set_property('contrast', self.config['contraste'])
        self.camara.set_property('brightness', self.config['brillo'])
        self.camara.set_property('hue', self.config['hue'])
        
        self.videoflip.set_property('method', 0)
        
        self.stop()
        self.efectos = []
        self.get_base_pipe()
        self.play()
        
    def re_init(self):
        """Restablece el pipe al estado original,
        pero manteniendo los valores de balance y
        los efectos configurados."""
    
        self.stop()
        self.get_base_pipe()
        self.play()
        
    def get_base_pipe(self):
        """Linkea los elementos base."""
        
        map(self.agregar, self.elementos_base)
        
        efectos = list(self.efectos)
        ef = []
        for efecto in efectos:
            ef.append(get_efecto(efecto))
            
        if ef:
            map(self.agregar, ef)
            
        if ef:
            self.camara.link(ef[0])
            
            for efecto in ef:
                index = ef.index(efecto)
                if len(ef) > index + 1:
                    ef[index].link(ef[index + 1])
                
            ef[-1].link(self.videoflip)
            
        else:
            self.camara.link(self.videoflip)
            
        self.videoflip.link(self.multi)
        self.multi.link(self.hilovideoapantalla)
        self.hilovideoapantalla.link(self.pantalla)
    
    def get_foto_pipe(self):
        """linkea elementos fotograficos."""
        
        queue = Gst.ElementFactory.make("queue", "pbqueue")
        queue.set_property("leaky", True)
        queue.set_property("max-size-buffers", 1)

        videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        pngenc = Gst.ElementFactory.make("pngenc", "pngenc")
        
        sink = Gst.ElementFactory.make('filesink', "archivo")
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(G.IMAGENES_JAMEDIA_VIDEO,"%s-%s.png" % (fecha, hora))
        self.patharchivo = archivo
        sink.set_property("location", self.patharchivo)

        fotobin = Gst.Bin()

        fotobin.add(queue)
        fotobin.add(videoconvert)
        fotobin.add(pngenc)
        fotobin.add(sink)

        queue.link(videoconvert)
        videoconvert.link(pngenc)
        pngenc.link(sink)

        pad = queue.get_static_pad("sink")
        fotobin.add_pad(Gst.GhostPad.new("sink", pad))
        
        map(self.agregar, [fotobin])
        
        self.multi.link(fotobin)
    
    def get_audio_video_pipe(self):
        """Linkea elementos para grabar audio y video."""
        
        # >>> Video
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
        
        que_video_mux = Gst.ElementFactory.make('queue', "que_video_mux")
        que_video_mux.set_property('max-size-buffers', 12000)
        que_video_mux.set_property('max-size-bytes', 0)
        que_video_mux.set_property('max-size-time', 0)

        videobin = Gst.Bin()

        videobin.add(que_encode_video)
        videobin.add(theoraenc)
        videobin.add(que_video_mux)

        que_encode_video.link(theoraenc)
        theoraenc.link(que_video_mux)

        pad = que_encode_video.get_static_pad("sink")
        videobin.add_pad(Gst.GhostPad.new("sink", pad))
        pad = que_video_mux.get_static_pad("src")
        videobin.add_pad(Gst.GhostPad.new("src", pad))
        # <<< Video
        
        # >>> Audio
        autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc")
        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")
        
        que_audio_mux = Gst.ElementFactory.make('queue', "que_audio_mux")
        que_audio_mux.set_property('max-size-buffers', 5000)
        que_audio_mux.set_property('max-size-bytes', 0)
        que_audio_mux.set_property('max-size-time', 0)
        
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
        # <<< Audio
        
        oggmux = Gst.ElementFactory.make('oggmux', "oggmux")
        
        sink = Gst.ElementFactory.make('filesink', "archivo")
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(G.VIDEO_JAMEDIA_VIDEO,"%s-%s.ogg" % (fecha, hora))
        self.patharchivo = archivo
        sink.set_property("location", archivo)
        
        map(self.agregar, [videobin, audiobin, oggmux, sink])
        
        self.multi.link(videobin)
        videobin.link(oggmux)
        audiobin.link(oggmux)
        oggmux.link(sink)
        
    def agregar_efecto(self, nombre_efecto):
        """Agrega un efecto según nombre_efecto."""
        
        self.efectos.append(nombre_efecto)
        self.stop()
        self.get_base_pipe()
        self.play()
        
    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        """Configura un efecto en el pipe."""
        
        print nombre_efecto, propiedad, valor
        #self.efectos_dic[nombre_efecto].set_property(propiedad, valor)
        
    def quitar_efecto(self, indice_efecto):
        """Quita el efecto correspondiente al indice que recibe."""
        
        if type(indice_efecto) == int:
            self.efectos.remove(self.efectos[indice_efecto])
            
        elif type(indice_efecto) == str:
            
            for efecto in self.efectos:
                if efecto == indice_efecto:
                    self.efectos.remove(efecto)
                    break
                
        self.stop()
        self.get_base_pipe()
        self.play()
        
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
        
        self.get_base_pipe()
        self.get_audio_video_pipe()
        
        self.play()
        self.estado = "GrabandoAudioVideoWebCam"
        
    def fotografiar(self, widget = None, event = None):
        """Toma una fotografia."""
        
        self.stop()
        
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
            
def salir(widget):
    import sys
    sys.exit()
    
    
if __name__=="__main__":
    
    from gi.repository import Gtk
    
    ventana = Gtk.Window()
    ventana.set_resizable(True)
    ventana.set_default_size(640, 480)
    ventana.set_position(Gtk.WindowPosition.CENTER)
    
    pantalla = Gtk.DrawingArea()
    ventana.add(pantalla)
    
    ventana.show_all()
    ventana.realize()
    
    xid = pantalla.get_property('window').get_xid()
    jamediawebcam = JAMediaWebCam(xid)
    jamediawebcam.play()
    
    ventana.connect("destroy", salir)
    
    Gtk.main()
    