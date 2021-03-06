#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Pango
from BusquedasTreeView import buscar_mas


class TextView(Gtk.TextView):

    def __init__(self):

        Gtk.TextView.__init__(self)

        self.set_border_width(15)
        self.set_editable(False)
        #self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.set_buffer(Gtk.TextBuffer())
        self.fontzise = 10
        font = "%s %s" % ("Monospace", self.fontzise)
        self.modify_font(Pango.FontDescription(font))

        self.show_all()

    def zoom(self, zoom):
        if zoom == "Alejar":
            self.fontzise -= 1
            if self.fontzise < 5:
                self.fontzise = 5
        elif zoom == "Acercar":
            self.fontzise += 1
            if self.fontzise > 20:
                self.fontzise = 20
        font = "%s %s" % ("Monospace", self.fontzise)
        self.modify_font(Pango.FontDescription(font))


class Lista(Gtk.TreeView):

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.TreeStore(GObject.TYPE_STRING,
            GObject.TYPE_STRING))

        self.valor_select = None

        self.set_property("rules-hint", True)
        self.set_property("enable-grid-lines", True)
        self.set_property("enable-tree-lines", True)

        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.__setear_columnas()
        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())
        self.show_all()

        self.connect("row-activated", self.__activar, None)
        self.connect("key-press-event", self.__keypress)

    def __keypress(self, widget, event):
        tecla = event.get_keycode()[1]
        model, _iter = self.get_selection().get_selected()
        path = model.get_path(_iter)
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        return False

    def __activar(self, treeview, path, view_column, user_param1):
        if self.row_expanded(path):
            self.collapse_row(path)
        elif not self.row_expanded(path):
            self.expand_to_path(path)

    def __setear_columnas(self):
        self.append_column(self.__construir_columa('Plugins', 0, True))
        self.append_column(self.__construir_columa('Descripción', 1, True))

    def __construir_columa(self, text, index, visible):
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna

    def __selecciones(self, treeselection, model, path, is_selected, listore):
        _iter = model.get_iter(path)
        valor = model.get_value(_iter, 0)
        if not is_selected and self.valor_select != valor:
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)
            self.scroll_to_cell(path)
        return True

    def buscar_mas(self, accion, texto):
        buscar_mas(self, accion, texto)
