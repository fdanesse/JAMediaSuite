#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGstreamer.py por:
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
from gi.repository import GObject

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaGstreamer.JAMediaGstreamer import JAMediaGstreamer

class Ventana(Gtk.Window):
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMedia Gstreamer.")
        
        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "ver.png"))
            
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.socket = Gtk.Socket()
        self.add(self.socket)
        
        self.jamedia_gstreamer = JAMediaGstreamer()
        self.socket.add_id(self.jamedia_gstreamer.get_id())
        
        self.show_all()
        self.realize()
        
        self.connect("destroy", self.salir)
        self.jamedia_gstreamer.connect('salir', self.salir)
        
    def salir(self, widget = None, senial = None):
        
        import sys
        sys.exit(0)
        
if __name__ == "__main__":
    
    Ventana()
    Gtk.main()
