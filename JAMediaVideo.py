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
from JAMediaObjects.JAMediaWidgets import ToolbarSalir
from JAMediaObjects.JAMediaWidgets import ToolbarGstreamerEfectos
from JAMediaObjects.JAMediaWebCam import JAMediaWebCam
from JAMediaObjects.JAMediaAudio import JAMediaAudio

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
        
        self.jamediawebcam = None
        self.jamediaaudio = None
        
        self.toolbar = None
        self.toolbar_salir = None
        self.toolbarprincipal = None
        self.toolbarvideo = None
        self.toolbarvideoconfig = None
        self.toolbarbalanceconfig = None
        self.toolbargstreamerefectos = None
        self.toolbarfotografia = None
        self.toolbarfotografiaconfig = None
        self.toolbargrabaraudio = None
        
        self.socketjamedia = None
        self.socketjamimagenes = None
        
        self.jamediaplayer = None
        self.jamimagenes = None
        self.pantalla = None
        
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
        
        self.toolbarfotografia = ToolbarFotografia()
        self.toolbarfotografiaconfig = ToolbarFotografiaBalance()
        
        self.toolbargstreamerefectos = ToolbarGstreamerEfectos()
        
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
        vbox.pack_start(self.toolbargstreamerefectos, False, False, 0)
        
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
            self.socketjamimagenes,
            self.toolbargstreamerefectos]
            
        map(self.ocultar, self.controlesdinamicos)
        map(self.mostrar, [self.toolbar, self.toolbarprincipal])
        
        xid = self.pantalla.get_property('window').get_xid()
        self.jamediawebcam = JAMediaWebCam(xid)
        self.jamediaaudio = JAMediaAudio(xid)
        
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar_salir.connect('salir', self.salir)
        
        self.toolbarprincipal.connect("menu", self.get_menu)
        self.toolbarprincipal.connect("rotar", self.set_rotacion)
        
        self.toolbarvideo.connect("accion", self.set_accion_video)
        self.toolbarvideo.connect("rotar", self.set_rotacion)
        self.toolbarvideo.connect("salir", self.get_menu_base)
        self.toolbarvideoconfig.connect('valor', self.set_balance)
        
        self.toolbarfotografia.connect("accion", self.set_accion_fotografia)
        self.toolbarfotografia.connect("rotar", self.set_rotacion)
        self.toolbarfotografia.connect("salir", self.get_menu_base)
        self.toolbarfotografiaconfig.connect('valor', self.set_balance)
        #self.toolbarfotografiaconfig.connect('run_rafaga', self.run_rafaga)
        
        self.toolbargrabaraudio.connect("accion", self.set_accion_audio)
        self.toolbargrabaraudio.connect("rotar", self.set_rotacion_audio)
        self.toolbargrabaraudio.connect("salir", self.get_menu_base)
        
        self.jamediaplayer.connect('salir', self.get_menu_base)
        self.jamimagenes.connect('salir', self.get_menu_base)
        
        self.pantalla.connect("button_press_event", self.clicks_en_pantalla)
        
        self.toolbargstreamerefectos.connect("agregar_efecto", self.agregar_efecto)
        self.toolbargstreamerefectos.connect("quitar_efecto", self.quitar_efecto)
        
        self.connect("destroy", self.salir)
        
        self.fullscreen()
        
        GObject.idle_add(self.jamediawebcam.reset)
        
    def set_rotacion(self, widget, valor):
        """Recibe rotación y la pasa a la webcam."""
        
        self.jamediawebcam.rotar(valor)
        
    def set_rotacion_audio(self, widget, valor):
        """Recibe rotación y la pasa al pipe de audio."""
        
        self.jamediaaudio.rotar(valor)
        
    def update_balance_toolbars(self):
        """Actualiza las toolbars de balance en video."""
        
        config = self.jamediawebcam.get_balance()
        
        self.toolbarvideoconfig.set_balance(
            brillo = config['brillo'],
            contraste = config['contraste'],
            saturacion = config['saturacion'],
            hue = config['hue'])
            
        self.toolbarfotografiaconfig.set_balance(
            brillo = config['brillo'],
            contraste = config['contraste'],
            saturacion = config['saturacion'],
            hue = config['hue'])
        
    def agregar_efecto(self, widget, nombre_efecto):
        """Recibe el nombre del efecto que debe agregarse
        al pipe de  JAMediaWebcam y ejecuta la acción."""
        
        if self.jamediawebcam.estado == "GrabandoAudioVideoWebCam":
            self.jamediawebcam.re_init()
            self.toolbarvideo.set_estado("detenido")
        
        self.jamediawebcam.agregar_efecto( nombre_efecto )
        
    def quitar_efecto(self, widget, indice_efecto):
        """Recibe el indice del efecto que debe quitarse
        del pipe de  JAMediaWebcam y ejecuta la acción."""
        
        if self.jamediawebcam.estado == "GrabandoAudioVideoWebCam":
            self.jamediawebcam.re_init()
            self.toolbarvideo.set_estado("detenido")
            
        self.jamediawebcam.quitar_efecto( indice_efecto )
        
    def reset(self):
        """Resetea la cámara quitando los efectos y
        actualiza los widgets correspondientes."""
        
        self.toolbargstreamerefectos.reset()
        self.jamediaplayer.lista_de_reproduccion.limpiar()
        self.jamimagenes.lista.limpiar()
        self.toolbargrabaraudio.set_estado("detenido")
        self.toolbarvideo.set_estado("detenido")
        self.toolbarfotografia.set_estado("detenido")
        self.jamediawebcam.reset()
        GObject.idle_add(self.update_balance_toolbars)
        
    def re_init(self):
        """Vuelve la camara al estado original manteniendo efectos."""
        
        self.jamediaplayer.lista_de_reproduccion.limpiar()
        self.jamimagenes.lista.limpiar()
        self.toolbargrabaraudio.set_estado("detenido")
        self.toolbarvideo.set_estado("detenido")
        self.toolbarfotografia.set_estado("detenido")
        self.jamediaaudio.stop()
        self.jamediawebcam.re_init()
        GObject.idle_add(self.update_balance_toolbars)
    
    def re_init_menu_audio(self):
        """Vuelve el audio al estado original manteniendo efectos."""
        
        self.jamediaplayer.lista_de_reproduccion.limpiar()
        self.jamimagenes.lista.limpiar()
        self.toolbargrabaraudio.set_estado("detenido")
        self.toolbarvideo.set_estado("detenido")
        self.toolbarfotografia.set_estado("detenido")
        self.jamediaaudio.re_init()
        GObject.idle_add(self.update_balance_toolbars)
        
    def reset_audio_pipe(self):
        """Resetea la cámara quitando los efectos y
        actualiza los widgets correspondientes."""
        
        #self.toolbargstreamerefectos.reset()
        self.jamediaplayer.lista_de_reproduccion.limpiar()
        self.jamimagenes.lista.limpiar()
        self.toolbargrabaraudio.set_estado("detenido")
        self.toolbarvideo.set_estado("detenido")
        self.toolbarfotografia.set_estado("detenido")
        #self.jamediawebcam.reset_audio_pipe()
        self.jamediaaudio.reset()
        GObject.idle_add(self.update_balance_toolbars)
        
    '''
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
        return True'''
        
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
            
            # FIXME:
                # Debido a que no todos los efectos se activan instantáneamente
                # es necesario modificar esto de forma tal que:
                    # O bien la imagen se toma del widget en el que se dibuja (problemas: escala y calidad).
                    # O bien se obtiene el frame de video en el pipe (lo ideal, pero como? :)).
                    # O bien se obtiene el buffer de video en el pipe (como hace record.activity).
            #'''
            if self.update_rafagas:
                # Si se está ejecutando ráfagas, la detiene.
                GObject.source_remove(self.update_rafagas)
                self.update_rafagas = False
                self.re_init()
                return
            
            if self.jamediawebcam.estado != "FotografiandoWebCam":
                # Si no se está fotografiando, toma una fotografía.
                self.jamediawebcam.fotografiar()
                self.toolbarfotografia.set_estado("grabando")
                time.sleep(0.8)
                self.re_init()
            
            else:
                # Si se está fotografiando, reinicia la camara.
                self.re_init()
                
        elif senial == 'configurar':
            # Sólo muestra u oculta controles.
            if self.toolbarfotografiaconfig.get_visible():
                self.toolbarfotografiaconfig.hide()
                self.toolbargstreamerefectos.hide()
                
            else:
                self.update_balance_toolbars()
                self.toolbarfotografiaconfig.show()
                self.toolbargstreamerefectos.show()
        
        elif senial == 'Reset':
            # Resetea completamente la cámara.
            self.reset()
            
    def set_accion_audio(self, widget, senial):
        """Cuando se hace click en grabar solo audio o
        en configurar."""
        
        if senial == 'grabar':
            if self.jamediaaudio.estado != "GrabandoAudio":
                self.jamediaaudio.grabar()
                self.toolbargrabaraudio.set_estado("grabando")
                
            else:
                self.re_init_menu_audio()
                
        #elif senial == 'configurar':
            # Sólo muestra u oculta los controles.
        #    if self.toolbarvideoconfig.get_visible():
        #        self.toolbaraudioconfig.hide()
        #        self.toolbaraudioefectos.hide()
                
        #    else:
        #        #self.update_balance_toolbars()
        #        self.toolbaraudioconfig.show()
        #        self.toolbaraudioefectos.show()
        
        elif senial == 'Reset':
            self.reset_audio_pipe()
            
    def set_accion_video(self, widget, senial):
        """Cuando se hace click en filmar o
        en configurar filmacion."""
        
        if senial == 'filmar':
            if self.jamediawebcam.estado != "GrabandoAudioVideoWebCam":
                # Si no está grabando, graba.
                self.jamediawebcam.grabar()
                self.toolbarvideo.set_estado("grabando")
                
            else:
                # Si está grabando, detiene.
                self.re_init()
                
        elif senial == 'configurar':
            # Sólo muestra u oculta los controles.
            if self.toolbarvideoconfig.get_visible():
                self.toolbarvideoconfig.hide()
                self.toolbargstreamerefectos.hide()
                
            else:
                self.update_balance_toolbars()
                self.toolbarvideoconfig.show()
                self.toolbargstreamerefectos.show()
                
        elif senial == 'Reset':
            self.reset()
            
    def get_menu_base(self, widget):
        """Cuando se sale de un menú particular,
        se vuelve al menú principal."""
        
        if self.update_rafagas:
            GObject.source_remove(self.update_rafagas)
            self.update_rafagas = False
        
        map(self.ocultar, self.controlesdinamicos)
        map(self.mostrar, [self.toolbar,
        self.toolbarprincipal, self.pantalla])
        
        GObject.idle_add(self.re_init)
        
    def get_menu(self, widget, menu):
        """Cuando se hace click en algún botón de
        la toolbar principal, se entra en el menú
        correspondiente o se ejecuta determinada acción."""
        
        map(self.ocultar, self.controlesdinamicos)
        
        if menu == "Filmar":
            map(self.mostrar, [self.toolbarvideo])
            
        elif menu == "Fotografiar":
            map(self.mostrar, [self.toolbarfotografia])
            
        elif menu == "Grabar":
            map(self.mostrar, [self.toolbargrabaraudio])
            self.jamediawebcam.stop()
            GObject.idle_add(self.jamediaaudio.re_init)
            
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
                
            GObject.idle_add(self.jamediaplayer.set_nueva_lista, archivos)
            
        elif menu == "Ver":
            self.jamediawebcam.stop()
            map(self.ocultar, [self.pantalla])
            map(self.mostrar, [self.socketjamimagenes])
            archivos = []
            
            for arch in os.listdir(G.IMAGENES_JAMEDIA_VIDEO):
                ar = os.path.join(G.IMAGENES_JAMEDIA_VIDEO, arch)
                archivos.append([arch, ar])
                
            GObject.idle_add(self.jamimagenes.set_lista, archivos)
            
        elif menu == "Reset":
            map(self.mostrar, [self.toolbar,
                self.toolbarprincipal, self.pantalla])
            GObject.idle_add(self.reset)
        
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
        self.jamediawebcam.reset()
        self.jamediawebcam.stop()
        sys.exit(0)
    
if __name__ == "__main__":
    JAMediaVideo()
    Gtk.main()
    