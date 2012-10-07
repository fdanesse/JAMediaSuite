#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import JAMImagenes
from JAMImagenes.JAMImagenes import JAMImagenes

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class Ventana(Gtk.Window):
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMImagenes")
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(3)
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.visor = JAMImagenes()
        self.socket.add_id(self.visor.get_id())
        self.show_all()
        self.realize()
        
        self.connect("destroy", self.salir)
        self.visor.connect("salir", self.salir)
        
    def salir(self, widget = None, senial = None):
        sys.exit(0)
    
if __name__ == "__main__":
    Ventana()
    Gtk.main()
    