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

from Widgets import ToolbarImagen
#from Widgets import ToolbarEditor

from Previews import Previews
from VisorImagenes import VisorImagenes
#from EditorImagenes import EditorImagenes

from JAMediaObjects.JAMediaWidgets import Acelerometro

PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(PATH, "Estilo.css")
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
        
        self.interface = False
        #self.acelerometro = Acelerometro()
        
        self.add(self.basebox)
        
        self.show_all()
        self.realize()
        
        #self.acelerometro.connect("angulo", self.__rotar)
        
    '''
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
    '''
        
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
            self.interface = Previews(path)
            
            self.basebox.pack_start(self.interface, True, True, 0)
            #self.show_all()
            self.interface.run()
            
            self.interface.connect('switch_to', self.switch_to)
            self.interface.connect('ver', self.__switch_to_visor)
            self.interface.connect('camara', self.__switch_to_camara)
            self.interface.connect('salir', self.__salir)
            
        ### Abre Editor de imagen cuando path es un archivo.
        '''
        elif os.path.isfile(path):
            
            self.interface = VisorImagenes(path)
            
            self.basebox.pack_start(self.interface, True, True, 0)
            self.show_all()
            self.interface.run()
            
            self.interface.connect('switch_to', self.switch_to)
            #self.interface.connect('ver', self.__switch_to_visor)
            #self.interface.connect('camara', self.__switch_to_camara)
            self.interface.connect('salir', self.__salir)'''
        
    def __switch_to_camara(self, widget):
        
        print "Ir al Visor de la Cámara"
        
    def __switch_to_visor(self, widget, path):
        
        if not path: return
        if path == None: return
        if not os.path.exists(path): return
        if not os.access(path, os.R_OK): return
        if path == os.path.dirname(os.environ["HOME"]): return
        
        ### Quitar Interfaz Anterior.
        for child in self.basebox.get_children():
            self.basebox.remove(child)
            child.destroy()
    
        self.interface = VisorImagenes(path)
        
        self.basebox.pack_start(self.interface, True, True, 0)
        #self.show_all()
        self.interface.run()
        
        self.interface.connect('switch_to', self.switch_to)
        #self.interface.connect('ver', self.__switch_to_visor)
        #self.interface.connect('camara', self.__switch_to_camara)
        self.interface.connect('salir', self.__salir)
        
    def __salir(self, widget):
        
        #self.__rotar(None, 0) Devuelve la pantalla a su estado original.
        self.emit("salir")
        