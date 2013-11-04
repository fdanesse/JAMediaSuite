#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaImagenes.py por:
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
from gi.repository import GLib

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMImagenes2
from JAMImagenes2.JAMImagenes import JAMImagenes

class Ventana(Gtk.Window):
    
    __gtype_name__ = 'WindowBase'
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMImagenes")
        self.set_resizable(True)
        self.set_default_size(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(0)
        #self.maximize()
        #self.fullscreen()
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaimagenes = JAMImagenes()
        self.socket.add_id(self.jamediaimagenes.get_id())
        
        self.show_all()
        self.realize()
        
        self.connect("delete-event", self.__salir)
        self.jamediaimagenes.connect("salir", self.__salir)
        
        ### Iniciar en path por defecto de JAMediaSuite.
        path = os.path.join(
            os.environ["HOME"],
            "JAMediaDatos", "Fotos")
        
        GLib.idle_add(
            self.jamediaimagenes.switch_to,
            None, path)
    
    def __salir(self, widget=None, signal=None):
        
        import sys
        sys.exit(0)

if __name__ == "__main__":
    
    Ventana()
    Gtk.main()
    