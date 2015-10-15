#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk


class Menu(gtk.MenuBar):

    __gsignals__ = {
    "save": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.MenuBar.__init__(self)

        archivo = gtk.MenuItem("Archivo")
        self.__marchivo = MenuArchivo()
        archivo.set_submenu(self.__marchivo)
        self.append(archivo)

        ayuda = gtk.MenuItem("Ayuda")
        self.__ayuda = MenuAyuda()
        ayuda.set_submenu(self.__ayuda)
        self.append(ayuda)

        self.show_all()

        self.__marchivo.connect("save", self.__emit_save_file)

    def __emit_save_file(self, submenu):
        self.emit("save")


class MenuArchivo(gtk.Menu):

    __gsignals__ = {
    "save": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Menu.__init__(self)

        guardar_como = gtk.MenuItem("Guardar Como...")
        self.append(guardar_como)
        self.show_all()
        guardar_como.connect("activate", self.__emit_save_file)

    def __emit_save_file(self, widget):
        self.emit("save")


class MenuAyuda(gtk.Menu):

    def __init__(self):

        gtk.Menu.__init__(self)

        self.show_all()
