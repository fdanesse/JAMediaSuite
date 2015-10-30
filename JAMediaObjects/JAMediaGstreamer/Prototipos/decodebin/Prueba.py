#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkX11

from Process import Process


class Ventana(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_size_request(320, 240)

        basebox = Gtk.HPaned()
        drawing = Gtk.DrawingArea()
        drawing.modify_bg(0, Gdk.Color(0, 0, 0))
        vbox = Gtk.VBox()

        boton1 = Gtk.Button("Sin Efecto")
        boton2 = Gtk.Button("Con Efecto")

        vbox.pack_start(boton1, False, False, 0)
        vbox.pack_start(boton2, False, False, 0)

        basebox.pack1(drawing, True, True)
        basebox.pack2(vbox, False, True)
        self.add(basebox)

        self.show_all()
        self.realize()

        self.process = Process(
            drawing.get_property('window').get_xid())

        self.process.play()

        self.connect("delete-event", self.__exit)

    def __exit(self, widget=None, senial=None):

        sys.exit(0)

if __name__ == "__main__":
    Ventana()
    Gtk.main()
