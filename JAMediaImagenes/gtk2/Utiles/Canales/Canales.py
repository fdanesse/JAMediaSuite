#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import gobject
import gtk
from BasePanel import BasePanel
from Menu import Menu

PATH = os.path.dirname(__file__)


class Canales(gtk.Window):

    def __init__(self, top, processor):

        gtk.Window.__init__(self)

        self.set_title("Canales")
        self.set_resizable(False)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_transient_for(top)

        self.__processor = processor
        vbox = gtk.VBox()
        self.__menu = Menu()
        self.__base_panel = BasePanel(self.__processor)

        vbox.pack_start(self.__menu, False, False, 0)
        vbox.pack_start(self.__base_panel, True, True, 0)
        self.add(vbox)
        self.show_all()

        self.__menu.connect("save", self.__save_file)
        self.__base_panel.connect("has_pixbuf", self.__has_pixbuf)

    def __has_pixbuf(self, base_panel, has_pixbuf):
        self.__menu.has_pixbuf(has_pixbuf)

    def __save_file(self, widget):
        path = self.__processor.get_file_path()
        if not path:
            return
        path = os.path.dirname(path)
        dialog = gtk.FileChooserDialog(parent=self.get_toplevel(),
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            title="Guardar Archivo",
            buttons=("Guardar", gtk.RESPONSE_ACCEPT,
            "Cancelar", gtk.RESPONSE_CANCEL))
        dialog.set_border_width(15)
        dialog.set_current_folder_uri("file://%s" % path)
        dialog.set_select_multiple(False)
        filtro = gtk.FileFilter()
        filtro.set_name("image")
        filtro.add_mime_type("image/*")
        dialog.add_filter(filtro)
        '''
        file_name = os.path.basename(self.__processor.get_file_path())
        if "." in file_name:
            ext = ".%s" % file_name.split(".")[-1]
            file_name = file_name.replace(ext, "")
        file_name = "%s%s%s" % (file_name, self.__base_panel.get_canales(), ".png")
        file_name = os.path.join(path, file_name)
        '''
        run = dialog.run()
        if run == gtk.RESPONSE_ACCEPT:
            #FIXME: Verificar Sobre Escrituras
            dial = DialogoGuardando(self.get_toplevel(),
                self.__processor.save_png, dialog.get_filename(),
                self.__base_panel.get_canales())
            dial.run()
        dialog.destroy()

    def run(self):
        self.__base_panel.run()


class DialogoGuardando(gtk.Dialog):

    def __init__(self, parent, func, file_name, canales):

        self.__func = func
        self.__file_name = file_name
        self.__canales = canales

        gtk.Dialog.__init__(self, parent=parent)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ff0000"))
        self.set_decorated(False)
        self.set_border_width(15)

        label = gtk.Label("Guardando Imagen...")
        label.show()

        self.vbox.pack_start(label, True, True, 5)
        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):
        gobject.timeout_add(200, self.__run_load_imagen)

    def __run_load_imagen(self):
        self.__func(self.__file_name, self.__canales)
        self.destroy()
        return False
