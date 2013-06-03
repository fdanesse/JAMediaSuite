#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTerminal.py por:
#       Flavio Danesse      <fdanesse@gmail.com>
#                           CeibalJAM! - Uruguay

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

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMediaTerminal

PATH = JAMediaTerminal.__path__[0]

from JAMediaTerminal.JAMediaTerminal import JAMediaTerminal

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(PATH, "Estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)

class Ventana(Gtk.Window):
    
    def __init__(self):
        
        Gtk.Window.__init__(self)
        
        self.set_title("JAMediaTerminal")
        
        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "bash.png"))
            
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        jamediaterminal = JAMediaTerminal()
        
        self.add(jamediaterminal)
        
        self.show_all()
        
        self.maximize()
        
        self.connect("destroy", self.__exit)
        
        self.set_decorated(True)
        
    def __exit(self, widget=None):
        """
        Sale de la aplicación.
        """
        
        sys.exit(0)
        
if __name__=="__main__":
    
    Ventana()
    Gtk.main()
