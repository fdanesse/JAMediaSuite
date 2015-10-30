#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import sys

class Ventana(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("Ventana")
        caja = gtk.VBox()
        boton = gtk.Button("Hola")
        etiqueta = gtk.Label("Hola")
        caja.add(boton)
        caja.add(etiqueta)
        self.add(caja)
        self.show_all()

        self.connect("delete-event", self.delete_event)
        boton.connect("clicked", self.new_ventana)

    def delete_event(self, widget, event=None):
        sys.exit(0)

    def new_ventana(self, widget):
        Ventana()

if __name__ == "__main__":
    miventana = Ventana()
    gtk.main()
