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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMedia.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    
class JAMImagenes(Gtk.Plug):
    """
    JAMImagenes:
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
    mediante python JAMImagenes.py
    """
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """
        JAMediaImagenes: Gtk.Plug para embeber en otra aplicacion.
        """
        
        Gtk.Plug.__init__(self, 0L)
        
        self.intervalo = 1000
        self.actualizador = None
        
        from JAMediaObjects.JAMediaWidgets import Lista
        from JAMediaObjects.JAMediaWidgets import ToolbarReproduccion
        from JAMediaObjects.JAMediaWidgets import ToolbarAccion
        from JAMediaObjects.JAMediaWidgets import ToolbarSalir

        from Widgets import VisorImagenes
        from Widgets import Toolbar
        from Widgets import ToolbarConfig
        from Widgets import MenuList

        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.toolbar_config = ToolbarConfig()
        self.toolbar_accion = ToolbarAccion()
        
        self.visor = VisorImagenes()
        self.lista = Lista()
        self.toolbar_reproduccion = ToolbarReproduccion()
        
        panel = Gtk.HPaned()
        
        scroll1 = self.__get_scroll()
        scroll1.add_with_viewport (self.visor)
        scroll2 = self.__get_scroll()
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
        
        self.lista.connect('nueva-seleccion', self.__cargar_imagen)
        
        self.toolbar.connect('acercar', self.__acercar)
        self.toolbar.connect('alejar', self.__alejar)
        self.toolbar.connect('original', self.__original)
        self.toolbar.connect('rotar-izquierda', self.__rotar_izquierda)
        self.toolbar.connect('rotar-derecha', self.__rotar_derecha)
        self.toolbar.connect('configurar', self.__configurar)
        
        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar_salir.connect('salir', self.__emit_salir)
        
        self.toolbar_reproduccion.connect('activar', self.__activar)
        self.lista.connect("button-press-event", self.__click_derecho_en_lista)
        self.toolbar_config.connect('run', self.__set_presentacion)
        self.visor.connect('ocultar_controles', self.__ocultar_controles)
        self.visor.connect("button_press_event", self.__clicks_en_pantalla)
        
        GObject.idle_add(self.__setup_init)
        
    def __click_derecho_en_lista(self, widget, event):
        """
        Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista de reproduccion, borrar el archivo o
        simplemente quitarlo de la lista.
        """
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
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
            menu.connect('accion', self.__set_accion)
            menu.popup(None, None, None, None, boton, tiempo)
            
        elif boton == 2:
            return
        
    def __set_accion(self, widget, lista, accion, iter):
        """
        Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.
        
        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar.
        """
        
        self.toolbar_accion.set_accion(lista, accion, iter)
        
    def __clicks_en_pantalla(self, widget, event):
        """
        Hace fullscreen y unfullscreen sobre la
        ventana principal cuando el usuario hace
        doble click en el visor.
        """
        
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w,h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            
            if ww == w and hh == h:
                ventana.unfullscreen()
                
            else:
                ventana.fullscreen()
                
    def __ocultar_controles(self, widget, valor):
        """
        Oculta o muestra los controles.
        """
        
        if valor and self.toolbar_config.ocultar_controles:
            
            map(self.__ocultar, self.controles_dinamicos)
            
            map(self.__ocultar, [
                self.toolbar_config,
                self.toolbar_accion,
                self.toolbar_salir])
                
        elif not valor:
            map(self.__mostrar, self.controles_dinamicos)
            
    def __ocultar(self, objeto):
        """
        Esta funcion es llamada desde self.ocultar_controles()
        """
        
        if objeto.get_visible(): objeto.hide()
        
    def __mostrar(self, objeto):
        """
        Esta funcion es llamada desde self.ocultar_controles()
        """
        
        if not objeto.get_visible(): objeto.show()
        
    def __activar(self, widget, senial):
        """
        Cuando se hace click en siguiente,
        anterior, pausa-play o stop.
        """
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        if senial == 'siguiente':
            self.lista.seleccionar_siguiente()
            
        elif senial == 'atras':
            self.lista.seleccionar_anterior()
            
        elif senial == 'stop':
            if self.actualizador:
                GObject.source_remove(self.actualizador)
                self.actualizador = None
                
            self.visor.presentacion = False
            self.toolbar_reproduccion.set_paused()
            
        elif senial == 'pausa-play':
            if self.actualizador:
                if self.actualizador:
                    GObject.source_remove(self.actualizador)
                    self.actualizador = None
                    
                self.visor.presentacion = False
                self.toolbar_reproduccion.set_paused()
                
            else:
                self.__set_presentacion()
                
    def __configurar(self, widget):
        """
        Muestra la toolbar de configuraciones.
        """
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
        
        map(self.__ocultar, [
            self.toolbar_accion,
            self.toolbar_salir])
            
        if self.toolbar_config.get_visible():
            self.toolbar_config.hide()
            
        else:
            self.toolbar_config.show_all()
            
        self.toolbar_reproduccion.set_paused()
        
    def __set_presentacion(self, widget = None, intervalo = None):
        """
        Lanza el modo diapositivas.
        """
        
        if intervalo and intervalo != None: self.intervalo = intervalo
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        self.visor.presentacion = True
        self.toolbar_reproduccion.set_playing()
        self.actualizador = GObject.timeout_add(self.intervalo, self.__handle_presentacion)
    
    def __handle_presentacion(self):
        """
        Cuando está en modo Diapositivas.
        """
        
        self.lista.seleccionar_siguiente()
        
        return True
    
    def __setup_init(self):
        
        print "JAMImagenes => OK"
        self.show_all()
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion,
            self.toolbar_salir])
            
    def __get_scroll(self):
        """
        Devuelve un scroll.
        """
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC,
        Gtk.PolicyType.AUTOMATIC)
        
        return scroll
        
    def __cargar_imagen(self, widget, path):
        """
        Carga la imagen activa.
        """
        
        # FIXME: Cuando se selecciona una imagen en la lista
        # y está corriendo modo presentacion, la misma se detiene
        # y la toolbar reproduccion no actualiza el icono play.
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.visor.set_imagen(path)
        
    def limpiar(self):
        """
        Limpia la lista de imagenes.
        """
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.lista.limpiar()
        # y agregar no pintar imagen
        
    def __set_item(self, item):
        """
        Agrega una imagen a la lista.
        """
        
        # item = [texto para mostrar, path oculto]
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.lista.limpiar()
        self.lista.agregar_items( [item] )
        self.lista.seleccionar_primero()
        
    def set_lista(self, items):
        """
        Setea toda la lista de imagenes según items.
        """
        
        # items = [ [texto para mostrar, path oculto], . . . ]
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.lista.limpiar()
        self.lista.agregar_items( items )
        self.lista.seleccionar_primero()
        
    def __acercar(self, widget):
        """
        Zoom in.
        """
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.visor.presentacion = False
        
        self.visor.acercar()
        
    def __alejar(self, widget):
        """
        Zoom out.
        """
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.visor.presentacion = False
        
        self.visor.alejar()
        
    def __original(self, widget):
        """
        Vuelve al tamaño original de la imagen.
        """
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.visor.presentacion = False
        
        self.visor.original()
        
    def __rotar_izquierda(self, widget):
        """
        Rota la imagen a la izquierda.
        """
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.visor.presentacion = False
        
        self.visor.rotar(-1)
        
    def __rotar_derecha(self, widget):
        """
        Rota la imagen a la derecha.
        """
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.visor.presentacion = False
        
        self.visor.rotar(1)
        
    def __confirmar_salir(self, widget = None, senial = None):
        """
        Recibe salir y lo pasa a la toolbar de confirmación.
        """
        
        map(self.__ocultar, [self.toolbar_config])
        
        self.toolbar_salir.run("JAMImagenes")
        
    def __emit_salir(self, widget):
        """
        Emite Salir.
        """
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        self.visor.presentacion = False
        
        map(self.__ocultar, [
            self.toolbar_config,
            self.toolbar_accion])
            
        self.toolbar_reproduccion.set_paused()
        
        self.emit('salir')
        