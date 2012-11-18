#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaAudio.py por:
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

import JAMediaGlobales as G
   
GObject.threads_init()
Gst.init([])
'''
CONFIG_DEFAULT = {
    'saturacion': 5,
    'contraste': 6,
    'brillo': 8,
    'hue': 0,
    }'''
'''
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
    
    return efectobin'''

class JAMediaAudio(GObject.GObject):
    """Interfaz para Audio, en base a Gstreamer 1.0."""
    
    def __init__(self, ventana_id):
        """ Recibe el id de un DrawingArea
        para mostrar el video. """
        
        GObject.GObject.__init__(self)
        
        self.name = "JAMediaAudio"
        self.ventana_id = ventana_id
        self.pipeline = None
        self.estado = None
        self.patharchivo = None
        
        self.autoaudiosrc = None
        self.multi = None
        self.hilovideoapantalla = None
        self.pantalla = None
        
        self.elementos_base = []
        '''
        self.config = {}
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']'''
        
        self.efecto_grafico_sobre_audio = 'wavescope'
        #wavescope, synaescope, spectrascope, spacescope, goom(problemas en calidad de grabacion de audio)
        self.efectos = []
        
        self.setup_init()
        
    def setup_init(self):
        """Crea todos los elementos a utilizar en el pipe.
        Linkea solo desde fuente de video a la pantalla."""
        
        self.pipeline = Gst.Pipeline()
        
        # Fuente de Video
        self.autoaudiosrc = Gst.ElementFactory.make('autoaudiosrc', "autoaudiosrc")
        
        # Enlace doble desde fuente.
        self.multi = Gst.ElementFactory.make('tee', "tee")
        
        self.videoflip = Gst.ElementFactory.make('videoflip', "videoflip")
        self.videobalance = Gst.ElementFactory.make('videobalance', "videobalance")
        self.gamma = Gst.ElementFactory.make('gamma', "gamma")
        
        self.hilovideoapantalla = Gst.ElementFactory.make('queue', "hilovideoapantalla")
        self.pantalla = Gst.ElementFactory.make('xvimagesink', "pantalla") # autovideosink o xvimagesink
        
        self.elementos_base = [
            self.autoaudiosrc,
            self.multi]
        
        self.get_base_pipe()
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
    
    def set_base_efecto(self, nombre):
        """Setea el efecto gráfico principal para el audio."""
        
        self.efecto_grafico_sobre_audio = nombre
        # Detener grabacion
        # reiniciar el pipe
        
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
        
    '''
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
        
        return config'''
    
    def reset(self):
        """Re establece el pipe al estado original (sin efectos)."""
        '''
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        
        self.camara.set_property('saturation', self.config['saturacion'])
        self.camara.set_property('contrast', self.config['contraste'])
        self.camara.set_property('brightness', self.config['brillo'])
        self.camara.set_property('hue', self.config['hue'])'''
        
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
        
        queue = Gst.ElementFactory.make("queue", "queue")
        efecto = Gst.ElementFactory.make(self.efecto_grafico_sobre_audio,
            self.efecto_grafico_sobre_audio)
        videoconvert = Gst.ElementFactory.make('videoconvert', "videoconvert")
        
        audiobin = Gst.Bin()
        
        audiobin.add(queue)
        audiobin.add(efecto)
        audiobin.add(videoconvert)

        queue.link(efecto)
        efecto.link(videoconvert)

        pad = queue.get_static_pad("sink")
        audiobin.add_pad(Gst.GhostPad.new("sink", pad))
        pad = videoconvert.get_static_pad("src")
        audiobin.add_pad(Gst.GhostPad.new("src", pad))
        
        map(self.agregar, [
            audiobin,
            # self.efectos,
            self.videobalance,
            self.videoflip,
            self.gamma,
            self.hilovideoapantalla,
            self.pantalla])
        
        self.autoaudiosrc.link(self.multi)
        self.multi.link(audiobin)
        audiobin.link(self.videobalance)
        self.videobalance.link(self.videoflip)
        self.videoflip.link(self.gamma)
        self.gamma.link(self.hilovideoapantalla)
        self.hilovideoapantalla.link(self.pantalla)
        
    def get_grabar_pipe(self):
        """Linkea elementos para grabar audio."""
        
        queue = Gst.ElementFactory.make("queue", "queue")
        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        vorbisenc = Gst.ElementFactory.make('vorbisenc', "vorbisenc")
        
        que_audio_mux = Gst.ElementFactory.make('queue', "que_audio_mux")
        que_audio_mux.set_property('max-size-buffers', 5000)
        que_audio_mux.set_property('max-size-bytes', 0)
        que_audio_mux.set_property('max-size-time', 0)
        
        oggmux = Gst.ElementFactory.make('oggmux', "oggmux")
        sink = Gst.ElementFactory.make('filesink', "archivo")
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(G.AUDIO_JAMEDIA_VIDEO,"%s-%s.ogg" % (fecha, hora))
        self.patharchivo = archivo
        sink.set_property("location", archivo)
        
        audiobin = Gst.Bin()
        
        audiobin.add(queue)
        audiobin.add(audioconvert)
        audiobin.add(vorbisenc)
        audiobin.add(que_audio_mux)
        audiobin.add(oggmux)
        audiobin.add(sink)
        
        queue.link(audioconvert)
        audioconvert.link(vorbisenc)
        vorbisenc.link(que_audio_mux)
        que_audio_mux.link(oggmux)
        oggmux.link(sink)
        
        pad = queue.get_static_pad("sink")
        audiobin.add_pad(Gst.GhostPad.new("sink", pad))
        
        map(self.agregar, [audiobin])
        
        self.multi.link(audiobin)
        
    '''
    def agregar_efecto(self, nombre_efecto):
        """Agrega un efecto según nombre_efecto."""
        
        self.efectos.append(nombre_efecto)
        self.stop()
        self.get_base_pipe()
        self.play()
        
    def quitar_efecto(self, indice_efecto):
        """Quita el efecto correspondiente al indice que recibe."""
        
        self.efectos.remove(self.efectos[indice_efecto])
        self.stop()
        self.get_base_pipe()
        self.play()'''
        
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
        self.get_grabar_pipe()
        
        self.play()
        self.estado = "GrabandoAudio"
        
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
    jamediaaudio = JAMediaAudio(xid)
    jamediaaudio.play()
    
    ventana.connect("destroy", salir)
    
    Gtk.main()
    