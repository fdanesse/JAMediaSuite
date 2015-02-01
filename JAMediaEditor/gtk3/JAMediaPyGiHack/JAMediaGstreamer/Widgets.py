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


class TextView(Gtk.TextView):

    def __init__(self):

        Gtk.TextView.__init__(self)

        self.set_editable(False)
        self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.set_buffer(Gtk.TextBuffer())
        self.show_all()


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

    def __buscar_recursivo_delante(self, model, _iter, texto):
        contenido = model.get_value(_iter, 0).lower()
        contenido1 = model.get_value(_iter, 1).lower()
        if texto in contenido or texto in contenido1:
            self.get_selection().select_iter(_iter)
            self.scroll_to_cell(model.get_path(_iter))
            return True
        else:
            if model.iter_has_child(_iter):
                self.expand_to_path(model.get_path(_iter))
                _iter = model.iter_children(_iter)
                while _iter:
                    ret = self.__buscar_recursivo_delante(model, _iter, texto)
                    if ret:
                        return ret
                    _iter = model.iter_next(_iter)
            else:
                return False
        return False

    def __buscar_recursivo_atras(self, model, _iter, texto):
        if model.iter_has_child(_iter):
            model2, _iter2 = self.get_selection().get_selected()
            _iter3 = model.iter_parent(_iter2)
            # valores del item analizado
            v1 = model.get_value(_iter, 0).lower()
            v2 = model.get_value(_iter, 1).lower()
            if _iter3:
                # valores del padre de lo seleccionado
                v11 = model2.get_value(_iter3, 0).lower()
                v22 = model2.get_value(_iter3, 1).lower()
            else:
                # valores de lo seleccionado
                v11 = model2.get_value(_iter2, 0).lower()
                v22 = model2.get_value(_iter2, 1).lower()
            if v1 != v11 and v2 != v22:
                self.expand_to_path(model.get_path(_iter))
                _iter2 = model.iter_children(_iter)
                item = _iter2
                _iter3 = None
                while item:
                    _iter3 = item
                    item = model.iter_next(item)
                while _iter3:
                    ret = self.__buscar_recursivo_atras(model, _iter3, texto)
                    if ret:
                        return ret
                    _iter3 = model.iter_previous(_iter3)
        contenido = model.get_value(_iter, 0).lower()
        contenido1 = model.get_value(_iter, 1).lower()
        if texto in contenido or texto in contenido1:
            self.get_selection().select_iter(_iter)
            self.scroll_to_cell(model.get_path(_iter))
            return True
        return False

    def buscar_delante(self, texto, _iter=False):
        model = self.get_model()
        if not _iter:
            _iter = model.get_iter_first()
        if not _iter:
            return
        texto = texto.lower()
        while _iter:
            ret = self.__buscar_recursivo_delante(model, _iter, texto)
            if ret:
                return ret
            _iter = model.iter_next(_iter)
        return False

    def buscar_detras(self, texto, _iter=False):
        model = self.get_model()
        if not _iter:
            _iter = model.get_iter_first()
            item = _iter
            _iter = None
            while item:
                _iter = item
                item = model.iter_next(item)
        if not _iter:
            return
        texto = texto.lower()
        while _iter:
            ret = self.__buscar_recursivo_atras(model, _iter, texto)
            if ret:
                return ret
            _iter = model.iter_previous(_iter)
        return False

    def buscar_mas(self, accion, texto):
        model, _iter = self.get_selection().get_selected()
        if accion == "Buscar Siguiente":
            if model.iter_has_child(_iter):
                # Si tiene hijos, buscar entre ellos
                self.expand_to_path(model.get_path(_iter))
                _iter2 = model.iter_children(_iter)
                ret = self.buscar_delante(texto, _iter2)
                if ret:
                    return ret

            # Si no tiene hijos, continuar en el mismo nivel
            _iter2 = model.iter_next(_iter)
            if _iter2:
                ret = self.buscar_delante(texto, _iter2)
                if ret:
                    return ret

            # Probablemente no hay mas iters en este nivel, buscar en el padre
            _iter2 = model.iter_parent(_iter)
            if _iter2:
                ret = self.buscar_delante(texto, model.iter_next(_iter2))
                if ret:
                    return ret

        elif accion == "Buscar Anterior":
            _iter2 = model.iter_previous(_iter)
            if _iter2:
                ret = self.buscar_detras(texto, _iter2)
                if ret:
                    return ret

            _iter2 = model.iter_parent(_iter)
            if _iter2:
                ret = self.buscar_detras(texto, _iter2)
                if ret:
                    return ret
