#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -inurl:(htm|html|php) intitle:"index of" +"last modified" +"parent directory" +description +size +(wma|mp3) "BANDA/CANCIÓN"
# http://alt1040.com/2008/11/convirtiendo-a-google-en-un-servicio-de-descarga-de-mp3

import os
import sys
import commands

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

import JAMediaObjects
import JAMediaObjects.JAMediaGlobales as G

import JAMediaWeb
from JAMediaWeb.JAMediaWeb import JAMediaWeb

JAMediaObjectsPath = JAMediaObjects.__path__[0]


class Ventana(Gtk.Window):

    def __init__(self):

        super(Ventana, self).__init__()

        self.set_title("JAMediaWeb")
        #self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
        #    "Iconos", "JAMedia.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)
        #self.modify_bg(0, G.GRIS)

        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaweb = JAMediaWeb()
        self.socket.add_id(self.jamediaweb.get_id())

        self.show_all()
        self.realize()

        self.connect("destroy", self.salir)
        self.jamediaweb.connect('salir', self.salir)

        GLib.idle_add(self.setup_init)

    def setup_init(self):

        self.jamediaweb.setup_init()

    def salir(self, widget = None, senial = None):

        sys.exit(0)

if __name__ == "__main__":

    jamedia = Ventana()
    Gtk.main()
