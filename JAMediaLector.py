#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

import JAMediaLector
from JAMediaLector.JAMediaLector import JAMediaLector

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMediaEstilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    
class Ventana(Gtk.Window):
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMediaLector")
        self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaLector.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(2)
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamedialector = JAMediaLector()
        self.socket.add_id(self.jamedialector.get_id())
        self.show_all()
        self.realize()
        
        self.connect("destroy", self.salir)
        self.jamedialector.connect('salir', self.salir)
        
        GLib.idle_add(self.setup_init)
        
    def setup_init(self):
        
        self.jamedialector.setup_init()
        self.jamedialector.pack_standar()
        
    def salir(self, widget = None, senial = None):
        
        sys.exit(0)
    
if __name__ == "__main__":
    Ventana()
    Gtk.main()
    