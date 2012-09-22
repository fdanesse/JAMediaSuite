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

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects
import JAMediaObjects.JAMediaGlobales as G

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
        self.modify_bg(0, G.GRIS)
        
        self.pista = ""
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaplayer = JAMediaPlayer()
        self.socket.add_id(self.jamediaplayer.get_id())
        self.show_all()
        self.realize()
        
        self.connect("destroy", self.salir)
        self.jamediaplayer.connect('salir', self.salir)
        
        GObject.idle_add(self.setup_init)
        
    def set_pista(self, pista):
        self.pista = pista
        
    def setup_init(self):
        self.jamediaplayer.setup_init()
        self.jamediaplayer.pack_standar()
        if self.pista: self.jamediaplayer.set_nueva_lista(self.pista)
        
    def salir(self, widget = None, senial = None):
        import commands
        commands.getoutput('killall mplayer')
        sys.exit(0)
        
if __name__ == "__main__":
    
    items = []
    if len(sys.argv) > 1:
        path = os.path.join(sys.argv[1])
        if os.path.exists(path):
            archivo = os.path.basename(path)
            items.append( [archivo,path] )
            jamedia = Ventana()
            jamedia.set_pista(items)
        else:
            jamedia = Ventana()
    else:
        jamedia = Ventana()
        
    Gtk.main()
    