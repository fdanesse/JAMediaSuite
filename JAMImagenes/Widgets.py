#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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

import os
import cairo
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import Visor

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMediaObjects.JAMFileSystem as JAMF
import JAMediaObjects.JAMediaGlobales as G
    
class VisorImagenes(Visor):
    """DrawingArea - Visor de Imágenes."""
    
    __gtype_name__ = 'VisorImagenes'
    
    def __init__(self):
        
        Visor.__init__(self)
        
        self.imagen_original = None
        self.imagen = None
        self.tamanio = None
        self.zoom = 1.0
        self.rotacion = None
        self.angulo = 0
        self.presentacion = False
        
        self.show_all()
        
    def rotar(self, angulo):
        if not self.imagen_original: return

        if angulo > 0: self.angulo += 90
        if angulo < 0: self.angulo -= 90
        
        if self.angulo == 0:
            self.rotacion = GdkPixbuf.PixbufRotation.NONE
            
        elif self.angulo == 90:
            self.rotacion = GdkPixbuf.PixbufRotation.CLOCKWISE
            
        elif self.angulo == 180:
            self.rotacion = GdkPixbuf.PixbufRotation.UPSIDEDOWN
            
        elif self.angulo == 270:
            self.rotacion = GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE
            
        elif self.angulo == 360:
            self.rotacion = GdkPixbuf.PixbufRotation.NONE
            
        elif self.angulo == -90:
            self.rotacion = GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE
            
        elif self.angulo == -180:
            self.rotacion = GdkPixbuf.PixbufRotation.UPSIDEDOWN
            
        elif self.angulo == -270:
            self.rotacion = GdkPixbuf.PixbufRotation.CLOCKWISE
            
        elif self.angulo == -360:
            self.rotacion = GdkPixbuf.PixbufRotation.NONE
        
        if self.angulo >= 360 or self.angulo <= -360: self.angulo = 0
        
        pixbuf = self.imagen_original.copy().rotate_simple(self.rotacion)
        self.tamanio = (int(pixbuf.get_width() * self.zoom),
            int(pixbuf.get_height() * self.zoom))
            
        self.get_property('window').invalidate_rect(self.get_allocation(), True)
        self.get_property('window').process_updates(True)
        
    def acercar(self):
        
        if not self.imagen_original: return
        self.angulo = -90
        self.rotar(1)
        self.set_zoom(self.zoom + 0.2)

    def alejar(self):
        
        if not self.imagen_original: return
        self.angulo = -90
        self.rotar(1)
        self.set_zoom(self.zoom - 0.2)
    
    def original(self):
        
        if not self.imagen_original: return
        self.angulo = -90
        self.rotar(1)
        self.set_zoom(1.0)
        
    def set_zoom(self, zoom):
        
        if not self.imagen_original: return
        self.zoom = zoom
        if self.zoom <= 0.2: self.zoom = 0.2
        self.tamanio = (int(self.imagen_original.get_width() * self.zoom),
            int(self.imagen_original.get_height() * self.zoom))
            
        self.get_property('window').invalidate_rect(self.get_allocation(), True)
        self.get_property('window').process_updates(True)
        
    def set_imagen(self, archivo = None):
        
        self.zoom = 1
        self.imagen_original = None
        self.tamanio = None
        self.rotacion = None
        
        if archivo and os.path.exists(archivo):
            self.imagen_original = GdkPixbuf.Pixbuf.new_from_file(archivo)
            self.tamanio = (self.imagen_original.get_width(),
                self.imagen_original.get_height())
        else:
            self.imagen_original = None
            self.imagen = None
            self.tamanio = None
            self.rotacion = None
        
        self.get_property('window').invalidate_rect(self.get_allocation(), True)
        self.get_property('window').process_updates(True)
        
    def do_draw(self, contexto):
        
        if not self.imagen_original:
            #self.modify_bg(0, Gdk.Color(65000, 65000, 65000))
            return
        
        width, height = self.tamanio
        self.set_size_request(width, height)
        self.imagen = self.imagen_original.copy()
        
        if self.presentacion: return self.draw_presentacion(contexto)
    
        if self.rotacion:
            self.imagen = self.imagen.rotate_simple(self.rotacion)
            
        self.imagen = self.imagen.scale_simple(width, height,
            GdkPixbuf.InterpType.TILES)
        rect = self.get_allocation()
        x = int((rect.width - width) / 2)
        y = int((rect.height - height) / 2)
        Gdk.cairo_set_source_pixbuf(contexto, self.imagen, x, y)
        contexto.paint()
        
    def draw_presentacion(self, contexto):
        
        rect = self.get_allocation()
        width, height = (rect.width, rect.height)
        self.imagen = self.imagen.scale_simple(width, height,
            GdkPixbuf.InterpType.TILES)
        Gdk.cairo_set_source_pixbuf(contexto, self.imagen, 0, 0)
        contexto.paint()

class Toolbar(Gtk.Toolbar):
    
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
        GObject.TYPE_NONE, ([])),
    'configurar': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, ([])),
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, ([]))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "escalaoriginal.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(1))
        boton.set_tooltip_text("Original.")
        boton.connect("clicked", self.original)
        self.insert(boton, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(1))
        boton.set_tooltip_text("Alejar.")
        boton.connect("clicked", self.alejar)
        self.insert(boton, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "acercar.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(1))
        boton.set_tooltip_text("Acercar.")
        boton.connect("clicked", self.acercar)
        self.insert(boton, -1)

        self.insert(G.get_separador(draw = True,
            ancho = 0, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "rotar.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(1))
        boton.set_tooltip_text("Izquierda.")
        boton.connect("clicked", self.rotar_izquierda)
        self.insert(boton, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "rotar.png")
        boton = G.get_boton(archivo, flip = True,
            rotacion = None, pixels = G.get_pixels(1))
        boton.set_tooltip_text("Derecha.")
        boton.connect("clicked", self.rotar_derecha)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = True,
            ancho = 0, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "configurar.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(1))
        boton.set_tooltip_text("Configurar.")
        boton.connect("clicked", self.configurar)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = True,
            ancho = 0, expand = False), -1)
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "salir.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir.")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 2, expand = False), -1)
        
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

    def configurar(self, widget):
        self.emit("configurar")
        
    def salir(self, widget):
        self.emit("salir")
        
class ToolbarConfig(Gtk.Box):
    """Toolbar con opciones de configuracion para
    modo presentacion de diapositivas."""
    
    __gsignals__ = {"run":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_INT, ))}
    
    def __init__(self):
        
        toolbar1 = Gtk.Toolbar()
        toolbar2 = Gtk.Toolbar()
        
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)
        
        self.ocultar_controles = False
        self.intervalo = 1.0
        
        toolbar1.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "salir.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Cancelar.")
        boton.connect("clicked", self.cancelar)
        toolbar1.insert(boton, -1)
        
        toolbar1.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Restar.")
        boton.connect("clicked", self.menos_intervalo)
        toolbar1.insert(boton, -1)
        
        toolbar1.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("Cambiar Imagen cada: %s Segundos" %(self.intervalo))
        self.label.show()
        item.add(self.label)
        toolbar1.insert(item, -1)
        
        toolbar1.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "acercar.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Sumar.")
        boton.connect("clicked", self.mas_intervalo)
        toolbar1.insert(boton, -1)
        
        toolbar1.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "play.png")
        boton = G.get_boton(archivo, flip = False,
            rotacion = None, pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Aceptar.")
        boton.connect("clicked", self.run_presentacion)
        toolbar1.insert(boton, -1)
        
        toolbar1.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        toolbar2.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        item = Gtk.ToolItem()
        label = Gtk.Label("Ocultar Controles:")
        label.show()
        item.add(label)
        toolbar2.insert(item, -1)
        
        toolbar2.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        switch = Gtk.Switch()
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar2.insert(item, -1)
        
        toolbar2.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.pack_start(toolbar1, True, True, 0)
        self.pack_start(toolbar2, True, True, 0)
        
        self.show_all()
        
        switch.connect('button-press-event', self.set_controles_view)
        
    def set_controles_view(self, widget, senial):
        """Almacena el estado de "ocultar_controles"."""
        
        self.ocultar_controles = not widget.get_active()
        
    def mas_intervalo(self, widget= None):
        
        self.intervalo += 0.1
        self.label.set_text("Cambiar Imagen cada: %s Segundos" %(self.intervalo))

    def menos_intervalo(self, widget= None):
        
        if self.intervalo > 0.3:
            self.intervalo -= 0.1
            self.label.set_text("Cambiar Imagen cada: %s Segundos" %(self.intervalo))

    def run_presentacion(self, widget= None):
        
        self.emit("run", int(self.intervalo*1000))
        self.hide()

    def cancelar(self, widget= None):
        
        self.hide()
        
class MenuList(Gtk.Menu):
    """Menu con opciones para operar sobre el archivo o
    el streaming seleccionado en la lista de reproduccion
    al hacer click derecho sobre él."""
    
    __gsignals__ = {
    'accion':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}
    
    def __init__(self, widget, boton, pos, tiempo, path, modelo):
        
        Gtk.Menu.__init__(self)
        
        iter = modelo.get_iter(path)
        uri = modelo.get_value(iter, 2)
        
        quitar = Gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.set_accion,
            widget, path, "Quitar")
        
        if JAMF.describe_acceso_uri(uri):
            lectura, escritura, ejecucion = JAMF.describe_acceso_uri(uri)
            
            if escritura:
                borrar = Gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.set_accion,
                    widget, path, "Borrar")
                    
        self.show_all()
        self.attach_to_widget(widget, self.null)
        
    def null(self):
        pass
    
    def set_accion(self, widget, path, accion):
        """Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.
        
        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar."""
        
        iter = widget.modelo.get_iter(path)
        self.emit('accion', widget, accion, iter)
        