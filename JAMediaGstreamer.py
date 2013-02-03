#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import gi
from gi.repository import Gtk
from gi.repository import GObject

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMediaGstreamer
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
        
        sys.exit(0)
        
if __name__ == "__main__":
    
    Ventana()
    Gtk.main()
