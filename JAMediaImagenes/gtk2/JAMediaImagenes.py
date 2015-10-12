#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import gtk
from Interfaz.MenuPrincipal import MenuPrincipal
from Processor.ImgProcessor import ImgProcessor

PATH = os.path.dirname(__file__)


class JAMediaImagenes(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("JAMediaImagenes")
        self.set_icon_from_file(os.path.join(PATH,
            "iconos", "JAMediaImagenes.svg"))
        self.set_resizable(True)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)

        self.__processor = ImgProcessor()

        __vbox_base = gtk.VBox()

        self.__menu = MenuPrincipal()
        self.__visor_imagen = gtk.Image()
        self.__status_bar = gtk.Statusbar()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(self.__visor_imagen)

        __vbox_base.pack_start(self.__menu, False, False)
        __vbox_base.pack_start(scroll, True, True, 0)
        __vbox_base.pack_start(self.__status_bar, False, False)

        self.add(__vbox_base)
        self.show_all()

        self.resize(640, 480)

        self.__processor.connect("update", self.__update_pixbuf)
        self.__menu.connect("open", self.__open_file)
        self.__menu.connect("close", self.__close_file)
        self.connect("delete-event", self.__salir)

        print "JAMediaImagenes process:", os.getpid()
        self.__close_file(False)

    def __close_file(self, menu=False):
        if self.__processor.has_changes():
            print "FIXME: Abrir Dialogo pidiendo confirmación para guardar o guardar como", self.__close_file
        self.__processor.close_file()
        self.__menu.has_file(False, False)
        #print "FIXME: Resetear Toolbars y StatusBars", self.__close_file

    def __update_pixbuf(self, processor, pixbuf):
        """
        Solo Actualiza lo que se ve.
        """
        #print "FIXME: agregar rotaciones y escalas, actualizar StatusBars", self.__update_pixbuf
        self.__visor_imagen.set_from_pixbuf(pixbuf)
        self.__status_bar.push(0, "Text")

    def __open_file(self, menu, filepath):
        """
        Cuando se abre un nuevo archivo.
        """
        if filepath:
            if os.path.exists(filepath):
                if os.path.isfile(filepath):
                    self.__close_file()
                    if self.__processor.open(filepath):
                        acceso = os.access(filepath, os.W_OK)
                        self.__menu.has_file(True, acceso)
                        #print "FIXME: Actualizar Toolbars", self.__open_file

    def __salir(self, widget=None, senial=None):
        gtk.main_quit()
        sys.exit(0)


if __name__ == "__main__":
    JAMediaImagenes()
    gtk.main()
