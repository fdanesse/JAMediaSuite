#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk


class MenuPrincipal(gtk.MenuBar):

    __gsignals__ = {
    "open": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.MenuBar.__init__(self)

        archivo = gtk.MenuItem('Archivo')
        marchivo = MenuArchivo()
        archivo.set_submenu(marchivo)
        self.append(archivo)

        self.show_all()

        marchivo.connect("open", self.__emit_open)

    def __emit_open(self, submenu, filepath):
        self.emit("open", filepath)


class MenuArchivo(gtk.Menu):

    __gsignals__ = {
    "open": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.Menu.__init__(self)

        self.__dir_path = False

        abrir = gtk.MenuItem('Abrir...')
        separador1 = gtk.SeparatorMenuItem()
        guardar = gtk.MenuItem('Guardar')
        guardar_como = gtk.MenuItem('Guardar Como...')
        separador2 = gtk.SeparatorMenuItem()
        imprimir = gtk.MenuItem('Imprimir...')
        separador3 = gtk.SeparatorMenuItem()
        propiedades = gtk.MenuItem('Propiedades...')
        separador4 = gtk.SeparatorMenuItem()
        cerrar = gtk.MenuItem('Cerrar')

        for item in [abrir, separador1, guardar, guardar_como, separador2,
            imprimir, separador3, propiedades, separador4, cerrar]:
                self.append(item)

        self.show_all()

        abrir.connect("activate", self.__open_file)

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
