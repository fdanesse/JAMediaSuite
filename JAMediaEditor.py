#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   IdeMain.py por:
#       Cristian García     <cristian99garcia@gmail.com>
#       Ignacio Rodriguez   <nachoel01@gmail.com>
#       Flavio Danesse      <fdanesse@gmail.com>

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
import json

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import JAMediaEditor
from JAMediaEditor.Widgets import Menu
from JAMediaEditor.BasePanel import BasePanel

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

home = os.environ["HOME"]

BatovideWorkSpace = os.path.join(
    home, 'BatovideWorkSpace')

if not os.path.exists(BatovideWorkSpace):
    os.mkdir(BatovideWorkSpace)
    
#PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMediaEditor.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    
class JAMediaEditor(Gtk.Window):
    
    __gtype_name__ = 'WindowJAMediaEditor'
    
    def __init__(self):
        
        Gtk.Window.__init__(self)
        
        self.set_title("JAMediaEditor")
        
        self.set_icon_from_file(os.path.join(
            JAMediaObjectsPath, "Iconos", "jamediaeditor.png"))
            
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.updater = False
        self.sourceview = False
        
        base_widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.menu = Menu()
        #toolbar = MainToolbar()
        self.base_panel = BasePanel()
        #trytoolbar = TryToolbar()
        
        base_widget.pack_start(self.menu, False, False, 0)
        #base_widget.pack_start(toolbar, False, False, 0)
        base_widget.pack_start(self.base_panel, True, True, 0)
        #base_widget.pack_start(trytoolbar, False, False, 0)
        
        self.add(base_widget)
        
        self.show_all()
        
        self.maximize()
        
        self.menu.connect('accion_ver', self.__ejecutar_accion_ver)
        self.menu.connect('accion_codigo', self.__ejecutar_accion_codigo)
        self.menu.connect('accion_proyecto', self.__ejecutar_accion_proyecto)
        self.menu.connect('accion_archivo', self.__ejecutar_accion_archivo)
        
        self.base_panel.connect("update", self.__new_handler)
        
        self.connect("destroy", self.__exit)
        
    def __ejecutar_accion_codigo(self, widget, accion):
        """
        Cuando se hace click en una opción del menú codigo.
        """
        
        self.base_panel.set_accion_codigo(widget, accion)
        
    def __ejecutar_accion_ver(self, widget, accion):
        """
        Cuando se hace click en una opción del menú ver.
        """
        
        self.base_panel.set_accion_ver(widget, accion)
        
    def __ejecutar_accion_archivo(self, widget, accion):
        """
        Cuando se hace click en una opción del menú que
        afecta al archivo seleccionado.
        """
        
        self.base_panel.set_accion_archivo(widget, accion)
        
    def __ejecutar_accion_proyecto(self, widget, accion):
        """
        Cuando se hace click en una opción del menú proyecto.
        """
        
        self.base_panel.set_accion_proyecto(widget, accion)
        
    def __exit(self, widget=None):
        """
        Sale de la aplicación.
        """
        
        import sys
        sys.exit(0)
        
    def __new_handler(self, widget, sourceview, reset):
        """
        Elimina o reinicia la funcion que
        actualiza las toolbars y menús.
        """
        
        if self.updater and self.updater != None:
            GObject.source_remove(self.updater)
            self.updater = False
            self.sourceview = False
            
        if reset:
            self.sourceview = sourceview
            self.updater = GObject.timeout_add(500, self.__update)

    def __update(self):
        """
        Actualiza las toolbars y menus.
        """
        
        retorno = True
        
        archivo = self.sourceview.archivo
        texto = ""
        buffer = self.sourceview.get_buffer()
        
        activar = [
            "Cerrar",
            "Guardar Como"]
            
        desactivar = []
        
        if archivo:
            if os.path.exists(archivo):
                arch = open(archivo, 'r')
                texto = arch.read()
                arch.close()
        
        ### Si hay texto en el archivo seleccionado.
        inicio, fin = buffer.get_bounds()
        buf = buffer.get_text(inicio, fin, 0)
        
        opciones_archivos = [
            "Seleccionar Todo",
            #"Ejecutar Archivo",
            #"Detener Ejecución",
            "Numeracion",
            "Aumentar",
            "Disminuir",
            "Formato",
            "Identar",
            "De Identar",
            "Identar con Espacios",
            "Identar con Tabulaciones",
            "Buscar Texto",
            "Reemplazar Texto",
            "Chequear",
            "Valorar"]
            
        if buf:
            for opcion in opciones_archivos:
                activar.append(opcion)
            
        else:
            for opcion in opciones_archivos:
                desactivar.append(opcion)
            
        ### Si el contenido del archivo es distindo al del buffer.
        if texto != buf:
            activar.append("Guardar")
            
        else:
            desactivar.append("Guardar")
            
        ### Si hay texto en el clipboard, se puede pegar
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        texto = clipboard.wait_for_text()
        
        if texto:
            activar.append("Pegar")
            
        else:
            desactivar.append("Pegar")
            
        try:
            ### Si se puede deshacer.
            if buffer.can_undo():
                activar.append("Deshacer")
                
            else:
                desactivar.append("Deshacer")
                
            ### Si se puede Rehacer.
            if buffer.can_redo():
                activar.append("Rehacer")
                
            else:
                desactivar.append("Rehacer")
        
            ### Si hay texto seleccionado, se puede copiar y cortar.
            if buffer.get_selection_bounds():
                activar.append("Cortar")
                activar.append("Copiar")
                
            else:
                desactivar.append("Cortar")
                desactivar.append("Copiar")
            
        except:
            ### Si no hay un sourceview, es porque no hay archivos abiertos.
            
            desactivar = [
                "Cortar",
                "Copiar",
                "Rehacer",
                "Deshacer",
                "Guardar",
                "Cerrar",
                "Guardar Como",
                "Pegar",
                "Seleccionar Todo",
                "Ejecutar Archivo",
                "Detener Ejecución",
                "Seleccionar Todo",
                "Numeracion",
                "Aumentar",
                "Disminuir",
                "Formato",
                "Identar",
                "De Identar",
                "Identar con Espacios",
                "Identar con Tabulaciones",
                "Buscar Texto",
                "Reemplazar Texto",
                "Chequear",
                "Valorar"]

            activar = []
            
            self.base_panel.infonotebook.set_introspeccion(None, "")
            retorno = False
            
        ### Actualizar el menu.
        self.menu.update_archivos(True, activar)
        self.menu.update_archivos(False, desactivar)
        
        ### Actualizar las toolbars.
        self.base_panel.toolbararchivo.update(True, activar)
        self.base_panel.toolbararchivo.update(False, desactivar)
        
        if self.base_panel.proyecto:
            codeviews = self.base_panel.workpanel.get_archivos_de_proyecto(self.base_panel.proyecto["path"])
            
            ### Si no hay archivos de proyecto abiertos, no hay proyecto abierto.
            if not codeviews:
                self.base_panel.cerrar_proyecto()
                self.menu.activar_proyecto(False)
                self.base_panel.toolbarproyecto.activar(False)
                
            else:
                self.menu.activar_proyecto(True)
                self.base_panel.toolbarproyecto.activar(True)
                
                if self.base_panel.workpanel.ejecucion:
                    self.base_panel.toolbarproyecto.dict_proyecto["Ejecutar Proyecto"].set_sensitive(False)
                    self.base_panel.toolbarproyecto.dict_proyecto["Detener Ejecución"].set_sensitive(True)
                    
                else:
                    self.base_panel.toolbarproyecto.dict_proyecto["Ejecutar Proyecto"].set_sensitive(True)
                    self.base_panel.toolbarproyecto.dict_proyecto["Detener Ejecución"].set_sensitive(False)
            
        else:
            self.menu.activar_proyecto(False)
            self.base_panel.toolbarproyecto.activar(False)
            
            if self.base_panel.workpanel.ejecucion:
                self.base_panel.toolbararchivo.dict_archivo["Ejecutar Archivo"].set_sensitive(False)
                self.base_panel.toolbararchivo.dict_archivo["Detener Ejecución"].set_sensitive(True)
                
            else:
                self.base_panel.toolbararchivo.dict_archivo["Ejecutar Archivo"].set_sensitive(True)
                self.base_panel.toolbararchivo.dict_archivo["Detener Ejecución"].set_sensitive(False)
            
        return retorno
    
if __name__=="__main__":
    JAMediaEditor()
    Gtk.main()
