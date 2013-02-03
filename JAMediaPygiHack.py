#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay - Activity Central
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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir

import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMediaPygiHack
from JAMediaPygiHack.JAMediaPygiHack import JAMediaPygiHack

import JAMediaGstreamer
from JAMediaGstreamer.JAMediaGstreamer import JAMediaGstreamer

class Ventana(Gtk.Window):
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMediaPygiHAck")
        
        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "ver.png"))
            
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.add(vbox)
        
        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        
        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(self.toolbar_salir, False, False, 0)
        
        self.socket_pygihack = Gtk.Socket()
        vbox.pack_start(self.socket_pygihack, True, True, 0)
        
        self.socket_gstreamer = Gtk.Socket()
        vbox.pack_start(self.socket_gstreamer, True, True, 0)
        
        self.show_all()
        self.realize()
        
        self.jamediapygihack = JAMediaPygiHack()
        self.socket_pygihack.add_id(self.jamediapygihack.get_id())
        
        self.jamediagstreamer = JAMediaGstreamer()
        self.socket_gstreamer.add_id(self.jamediagstreamer.get_id())
        
        self.socket_gstreamer.hide()
        self.toolbar_salir.hide()
        
        self.connect("destroy", self.salir)
        #self.jamediapygihack.connect('salir', self.salir)
        #self.jamediagstreamer.connect('salir', self.salir)
    
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar.connect('view', self.switch)
        self.toolbar_salir.connect('salir', self.salir)
        
    def switch(self, widget, nombre):
        
        self.toolbar_salir.hide()
        
        if nombre == 'pygi':
            self.socket_gstreamer.hide()
            self.socket_pygihack.show()
            
        elif nombre == 'gstreamer':
            self.socket_pygihack.hide()
            self.socket_gstreamer.show()
            
    def confirmar_salir(self, widget = None, senial = None):
        
        self.toolbar_salir.run("JAMediaPygiHack")
        
    def salir(self, widget = None, senial = None):
        
        sys.exit(0)
    
class Toolbar(Gtk.Toolbar):
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'view':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        self.boton_pygi = Gtk.ToggleToolButton()
        label = Gtk.Label('Pygi')
        label.modify_fg(0, Gdk.Color(65535, 65535, 65535))
        self.boton_pygi.set_icon_widget(label)
        label.show()
        self.boton_pygi.set_tooltip_text("JAMedia PygiHack")
        self.boton_pygi.connect("clicked", self.switch)
        self.insert(self.boton_pygi, -1)
        
        self.boton_gstreamer = Gtk.ToggleToolButton()
        label = Gtk.Label('Gstreamer')
        label.modify_fg(0, Gdk.Color(65535, 65535, 65535))
        self.boton_gstreamer.set_icon_widget(label)
        label.show()
        self.boton_gstreamer.set_tooltip_text("JAMedia Gstreamer")
        self.boton_gstreamer.connect("clicked", self.switch)
        self.insert(self.boton_gstreamer, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
            
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","ceibaljam.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","uruguay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","licencia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("fdanesse@gmail.com")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos","salir.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        self.show_all()
        
        self.boton_pygi.set_active(True)
        
    def switch(self, widget):
        
        if widget == self.boton_pygi:
            nombre = 'pygi'
            self.emit('view', nombre)
            
        elif widget == self.boton_gstreamer:
            nombre = 'gstreamer'
            self.emit('view', nombre)
        
        self.boton_gstreamer.set_active(False)
        self.boton_pygi.set_active(False)
        
    def salir(self, widget):
        
        self.emit('salir')
        
if __name__ == "__main__":
    Ventana()
    Gtk.main()
