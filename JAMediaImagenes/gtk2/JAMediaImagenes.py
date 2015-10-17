#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import gobject
import gtk
from Interfaz.MenuPrincipal import MenuPrincipal
from Interfaz.ToolbarPrincipal import ToolbarPrincipal
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
        self.set_size_request(640, 480)
        self.set_position(gtk.WIN_POS_CENTER)

        self.__utiles = {}
        self.__processor = ImgProcessor()

        vbox_base = gtk.VBox()

        self.__menu = MenuPrincipal()
        self.__toolbar = ToolbarPrincipal()
        self.__visor_imagen = gtk.Image()
        self.__status_bar = gtk.Statusbar()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(self.__visor_imagen)

        vbox_base.pack_start(self.__menu, False, False)
        vbox_base.pack_start(self.__toolbar, False, False)
        vbox_base.pack_start(scroll, True, True, 0)
        vbox_base.pack_start(self.__status_bar, False, False)

        self.add(vbox_base)
        self.show_all()

        self.__menu.connect("open", self.__open_file)
        self.__menu.connect("close", self.__close_file)
        self.__menu.connect("open-util", self.__open_util)
        self.connect("delete-event", self.__salir)
        self.__toolbar.connect("accion", self.__action_toolbar)
        #self.__visor_imagen.connect("size-allocate", self.__size_allocate)
        #self.connect("key-press-event", self.__key_press_event)

        print "JAMediaImagenes process:", os.getpid()
        self.__close_file(False)

    #def __size_allocate(self, window, event):
    #    self.__visor_imagen.disconnect_by_func(self.__size_allocate)
    #    gobject.idle_add(self.__reload)
    #    return True

    #def __reload(self):
    #    pixbuf = self.__processor.get_pixbuf_channles(
    #        self.__visor_imagen, "Original")
    #    self.__visor_imagen.set_from_pixbuf(pixbuf)
    #    self.__visor_imagen.connect("size-allocate", self.__size_allocate)
    #    return False

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

    def __action_toolbar(self, toolbar, accion):
        if "open" in accion:
            #FIXME: Agregar preview para imagen seleccionada
            dialog = gtk.FileChooserDialog(parent=self.get_toplevel(),
                action=gtk.FILE_CHOOSER_ACTION_OPEN,
                title="Abrir Archivo",
                buttons=("Abrir", gtk.RESPONSE_ACCEPT,
                "Cancelar", gtk.RESPONSE_CANCEL))
            dialog.set_border_width(15)
            file_path = self.__processor.get_file_path()
            if file_path:
                dir_path = os.path.dirname(self.__processor.get_file_path())
                dialog.set_current_folder_uri("file://%s" % dir_path)
            dialog.set_select_multiple(False)
            filtro = gtk.FileFilter()
            filtro.set_name("image")
            filtro.add_mime_type("image/*")
            dialog.add_filter(filtro)
            run = dialog.run()
            if run == gtk.RESPONSE_ACCEPT:
                filepath = os.path.realpath(dialog.get_filename())
                self.__open_file(False, filepath)
                dir_path = os.path.dirname(filepath)
                self.__menu.set_dir_path(dir_path)
            dialog.destroy()

        else:
            print accion

    def __open_util(self, menu, text):
        util = self.__utiles.get(text, False)
        if not util:
            self.__utiles[text] = Canales(self, self.__processor)
            self.__utiles[text].connect("delete-event", self.__close_util)
            gobject.idle_add(self.__utiles[text].run)

    def __close_util(self, widget=False, senial=False):
        utiles = self.__utiles.items()
        for util in utiles:
            if widget in util:
                del(self.__utiles[util[0]])

    def __close_file(self, menu=False):
        #if self.__processor.has_changes():
        #    print "FIXME: Abrir Dialogo pidiendo confirmación para guardar o guardar como", self.__close_file
        self.__processor.close_file()
        self.__menu.has_file(False, False)
        self.__toolbar.has_file(False, False)
        self.__update_status_bar(False)
        self.__visor_imagen.set_from_pixbuf(None)
        #print "FIXME: Resetear Toolbars y StatusBars", self.__close_file
        utiles = self.__utiles.items()
        for util in utiles:
            util[1].run()

    def __update_status_bar(self, info):
        text = "Img: "
        if info:
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
                    info = self.__processor.open(filepath)
                    acceso = os.access(filepath, os.W_OK)
                    self.__menu.has_file(True, acceso)
                    self.__update_status_bar(info)
                    self.__toolbar.has_file(True, acceso,
                        os.path.dirname(filepath))
                    pixbuf = self.__processor.get_pixbuf_channles(
                        self.__visor_imagen, "Original")
                    self.__visor_imagen.set_from_pixbuf(pixbuf)
                    utiles = self.__utiles.items()
                    for util in utiles:
                        util[1].run()

    def __salir(self, widget=None, senial=None):
        gtk.main_quit()
        sys.exit(0)


if __name__ == "__main__":
    JAMediaImagenes()
    gtk.main()
