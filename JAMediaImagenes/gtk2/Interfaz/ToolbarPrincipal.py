#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
import commands


class ToolbarPrincipal(gtk.Toolbar):

    __gsignals__ = {
    "accion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        abrir = gtk.ToolButton()
        abrir.set_stock_id(gtk.STOCK_OPEN)
        abrir.set_tooltip_text("Abrir")
        abrir.connect("clicked", self.__emit_senial, "open")
        self.insert(abrir, -1)

        self.__guardar = gtk.ToolButton()
        self.__guardar.set_stock_id(gtk.STOCK_SAVE)
        self.__guardar.set_tooltip_text("Guardar")
        self.__guardar.connect("clicked", self.__emit_senial, "save")
        self.insert(self.__guardar, -1)

        self.__guardar_como = gtk.ToolButton()
        self.__guardar_como.set_stock_id(gtk.STOCK_SAVE_AS)
        self.__guardar_como.set_tooltip_text("Guardar Como")
        self.__guardar_como.connect("clicked", self.__emit_senial, "save_as")
        self.insert(self.__guardar_como, -1)

        self.insert(gtk.SeparatorToolItem(), -1)

        self.__zoom_in = gtk.ToolButton()
        self.__zoom_in.set_stock_id(gtk.STOCK_ZOOM_IN)
        self.__zoom_in.set_tooltip_text("Acercar")
        self.__zoom_in.connect("clicked", self.__emit_senial, "zoom_in")
        self.insert(self.__zoom_in, -1)

        self.__zoom_out = gtk.ToolButton()
        self.__zoom_out.set_stock_id(gtk.STOCK_ZOOM_OUT)
        self.__zoom_out.set_tooltip_text("Alejar")
        self.__zoom_out.connect("clicked", self.__emit_senial, "zoom_out")
        self.insert(self.__zoom_out, -1)

        self.__zoom_100 = gtk.ToolButton()
        self.__zoom_100.set_stock_id(gtk.STOCK_ZOOM_100)
        self.__zoom_100.set_tooltip_text("Ver a tamaño original")
        self.__zoom_100.connect("clicked", self.__emit_senial, "zoom_100")
        self.insert(self.__zoom_100, -1)

        self.__zoom_fit = gtk.ToolButton()
        self.__zoom_fit.set_stock_id(gtk.STOCK_ZOOM_FIT)
        self.__zoom_fit.set_tooltip_text("Ocupar todo el espacio disponible")
        self.__zoom_fit.connect("clicked", self.__emit_senial, "zoom_fit")
        self.insert(self.__zoom_fit, -1)

        self.insert(gtk.SeparatorToolItem(), -1)

        self.__izquierda = gtk.ToolButton()
        self.__izquierda.set_stock_id(gtk.STOCK_UNDO)
        self.__izquierda.set_tooltip_text("Rotar a la izquierda")
        self.__izquierda.connect("clicked", self.__emit_senial, "izquierda")
        self.insert(self.__izquierda, -1)

        self.__derecha = gtk.ToolButton()
        self.__derecha.set_stock_id(gtk.STOCK_REDO)
        self.__derecha.set_tooltip_text("Rotar a la derecha")
        self.__derecha.connect("clicked", self.__emit_senial, "derecha")
        self.insert(self.__derecha, -1)

        self.insert(gtk.SeparatorToolItem(), -1)

        self.__anterior = gtk.ToolButton()
        self.__anterior.set_stock_id(gtk.STOCK_GO_BACK)
        self.__anterior.set_tooltip_text("Ver imagen anterior")
        self.__anterior.connect("clicked", self.__emit_senial, "anterior")
        self.insert(self.__anterior, -1)

        self.__siguiente = gtk.ToolButton()
        self.__siguiente.set_stock_id(gtk.STOCK_GO_FORWARD)
        self.__siguiente.set_tooltip_text("Ver imagen siguiente")
        self.__siguiente.connect("clicked", self.__emit_senial, "siguiente")
        self.insert(self.__siguiente, -1)

        self.show_all()

    def __emit_senial(self, widget, senial):
        self.emit("accion", senial)

    def has_file(self, hasfile, acceso, dirpath=False):
        buttons = [self.__guardar, self.__guardar_como, self.__zoom_in,
            self.__zoom_out, self.__zoom_100, self.__zoom_fit,
            self.__izquierda, self.__derecha, self.__anterior,
            self.__siguiente]
        for button in buttons:
            button.set_sensitive(hasfile)
        self.__guardar.set_sensitive(acceso)
        paths = 0
        if dirpath:
            files = os.listdir(dirpath)
            for f in files:
                path = os.path.join(dirpath, f)
                datos = commands.getoutput(
                    'file -ik %s%s%s' % ("\"", path, "\""))
                if "image" in datos:
                    paths += 1
                    if paths > 1:
                        break
        for button in [self.__anterior, self.__siguiente]:
            button.set_sensitive(bool(paths > 1))
