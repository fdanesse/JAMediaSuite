#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaVideo.py por:
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
import sys
import time

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkX11

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import Visor
from JAMediaObjects.JAMediaWidgets import JAMediaButton
from JAMediaObjects.JAMediaWebCam import JAMediaWebCam
from JAMediaObjects.JAMediaWidgets import ToolbarSalir

import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMediaVideo
from JAMediaVideo.Widgets import Toolbar
from JAMediaVideo.Widgets import ToolbarPrincipal
from JAMediaVideo.Widgets import ToolbarVideo
from JAMediaVideo.Widgets import ToolbarFotografia
from JAMediaVideo.Widgets import ToolbarGrabarAudio
from JAMediaVideo.Widgets import ToolbarVideoBalance
from JAMediaVideo.Widgets import ToolbarFotografiaBalance

import JAMedia
from JAMedia.JAMedia import JAMediaPlayer

import JAMImagenes
from JAMImagenes.JAMImagenes import JAMImagenes

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMediaEstilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()
context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    
GObject.threads_init()
Gdk.threads_init()
    
class JAMediaVideo(Gtk.Window):
    
    def __init__(self):
        
        super(JAMediaVideo, self).__init__()
        
        self.set_title("JAMediaVideo")
        self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaVideo.png"))
        self.set_resizable(True)
        self.set_default_size(640, 480)
        #self.fullscreen()
        self.set_position(Gtk.WindowPosition.CENTER)
        #self.modify_bg(0, G.GRIS)
        #self.set_opacity(0.5)
        
        self.pantalla = None
        self.jamediawebcam = None
        self.toolbar = None
        self.toolbar_salir = None
        self.toolbarprincipal = None
        self.toolbarvideo = None
        self.toolbarbalanceconfig = None
        self.toolbarfotografia = None
        self.toolbargrabaraudio = None
        self.jamediaplayer = None
        self.jamimagenes = None
        
        self.controlesdinamicos = None
        
        self.update_rafagas = False
        
        self.setup_init()
        
    def setup_init(self):
        """Genera y empaqueta toda la interfaz."""
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)
        self.show_all()
        
        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.toolbarprincipal = ToolbarPrincipal()
        self.toolbarvideo = ToolbarVideo()
        self.toolbarvideoconfig = ToolbarVideoBalance()
        self.toolbarfotografiaconfig = ToolbarFotografiaBalance()
        self.toolbarfotografia = ToolbarFotografia()
        self.toolbargrabaraudio = ToolbarGrabarAudio()
        self.socketjamedia = Gtk.Socket()
        self.socketjamimagenes = Gtk.Socket()
        self.pantalla = Visor()
        
        vbox.pack_start(self.toolbar, False, True, 0)
        vbox.pack_start(self.toolbar_salir, False, True, 0)
        vbox.pack_start(self.toolbarprincipal, False, True, 0)
        
        vbox.pack_start(self.toolbarvideo, False, True, 0)
        vbox.pack_start(self.toolbarfotografia, False, True, 0)
        vbox.pack_start(self.toolbarvideoconfig, False, True, 0)
        vbox.pack_start(self.toolbarfotografiaconfig, False, True, 0)
        
        vbox.pack_start(self.toolbargrabaraudio, False, True, 0)
        vbox.pack_start(self.socketjamedia, True, True, 0)
        vbox.pack_start(self.socketjamimagenes, True, True, 0)
        vbox.pack_start(self.pantalla, True, True, 0)
        
        self.jamediaplayer = JAMediaPlayer()
        self.socketjamedia.add_id(self.jamediaplayer.get_id())
        
        self.jamimagenes = JAMImagenes()
        self.socketjamimagenes.add_id(self.jamimagenes.get_id())
        
        self.show_all()
        self.realize()
        
        GObject.idle_add(self.setup_init2)
        
    def setup_init2(self):
        """Inicializa la aplicación a su estado fundamental."""
        
        self.jamediaplayer.setup_init()
        self.jamediaplayer.switch_reproductor(None, "JAMediaReproductor")
        
        self.controlesdinamicos = [
            self.toolbar,
            self.toolbar_salir,
            self.toolbarprincipal,
            self.toolbarvideo,
            self.toolbarvideoconfig,
            self.toolbarfotografiaconfig,
            self.toolbarfotografia,
            self.toolbargrabaraudio,
            self.socketjamedia,
            self.socketjamimagenes]
            
        map(self.ocultar, self.controlesdinamicos)
        map(self.mostrar, [self.toolbar, self.toolbarprincipal])
        
        xid = self.pantalla.get_property('window').get_xid()
        self.jamediawebcam = JAMediaWebCam(xid)
        
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar_salir.connect('salir', self.salir)
        
        self.toolbarprincipal.connect("menu", self.get_menu)
        
        self.toolbarvideo.connect("accion", self.set_accion_video)
        self.toolbargrabaraudio.connect("accion", self.set_accion_audio)
        self.toolbarfotografia.connect("accion", self.set_accion_fotografia)
        
        self.toolbarvideo.connect("salir", self.get_menu_base)
        self.toolbarfotografia.connect("salir", self.get_menu_base)
        self.toolbargrabaraudio.connect("salir", self.get_menu_base)
        self.jamediaplayer.connect('salir', self.get_menu_base)
        self.jamimagenes.connect('salir', self.get_menu_base)
        
        self.toolbarvideoconfig.connect('valor', self.set_balance)
        self.toolbarfotografiaconfig.connect('valor', self.set_balance)
        self.toolbarfotografiaconfig.connect('run_rafaga', self.run_rafaga)
        
        self.pantalla.connect("button_press_event", self.clicks_en_pantalla)
        
        self.connect("destroy", self.salir)
        
        self.jamediawebcam.play()
        
    def run_rafaga(self, widget, valor):
        """ Comienza fotografías en ráfaga. """
        
        if self.update_rafagas:
            GObject.source_remove(self.update_rafagas)
            self.update_rafagas = False
            
        self.update_rafagas = GObject.timeout_add(int(valor)*1000, self.ejecute_rafaga)
        self.toolbarfotografia.set_estado("grabando")
        
    def ejecute_rafaga(self):
        
        self.jamediawebcam.fotografiar()
        time.sleep(0.8)
        return True
        
    def set_balance(self, widget, valor, tipo):
        """ Setea valores en Balance de Video.
        valor es % float"""
        
        if tipo == "saturacion":
            self.jamediawebcam.set_balance(saturacion = valor)
            
        elif tipo == "contraste":
            self.jamediawebcam.set_balance(contraste = valor)
            
        elif tipo == "brillo":
            self.jamediawebcam.set_balance(brillo = valor)
            
        elif tipo == "hue":
            self.jamediawebcam.set_balance(hue = valor)
    
    def clicks_en_pantalla(self, widget, event):
        """Hace fullscreen y unfullscreen sobre la
        ventana principal cuando el usuario hace
        doble click en el visor."""
        
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w,h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            
            if ww == w and hh == h:
                ventana.unfullscreen()
                
            else:
                ventana.fullscreen()

    def set_accion_fotografia(self, widget, senial):
        """Cuando se hace click en tomar fotografia o
        en configurar."""
        
        if senial == 'fotografiar':
            if self.update_rafagas:
                GObject.source_remove(self.update_rafagas)
                self.update_rafagas = False
                self.toolbarfotografia.set_estado("detenido")
            
            if self.jamediawebcam.estado != "FotografiandoWebCam":
                self.jamediawebcam.fotografiar()
                self.toolbarfotografia.set_estado("grabando")
                time.sleep(0.8)
                self.jamediawebcam.reset()
                
                config = self.jamediawebcam.get_balance()
                self.toolbarfotografiaconfig.set_balance(
                    brillo = config['brillo'],
                    contraste = config['contraste'],
                    saturacion = config['saturacion'],
                    hue = config['hue'])
                    
                self.toolbarfotografia.set_estado("detenido")
                
            else:
                self.jamediawebcam.reset()
                config = self.jamediawebcam.get_balance()
                self.toolbarfotografiaconfig.set_balance(
                    brillo = config['brillo'],
                    contraste = config['contraste'],
                    saturacion = config['saturacion'],
                    hue = config['hue'])
                    
                self.toolbarfotografia.set_estado("detenido")
                
        elif senial == 'configurar':
            if self.toolbarfotografiaconfig.get_visible():
                self.toolbarfotografiaconfig.hide()
                
            else:
                config = self.jamediawebcam.get_balance()
                self.toolbarfotografiaconfig.set_balance(
                    brillo = config['brillo'],
                    contraste = config['contraste'],
                    saturacion = config['saturacion'],
                    hue = config['hue'])
                self.toolbarfotografiaconfig.show()
                
    def set_accion_audio(self, widget, senial):
        """Cuando se hace click en grabar solo audio o
        en configurar."""
        
        if senial == 'grabar':
            if self.jamediawebcam.estado != "GrabandoAudioPulsersc":
                self.jamediawebcam.grabarsoloaudio()
                self.toolbargrabaraudio.set_estado("grabando")
                
            else:
                self.jamediawebcam.reset()
                self.toolbargrabaraudio.set_estado("detenido")
                
        elif senial == 'configurar':
            self.jamediawebcam.reset()
            self.toolbargrabaraudio.set_estado("detenido")
            # Mostrar controles de configuración.
            
    def set_accion_video(self, widget, senial):
        """Cuando se hace click en filmar o
        en configurar filmacion."""
        
        if senial == 'filmar':
            if self.jamediawebcam.estado != "GrabandoAudioVideoWebCam":
                self.jamediawebcam.grabar()
                self.toolbarvideo.set_estado("grabando")
                
            else:
                self.jamediawebcam.reset()
                config = self.jamediawebcam.get_balance()
                self.toolbarvideoconfig.set_balance(
                    brillo = config['brillo'],
                    contraste = config['contraste'],
                    saturacion = config['saturacion'],
                    hue = config['hue'])
                self.toolbarvideo.set_estado("detenido")
                
        elif senial == 'configurar':
            if self.toolbarvideoconfig.get_visible():
                self.toolbarvideoconfig.hide()
                
            else:
                config = self.jamediawebcam.get_balance()
                self.toolbarvideoconfig.set_balance(
                    brillo = config['brillo'],
                    contraste = config['contraste'],
                    saturacion = config['saturacion'],
                    hue = config['hue'])
                self.toolbarvideoconfig.show()
                
    def get_menu_base(self, widget):
        """Cuando se sale de un menú particular,
        se vuelve al menú principal."""
        
        if self.update_rafagas:
            GObject.source_remove(self.update_rafagas)
            self.update_rafagas = False
            
        self.jamediawebcam.reset()
        self.toolbargrabaraudio.set_estado("detenido")
        self.toolbarvideo.set_estado("detenido")
        self.toolbarfotografia.set_estado("detenido")
        
        map(self.ocultar, self.controlesdinamicos)
        map(self.mostrar, [self.toolbar,
        self.toolbarprincipal, self.pantalla])
        
    def get_menu(self, widget, menu):
        """Cuando se hace click en algún botón de
        la toolbar principal, se entra en el menú correspondiente."""
        
        map(self.ocultar, self.controlesdinamicos)
        
        if menu == "Filmar":
            map(self.mostrar, [self.toolbarvideo])
            
        elif menu == "Fotografiar":
            map(self.mostrar, [self.toolbarfotografia])
            
        elif menu == "Grabar":
            map(self.mostrar, [self.toolbargrabaraudio])
            
        elif menu == "Reproducir":
            self.jamediawebcam.stop()
            map(self.ocultar, [self.pantalla])
            map(self.mostrar, [self.socketjamedia])
            archivos = []
            
            for arch in os.listdir(G.AUDIO_JAMEDIA_VIDEO):
                ar = os.path.join(G.AUDIO_JAMEDIA_VIDEO, arch)
                archivos.append([arch, ar])
                
            for arch in os.listdir(G.VIDEO_JAMEDIA_VIDEO):
                ar = os.path.join(G.VIDEO_JAMEDIA_VIDEO, arch)
                archivos.append([arch, ar])
                
            self.jamediaplayer.set_nueva_lista(archivos)
            
        elif menu == "Ver":
            self.jamediawebcam.stop()
            map(self.ocultar, [self.pantalla])
            map(self.mostrar, [self.socketjamimagenes])
            archivos = []
            
            for arch in os.listdir(G.IMAGENES_JAMEDIA_VIDEO):
                ar = os.path.join(G.IMAGENES_JAMEDIA_VIDEO, arch)
                archivos.append([arch, ar])
                
            self.jamimagenes.set_lista(archivos)
        
    def ocultar(self, objeto):
        """Esta funcion es llamada desde self.get_menu()"""
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        """Esta funcion es llamada desde self.get_menu()"""
        
        if not objeto.get_visible(): objeto.show()
        
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        self.toolbar_salir.run("JAMediaVideo")
        
    def salir(self, widget = None, senial = None):
        sys.exit(0)
    
if __name__ == "__main__":
    JAMediaVideo()
    Gtk.main()
    