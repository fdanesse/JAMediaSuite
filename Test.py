#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os
import sys
import commands
 
import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
 
import JAMedia
from JAMedia.JAMedia import JAMediaPlayer
 
import JAMediaObjects
 
JAMediaObjectsPath = JAMediaObjects.__path__[0]
 
class Ventana(Gtk.Window):

    def __init__(self):
        super(Ventana, self).__init__()

        self.set_title("JAMedia")
        self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaplayer = JAMediaPlayer()
        self.socket.add_id(self.jamediaplayer.get_id())
        self.show_all()
        self.realize()
       
        self.connect("destroy", self.salir)
        self.jamediaplayer.connect('salir', self.salir)
       
        GObject.idle_add(self.setup_init)
       
    def setup_init(self):
        self.jamediaplayer.setup_init()
     
    def salir(self, widget = None, senial = None):
        sys.exit(0)
   
if __name__ == "__main__":
    Ventana()
    Gtk.main()
    