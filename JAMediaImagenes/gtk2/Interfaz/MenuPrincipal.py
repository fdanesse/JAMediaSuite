#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk

from Dialogos import OpenDialog


class MenuPrincipal(gtk.MenuBar):

    __gsignals__ = {
    "open": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "close": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "open-util": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.MenuBar.__init__(self)

        archivo = gtk.MenuItem("Archivo")
        self.__marchivo = MenuArchivo()
        archivo.set_submenu(self.__marchivo)
        self.append(archivo)

        utiles = gtk.MenuItem("Utiles")
        self.__utiles = MenuUtiles()
        utiles.set_submenu(self.__utiles)
        self.append(utiles)

        ayuda = gtk.MenuItem("Ayuda")
        self.__ayuda = MenuAyuda()
        ayuda.set_submenu(self.__ayuda)
        self.append(ayuda)

        self.show_all()

        self.__marchivo.connect("open", self.__emit_open_file)
        self.__marchivo.connect("close", self.__emit_close_file)

        self.__utiles.connect("open-util", self.__emit_util)

    def __emit_util(self, menu, text):
        self.emit("open-util", text)

    def __emit_close_file(self, submenu):
        self.emit("close")

    def __emit_open_file(self, submenu, filepath):
        self.emit("open", filepath)

    def has_file(self, hasfile, writable):
        self.__marchivo.has_file(hasfile, writable)
        self.__utiles.get_attach_widget().set_sensitive(hasfile)

    def set_dir_path(self, dir_path):
        self.__marchivo.set_dir_path(dir_path)


class MenuArchivo(gtk.Menu):

    __gsignals__ = {
    "open": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "close": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Menu.__init__(self)

        self.__dir_path = False

        self.__abrir = gtk.MenuItem("Abrir...")
        separador1 = gtk.SeparatorMenuItem()
        self.__guardar = gtk.MenuItem("Guardar")
        self.__guardar_como = gtk.MenuItem("Guardar Como...")
        separador2 = gtk.SeparatorMenuItem()
        self.__imprimir = gtk.MenuItem("Imprimir...")
        separador3 = gtk.SeparatorMenuItem()
        self.__propiedades = gtk.MenuItem("Propiedades...")
        separador4 = gtk.SeparatorMenuItem()
        self.__cerrar = gtk.MenuItem("Cerrar")

        for item in [self.__abrir, separador1, self.__guardar,
            self.__guardar_como, separador2, self.__imprimir, separador3,
            self.__propiedades, separador4, self.__cerrar]:
                self.append(item)

        self.show_all()

        self.__abrir.connect("activate", self.__open_file)
        self.__cerrar.connect("activate", self.__close_file)

    def __close_file(self, widget):
        self.emit("close")

    def __open_file(self, widget):
        dialog = OpenDialog(parent=self.get_toplevel(),
            dir_path=self.__dir_path)
        run = dialog.run()
        if run == gtk.RESPONSE_ACCEPT:
            filepath = os.path.realpath(dialog.get_filename())
            self.__dir_path = os.path.dirname(filepath)
            self.emit("open", filepath)
        dialog.destroy()

    def has_file(self, hasfile, writable):
        for item in [self.__guardar, self.__guardar_como, self.__imprimir,
            self.__propiedades, self.__cerrar]:
                item.set_sensitive(hasfile)
        if hasfile and not writable:
            self.__guardar.set_sensitive(False)

    def set_dir_path(self, dir_path):
        self.__dir_path = dir_path


class MenuUtiles(gtk.Menu):

    __gsignals__ = {
    "open-util": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Menu.__init__(self)

        self.__canales = gtk.MenuItem("Canales...")
        self.append(self.__canales)
        #FIXME: Agregar Cerrar Todos

        self.show_all()

        self.__canales.connect("activate", self.__emit_util)

    def __emit_util(self, item):
        self.emit("open-util", item.get_label())


class MenuAyuda(gtk.Menu):

    def __init__(self):

        gtk.Menu.__init__(self)

        self.show_all()
