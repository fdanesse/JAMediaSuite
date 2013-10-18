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
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}
    
    def __init__(self, paquete, modulo):
        
        Gtk.TreeView.__init__(self,
            Gtk.TreeStore(
                GdkPixbuf.Pixbuf,
                GObject.TYPE_STRING))
        
        self.objetos = {}
        self.path_modulo = ""
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
        self.append_column (columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Objeto', celda_de_texto, text=1)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
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
            self.emit('update',
                self.path_modulo,
                self.objetos['tipo'],
                self.objetos['modulo'],
                datos,
                self.objetos['objetos'].get(datos, False))
            
        return True
    
    def __load(self, paquete, modulo):
        """
        Llena el treeview con los datos de un paquete.
        (Clases, funciones, constantes y otros.)
        """
        
        self.get_model().clear()
        
        self.objetos = {
            'tipo': paquete,
            'modulo': modulo,
            'objetos':{},
            }
            
        if paquete == "python-gi":
            self.__load_gi(modulo)
            
        elif paquete == "python":
            self.__load_normal(modulo)
            
    def __load_normal(self, modulo):
        """
        Funcion llamada desde __load(paquete, modulo)
        """
        
        import commands
        import shelve
        
        ejecutable = os.path.join(BASEPATH, 'SpyderHack', 'Dir_Modulo.py')
        commands.getoutput('python %s %s' % (ejecutable, modulo))
        archivo = shelve.open(os.path.join("/dev/shm", "shelvein"))
        
        dict = {}
        for key in archivo.keys():
            dict[key] = archivo[key]
        archivo.close()
        
        os.remove(os.path.join("/dev/shm", "shelvein"))
        
        CLASES = dict['CLASES']
        FUNCIONES = dict['FUNCIONES']
        CONSTANTES = dict['CONSTANTES']
        DESCONOCIDOS = dict['DESCONOCIDOS']
        self.path_modulo = dict['PATH']
        
        self.__run_load(CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS)
        
    def __load_gi(self, modulo):
        """
        Funcion llamada desde __load(paquete, modulo)
        """
        
        from Gi_Import import get_info
        CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS, self.path_modulo = get_info(modulo)
        self.__run_load(CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS)
        
    def __run_load(self, CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS):
        """
        Llena el TreeView con clases, funciones, etc . . .
        """
        
        ### Iters Base
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "class.svg")
        pixbufclase = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "def.svg")
        pixbuffunc = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "const.svg")
        pixbufconst = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        #icono = os.path.join(JAMediaObjectsPath, "Iconos", "otros.svg")
        #pixbufotros = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        
        iter = self.get_model().get_iter_first()
        
        iterclass = self.get_model().append(iter,[ pixbufclase, 'Clases'])
        iterfunc = self.get_model().append(iter,[ pixbuffunc, 'Funciones'])
        iterconst = self.get_model().append(iter,[ pixbufconst, 'Constantes'])
        #iterotros = self.get_model().append(iter,[ pixbufotros, 'Otros'])
        
        for clase in CLASES:
            self.get_model().append(iterclass,[ None, clase[0] ])
            self.objetos['objetos'][clase[0]] = (clase[1], clase[2], clase[3])
            
        for funcion in FUNCIONES:
            self.get_model().append(iterfunc,[ None, funcion[0] ])
            self.objetos['objetos'][funcion[0]] = (funcion[1], funcion[2], funcion[3])
            
        for const in CONSTANTES:
            self.get_model().append(iterconst,[ None, const[0] ])
            self.objetos['objetos'][const[0]] = (const[1], const[2], const[3])
            
        #for otros in DESCONOCIDOS:
        #    self.get_model().append(iterotros,[ None, otros[0] ])
        #    self.objetos['objetos'][otros[0]] = (otros[1], otros[2], otros[3])
        