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

CONFIG_DEFAULT = {
    'device': "/dev/video0",
    'saturacion': 5,
    'contraste': 6,
    'brillo': 8,
    'hue': 0,
    'gamma': 1.0,
    }


class JAMediaWebCam(GObject.GObject):
    """
    Interfaz para Webcam, en base a Gstreamer 1.0.
    
    estados posibles:
        
        stoped
        playing
        GrabandoAudioVideo
        Fotografiando
        
    Guía para utilizar JAMediaWebCam:
        
        from gi.repository import GdkX11
        
        xid = self.pantalla.get_property('window').get_xid()
        self.jamediawebcam = JAMediaWebCam(xid)
        GObject.idle_add(self.jamediawebcam.reset)
        o
        GObject.idle_add(self.jamediawebcam.play)
    """
    
    __gsignals__ = {
    "estado":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self, ventana_id):
        """ Recibe el id de un DrawingArea
        para mostrar el video. """
        
        GObject.GObject.__init__(self)
        
        self.name = "JAMediaWebCam"
        self.ventana_id = ventana_id
        self.pipeline = None
        self.estado = 'stoped'
        self.patharchivo = None
        
        self.camara = None
        self.gamma = None
        self.videoflip = None
        
        self.config = {}
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        self.config['gamma'] = CONFIG_DEFAULT['gamma']
        
        self.efectos = []
        self.config_efectos = {}
        
        self.setup_init()
        
    def setup_init(self):
        """Crea todos los elementos permanentes del pipe y
        llama a set_base_pipe para linkear elementos bases."""
        
        if self.pipeline:
            del(self.pipeline)
            
        self.pipeline = Gst.Pipeline()
        
        self.efectos = []
        self.config_efectos = {}
        
        self.camara = JAMedia_Camara_bin()
        
        self.gamma = Gst.ElementFactory.make('gamma', "gamma")
        
        self.videoflip = Gst.ElementFactory.make(
            'videoflip', "videoflip")
        
        self.set_base_pipe()
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)
        
    def set_base_pipe(self):
        """Linkea los elementos base."""
        
        #self.camara
        
        #efectos
        #self.gamma
        #self.videoflip
        
        multi_out_tee = Gst.ElementFactory.make('tee', "multi_out_tee")
        
        queue_xvimagesink = Gst.ElementFactory.make('queue', "queue_xvimagesink")
        queue_xvimagesink.set_property('max-size-buffers', 1000)
        queue_xvimagesink.set_property('max-size-bytes', 0)
        queue_xvimagesink.set_property('max-size-time', 0)
        
        pantalla = Gst.ElementFactory.make('xvimagesink', "xvimagesink")
        
        efectos_bin = Efectos_Video_bin(self.efectos, self.config_efectos)
        
        fotobin = Foto_bin()
        
        self.pipeline.add(self.camara)
        self.pipeline.add(efectos_bin)
        self.pipeline.add(self.gamma)
        self.pipeline.add(self.videoflip)
        self.pipeline.add(multi_out_tee)
        
        self.pipeline.add(queue_xvimagesink)    # multi_out_tee. #1
        self.pipeline.add(pantalla)
        
        self.pipeline.add(fotobin)
        
        self.camara.link(efectos_bin)
        efectos_bin.link(self.gamma)
        self.gamma.link(self.videoflip)
        self.videoflip.link(multi_out_tee)
        
        multi_out_tee.link(queue_xvimagesink)   # multi_out_tee. #1
        queue_xvimagesink.link(pantalla)
        
        multi_out_tee.link(fotobin)
        
    def reset(self):
        """Re establece la cámara y el pipe a sus estados
        originales (pipe = sólo camara a pantalla, sin efectos)."""
        
        self.config['device'] = CONFIG_DEFAULT['device']
        self.config['saturacion'] = CONFIG_DEFAULT['saturacion']
        self.config['contraste'] = CONFIG_DEFAULT['contraste']
        self.config['brillo'] = CONFIG_DEFAULT['brillo']
        self.config['hue'] = CONFIG_DEFAULT['hue']
        self.config['gamma'] = CONFIG_DEFAULT['gamma']
        
        self.camara.camara.set_property('saturation', self.config['saturacion'])
        self.camara.camara.set_property('contrast', self.config['contraste'])
        self.camara.camara.set_property('brightness', self.config['brillo'])
        self.camara.camara.set_property('hue', self.config['hue'])
        
        self.gamma.set_property('gamma', self.config['gamma'])
        
        self.videoflip.set_property('method', 0)
        
        self.stop()
        
        map(self.remover, self.pipeline.children)
        
        self.setup_init()
        
        self.play()
        
    def set_estado(self, valor):
        """Autoseteo e informe de estado del pipe, según
        esté corriendo o no y segun los elementos en el pipe."""
        
        estado = valor
        
        if estado == 'stoped':
            pass
            
        elif estado == 'playing':
            #if self.pipeline.get_by_name('foto_bin'):
            #    estado = 'Fotografiando'
            
            #elif self.pipeline.get_by_name('video_bin'):
            if self.pipeline.get_by_name('video_bin'):
                estado = 'GrabandoAudioVideo'
            
        else:
            print "????", valor
            
        if estado != self.estado:
            self.estado = estado
            self.emit('estado', self.estado)
            
    def play(self, widget = None, event = None):
        
        self.pipeline.set_state(Gst.State.PLAYING)
        self.set_estado("playing")
        
    def stop(self, widget= None, event= None):
        """Detiene y limpia el pipe."""
        
        self.pipeline.set_state(Gst.State.NULL)
        
        try:
            if os.path.exists(self.patharchivo):
                os.chmod(self.patharchivo, 0755)
                
        except:
            pass
        
        self.set_estado("stoped")
        
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
        Recibe % en float."""
        
        # Rangos: int. -2147483648 2147483647
        min	= 2147483648
        #max = 2147483647
        total = 4294967295
        
        if saturacion != None:
            new_valor = int (total * int(saturacion) / 100)
            new_valor -= min
            self.config['saturacion'] = new_valor
            self.camara.camara.set_property('saturation', self.config['saturacion'])
            
        if contraste != None:
            new_valor = int (total * int(contraste) / 100)
            new_valor -= min
            self.config['contraste'] = new_valor
            self.camara.camara.set_property('contrast', self.config['contraste'])
            
        if brillo != None:
            new_valor = int (total * int(brillo) / 100)
            new_valor -= min
            self.config['brillo'] = new_valor
            self.camara.camara.set_property('brightness', self.config['brillo'])
            
        if hue != None:
            new_valor = int (total * int(hue) / 100)
            new_valor -= min
            self.config['hue'] = new_valor
            self.camara.camara.set_property('hue', self.config['hue'])
            
        if gamma != None:
            # Double. Range: 0,01 - 10 Default: 1
            self.config['gamma'] = (10.0 * gamma / 100.0)
            self.gamma.set_property('gamma', self.config['gamma'])
            
    def get_balance(self):
        """Retorna los valores actuales de
        balance en %."""
        
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
        
        config['gamma'] = self.config['gamma'] * 100.0 / 10.0
        
        return config
    
    def fotografiar(self, widget = None, event = None):
        """Toma una fotografia."""
        
        foto_bin = self.pipeline.get_by_name("foto_bin")
        gdkpixbufsink = self.pipeline.get_by_name("gdkpixbufsink")
        
        if gdkpixbufsink and gdkpixbufsink != None:
            pixbuf = gdkpixbufsink.get_property('last-pixbuf')
            
            if pixbuf and pixbuf != None:
                
                fecha = datetime.date.today()
                hora = time.strftime("%H-%M-%S")
                archivo = os.path.join(
                    G.IMAGENES_JAMEDIA_VIDEO,
                    "%s-%s.png" % (fecha, hora))
                
                self.patharchivo = archivo
                
                pixbuf.savev(self.patharchivo, "png", [], [])
        
    def grabar(self, widget= None, event= None):
        """ Graba Audio y Video desde la webcam. """
        
        self.stop()
        
        multi_out_tee = self.pipeline.get_by_name('multi_out_tee')
        
        # FIXME: Verificar que ya no estén estos elementos en el pipe
        video_bin = Theoraenc_bin()
        audio_bin = Vorbisenc_bin()
        
        oggmux = Gst.ElementFactory.make('oggmux', "oggmux")
        filesink = Gst.ElementFactory.make('filesink', "filesink")
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(
            G.VIDEO_JAMEDIA_VIDEO,"%s-%s.ogg" % (fecha, hora))
        self.patharchivo = archivo
        filesink.set_property("location", archivo)
        
        self.pipeline.add(video_bin)
        self.pipeline.add(audio_bin)
        self.pipeline.add(oggmux)
        self.pipeline.add(filesink)
        
        multi_out_tee.link(video_bin)
        video_bin.link(oggmux)
        audio_bin.link(oggmux)
        oggmux.link(filesink)
        
        self.play()
        
    def stop_grabar(self):
        """Detiene la grabación en progreso."""

        self.stop()
        
        multi_out_tee = self.pipeline.get_by_name('multi_out_tee')
        
        video_bin = self.pipeline.get_by_name('video_bin')
        audio_bin = self.pipeline.get_by_name('audio_bin')
        
        oggmux = self.pipeline.get_by_name('oggmux')
        filesink = self.pipeline.get_by_name('filesink')
        
        multi_out_tee.unlink(video_bin)
        video_bin.unlink(oggmux)
        audio_bin.unlink(oggmux)
        oggmux.unlink(filesink)
        
        self.pipeline.remove(video_bin)
        self.pipeline.remove(audio_bin)
        self.pipeline.remove(oggmux)
        self.pipeline.remove(filesink)
        
        self.play()
    
    def remover(self, objeto):
        """Para remover objetos en el pipe."""
        
        if objeto in self.pipeline.children: self.pipeline.remove(objeto)
        
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
            print "###", err, debug
            
    def agregar_efecto(self, nombre_efecto):
        """Agrega un efecto según su nombre."""
        
        self.efectos.append( nombre_efecto )
        self.config_efectos[nombre_efecto] = {}
        
        self.stop()
        
        # Quitar efectos
        efectos_bin = self.pipeline.get_by_name('efectos_bin')
        jamedia_camara_bin = self.pipeline.get_by_name('jamedia_camara_bin')
        jamedia_camara_bin.unlink(efectos_bin)
        efectos_bin.unlink(self.gamma)
        self.pipeline.remove(efectos_bin)
        del(efectos_bin)
        
        # Agregar efectos
        efectos_bin = Efectos_Video_bin(self.efectos, self.config_efectos)
        self.pipeline.add(efectos_bin)
        jamedia_camara_bin.link(efectos_bin)
        efectos_bin.link(self.gamma)
        
        self.play()
        
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
        
        self.stop()
        
        # Quitar efectos
        efectos_bin = self.pipeline.get_by_name('efectos_bin')
        jamedia_camara_bin = self.pipeline.get_by_name('jamedia_camara_bin')
        jamedia_camara_bin.unlink(efectos_bin)
        efectos_bin.unlink(self.gamma)
        self.pipeline.remove(efectos_bin)
        del(efectos_bin)
        
        # Agregar efectos
        efectos_bin = Efectos_Video_bin(self.efectos, self.config_efectos)
        self.pipeline.add(efectos_bin)
        jamedia_camara_bin.link(efectos_bin)
        efectos_bin.link(self.gamma)
        
        self.play()
        
    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        """Configura un efecto en el pipe."""
        
        efectos_bin = self.pipeline.get_by_name('efectos_bin')
        bin_efecto = efectos_bin.get_by_name(nombre_efecto)
        bin_efecto.get_by_name(nombre_efecto).set_property(propiedad, valor)
        self.config_efectos[nombre_efecto][propiedad] = valor
        efectos_bin.config_efectos[nombre_efecto][propiedad] = valor
        
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
        
        self.set_name('video_bin')
        
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
        
        self.set_name('audio_bin')
        
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
        queue.set_property('max-size-buffers', 1000)
        queue.set_property('max-size-bytes', 0)
        queue.set_property('max-size-time', 0)
        
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
    