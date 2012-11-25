#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaVideoAplicaciones.py por:
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
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir
from JAMediaObjects.JAMediaWidgets import Visor
from JAMediaObjects.JAMediaWidgets import WidgetsGstreamerEfectos
from JAMediaObjects.JAMediaGstreamer.JAMediaWebCam import JAMediaWebCam
from JAMediaObjects.JAMediaGstreamer.JAMediaAudio import JAMediaAudio

from Widgets import ToolbarVideo
from Widgets import ToolbarFotografia
from Widgets import ToolbarGrabarAudio

from Widgets import ToolbarBalanceConfig
from Widgets import WidgetEfecto_en_Pipe

import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

GObject.threads_init()
Gdk.threads_init()

class JAMediaVideoWidget(Gtk.Plug):
    """Plug - Interfaz para Webcam con grabación de audio y video."""
        
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """JAMediaVideoWidget: Gtk.Plug para embeber en otra aplicacion."""
        
        Gtk.Plug.__init__(self, 0L)
        
        self.toolbar_salir = None
        self.toolbar = None
        self.pantalla = None
        self.balance_widget = None
        self.controles_dinamicos = []
        self.jamediawebcam = None
        self.box_config = None
        self.widget_efectos = None
        self.hbox_efectos_en_pipe = None
        
        self.show_all()
        
    def setup_init(self):
        """Se crea la interfaz grafica,
        se setea y se empaqueta todo."""
        
        # Widgets Base: - vbox - toolbars - panel
        basebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbar_salir = ToolbarSalir()
        self.toolbar = ToolbarVideo()
        hpanel = Gtk.HPaned()
        
        basebox.pack_start(self.toolbar_salir, False, True, 0)
        basebox.pack_start(self.toolbar, False, True, 0)
        basebox.pack_start(hpanel, True, True, 0)
        
        self.add(basebox)
        
        # Panel lado Izquierdo: vbox - pantalla - hbox_efectos_aplicados
        vbox_izq_panel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.pantalla = Visor()
        eventbox = Gtk.EventBox()
        eventbox.modify_bg(0, G.NEGRO)
        
        self.hbox_efectos_en_pipe = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.hbox_efectos_en_pipe.set_size_request(-1, G.get_pixels(1.0))
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scroll.add_with_viewport(eventbox)
        
        eventbox.add(self.hbox_efectos_en_pipe)
        
        vbox_izq_panel.pack_start(self.pantalla, True, True, 0)
        vbox_izq_panel.pack_start(scroll, False, False, 0)
        
        hpanel.pack1(vbox_izq_panel, resize = True, shrink = True)
        
        # Panel lado Derecho: eventbox - vbox - scroll - balance_widget - widget_efectos
        self.box_config = Gtk.EventBox()
        self.box_config.set_size_request(G.get_pixels(5.0), -1)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.balance_widget = ToolbarBalanceConfig()
        vbox.pack_start(self.balance_widget , False, True, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(vbox)
        self.box_config.add(scroll)
        
        self.widget_efectos = WidgetsGstreamerEfectos()
        
        vbox.pack_start(self.widget_efectos , False, True, 0)
        
        hpanel.pack2(self.box_config, resize = False, shrink = False)
        
        self.show_all()
        self.realize()
        
        xid = self.pantalla.get_property('window').get_xid()
        self.jamediawebcam = JAMediaWebCam(xid)
        
        self.controles_dinamicos = [
            self.toolbar_salir,
            self.box_config,
            ]
            
        map(self.ocultar, self.controles_dinamicos)
        
        self.pantalla.connect("button_press_event", self.clicks_en_pantalla)
        
        self.toolbar.connect("rotar", self.set_rotacion)
        self.toolbar.connect("accion", self.set_accion)
        self.toolbar.connect('salir', self.confirmar_salir)
        
        self.balance_widget.connect('valor', self.set_balance)
        
        self.widget_efectos.connect("click_efecto", self.click_efecto)
        #self.widget_efectos.connect("quitar_efecto", self.quitar_efecto)
        
        self.toolbar_salir.connect('salir', self.emit_salir)
        
    def reset(self):
        """Resetea la cámara quitando los efectos y
        actualiza los widgets correspondientes."""
        
        self.toolbar.set_estado("detenido")
        for efecto in self.hbox_efectos_en_pipe.get_children():
            efecto.destroy()
            
        for button in self.widget_efectos.gstreamer_efectos.get_children():
            button.des_seleccionar()
            
        self.jamediawebcam.reset()
        GObject.idle_add(self.update_balance_toolbars)
        
    def re_init(self):
        """Vuelve la camara al estado original manteniendo efectos."""
        
        self.toolbar.set_estado("detenido")
        self.jamediawebcam.re_init()
        GObject.idle_add(self.update_balance_toolbars)
        
    def cargar_efectos(self, efectos):
        """Agrega los widgets con efectos a la paleta de configuración."""
        
        self.widget_efectos.cargar_efectos(efectos)
        
    def click_efecto(self, widget, nombre_efecto):
        """Recibe el nombre del efecto sobre el que
        se ha hecho click y decide si debe agregarse
        al pipe de JAMediaWebcam."""
        
        agregar = False
        
        if self.jamediawebcam.efectos:
            if not nombre_efecto in self.jamediawebcam.efectos:
            # Si el efecto no está en el pipe.
                agregar = True
            
        else:
            # Si no se han agregado efectos.
            agregar = True
            
        if agregar:
            if self.jamediawebcam.estado == "GrabandoAudioVideoWebCam":
                self.jamediawebcam.re_init()
                self.toolbar.set_estado("detenido")
            
            # Agrega un widget a self.hbox_efectos_en_pipe
            botonefecto = WidgetEfecto_en_Pipe()
            botonefecto.set_tooltip(nombre_efecto)
            lado = G.get_pixels(1.0)
            botonefecto.set_tamanio(lado, lado)
            
            archivo = os.path.join(JAMediaObjectsPath, "Iconos", '%s.png' %(nombre_efecto))
            
            if not os.path.exists(archivo):
                archivo = os.path.join(JAMediaObjectsPath, "Iconos", '%s.png' %('ver'))
                
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, lado, lado)
            botonefecto.imagen.set_from_pixbuf(pixbuf)
            
            self.hbox_efectos_en_pipe.pack_start(botonefecto, False, False, 0)
            self.jamediawebcam.agregar_efecto( nombre_efecto )
            
        else:
            # Si el usuario hace click sobre el botón de un efecto
            # que ya se encuentra en el pipe de la camara, se quita
            # el efecto del pipe y se deseleccia el botón correspondiente.
            if self.jamediawebcam.estado == "GrabandoAudioVideoWebCam":
                self.jamediawebcam.re_init()
                self.toolbar.set_estado("detenido")
                
            self.widget_efectos.des_seleccionar_efecto(nombre_efecto)
            
            # Quitar el widget de self.hbox_efectos_en_pipe
            for efecto in self.hbox_efectos_en_pipe.get_children():
                if efecto.get_tooltip_text() == nombre_efecto:
                    efecto.destroy()
                    break
            
            self.jamediawebcam.quitar_efecto(nombre_efecto)
        
    def update_balance_toolbars(self):
        """Actualiza las toolbars de balance en video."""
        
        config = self.jamediawebcam.get_balance()
        
        self.balance_widget.set_balance(
            brillo = config['brillo'],
            contraste = config['contraste'],
            saturacion = config['saturacion'],
            hue = config['hue'])
            
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
            
    def set_rotacion(self, widget, valor):
        """Recibe rotación y la pasa a la webcam."""
        
        self.jamediawebcam.rotar(valor)
        
    def set_accion(self, widget, senial):
        """Cuando se hace click en filmar o
        en configurar filmacion."""
        
        if senial == 'filmar':
            if self.jamediawebcam.estado != "GrabandoAudioVideoWebCam":
                # Si no está grabando, graba.
                self.jamediawebcam.grabar()
                self.toolbar.set_estado("grabando")
                
            else:
                # Si está grabando, detiene.
                self.re_init()
            
        elif senial == 'configurar':
            # Sólo muestra u oculta los controles.
            if self.box_config.get_visible():
                self.box_config.hide()
                
            else:
                self.box_config.show()
                GObject.idle_add(self.update_balance_toolbars)
                
        elif senial == 'Reset':
            self.reset()
            
    def play(self):
        
        GObject.idle_add(self.jamediawebcam.re_init)
        
    def ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
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
                
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        self.toolbar_salir.run("Menú Video.")
        
    def emit_salir(self, widget):
        """Emite salir para que cuando esta embebida, la
        aplicacion decida que hacer, si salir, o cerrar solo
        la aplicacion embebida."""
        
        self.reset()
        self.jamediawebcam.stop()
        self.emit('salir')
    

class JAMediaFotografiaWidget(Gtk.Plug):
    """Plug - Interfaz para Webcam con grabación de audio y video."""
        
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """JAMediaFotografiaWidget: Gtk.Plug para embeber en otra aplicacion."""
        
        Gtk.Plug.__init__(self, 0L)
        
        self.toolbar_salir = None
        self.toolbar = None
        self.pantalla = None
        self.balance_widget = None
        self.controles_dinamicos = []
        self.jamediawebcam = None
        self.box_config = None
        self.widget_efectos = None
        self.hbox_efectos_en_pipe = None
        
        self.show_all()
        
    def setup_init(self):
        """Se crea la interfaz grafica,
        se setea y se empaqueta todo."""
        
        # Widgets Base: - vbox - toolbars - panel
        basebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbar_salir = ToolbarSalir()
        self.toolbar = ToolbarFotografia()
        hpanel = Gtk.HPaned()
        
        basebox.pack_start(self.toolbar_salir, False, True, 0)
        basebox.pack_start(self.toolbar, False, True, 0)
        basebox.pack_start(hpanel, True, True, 0)
        
        self.add(basebox)
        
        # Panel lado Izquierdo: vbox - pantalla - hbox_efectos_aplicados
        vbox_izq_panel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.pantalla = Visor()
        eventbox = Gtk.EventBox()
        eventbox.modify_bg(0, G.NEGRO)
        
        self.hbox_efectos_en_pipe = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.hbox_efectos_en_pipe.set_size_request(-1, G.get_pixels(1.0))
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scroll.add_with_viewport(eventbox)
        
        eventbox.add(self.hbox_efectos_en_pipe)
        
        vbox_izq_panel.pack_start(self.pantalla, True, True, 0)
        vbox_izq_panel.pack_start(scroll, False, False, 0)
        
        hpanel.pack1(vbox_izq_panel, resize = True, shrink = True)
        
        # Panel lado Derecho: eventbox - vbox - scroll - balance_widget - widget_efectos
        self.box_config = Gtk.EventBox()
        self.box_config.set_size_request(G.get_pixels(5.0), -1)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.balance_widget = ToolbarBalanceConfig()
        vbox.pack_start(self.balance_widget , False, True, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(vbox)
        self.box_config.add(scroll)
        
        self.widget_efectos = WidgetsGstreamerEfectos()
        
        vbox.pack_start(self.widget_efectos , False, True, 0)
        
        hpanel.pack2(self.box_config, resize = False, shrink = False)
        
        self.show_all()
        self.realize()
        
        xid = self.pantalla.get_property('window').get_xid()
        self.jamediawebcam = JAMediaWebCam(xid)
        
        self.controles_dinamicos = [
            self.toolbar_salir,
            self.box_config,
            ]
            
        map(self.ocultar, self.controles_dinamicos)
        
        self.pantalla.connect("button_press_event", self.clicks_en_pantalla)
        
        self.toolbar.connect("rotar", self.set_rotacion)
        self.toolbar.connect("accion", self.set_accion)
        self.toolbar.connect('salir', self.confirmar_salir)
        
        self.balance_widget.connect('valor', self.set_balance)
        
        self.widget_efectos.connect("click_efecto", self.click_efecto)
        #self.widget_efectos.connect("quitar_efecto", self.quitar_efecto)
        
        self.toolbar_salir.connect('salir', self.emit_salir)
        
    def reset(self):
        """Resetea la cámara quitando los efectos y
        actualiza los widgets correspondientes."""
        
        self.toolbar.set_estado("detenido")
        for efecto in self.hbox_efectos_en_pipe.get_children():
            efecto.destroy()
            
        for button in self.widget_efectos.gstreamer_efectos.get_children():
            button.des_seleccionar()
            
        self.jamediawebcam.reset()
        GObject.idle_add(self.update_balance_toolbars)
        
    def re_init(self):
        """Vuelve la camara al estado original manteniendo efectos."""
        
        self.toolbar.set_estado("detenido")
        self.jamediawebcam.re_init()
        GObject.idle_add(self.update_balance_toolbars)
        
    def cargar_efectos(self, efectos):
        """Agrega los widgets con efectos a la paleta de configuración."""
        
        self.widget_efectos.cargar_efectos(efectos)
    
    def click_efecto(self, widget, nombre_efecto):
        """Recibe el nombre del efecto sobre el que
        se ha hecho click y decide si debe agregarse
        al pipe de JAMediaWebcam."""
        
        agregar = False
        
        if self.jamediawebcam.efectos:
            if not nombre_efecto in self.jamediawebcam.efectos:
            # Si el efecto no está en el pipe.
                agregar = True
            
        else:
            # Si no se han agregado efectos.
            agregar = True
            
        if agregar:
            if self.jamediawebcam.estado == "FotografiandoWebCam":
                self.jamediawebcam.re_init()
                self.toolbar.set_estado("detenido")
            
            # Agrega un widget a self.hbox_efectos_en_pipe
            botonefecto = WidgetEfecto_en_Pipe()
            botonefecto.set_tooltip(nombre_efecto)
            lado = G.get_pixels(1.0)
            botonefecto.set_tamanio(lado, lado)
            
            archivo = os.path.join(JAMediaObjectsPath, "Iconos", '%s.png' %(nombre_efecto))
            
            if not os.path.exists(archivo):
                archivo = os.path.join(JAMediaObjectsPath, "Iconos", '%s.png' %('ver'))
                
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, lado, lado)
            botonefecto.imagen.set_from_pixbuf(pixbuf)
            
            self.hbox_efectos_en_pipe.pack_start(botonefecto, False, False, 0)
            self.jamediawebcam.agregar_efecto( nombre_efecto )
            
        else:
            # Si el usuario hace click sobre el botón de un efecto
            # que ya se encuentra en el pipe de la camara, se quita
            # el efecto del pipe y se deseleccia el botón correspondiente.
            if self.jamediawebcam.estado == "FotografiandoWebCam":
                self.jamediawebcam.re_init()
                self.toolbar.set_estado("detenido")
                
            self.widget_efectos.des_seleccionar_efecto(nombre_efecto)
            
            # Quitar el widget de self.hbox_efectos_en_pipe
            for efecto in self.hbox_efectos_en_pipe.get_children():
                if efecto.get_tooltip_text() == nombre_efecto:
                    efecto.destroy()
                    break
            
            self.jamediawebcam.quitar_efecto(nombre_efecto)
        
    def update_balance_toolbars(self):
        """Actualiza las toolbars de balance en video."""
        
        config = self.jamediawebcam.get_balance()
        
        self.balance_widget.set_balance(
            brillo = config['brillo'],
            contraste = config['contraste'],
            saturacion = config['saturacion'],
            hue = config['hue'])
            
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
            
    def set_rotacion(self, widget, valor):
        """Recibe rotación y la pasa a la webcam."""
        
        self.jamediawebcam.rotar(valor)
    
    def set_accion(self, widget, senial):
        """Cuando se hace click en fotografiar o
        en configurar filmacion."""
        
        if senial == 'fotografiar':
            if self.jamediawebcam.estado != "FotografiandoWebCam":
                # Si no está fotografiando, fotografía.
                self.jamediawebcam.fotografiar()
                self.toolbar.set_estado("grabando")
                # FIXME: Hay que mejorar las fotografias.
                time.sleep(3.5)
                self.re_init()
                
            else:
                # Si está grabando, detiene.
                self.re_init()
            
        elif senial == 'configurar':
            # Sólo muestra u oculta los controles.
            if self.box_config.get_visible():
                self.box_config.hide()
                
            else:
                self.box_config.show()
                GObject.idle_add(self.update_balance_toolbars)
                
        elif senial == 'Reset':
            self.reset()
            
    def play(self):
        
        GObject.idle_add(self.jamediawebcam.re_init)
        
    def ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
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
                
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        self.toolbar_salir.run("Menú Video.")
        
    def emit_salir(self, widget):
        """Emite salir para que cuando esta embebida, la
        aplicacion decida que hacer, si salir, o cerrar solo
        la aplicacion embebida."""
        
        self.reset()
        self.jamediawebcam.stop()
        self.emit('salir')
        
class JAMediaAudioWidget(Gtk.Plug):
    """Plug - Interfaz para Webcam con grabación de audio."""
        
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """JAMediaAudioWidget: Gtk.Plug para embeber en otra aplicacion."""
        
        Gtk.Plug.__init__(self, 0L)
        
        self.toolbar_salir = None
        self.toolbar = None
        self.pantalla = None
        self.balance_widget = None
        self.controles_dinamicos = []
        self.jamediawebcam = None
        self.box_config = None
        self.widget_efectos = None
        self.hbox_efectos_en_pipe = None
        
        self.show_all()
        
    def setup_init(self):
        """Se crea la interfaz grafica,
        se setea y se empaqueta todo."""
        
        # Widgets Base: - vbox - toolbars - panel
        basebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbar_salir = ToolbarSalir()
        self.toolbar = ToolbarGrabarAudio()
        hpanel = Gtk.HPaned()
        
        basebox.pack_start(self.toolbar_salir, False, True, 0)
        basebox.pack_start(self.toolbar, False, True, 0)
        basebox.pack_start(hpanel, True, True, 0)
        
        self.add(basebox)
        
        # Panel lado Izquierdo: vbox - pantalla - hbox_efectos_aplicados
        vbox_izq_panel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.pantalla = Visor()
        eventbox = Gtk.EventBox()
        eventbox.modify_bg(0, G.NEGRO)
        
        self.hbox_efectos_en_pipe = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.hbox_efectos_en_pipe.set_size_request(-1, G.get_pixels(1.0))
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scroll.add_with_viewport(eventbox)
        
        eventbox.add(self.hbox_efectos_en_pipe)
        
        vbox_izq_panel.pack_start(self.pantalla, True, True, 0)
        vbox_izq_panel.pack_start(scroll, False, False, 0)
        
        hpanel.pack1(vbox_izq_panel, resize = True, shrink = True)
        
        # Panel lado Derecho: eventbox - vbox - scroll - balance_widget - widget_efectos
        self.box_config = Gtk.EventBox()
        self.box_config.set_size_request(G.get_pixels(5.0), -1)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.balance_widget = ToolbarBalanceConfig()
        vbox.pack_start(self.balance_widget , False, True, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(vbox)
        self.box_config.add(scroll)
        
        self.widget_efectos = WidgetsGstreamerEfectos()
        
        vbox.pack_start(self.widget_efectos , False, True, 0)
        
        hpanel.pack2(self.box_config, resize = False, shrink = False)
        
        self.show_all()
        self.realize()
        
        xid = self.pantalla.get_property('window').get_xid()
        self.jamediawebcam = JAMediaAudio(xid)
        
        self.controles_dinamicos = [
            self.toolbar_salir,
            self.box_config,
            ]
            
        map(self.ocultar, self.controles_dinamicos)
        
        self.pantalla.connect("button_press_event", self.clicks_en_pantalla)
        
        self.toolbar.connect("rotar", self.set_rotacion)
        self.toolbar.connect("accion", self.set_accion)
        self.toolbar.connect('salir', self.confirmar_salir)
        
        self.balance_widget.connect('valor', self.set_balance)
        
        #self.widget_efectos.connect("click_efecto", self.click_efecto)
        #self.widget_efectos.connect("quitar_efecto", self.quitar_efecto)
        
        self.toolbar_salir.connect('salir', self.emit_salir)
        
    def reset(self):
        """Resetea la cámara quitando los efectos y
        actualiza los widgets correspondientes."""
        
        self.toolbar.set_estado("detenido")
        for efecto in self.hbox_efectos_en_pipe.get_children():
            efecto.destroy()
            
        for button in self.widget_efectos.gstreamer_efectos.get_children():
            button.des_seleccionar()
            
        self.jamediawebcam.reset()
        GObject.idle_add(self.update_balance_toolbars)
        
    def re_init(self):
        """Vuelve la camara al estado original manteniendo efectos."""
        
        self.toolbar.set_estado("detenido")
        self.jamediawebcam.re_init()
        GObject.idle_add(self.update_balance_toolbars)
        
    def cargar_efectos(self, efectos):
        """Agrega los widgets con efectos a la paleta de configuración."""
        
        self.widget_efectos.cargar_efectos(efectos)
    '''
    def click_efecto(self, widget, nombre_efecto):
        """Recibe el nombre del efecto sobre el que
        se ha hecho click y decide si debe agregarse
        al pipe de JAMediaWebcam."""
        
        agregar = False
        
        if self.jamediawebcam.efectos:
            if not nombre_efecto in self.jamediawebcam.efectos:
            # Si el efecto no está en el pipe.
                agregar = True
            
        else:
            # Si no se han agregado efectos.
            agregar = True
            
        if agregar:
            if self.jamediawebcam.estado == "FotografiandoWebCam":
                self.jamediawebcam.re_init()
                self.toolbar.set_estado("detenido")
            
            # Agrega un widget a self.hbox_efectos_en_pipe
            botonefecto = WidgetEfecto_en_Pipe()
            botonefecto.set_tooltip(nombre_efecto)
            lado = G.get_pixels(1.0)
            botonefecto.set_tamanio(lado, lado)
            
            archivo = os.path.join(JAMediaObjectsPath, "Iconos", '%s.png' %(nombre_efecto))
            
            if not os.path.exists(archivo):
                archivo = os.path.join(JAMediaObjectsPath, "Iconos", '%s.png' %('ver'))
                
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, lado, lado)
            botonefecto.imagen.set_from_pixbuf(pixbuf)
            
            self.hbox_efectos_en_pipe.pack_start(botonefecto, False, False, 0)
            self.jamediawebcam.agregar_efecto( nombre_efecto )
            
        else:
            # Si el usuario hace click sobre el botón de un efecto
            # que ya se encuentra en el pipe de la camara, se quita
            # el efecto del pipe y se deseleccia el botón correspondiente.
            if self.jamediawebcam.estado == "FotografiandoWebCam":
                self.jamediawebcam.re_init()
                self.toolbar.set_estado("detenido")
                
            self.widget_efectos.des_seleccionar_efecto(nombre_efecto)
            
            # Quitar el widget de self.hbox_efectos_en_pipe
            for efecto in self.hbox_efectos_en_pipe.get_children():
                if efecto.get_tooltip_text() == nombre_efecto:
                    efecto.destroy()
                    break
            
            self.jamediawebcam.quitar_efecto(nombre_efecto)'''
        
    def update_balance_toolbars(self):
        """Actualiza las toolbars de balance en video."""
        
        config = self.jamediawebcam.get_balance()
        
        self.balance_widget.set_balance(
            brillo = config['brillo'],
            contraste = config['contraste'],
            saturacion = config['saturacion'],
            hue = config['hue'])
            
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
            
    def set_rotacion(self, widget, valor):
        """Recibe rotación y la pasa a la webcam."""
        
        self.jamediawebcam.rotar(valor)
    
    def set_accion(self, widget, senial):
        """Cuando se hace click en fotografiar o
        en configurar filmacion."""
        
        if senial == 'grabar':
            if self.jamediawebcam.estado != "GrabandoAudio":
                # Si no está fotografiando, fotografía.
                self.jamediawebcam.grabar()
                self.toolbar.set_estado("grabando")
                
            else:
                # Si está grabando, detiene.
                self.re_init()
            
        elif senial == 'configurar':
            # Sólo muestra u oculta los controles.
            if self.box_config.get_visible():
                self.box_config.hide()
                
            else:
                self.box_config.show()
                GObject.idle_add(self.update_balance_toolbars)
                
        elif senial == 'Reset':
            self.reset()
            
    def play(self):
        
        GObject.idle_add(self.jamediawebcam.re_init)
        
    def ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
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
                
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        self.toolbar_salir.run("Menú Audio.")
        
    def emit_salir(self, widget):
        """Emite salir para que cuando esta embebida, la
        aplicacion decida que hacer, si salir, o cerrar solo
        la aplicacion embebida."""
        
        self.reset()
        self.jamediawebcam.stop()
        self.emit('salir')
        