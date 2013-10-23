#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ApiWidget.py por:
#       Flavio Danesse <fdanesse@gmail.com>, <fdanesse@activitycentral.com>
#       CeibalJAM - Uruguay - Activity Central

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
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

BASEPATH = os.path.dirname(__file__)

class ApiWidget(Gtk.TreeView):
    """
    TreeView para mostrar:
        Clases, Funciones, Constantes y Otros items del modulo.
    """
    
    __gsignals__ = {
    "update":(GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}
    
    def __init__(self, paquete, modulo):
        
        Gtk.TreeView.__init__(self,
            Gtk.TreeStore(
                GdkPixbuf.Pixbuf, GObject.TYPE_STRING))
        
        self.objetos = {}
        self.old_update = False
        
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.TOUCH_MASK)
            
        self.set_property("enable-grid-lines", True)
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        
        self.__construir_columnas()
        
        self.connect("row-activated", self.__activar, None)
        self.connect("key-press-event", self.__keypress)
        
        self.get_selection().set_select_function(self.__selecciones, self.get_model())
        
        self.show_all()
        
        self.__load(paquete, modulo)
        
    def __construir_columnas(self):
        
        celda_de_imagen = Gtk.CellRendererPixbuf()
        columna = Gtk.TreeViewColumn(None, celda_de_imagen, pixbuf=0)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Objeto', celda_de_texto, text=1)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)
        
    def __keypress(self, widget, event):
        """
        Cuando se presiona una tecla.
        """
        
        tecla = event.get_keycode()[1]
        model, iter = self.get_selection().get_selected()
        path = self.get_model().get_path(iter)
        
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
    
    def __activar (self, treeview, path, view_column, user_param1):
        """
        Cuando se hace doble click en "Clases", "Funciones", etc . . .
        """
        
        iter = treeview.get_model().get_iter(path)
        #valor = treeview.get_model().get_value(iter, 1)
        
        if treeview.row_expanded(path):
            treeview.collapse_row(path)
            
        elif not treeview.row_expanded(path):
            treeview.expand_to_path(path)
    
    def __selecciones(self, treeselection, modelo, path, is_selected, treestore):
        """
        Cuando se selecciona una clase, funcion, etc . . .
        """
        
        iter = modelo.get_iter(path)
        datos = modelo.get_value(iter, 1)
        
        if not is_selected and self.old_update != datos:
            self.old_update = datos
            self.emit('update', self.objetos.get(datos, {}))
            self.scroll_to_cell(path)
            
        return True
    
    def __load(self, tipo, modulo):
        """
        Llena el treeview con los datos de un paquete.
        (Clases, funciones, constantes y otros.)
        """
        
        self.get_model().clear()
        
        import commands
        import json
        import codecs
        
        self.objetos = {}
        
        if tipo == "python-gi":
            ejecutable = os.path.join(BASEPATH, 'SpyderHack', 'Dir_Gi_Modulo.py')
            
        elif tipo == "python" or tipo == "Otros":
            ejecutable = os.path.join(BASEPATH, 'SpyderHack', 'Dir_Modulo.py')
        
        commands.getoutput('python %s %s' % (ejecutable, modulo))
        
        path = os.path.join("/dev/shm", "spyder_hack_out.json")
        
        archivo = codecs.open(path, "r", "utf-8")
        dict = json.JSONDecoder("utf-8").decode(archivo.read())
        archivo.close()
        
        if dict.get(modulo, False):
            iter = self.get_model().get_iter_first()
            self.__add_modulo_dict(dict[modulo], iter, tipo)
            
    def __add_modulo_dict(self, dict, iter, tipo):
        
        ### Iconos Representativos
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "class.svg")
        pixbufclase = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "def.svg")
        pixbuffunc = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "const.svg")
        pixbufconst = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "otros.svg")
        pixbufotros = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        
        modulo_path = dict.get("PATH", '')
        
        if dict.get("CLASES", False):
            newiter = self.get_model().append(iter,[ pixbufclase, 'Clases' ])
            for lista in dict.get("CLASES", []):
                self.__add(newiter, None, lista, modulo_path, tipo)
                
        if dict.get("FUNCIONES", False):
            newiter = self.get_model().append(iter,[ pixbuffunc, 'Funciones' ])
            for lista in dict.get("FUNCIONES", []):
                self.__add(newiter, None, lista, modulo_path, tipo)
                
        if dict.get("CONSTANTES", False):
            newiter = self.get_model().append(iter,[ pixbufconst, 'Constantes' ])
            for lista in dict.get("CONSTANTES", []):
                self.__add(newiter, None, lista, modulo_path, tipo)
                
        if dict.get("DESCONOCIDOS", False):
            newiter = self.get_model().append(iter,[ pixbufotros, 'Otros' ])
            for lista in dict.get("DESCONOCIDOS", []):
                self.__add(newiter, None, lista, modulo_path, tipo)
        
        for key in dict.keys():
            if key not in ["CLASES", "FUNCIONES", "CONSTANTES", "DESCONOCIDOS", "PATH"]:
                newiter = self.get_model().append(iter,[ None, key ])
                try:
                    self.__add_modulo_dict(dict[key], newiter, tipo)
                except:
                    print "Key no Esperado:", type(dict[key]), key
                
    def __add(self, iter, pixbuf, lista, modulo_path, tipo):
        
        self.get_model().append(iter,[ pixbuf, lista[0] ])
        self.objetos[lista[0]] = (lista[0], lista[1], lista[2], lista[3], modulo_path, tipo)
        