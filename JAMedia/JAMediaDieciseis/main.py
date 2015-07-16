#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gobject
import gtk

gobject.threads_init()

from Interfaz.JAMedia import JAMedia
import Reproductor


class Aplicacion(gobject.GObject):

    def __init__(self):

        gobject.GObject.__init__(self)

        self.interfaz = JAMedia()

        self.interfaz.connect("realize", self.__interfaz_realized)
        self.interfaz.connect("delete-event", self.__salir)
        self.interfaz.connect("destroy", self.__salir)
        print "JAMedia process:", os.getpid()

    def __interfaz_realized(self, interfaz):
        print self.__interfaz_realized, interfaz

    def __salir(self, widget=None, senial=None):
        self.interfaz.stop()
        gtk.main_quit()


if __name__ == "__main__":
    app = Aplicacion()
    gtk.main()
    print "Saliendo de JAMedia"
    sys.exit(0)
