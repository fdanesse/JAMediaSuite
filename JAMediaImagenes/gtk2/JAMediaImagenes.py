#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import gobject
import gtk
from Interfaz.MenuPrincipal import MenuPrincipal
from Processor.ImgProcessor import ImgProcessor
from Utiles.Canales.Canales import Canales

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

        self.__utiles = {}
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
        self.__menu.connect("open-util", self.__open_util)
        self.connect("delete-event", self.__salir)
        #self.connect("key-press-event", self.__key_press_event)

        print "JAMediaImagenes process:", os.getpid()
        self.__close_file(False)

    #def __key_press_event(self, widget, event):
    #    key = gtk.gdk.keyval_name(event.keyval)
    #    if key == "Right":
    #        pass
    #    elif key == "Left":
    #        pass
    #    elif key == "Delete":
    #        pass # Eliminar
    #    elif key == "KP_Add":
    #        pass # zoom in
    #    elif key == "KP_Subtract":
    #        pass # zoom out
    #    return False

    def __open_util(self, menu, text):
        util = self.__utiles.get(text, False)
        if not util:
            self.__utiles[text] = Canales(self)
            self.__utiles[text].connect("delete-event", self.__close_util)
            gobject.idle_add(self.__utiles[text].set_file,
                self.__processor.get_file_path())

    def __close_util(self, widget=False, senial=False):
        utiles = self.__utiles.items()
        for util in utiles:
            if widget in util:
                del(self.__utiles[util[0]])

    def __close_file(self, menu=False):
        if self.__processor.has_changes():
            print "FIXME: Abrir Dialogo pidiendo confirmación para guardar o guardar como", self.__close_file
        self.__processor.close_file()
        self.__menu.has_file(False, False)
        #print "FIXME: Resetear Toolbars y StatusBars", self.__close_file

    def __scale_full(self, pixbuf):
        """
        Escala ocupando todo el espacio visible del widget donde debe dibujarse
        """
        rect = self.__visor_imagen.get_parent().get_allocation()
        src_width, src_height = pixbuf.get_width(), pixbuf.get_height()
        scale = min(float(rect.width) / src_width,
            float(rect.height) / src_height)
        new_width = int(scale * src_width)
        new_height = int(scale * src_height)
        pixbuf = pixbuf.scale_simple(new_width,
            new_height, gtk.gdk.INTERP_BILINEAR)
        return pixbuf

    def __update_pixbuf(self, processor, pixbuf, info):
        """
        Solo Actualiza lo que se ve.
        """
        #print "FIXME: agregar rotaciones y escalas, actualizar StatusBars", self.__update_pixbuf

        if pixbuf:
            pixbuf = self.__scale_full(pixbuf)

        self.__visor_imagen.set_from_pixbuf(pixbuf)
        text = "Img: "
        if pixbuf:
            text = "%s %s   Size: %s   Ext: %s   Mime: %s   Kb: %.2f" % (
                text, info.get("path", ""), info.get("size", ""),
                info.get("name", ""), info.get("mime_types", ""),
                info.get("mb", 0.0) / 1024.0)
        self.__status_bar.push(0, text)

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
