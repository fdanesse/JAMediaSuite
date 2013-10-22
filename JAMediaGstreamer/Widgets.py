#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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

import os

from gi.repository import Gtk
from gi.repository import Gdk
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
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(
            self, Gtk.TreeStore(
            GObject.TYPE_STRING,
            GObject.TYPE_STRING))
        
        self.valor_select = None
        
        self.set_property("rules-hint", True)
        self.set_property("enable-grid-lines", True)
        self.set_property("enable-tree-lines", True)
        
        self.set_headers_clickable(True)
        self.set_headers_visible(True)
        
        self.setear_columnas()
        
        self.get_selection().set_select_function(self.selecciones, self.get_model())
        
        self.show_all()
        
        self.connect("row-activated", self.activar, None)
        
        self.connect("key-press-event", self.keypress)
        
    def keypress(self, widget, event):
        
        tecla = event.get_keycode()[1]
        model, iter = self.get_selection().get_selected()
        path = model.get_path(iter)
        
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
    
    def activar (self, treeview, path, view_column, user_param1):
        
        iter = self.get_model().get_iter(path)
        
        if self.row_expanded(path):
            self.collapse_row(path)
            
        elif not self.row_expanded(path):
            self.expand_to_path(path)
        
    def setear_columnas(self):
        
        self.append_column(self.construir_columa('Plugins', 0, True))
        self.append_column(self.construir_columa('Descripción', 1, True))
        
    def construir_columa(self, text, index, visible):
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text = index)
        
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        
        return columna
    
    def selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """
        
        # model y listore son ==
        iter = model.get_iter(path)
        valor =  model.get_value(iter, 0)
        
        if not is_selected and self.valor_select != valor:
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)
            self.scroll_to_cell(path)
            
        return True
    