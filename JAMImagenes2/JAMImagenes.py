#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMImagenes.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM - Uruguay

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

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from Widgets import Toolbar
from Widgets import ToolbarImagen

from Previews import Previews
from VisorImagenes import VisorImagenes

from JAMediaObjects.JAMediaWidgets import Acelerometro

PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(PATH, "JAMediaImagenes.css")
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
    """
    
    __gtype_name__ = 'PlugBase'
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """
        JAMImagenes: Gtk.Plug para embeber en otra aplicación.
        """
        
        Gtk.Plug.__init__(self, 0L)
        
        self.basebox = Gtk.VBox(
            orientation=Gtk.Orientation.VERTICAL)
        
        self.toolbar = False
        self.visor = False
        self.acelerometro = Acelerometro()
        
        self.add(self.basebox)
        
        self.show_all()
        self.realize()
        
        self.acelerometro.connect("angulo", self.__rotar)
        self.connect("motion-notify-event",
            self.__do_motion_notify_event)
    
    def __rotar(self, widget, angulo):
        """
        Rota la pantalla según el ángulo
        enviado por el acelerometro.
        """
        
        import commands
        
        if angulo == 270:
            commands.getoutput('xrandr --output lvds --rotate right')
            
        elif angulo == 90:
            commands.getoutput('xrandr --output lvds --rotate left')
            
        elif angulo == 180:
            commands.getoutput('xrandr --output lvds --rotate inverted')
            
        elif angulo == 0:
            commands.getoutput('xrandr --output lvds --rotate normal')
        
    def switch_to(self, widget, path):
        """
        Empaqueta toolbar y visor según valor.
        """
        
        if not path: return
        if path == None: return
        if not os.path.exists(path): return
        if not os.access(path, os.R_OK): return
        if path == os.path.dirname(os.environ["HOME"]): return
        
        ### Quitar Interfaz Anterior.
        for child in self.basebox.get_children():
            self.basebox.remove(child)
            child.destroy()
        
        ### Abre vista previews cuando path es un directorio.
        if os.path.isdir(path):
            self.toolbar = Toolbar(path)
            self.visor = Previews(path)
            self.toolbar.connect('salir', self.__salir)
            
            scroll = Gtk.ScrolledWindow()
            
            scroll.set_policy(
                Gtk.PolicyType.NEVER,
                Gtk.PolicyType.AUTOMATIC)
                
            scroll.add_with_viewport(self.visor)
            
        ### Abre vista imagen cuando path es un archivo.
        elif os.path.isfile(path):
            self.toolbar = ToolbarImagen(path)
            self.visor = VisorImagenes(path)
            self.toolbar.connect('salir', self.__salir)
            
            scroll = Gtk.ScrolledWindow()
            
            scroll.set_policy(
                Gtk.PolicyType.NEVER,
                Gtk.PolicyType.AUTOMATIC)
                
            scroll.add_with_viewport(self.visor)
            
        ### Empaquetado.
        self.basebox.pack_start(self.toolbar, False, False, 0)
        self.basebox.pack_start(scroll, True, True, 0)
        
        self.show_all()
        
        self.visor.load_previews(path)
        self.visor.connect('switch_to', self.switch_to)
        self.toolbar.connect('switch_to', self.switch_to)
        
        self.get_toplevel().set_sensitive(True)
    
    def __do_motion_notify_event(self, widget, event):
        """
        Cuando se mueve el mouse sobre la ventana.
        """
        
        x, y = self.get_toplevel().get_pointer()
        
        rect = self.toolbar.get_allocation()
        
        arriba = range(0, rect.height)
        
        if y in arriba:
            self.toolbar.show()
            return
        
        else:
            self.toolbar.hide()
            return
        
    def __salir(self, widget):
        
        self.__rotar(None, 0)
        self.emit("salir")
        