#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk


class MenuPrincipal(gtk.MenuBar):

    __gsignals__ = {
    "open": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "close": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.MenuBar.__init__(self)

        archivo = gtk.MenuItem('Archivo')
        self.__marchivo = MenuArchivo()
        archivo.set_submenu(self.__marchivo)
        self.append(archivo)

        self.show_all()

        self.__marchivo.connect("open", self.__emit_open_file)
        self.__marchivo.connect("close", self.__emit_close_file)

    def __emit_close_file(self, submenu):
        self.emit("close")

    def __emit_open_file(self, submenu, filepath):
        self.emit("open", filepath)

    def has_file(self, hasfile, writable):
        self.__marchivo.has_file(hasfile, writable)


class MenuArchivo(gtk.Menu):

    __gsignals__ = {
    "open": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "close": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Menu.__init__(self)

        self.__dir_path = False

        self.__abrir = gtk.MenuItem('Abrir...')
        separador1 = gtk.SeparatorMenuItem()
        self.__guardar = gtk.MenuItem('Guardar')
        self.__guardar_como = gtk.MenuItem('Guardar Como...')
        separador2 = gtk.SeparatorMenuItem()
        self.__imprimir = gtk.MenuItem('Imprimir...')
        separador3 = gtk.SeparatorMenuItem()
        self.__propiedades = gtk.MenuItem('Propiedades...')
        separador4 = gtk.SeparatorMenuItem()
        self.__cerrar = gtk.MenuItem('Cerrar')

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
        dialog = gtk.FileChooserDialog(parent=self.get_toplevel(),
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            title="Abrir Archivo",
            buttons=("Abrir", gtk.RESPONSE_ACCEPT,
            "Cancelar", gtk.RESPONSE_CANCEL))
        dialog.set_border_width(15)
        if self.__dir_path:
            dialog.set_current_folder_uri("file://%s" % self.__dir_path)
        dialog.set_select_multiple(False)
        filtro = gtk.FileFilter()
        filtro.set_name("image")
        filtro.add_mime_type("image/*")
        dialog.add_filter(filtro)
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
