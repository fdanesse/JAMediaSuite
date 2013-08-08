#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir

from JAMediaObjects.JAMediaGlobales import get_separador
from JAMediaObjects.JAMediaGlobales import get_pixels
from JAMediaObjects.JAMediaGlobales import get_boton

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaPygiHack.JAMediaPygiHack import JAMediaPygiHack

from JAMediaGstreamer.JAMediaGstreamer import JAMediaGstreamer

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()

style_path = os.path.join(
    JAMediaObjectsPath, "JAMediaPygiHack.css")
    
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    
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
        
        self.connect("destroy", self.__salir)
    
        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar.connect('view', self.__switch)
        
        self.toolbar_salir.connect('salir', self.__salir)
        
    def __switch(self, widget, nombre):
        """
        Cambia la vista entre PygiHack
        JAMediaGstreamer.
        """
        
        self.toolbar_salir.hide()
        
        if nombre == 'pygi':
            self.socket_gstreamer.hide()
            self.socket_pygihack.show()
            
        elif nombre == 'gstreamer':
            self.socket_pygihack.hide()
            self.socket_gstreamer.show()
            
    def __confirmar_salir(self, widget = None, senial = None):
        """
        Pide confirmación para salir.
        """
        
        self.toolbar_salir.run("JAMediaPygiHack")
        
    def __salir(self, widget = None, senial = None):
        """
        Cierra la aplicación.
        """
        
        import sys
        sys.exit(0)
    
class Toolbar(Gtk.Toolbar):
    """
    Toolbar principal de JAMediaPygiHack.
    """
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'view':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        item = Gtk.ToolItem()
        item.set_expand(False)
        self.boton_pygi = Gtk.RadioButton.new_with_label(
                None, 'Pygi')
        self.boton_pygi.set_tooltip_text("JAMedia PygiHack")
        self.boton_pygi.connect("toggled", self.__switch)
        item.add(self.boton_pygi)
        self.insert(item, -1)
        
        item = Gtk.ToolItem()
        item.set_expand(False)
        self.boton_gstreamer = Gtk.RadioButton.new_with_label(
                None, 'Gstreamer')
        self.boton_gstreamer.set_tooltip_text("JAMedia Gstreamer")
        self.boton_gstreamer.connect("toggled", self.__switch)
        item.add(self.boton_gstreamer)
        self.insert(item, -1)
        
        self.boton_gstreamer.join_group(self.boton_pygi)
        
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
            
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","ceibaljam.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","uruguay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","licencia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(0.8))
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
        
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos","salir.png")
        boton = get_boton(archivo, flip = False,
            pixels = get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        self.show_all()
        
        self.boton_pygi.set_active(True)
        
    def __switch(self, widget):
        
        nombre = None
        
        if self.boton_pygi.get_active():
            nombre = 'pygi'
            
        elif self.boton_gstreamer.get_active():
            nombre = 'gstreamer'
        
        self.emit('view', nombre)
        
    def __salir(self, widget):
        
        self.emit('salir')
        
if __name__ == "__main__":
    Ventana()
    Gtk.main()
