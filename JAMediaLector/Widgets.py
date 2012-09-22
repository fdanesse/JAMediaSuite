#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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

# http://www.roojs.org/seed/gir-1.1-gtk-2.0/Poppler.Page.html

import os

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import Visor
from JAMediaObjects.JAMediaWidgets import JAMediaButton

import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class Toolbar(Gtk.Toolbar):
    """Toolbar principal de JAMediaLector."""
    
    __gsignals__ = {
    'abrir':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, []),
    'config':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, []),
    'salir':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, [])}
    
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaLector.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        #self.insert(G.get_separador(draw = False, ancho = 1, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "iconplay.png")
        self.abrir = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        self.abrir.set_tooltip_text("Abrir un Archivo.")
        self.abrir.connect("clicked", self.emit_abrir)
        self.insert(self.abrir, -1)
        
        #self.insert(G.get_separador(draw = False, ancho = 1, expand = False), -1)

        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "configurar.png")
        self.configurar = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        self.configurar.set_tooltip_text("Configuraciones.")
        self.configurar.connect("clicked", self.emit_config)
        self.insert(self.configurar, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","ceibaljam.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        #self.insert(G.get_separador(draw = False, ancho = 1, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","uruguay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        #self.insert(G.get_separador(draw = False, ancho = 1, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","licencia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        #self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("fdanesse@gmail.com")
        self.label.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","salir.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        self.show_all()
        
    def emit_config(self, widget):
        """Cuando se hace click en el boton configurar
        de la toolbar principal de JAMedia."""
        
        self.emit('config')
        
    def emit_abrir(self, widget):
        
        self.emit('abrir')
        
    def salir(self, widget):
        """Cuando se hace click en el boton salir
        de la toolbar principal."""
        
        self.emit('salir')

class ToolbarTry(Gtk.Toolbar):
    """Toolbar para informacion."""
    
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.show_all()
        
class ToolbarLector(Gtk.Toolbar):
    """Toolbar con funcionalidades para
    el lector pdf."""
    
    __gsignals__ = {
    'acercar': (GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, ([])),
    'alejar': (GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, ([])),
    'original': (GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, ([])),
    'rotar-izquierda': (GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, ([])),
    'rotar-derecha': (GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, ([]))}
    
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        
        #self.insert(get_separador(draw = False, ancho = 3, expand = False), -1)
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","escalaoriginal.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(65000, 65000, 65000), pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Original")
        boton.connect("clicked", self.original)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","alejar.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(65000, 65000, 65000), pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Alejar")
        boton.connect("clicked", self.alejar)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","acercar.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(65000, 65000, 65000), pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Acercar")
        boton.connect("clicked", self.acercar)
        self.insert(boton, -1)
        '''
        self.insert(G.get_separador(draw = True, ancho = 0, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","rotar.png")
        boton = G.get_boton(archivo, flip = False, color = Gdk.Color(65000, 65000, 65000))
        boton.set_tooltip_text("Rotar")
        boton.connect("clicked", self.rotar_izquierda)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","rotar.png")
        boton = G.get_boton(archivo, flip = True, color = Gdk.Color(65000, 65000, 65000))
        boton.set_tooltip_text("Rotar")
        boton.connect("clicked", self.rotar_derecha)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = True, ancho = 0, expand = False), -1)'''
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
           
    def acercar(self, widget):
        self.emit("acercar")

    def alejar(self, widget):
        self.emit("alejar")
        
    def original(self, widget):
        self.emit("original")
        
    def rotar_izquierda(self, widget):
        self.emit("rotar_izquierda")
        
    def rotar_derecha(self, widget):
        self.emit("rotar_derecha")

class ToolbarPaginas(Gtk.Box):
    """Toolbara desplazarse por las páginas de un pdf."""
    
    __gsignals__ = {"activar":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        
        self.botonsiguiente = G.get_boton(os.path.join(JAMediaObjectsPath,
            "Iconos", "siguiente.png"), pixels = G.get_pixels(0.8))
        self.botonsiguiente.set_tooltip_text("Siguiente")
        self.botonsiguiente.connect("clicked", self.clickensiguiente)
        self.pack_end(self.botonsiguiente, False, True, 3)
        
        self.label = Gtk.Label("pág: - de ----")
        self.pack_end(self.label, False, True, 3)
        
        self.botonatras = G.get_boton(os.path.join(JAMediaObjectsPath,
            "Iconos", "siguiente.png"), flip = True, pixels = G.get_pixels(0.8))
        self.botonatras.set_tooltip_text("Anterior")
        self.botonatras.connect("clicked", self.clickenatras)
        self.pack_end(self.botonatras, False, True, 0)
        
        self.show_all()
        
    def set_pagina(self, pag, paginas):
        if paginas:
            self.label.set_text("pág: %s de %s" % (pag, paginas))
        else:
            self.label.set_text("pág: - de ----")
        
    def clickenatras(self, widget= None, event= None):
        self.emit("activar", "atras")
        
    def clickensiguiente(self, widget= None, event= None):
        self.emit("activar", "siguiente")
        
class PreviewContainer(Gtk.Box):
    """Contenedor de previews de paginas en pdf"""
    
    __gsignals__ = {"nueva_seleccion":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_INT,))}
    
    def __init__(self):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)
        self.item_seleccionado = None
        self.show_all()
        
    def limpiar(self):
        """Elimina Todos los previews de paginas pdf"""
        
        for child in self.get_children():
            self.remove(child)
            child.destroy()
            
    def llenar(self, documento):
        """Genera todos los previews del documento cargado"""
        
        self.limpiar()
        paginas = documento.get_n_pages()
        for pagina in range(paginas):
            pagina = documento.get_page(pagina)
            preview = Preview(pagina)
            preview.connect("clicked", self.nueva_seleccion)
            preview.set_tooltip("Pág: %s" % (pagina))
            preview.show_all()
            self.pack_start(preview, False, False, 0)
        
        self.get_children()[0].seleccionar()
        self.emit("nueva_seleccion", 0)
        
    def nueva_seleccion(self, widget, event):
        """Cuando se selecciona una pagina en los previews"""
        
        self.item_seleccionado = widget
        previews = self.get_children()
        map(self.des_seleccionar, previews)
        index = previews.index(widget)
        self.emit("nueva_seleccion", index)
        
    def seleccionar(self, index):
        """Manda seleccionar un preview"""
        
        previews = self.get_children()
        preview = previews[index]
        preview.seleccionar()
        self.nueva_seleccion(preview, None)
        
    def des_seleccionar(self, objeto):
        """Deselecciona todos los previews menos el que
        el usuario ha seleccionado."""
        
        if objeto.estado_select and objeto != self.item_seleccionado:
            objeto.des_seleccionar()

class Preview(JAMediaButton):
    """Preview para las paginas del documento pdf."""
    
    def __init__(self, pagina):
        
        JAMediaButton.__init__(self)
        
        self.color = Gdk.Color(65000,65000,50000)
        
        for child in self.get_children():
            self.remove(child)
            child.destroy()
        
        self.pagina = pagina
        self.zoom = 0.2
        self.set_zoom(self.zoom)

    def seleccionar(self):
        """Marca como seleccionado"""
        
        self.estado_select = True
        self.colornormal = self.color
        self.colorselect = self.color
        self.colorclicked = self.color
        self.modify_bg(0, self.colornormal)
        
    def des_seleccionar(self):
        """Desmarca como seleccionado"""
        
        self.estado_select = False
        self.colornormal = G.BLANCO
        self.colorselect = G.AMARILLO
        self.colorclicked = self.color
        self.modify_bg(0, self.colornormal)
        
    def set_zoom(self, zoom):
        self.zoom = zoom
        if self.zoom <= 0.2: self.zoom = 0.2
        w,h = self.pagina.get_size()
        w,h = (int(w * self.zoom), int(h * self.zoom))
        self.set_size_request( int(w), int(h) )
        
    def do_draw(self, context):
        if not self.pagina: return
        context.scale(self.zoom, self.zoom)
        self.pagina.render(context)
        
    def set_imagen(self, archivo = None):
        pass
        
class Drawing(Visor):
    """Donde se dibujan las paginas del documento"""
    
    def __init__(self):
        Visor.__init__(self)
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(65000, 65000, 65000))
        self.pagina = None
        self.zoom = 1.0
        self.show_all()
        
    def set_pagina(self, pagina):
        """Setea la pagina activa para dibujarla"""
        
        if pagina:
            self.pagina = pagina
            w,h = self.pagina.get_size()
            self.set_size_request( int(w), int(h) )
        else:
            self.pagina = None
        self.queue_draw()
        
    def acercar(self, widget = None):
        self.set_zoom(self.zoom + 0.2)
        
    def alejar(self, widget = None):
        self.set_zoom(self.zoom - 0.2)
        
    def original(self, widget = None):
        self.set_zoom(1.0)
        
    def set_zoom(self, zoom):
        self.zoom = zoom
        if self.zoom <= 0.2: self.zoom = 0.2
        w,h = self.pagina.get_size()
        w,h = (int(w * self.zoom), int(h * self.zoom))
        self.set_size_request( int(w), int(h) )
        self.get_property('window').invalidate_rect(self.get_allocation(), True)
        self.get_property('window').process_updates(True)
        
    def do_draw(self, context):
        if not self.pagina: return
        context.scale(self.zoom, self.zoom)
        self.pagina.render(context)
        
class Selector_de_Archivos (Gtk.FileChooserDialog):
    """Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio."""
    
    __gsignals__ = {'archivos-seleccionados':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self, jamedialector):
        Gtk.FileChooserDialog.__init__(self, title = "Abrir Archivos pdf",
        parent = jamedialector, action = Gtk.FileChooserAction.OPEN)
        self.set_default_size( 640, 480 )
        self.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        self.set_current_folder_uri("file:///media")
        self.set_select_multiple(False)
        
        # extras
        hbox = Gtk.HBox()
        boton_abrir_directorio = Gtk.Button("Abrir")
        boton_salir = Gtk.Button("Salir")
        hbox.pack_end(boton_salir, True, True, 5)
        hbox.pack_end(boton_abrir_directorio, True, True, 5)
        self.set_extra_widget(hbox)
        
        filter = Gtk.FileFilter()
        filter.set_name("Archivos")
        filter.add_mime_type("application/pdf")
        filter.add_mime_type("image/vnd.djvu")
        filter.add_mime_type("image/x.djvu")
        filter.add_mime_type("text/plain")
        self.add_filter(filter)
        
        self.add_shortcut_folder_uri("file:///media/")
        
        # Callbacks
        boton_salir.connect("clicked", self.salir)
        boton_abrir_directorio.connect("clicked",self.abrir_directorio)
        
        self.show_all()
        self.resize( 640, 480 )
        
    def abrir_directorio(self, widget):
        """Manda una señal con el archivo seleccionado."""
        
        self.emit('archivos-seleccionados', self.get_filenames()[0])
        self.salir(None)
        
    def salir(self, widget):
        self.destroy()
        
class TextView(Gtk.TextView):
    """Visor de archivos de Texto."""
    
    def __init__(self):
        
        Gtk.TextView.__init__(self)
        
        self.set_editable(False)
        self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        #self.set_justification(Gtk.Justification.FILL)
        #self.set_pixels_above_lines(5)
        #self.set_pixels_below_lines(15)
        #self.set_pixels_inside_wrap(5)
        #self.set_left_margin(10)
        #self.set_right_margin(10)
        
        self.set_buffer(Gtk.TextBuffer())
        
class ToolbarConfig(Gtk.Toolbar):
    """Toolbar para que el usuario configure JAMedia."""
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        self.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        
        self.ocultar_controles = False
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        item = Gtk.ToolItem()
        label = Gtk.Label("Ocultar Controles:")
        label.show()
        item.add(label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        switch = Gtk.Switch()
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
        
        switch.connect('button-press-event', self.set_controles_view)
        
    def set_controles_view(self, widget, senial):
        """Almacena el estado de "ocultar_controles"."""
        
        self.ocultar_controles = not widget.get_active()
        