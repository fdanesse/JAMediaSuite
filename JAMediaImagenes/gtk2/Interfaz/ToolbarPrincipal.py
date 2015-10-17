#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject

BASE_PATH = os.path.dirname(__file__)


class ToolbarPrincipal(gtk.Toolbar):

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        """
        abrir
        guardar
        guardar como

        zoom-in
        zoom-out
        original resolution
        fullwidget

        rotar izquierda
        rotar derecha

        anterior
        siguiente
        """

        abrir = gtk.ToolButton()
        abrir.set_stock_id(gtk.STOCK_OPEN)
        abrir.set_tooltip_text("Abrir")
        abrir.connect("clicked", self.__emit_senial, "open")
        self.insert(abrir, -1)

        guardar = gtk.ToolButton()
        guardar.set_stock_id(gtk.STOCK_SAVE)
        guardar.set_tooltip_text("Guardar")
        abrir.connect("clicked", self.__emit_senial, "save")
        self.insert(guardar, -1)

        guardar_como = gtk.ToolButton()
        guardar_como.set_stock_id(gtk.STOCK_SAVE_AS)
        guardar_como.set_tooltip_text("Guardar Como")
        guardar_como.connect("clicked", self.__emit_senial, "save_as")
        self.insert(guardar_como, -1)

        self.insert(gtk.SeparatorToolItem(), -1)

        zoom_in = gtk.ToolButton()
        zoom_in.set_stock_id(gtk.STOCK_ZOOM_IN)
        zoom_in.set_tooltip_text("Acercar")
        zoom_in.connect("clicked", self.__emit_senial, "zoom_in")
        self.insert(zoom_in, -1)

        zoom_out = gtk.ToolButton()
        zoom_out.set_stock_id(gtk.STOCK_ZOOM_OUT)
        zoom_out.set_tooltip_text("Alejar")
        zoom_out.connect("clicked", self.__emit_senial, "zoom_out")
        self.insert(zoom_out, -1)

        zoom_100 = gtk.ToolButton()
        zoom_100.set_stock_id(gtk.STOCK_ZOOM_100)
        zoom_100.set_tooltip_text("Ver a tamaño original")
        zoom_100.connect("clicked", self.__emit_senial, "zoom_100")
        self.insert(zoom_100, -1)

        zoom_fit = gtk.ToolButton()
        zoom_fit.set_stock_id(gtk.STOCK_ZOOM_FIT)
        zoom_fit.set_tooltip_text("Ocupar todo el espacio disponible")
        zoom_fit.connect("clicked", self.__emit_senial, "zoom_fit")
        self.insert(zoom_fit, -1)

        self.insert(gtk.SeparatorToolItem(), -1)

        izquierda = gtk.ToolButton()
        izquierda.set_stock_id(gtk.STOCK_UNDO)
        izquierda.set_tooltip_text("Rotar a la izquierda")
        izquierda.connect("clicked", self.__emit_senial, "izquierda")
        self.insert(izquierda, -1)

        derecha = gtk.ToolButton()
        derecha.set_stock_id(gtk.STOCK_REDO)
        derecha.set_tooltip_text("Rotar a la derecha")
        derecha.connect("clicked", self.__emit_senial, "derecha")
        self.insert(derecha, -1)

        self.insert(gtk.SeparatorToolItem(), -1)

        anterior = gtk.ToolButton()
        anterior.set_stock_id(gtk.STOCK_GO_BACK)
        anterior.set_tooltip_text("Ver imagen anterior")
        anterior.connect("clicked", self.__emit_senial, "anterior")
        self.insert(anterior, -1)

        siguiente = gtk.ToolButton()
        siguiente.set_stock_id(gtk.STOCK_GO_FORWARD)
        siguiente.set_tooltip_text("Ver imagen siguiente")
        siguiente.connect("clicked", self.__emit_senial, "siguiente")
        self.insert(siguiente, -1)

        self.show_all()

    def __emit_senial(self, widget, senial):
        self.emit('accion', senial)

