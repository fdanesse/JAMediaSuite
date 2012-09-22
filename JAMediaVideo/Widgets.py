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

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import JAMediaButton
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class Toolbar(Gtk.Toolbar):
    """ Toolbar principal. """
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, [])}
    
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaVideo.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
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
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
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
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
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
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
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
        
    def salir(self, widget):
        """Cuando se hace click en el boton salir
        de la toolbar principal."""
        
        self.emit('salir')
        
class ToolbarPrincipal(Gtk.Toolbar):
    """ Toolbar principal. """
    
    __gsignals__ = {
    'menu':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "camara.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Filmar")
        boton.connect("clicked", self.emit_senial, "Filmar")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "foto.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Fotografiar")
        boton.connect("clicked", self.emit_senial, "Fotografiar")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "microfono.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Grabar")
        boton.connect("clicked", self.emit_senial, "Grabar")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "iconplay.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Reproducir")
        boton.connect("clicked", self.emit_senial, "Reproducir")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "monitor.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Ver")
        boton.connect("clicked", self.emit_senial, "Ver")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def emit_senial(self, widget, text):
        """Cuando se hace click en algún boton."""
        
        self.emit('menu', text)
        
class ToolbarVideo(Gtk.Toolbar):
    """ Toolbar de filmación. """
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, []),
    'accion':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.color = Gdk.Color(0, 0, 0)
        self.actualizador = None
        
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "camara.png")
        self.filmar = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        self.filmar.set_tooltip_text("Filmar")
        self.filmar.connect("clicked", self.emit_senial, "filmar")
        self.insert(self.filmar, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "configurar.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.emit_senial, "configurar")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","salir.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def set_estado(self, estado):
        """Cuando está grabando cambiará los colores
        intermitentemente en el botón correspondiente."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if estado == "grabando":
            self.actualizador = GObject.timeout_add(400, self.handle)
        elif estado == "detenido":
            self.color = Gdk.Color(0, 0, 0)
            self.modify_bg(0, self.color)
            
    def handle(self):
        """Cambia el color para advertir al usuario
        de que está grabando desde la webcam."""
        
        if self.color == Gdk.Color(0, 0, 0):
            self.color = Gdk.Color(65000,26000,0)
        elif self.color == Gdk.Color(65000,26000,0):
            self.color = Gdk.Color(0, 0, 0)
            
        self.modify_bg(0, self.color)
        return True
    
    def emit_senial(self, widget, senial):
        """Emite filmar o configurar."""
        
        self.emit('accion', senial)
        
    def salir(self, widget):
        """Para Salir al menú principal."""
        
        self.emit('salir')
        
class ToolbarFotografia(Gtk.Toolbar):
    """ Toolbar Fotografias. """
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, []),
    'accion':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.color = Gdk.Color(0, 0, 0)
        self.actualizador = None
        
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "foto.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Fotografiar")
        boton.connect("clicked", self.emit_senial, "fotografiar")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        #archivo = os.path.join(JAMediaObjectsPath, "Iconos", "configurar.png")
        #boton = G.get_boton(archivo, flip = False,
        #    color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        #boton.set_tooltip_text("Configurar")
        #boton.connect("clicked", self.emit_senial, "configurar")
        #self.insert(boton, -1)
        
        #self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","salir.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def set_estado(self, estado):
        """Cuando está grabando cambiará los colores
        intermitentemente en el botón correspondiente."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if estado == "grabando":
            self.actualizador = GObject.timeout_add(400, self.handle)
        elif estado == "detenido":
            self.color = Gdk.Color(0, 0, 0)
            self.modify_bg(0, self.color)
            
    def handle(self):
        """Cambia el color para advertir al usuario
        de que está grabando desde la webcam."""
        
        if self.color == Gdk.Color(0, 0, 0):
            self.color = Gdk.Color(65000,26000,0)
        elif self.color == Gdk.Color(65000,26000,0):
            self.color = Gdk.Color(0, 0, 0)
            
        self.modify_bg(0, self.color)
        return True
    
    def emit_senial(self, widget, senial):
        """Emite grabar o configurar."""
        
        self.emit('accion', senial)
        
    def salir(self, widget):
        """Para Salir al menú principal."""
        
        self.emit('salir')
        
class ToolbarGrabarAudio(Gtk.Toolbar):
    """ Toolbar Fotografias. """
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, []),
    'accion':(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.color = Gdk.Color(0, 0, 0)
        self.actualizador = None
        
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "microfono.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Grabar")
        boton.connect("clicked", self.emit_senial, "grabar")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        #archivo = os.path.join(JAMediaObjectsPath, "Iconos", "configurar.png")
        #boton = G.get_boton(archivo, flip = False,
        #    color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        #boton.set_tooltip_text("Configurar")
        #boton.connect("clicked", self.emit_senial, "configurar")
        #self.insert(boton, -1)
        
        #self.insert(G.get_separador(draw = False, ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos","salir.png")
        boton = G.get_boton(archivo, flip = False,
            color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def set_estado(self, estado):
        """Cuando está grabando cambiará los colores
        intermitentemente en el botón correspondiente."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if estado == "grabando":
            self.actualizador = GObject.timeout_add(400, self.handle)
        elif estado == "detenido":
            self.color = Gdk.Color(0, 0, 0)
            self.modify_bg(0, self.color)
            
    def handle(self):
        """Cambia el color para advertir al usuario
        de que está grabando desde la webcam."""
        
        if self.color == Gdk.Color(0, 0, 0):
            self.color = Gdk.Color(65000,26000,0)
        elif self.color == Gdk.Color(65000,26000,0):
            self.color = Gdk.Color(0, 0, 0)
            
        self.modify_bg(0, self.color)
        return True
    
    def emit_senial(self, widget, senial):
        """Emite grabar o configurar."""
        
        self.emit('accion', senial)
        
    def salir(self, widget):
        """Para Salir al menú principal."""
        
        self.emit('salir')
        