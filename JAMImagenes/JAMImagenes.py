#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMImagenes.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
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

# Para embeber el Visor de Imagenes en otro sitio:
#   from JAMImagenes import JAMImagenesObject
#   self.socket = Gtk.Socket()
#   self.add(self.socket)
#   self.visor = JAMImagenesObject()
#   self.socket.add_id(self.visor.get_id())

import os
import sys

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import Lista
from JAMediaObjects.JAMediaWidgets import ToolbarReproduccion
from JAMediaObjects.JAMediaWidgets import ToolbarAccion
from JAMediaObjects.JAMediaWidgets import ToolbarSalir

from Widgets import JAMVisor
from Widgets import Toolbar
from Widgets import ToolbarConfig
from Widgets import MenuList

class JAMImagenes(Gtk.Plug):
    """JAMImagenes:
        Visor de Imagenes.
            
        Implementado sobre:
            python 2.7.3 y Gtk 3
        
        Es un Gtk.Plug para embeber en cualquier contenedor
        dentro de otra aplicacion.
        
    Para ello, es necesario crear en la aplicacion donde
    será enbebida JAMImagenes, un socket:
        
    import JAMImagenes
    from JAMImagenes.JAMImagenes import JAMImagenes
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaimagenes = JAMImagenes()
        socket.add_id(self.jamediaimagenes.get_id()
        
    y luego proceder de la siguiente forma:
        
            GObject.idle_add(self.setup_init)
        
        def setup_init(self):
            self.jamediaimagenes.setup_init()
            
    NOTA: Tambien se puede ejecutar JAMImagenes directamente
    mediante python JAMImagenes.py"""
    
    __gsignals__ = {'salir':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """JAMediaImagenes: Gtk.Plug para embeber en otra aplicacion."""
        
        Gtk.Plug.__init__(self, 0L)
        
        self.intervalo = 1000
        self.actualizador = None
        
        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.toolbar_config = ToolbarConfig()
        self.toolbar_accion = ToolbarAccion()
        
        self.visor = JAMVisor()
        self.lista = Lista()
        self.toolbar_reproduccion = ToolbarReproduccion()
        
        panel = Gtk.HPaned()
        
        scroll1 = self.get_scroll()
        scroll1.add_with_viewport (self.visor)
        scroll2 = self.get_scroll()
        scroll2.add_with_viewport (self.lista)
        
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox2.pack_start(scroll2, True, True,0)
        self.vbox2.pack_start(self.toolbar_reproduccion, False, True, 0)
        
        panel.pack1(scroll1, resize=True, shrink=True)
        panel.pack2(self.vbox2, resize=False, shrink=False)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        vbox.pack_start(self.toolbar, False, True, 0)
        vbox.pack_start(self.toolbar_salir, False, True, 0)
        vbox.pack_start(self.toolbar_config, False, True, 0)
        vbox.pack_start(self.toolbar_accion, False, True, 0)
        vbox.pack_start(panel, True, True, 0)
        
        self.controles_dinamicos = [self.toolbar, self.vbox2]
        # [self.toolbar_config, self.toolbar_accion]
        
        self.add(vbox)
        
        self.lista.connect('nueva-seleccion', self.cargar_imagen)
        
        self.toolbar.connect('acercar', self.acercar)
        self.toolbar.connect('alejar', self.alejar)
        self.toolbar.connect('original', self.original)
        self.toolbar.connect('rotar-izquierda', self.rotar_izquierda)
        self.toolbar.connect('rotar-derecha', self.rotar_derecha)
        self.toolbar.connect('configurar', self.configurar)
        
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar_salir.connect('salir', self.emit_salir)
        
        self.toolbar_reproduccion.connect('activar', self.activar)
        self.lista.connect("button-press-event", self.click_derecho_en_lista)
        self.toolbar_config.connect('run', self.set_presentacion)
        self.visor.connect('ocultar_controles', self.ocultar_controles)
        self.visor.connect("button_press_event", self.clicks_en_pantalla)
        
        GObject.idle_add(self.setup_init)
        
    def click_derecho_en_lista(self, widget, event):
        """Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista de reproduccion, borrar el archivo o
        simplemente quitarlo de la lista."""
        
        if self.actualizador: GObject.source_remove(self.actualizador)
        self.actualizador = None
        
        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)
        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(int(pos[0]), int(pos[1]))
        except:
            return
        # TreeView.get_path_at_pos(event.x, event.y) devuelve:
        # * La ruta de acceso en el punto especificado (x, y), en relación con las coordenadas widget
        # * El gtk.TreeViewColumn en ese punto
        # * La coordenada X en relación con el fondo de la celda
        # * La coordenada Y en relación con el fondo de la celda
        if boton == 1:
            return
        elif boton == 3:
            menu = MenuList(widget, boton, pos, tiempo, path, widget.modelo)
            menu.connect('accion', self.set_accion)
            menu.popup(None, None, None, None, boton, tiempo)
        elif boton == 2:
            return
        
    def set_accion(self, widget, lista, accion, iter):
        """Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.
        
        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar."""
        
        self.toolbar_accion.set_accion(lista, accion, iter)
        
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
                
    def ocultar_controles(self, widget, valor):
        """Oculta o muestra los controles."""
        
        if valor and self.toolbar_config.ocultar_controles:
            map(self.ocultar, self.controles_dinamicos)
            map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion, self.toolbar_salir])
        elif not valor:
            map(self.mostrar, self.controles_dinamicos)
            
    def ocultar(self, objeto):
        """Esta funcion es llamada desde self.ocultar_controles()"""
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        """Esta funcion es llamada desde self.ocultar_controles()"""
        
        if not objeto.get_visible(): objeto.show()
        
    def activar(self, widget, senial):
        """Cuando se hace click en siguiente,
        anterior, pausa-play o stop."""
        
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
                
        if senial == 'siguiente':
            self.lista.seleccionar_siguiente()
            self.toolbar_reproduccion.set_playing()
        elif senial == 'atras':
            self.lista.seleccionar_anterior()
            self.toolbar_reproduccion.set_playing()
        elif senial == 'stop':
            if self.actualizador: GObject.source_remove(self.actualizador)
            self.actualizador = None
            self.visor.presentacion = False
            self.toolbar_reproduccion.set_paused()
        elif senial == 'pausa-play':
            if self.actualizador:
                if self.actualizador: GObject.source_remove(self.actualizador)
                self.actualizador = None
                self.visor.presentacion = False
                self.toolbar_reproduccion.set_paused()
            else:
                self.set_presentacion()
                self.toolbar_reproduccion.set_playing()
                
    def configurar(self, widget):
        """Muestra la toolbar de configuraciones."""
        
        if self.actualizador: GObject.source_remove(self.actualizador)
        self.actualizador = None
        
        if self.toolbar_config.get_visible():
            self.toolbar_config.hide()
        else:
            self.toolbar_config.show_all()
        
    def set_presentacion(self, widget = None, intervalo = None):
        """Lanza el modo diapositivas."""
        
        if intervalo and intervalo != None: self.intervalo = intervalo
        if self.actualizador: GObject.source_remove(self.actualizador)
        self.actualizador = None
        self.visor.presentacion = True
        self.actualizador = GObject.timeout_add(self.intervalo, self.handlepresentacion)
    
    def handlepresentacion(self):
        """Cuando está en moodo Diapositivas."""
        
        self.lista.seleccionar_siguiente()
        return True
    
    def setup_init(self):
        print "JAMImagenes => OK"
        self.show_all()
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion, self.toolbar_salir])
                
    def get_scroll(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC,
        Gtk.PolicyType.AUTOMATIC)
        return scroll
        
    def cargar_imagen(self, widget, path):
        """Carga la imagen activa."""
        
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.visor.set_imagen(path)
        
    def limpiar(self):
        """Limpia la lista de imagenes."""
        
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.lista.limpiar()
        # y agregar no pintar imagen
        
    def set_item(self, item):
        """Agrega una imagen a la lista."""
        
        # item = [texto para mostrar, path oculto]
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.lista.limpiar()
        self.lista.agregar_items( [item] )
        self.lista.seleccionar_primero()
        
    def set_lista(self, items):
        """Setea toda la lista de imagenes."""
        
        # items = [ [texto para mostrar, path oculto], . . . ]
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.lista.limpiar()
        self.lista.agregar_items( items )
        self.lista.seleccionar_primero()
        
    def acercar(self, widget):
        
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.visor.presentacion = False
        self.visor.acercar()
        
    def alejar(self, widget):
        
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.visor.presentacion = False
        self.visor.alejar()
        
    def original(self, widget):
        
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.visor.presentacion = False
        self.visor.original()
        
    def rotar_izquierda(self, widget):
        
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.visor.presentacion = False
        self.visor.rotar(-1)
        
    def rotar_derecha(self, widget):
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.visor.presentacion = False
        self.visor.rotar(1)
        
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        self.toolbar_salir.run("JAMImagenes")
        
    def emit_salir(self, widget):
        
        if self.actualizador: GObject.source_remove(self.actualizador)
        self.actualizador = None
        self.visor.presentacion = False
        map(self.ocultar, [self.toolbar_config,
                self.toolbar_accion])
        self.toolbar_reproduccion.set_paused()
        self.emit('salir')
        