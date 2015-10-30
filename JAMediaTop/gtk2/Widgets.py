#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

import os
import sys
import gtk
import gobject

from Control.Control import get_dict
from Control.Control import PATH


class TopView(gtk.TreeView):

    def __init__(self):

        gtk.TreeView.__init__(self, gtk.ListStore(
            gobject.TYPE_INT, gobject.TYPE_STRING, gobject.TYPE_INT,
            gobject.TYPE_INT, gobject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_property("enable-grid-lines", True)
        self.set_property("enable-tree-lines", True)
        #self.set_tooltip_text("Click Derecho para Opciones")

        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.__setear_columnas()
        self.show_all()

        #self.set_sensitive(False)

        #self.treeselection = self.get_selection()
        #self.treeselection.set_select_function(self.selecciones, self.modelo)

        #self.connect("row-expanded", self.__expandir, None)
        #self.connect("row-activated", self.activar, None)
        #self.connect("row-collapsed", self.colapsar, None)

        gobject.timeout_add(2000, self.__update)

    def __update(self):
        _dict = get_dict(PATH)
        items = []
        for key in _dict.keys():
            items.append([int(key), _dict[key]['name'], 0, 0, ""])
        self.__set_list(items)
        gobject.timeout_add(2000, self.__update)
        return False

    def __setear_columnas(self):
        self.append_column(self.__construir_columa('Pid', 0, True))
        self.append_column(self.__construir_columa('Proceso', 1, True))
        self.append_column(self.__construir_columa('CPU', 2, True))
        self.append_column(self.__construir_columa('Memoria', 3, True))
        self.append_column(self.__construir_columa('Ejecutable', 4, True))

    def __construir_columa(self, text, index, visible):
        render = gtk.CellRendererText()
        columna = gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('resizable', True)
        columna.set_property('visible', visible)
        #columna.set_sizing(gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna

    def __ejecutar_agregar_items(self, items):
        if not items:
            return False
        self.get_model().append(items[0])
        items.remove(items[0])
        gobject.idle_add(self.__ejecutar_agregar_items, items)
        return False

    def __set_list(self, items):
        self.get_model().clear()
        gobject.idle_add(self.__ejecutar_agregar_items, items)
