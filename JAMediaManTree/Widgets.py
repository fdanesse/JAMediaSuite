#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
#
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
from gi.repository import GObject
from gi.repository import GtkSource

class TreeView(Gtk.TreeView):
    
    __gtype_name__ = 'TreeViewManTree'
    
    __gsignals__ = {
    'nueva-seleccion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self, dict):

        Gtk.TreeView.__init__(self, Gtk.TreeStore(GObject.TYPE_STRING))
        
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        
        self.__set_columnas()
        self.set_headers_visible(False)
        
        self.valor_select = None

        self.show_all()
        
        treeselection = self.get_selection()
        treeselection.set_select_function(self.__selecciones, self.get_model())
        
        items = []
        for grupo in dict.keys():
            items.append([grupo, dict[grupo].keys()])
            
        GObject.idle_add(self.__load_estructura, items)

    def __set_columnas(self):
        """
        Crea y agrega las columnas al TreeView.
        """
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('text', render, text=0)
        columna.set_property('resizable', True)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)
        
    def __load_estructura(self, estructura):
        """
        Carga La Estructura del Man.
        """
        
        self.get_model().clear()
        
        iter = self.get_model().get_iter_first()
        
        hijos = []
        for item in estructura:
            grupo, items = item
            iteractual = self.get_model().append(iter, [grupo])
            
            hijos.append([self.get_model().get_path(iteractual), items])
            
        for hijo in hijos:
            path, items = hijo
            iter = self.get_model().get_iter(path)
            
            for item in items:
                self.get_model().append(iter, [item])
                
    def __selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """
        
        # model y listore son ==
        iter = model.get_iter(path)
        valor =  model.get_value(iter, 0)
        
        if not is_selected and self.valor_select != valor:
            self.scroll_to_cell(model.get_path(iter))
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)
            
        return True
    
    def do_row_activated(self, path, column):
        """
        Cuando se hace doble click sobre una fila.
        """
        
        if self.row_expanded(path):
            self.collapse_row(path)
            
        else:
            self.expand_to_path(path)
    
    '''
    # FIXME: Reescribir.
    def do_key_press_event(self, event):
        """
        Funciones adicionales para moverse en el TreeView
        """

        tecla = event.keyval

        model, iter = self.get_selection().get_selected()

        if iter is None: return

        path = self.get_model().get_path(iter)

        if tecla == 65293:
            if self.row_expanded(path):
                self.collapse_row(path)
                
            else:
                self.expand_to_path(path)
    
        elif tecla == 65361:

            if self.row_expanded(path):
                self.collapse_row(path)
                return False

            len_max = len(str(path).split(":"))

            if len_max > 1:
                path = str(path).split(":")
                path_str = ""
                
                for x in path:
                    if path_str != "":
                        path_str = path_str + ":" + x
                        
                    else:
                        path_str = x

                n = len(path[len(path) - 1]) + 1
                path_str = path_str[:-n]

                try:
                    new_path = Gtk.TreePath.new_from_string(path_str)
                    iter = self.get_model().get_iter(new_path)
                    self.get_selection().select_iter(iter)
                    self.scroll_to_cell(new_path)
                    
                except:
                    return False
            else:
                iter = self.get_model().get_iter_first()
                self.get_selection().select_iter(iter)
                path = model.get_path(iter)
                self.scroll_to_cell(path)

        elif tecla == 65363:
            if not self.row_expanded(path):
                self.expand_to_path(path)

        else:
            pass
        
        return False'''
    
class SourceView(GtkSource.View):

    __gtype_name__ = 'SourceViewManTree'
    
    def __init__(self):

        GtkSource.View.__init__(self)
        
        self.set_editable(False)
        
        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)
        
        self.show_all()
        