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

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import Gst
from gi.repository import GstVideo
from gi.repository import GdkPixbuf

from JAMediaObjects.JAMediaGlobales import get_imagenes_directory
from JAMediaObjects.JAMediaGlobales import get_video_directory

from JAMediaBins import Efectos_Video_bin
from JAMediaBins import Foto_bin
from JAMediaBins import Vorbisenc_bin
from JAMediaBins import Theoraenc_bin
from JAMediaBins import JAMedia_Camara_bin

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
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """
        
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
        
        self.control_rafaga = False
        
        self.__setup_init()
        
    def __setup_init(self):
        """
        Crea todos los elementos permanentes del pipe y
        llama a set_base_pipe para linkear elementos bases.
        """
        
        if self.pipeline:
            del(self.pipeline)
            
        self.pipeline = Gst.Pipeline()
        
        self.efectos = []
        self.config_efectos = {}
        
        self.camara = JAMedia_Camara_bin()
        
        self.gamma = Gst.ElementFactory.make('gamma', "gamma")
        
        self.videoflip = Gst.ElementFactory.make(
            'videoflip', "videoflip")
        
        self.__set_base_pipe()
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)
        
    def __set_base_pipe(self):
        """
        Linkea los elementos base.
        """
        
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
        """
        Re establece la cámara y el pipe a sus estados
        originales (pipe = sólo camara a pantalla, sin efectos).
        """
        
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
        
        map(self.__remover, self.pipeline.children)
        
        self.__setup_init()
        
        self.play()
        
    def __set_estado(self, valor):
        """
        Autoseteo e informe de estado del pipe, según
        esté corriendo o no y segun los elementos en el pipe.
        """
        
        estado = valor
        
        if estado == 'stoped':
            pass
            
        elif estado == 'playing':
            #if self.pipeline.get_by_name('foto_bin'):
            #    estado = 'Fotografiando'
            
            #elif self.pipeline.get_by_name('video_bin'):
            if self.pipeline.get_by_name('video_theoraenc_bin'):
                estado = 'GrabandoAudioVideo'
            
        else:
            print "????", valor
            
        if estado != self.estado:
            self.estado = estado
            self.emit('estado', self.estado)
            
    def play(self, widget = None, event = None):
        
        self.pipeline.set_state(Gst.State.PLAYING)
        self.__set_estado("playing")
        
    def stop(self, widget= None, event= None):
        """
        Detiene y limpia el pipe.
        """
        
        self.pipeline.set_state(Gst.State.NULL)
        
        try:
            if os.path.exists(self.patharchivo):
                os.chmod(self.patharchivo, 0755)
                
        except:
            pass
        
        self.__set_estado("stoped")
        
    def rotar(self, valor):
        """
        Rota el Video.
        """
        
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
        """
        Seteos de balance en la fuente de video.
        Recibe % en float.
        """
        
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
        """
        Retorna los valores actuales de
        balance en %.
        """
        
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
        """
        Toma una fotografia.
        """
        
        foto_bin = self.pipeline.get_by_name("foto_bin")
        gdkpixbufsink = self.pipeline.get_by_name("gdkpixbufsink")
        
        if gdkpixbufsink and gdkpixbufsink != None:
            pixbuf = gdkpixbufsink.get_property('last-pixbuf')
            
            if pixbuf and pixbuf != None:
                import time
                import datetime
                
                fecha = datetime.date.today()
                hora = time.strftime("%H-%M-%S")
                archivo = os.path.join(
                    get_imagenes_directory(),
                    "%s-%s.png" % (fecha, hora))
                
                self.patharchivo = archivo
                
                pixbuf.savev(self.patharchivo, "png", [], [])
        
    def set_rafaga(self, segundos):
        """
        Comienza secuencia de fotografías en ráfaga.
        """
        
        if self.control_rafaga:
            GObject.source_remove(self.control_rafaga)
            self.control_rafaga = False
            
        self.__set_estado("Fotografiando")
        
        self.control_rafaga = GObject.timeout_add(
            int(segundos*1000), self.__rafaga)
        
    def stop_rafagas(self):
        """
        Detiene el proceso de fotografías en ráfagas.
        """
        
        self.__set_estado("playing")
        
        if self.control_rafaga:
            GObject.source_remove(self.control_rafaga)
            self.control_rafaga = False
        
    def __rafaga(self):
        """
        Toma una fotografía cuando se ha seteado ráfagas.
        """
        
        if not self.estado == "Fotografiando":
            return False
    
        else:
            self.fotografiar(widget = None, event = None)
            return True
        
    def grabar(self, widget= None, event= None):
        """
        Graba Audio y Video desde la webcam.
        """
        
        import time
        import datetime
        
        self.stop()
        
        multi_out_tee = self.pipeline.get_by_name('multi_out_tee')
        
        # FIXME: Verificar que ya no estén estos elementos en el pipe
        video_bin = Theoraenc_bin()
        audio_bin = Vorbisenc_bin()
        
        oggmux = Gst.ElementFactory.make('oggmux', "oggmux")
        filesink = Gst.ElementFactory.make('filesink', "filesink")
        
        fecha = datetime.date.today()
        hora = time.strftime("%H-%M-%S")
        archivo = os.path.join(get_video_directory(),"%s-%s.ogg" % (fecha, hora))
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
        """
        Detiene la grabación en progreso.
        """

        self.stop()
        
        multi_out_tee = self.pipeline.get_by_name('multi_out_tee')
        
        video_bin = self.pipeline.get_by_name('video_theoraenc_bin')
        audio_bin = self.pipeline.get_by_name('audio_vorbisenc_bin')
        
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
    
    def __remover(self, objeto):
        """
        Para remover objetos en el pipe.
        """
        
        if objeto in self.pipeline.children: self.pipeline.remove(objeto)
        
    def __sync_message(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """
        
        try:
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return
            
        except:
            pass
    
    def __on_mensaje(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """
        
        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "###", err, debug
            
    def agregar_efecto(self, nombre_efecto):
        """
        Agrega un efecto según su nombre.
        """
        
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
        """
        Quita el efecto correspondiente al indice o
        al nombre que recibe.
        """

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
        """
        Configura un efecto en el pipe.
        """
        
        efectos_bin = self.pipeline.get_by_name('efectos_bin')
        bin_efecto = efectos_bin.get_by_name(nombre_efecto)
        bin_efecto.get_by_name(nombre_efecto).set_property(propiedad, valor)
        self.config_efectos[nombre_efecto][propiedad] = valor
        efectos_bin.config_efectos[nombre_efecto][propiedad] = valor
        
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
    
    from gi.repository import GdkX11
    
    xid = pantalla.get_property('window').get_xid()
    jamediawebcam = JAMediaWebCam(xid)
    jamediawebcam.play()
    
    ventana.connect("destroy", salir)
    
    Gtk.main()
    