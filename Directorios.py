#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Directorios.py por:
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

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
import JAMediaObjects.JAMFileSystem as JAMF
import JAMediaObjects.JAMediaGlobales as G

ICONOS = os.path.join(JAMediaObjects.__path__[0], "Iconos")

class Directorios(Gtk.TreeView):
    """TreView para toda la estructura de directorios."""
    
    __gsignals__ = {
    "info":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "borrar":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self)
        
        self.set_property("enable-grid-lines", True)
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        self.set_tooltip_text("Click Derecho para Opciones")
        self.modelo = TreeStoreModel()
        self.construir_columnas()
        self.connect("row-expanded", self.expandir, None)
        self.connect("row-activated", self.activar, None)
        self.connect("row-collapsed", self.colapsar, None)
        
        # http://developer.gnome.org/gtkmm/stable/group__gdkmmEnums.html
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
        Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.TOUCH_MASK)
        self.connect("button-press-event", self.handler_click)
        self.connect("key-press-event", self.keypress)
        
        self.set_model(self.modelo)
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.selecciones, self.modelo)
        self.show_all()
        
        self.dir_select = None
        self.direccion_seleccionada = None
        self.direccion_seleccionada_para_cortar = None

    def keypress(self, widget, event):
        """Para navegar por los directorios."""
        
        # derecha 114 izquierda 113 suprimir 119 backspace 22 (en xo no existe suprimir)
        tecla = event.get_keycode()[1]
        model, iter = self.treeselection.get_selected()
        valor = self.modelo.get_value(iter, 2)
        path = self.modelo.get_path(iter)
        
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
                
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
                
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
                
        elif tecla == 119:
            # suprimir
            self.get_accion(None, path, "Borrar")
            
        else:
            pass
        
        return False
        
    def selecciones(self, treeselection, model, path, is_selected, treestore):
        """Cuando se selecciona un archivo o directorio."""
        
        iter = model.get_iter(path)
        directorio =  model.get_value(iter, 2)
        
        if not is_selected and self.dir_select != directorio:
            self.dir_select = directorio
            self.emit('info', self.dir_select)
            
        return True
    
    def construir_columnas(self):
        
        celda_de_imagen = Gtk.CellRendererPixbuf()
        columna = Gtk.TreeViewColumn(None, celda_de_imagen, pixbuf=0)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Nombre', celda_de_texto, text=1)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)

        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(None, celda_de_texto, text=2)
        columna.set_property('resizable', False)
        columna.set_property('visible', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Tamaño', celda_de_texto, text=3)
        columna.set_property('resizable', True)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
    def leer_directorio(self, directorio):
        
        self.modelo.clear()
        self.leer( (directorio, False) )
        
    def leer(self, dir):
        
        archivo = ""
        
        try:
            directorio = dir[0]
            path = dir[1]
            
            if path:
                iter = self.modelo.get_iter(path)
                
            else:
                iter = self.modelo.get_iter_first()
                
            archivos = []
            
            for archivo in os.listdir(os.path.join(directorio)):
                direccion = os.path.join(directorio, archivo)
                
                if os.path.isdir(direccion):
                    icono = None
                    lectura, escritura, ejecucion = JAMF.describe_acceso_uri(direccion)
                    
                    if not lectura:
                        icono = os.path.join(ICONOS, "cerrado.png")
                        
                    else:
                        icono = os.path.join(ICONOS, "directorio.png")
                        
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, G.get_pixels(0.8))
                    iteractual = self.modelo.append(iter,[pixbuf,
                    archivo, direccion, ""])
                    self.agregar_nada(iteractual)
                    
                elif os.path.isfile(direccion):
                    archivos.append(direccion)
                    
            for x in archivos:
                archivo = os.path.basename(x)
                icono = None
                tipo = JAMF.describe_archivo(x)
                
                if 'video' in tipo:
                    icono = os.path.join(ICONOS, "video.png")
                    
                elif 'audio' in tipo:
                    icono = os.path.join(ICONOS, "sonido.png")
                    
                elif 'image' in tipo and not 'iso' in tipo:
                    #icono = os.path.join(x) #exige en rendimiento
                    icono = os.path.join(ICONOS, "imagen.png")
                    
                elif 'pdf' in tipo:
                    icono = os.path.join(ICONOS, "pdf.png")
                    
                elif 'zip' in tipo or 'rar' in tipo:
                    icono = os.path.join(ICONOS, "zip.png")
                    
                else:
                    icono = os.path.join(ICONOS, "archivo.png")
                    
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, G.get_pixels(0.8))
                self.modelo.append(iter,[pixbuf, archivo,
                x, str(os.path.getsize(x))+" bytes"])
                
        except:
            print "**** Error de acceso a un archivo o directorio ****", dir, archivo
            
    def agregar_nada(self, iterador):
        
        self.modelo.append(iterador,[None, "(Vacío, Sin Permisos o link)", None, None])
        
    def expandir (self, treeview, iter, path, user_param1):
        
        iterdelprimerhijo = treeview.modelo.iter_children(iter)
        valordelprimerhijoenlafila = treeview.modelo.get_value(iterdelprimerhijo, 1)
        valor = treeview.modelo.get_value(iter, 2)
        dir = (valor, path)
        
        if os.path.islink(os.path.join(valor)): return
    
        try:
            if os.listdir(os.path.join(valor)) \
                and valordelprimerhijoenlafila == "(Vacío, Sin Permisos o link)":
                self.leer(dir)
                treeview.modelo.remove(iterdelprimerhijo)
                
            else:
                #print "Esta direccion está vacía o ya fue llenada."
                pass
            
        except:
                #print "No tienes permisos de lectura sobre este directorio."
                pass
            
    def activar (self, treeview, path, view_column, user_param1):
        
        iter = treeview.modelo.get_iter(path)
        valor = treeview.modelo.get_value(iter, 2)
        
        try:
            if os.path.isdir(os.path.join(valor)):
                if treeview.row_expanded(path):
                    treeview.collapse_row(path)
                    
                elif not treeview.row_expanded(path):
                    treeview.expand_to_path(path)
                    
        except:
            pass
        
    def colapsar(self, treeview, iter, path, user_param1):
        
        while treeview.modelo.iter_n_children(iter):
            iterdelprimerhijo = treeview.modelo.iter_children(iter)
            treeview.modelo.remove(iterdelprimerhijo)
            
        self.agregar_nada(iter)
        
    def handler_click(self, widget, event):
        
        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)
        
        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(int(pos[0]), int(pos[1]))
        except:
            return
        
        # TreeView.get_path_at_pos(event.x, event.y) devuelve:
        # * La ruta de acceso en el punto especificado (x, y), en relación con las coordenadas widget
        # * El gtk.TreeViewColumn en ese punto
        # * La coordenada X en relación con el fondo de la celda
        # * La coordenada Y en relación con el fondo de la celda
        
        if boton == 1:
            return
        
        elif boton == 3:
            menu = MenuList(widget, boton, pos, tiempo, path, self.modelo)
            menu.connect('accion', self.get_accion)
            menu.popup(None, None, None, None, boton, tiempo)
            
        elif boton == 2:
            return
        
    def get_accion(self, widget, path, accion):
        
        iter = self.modelo.get_iter(path)
        direccion = self.modelo.get_value(iter, 2)
        lectura, escritura, ejecucion = JAMF.describe_acceso_uri(direccion)

        if accion == "Copiar":
            self.direccion_seleccionada = direccion
            
        elif accion == "Borrar":
            self.direccion_seleccionada = direccion
            # "Emite 'borrar' para pedir confirmacion en toolbaraccion."
            self.emit('borrar', self.direccion_seleccionada, self.modelo, iter)
            self.direccion_seleccionada = None

        elif accion == "Pegar":
            if self.direccion_seleccionada_para_cortar:
                if JAMF.mover(self.direccion_seleccionada_para_cortar, direccion):
                    self.collapse_row(path)
                    self.expand_to_path(path)
                    self.direccion_seleccionada_para_cortar = None
                    
            else:
                if JAMF.copiar(self.direccion_seleccionada, direccion):
                    self.collapse_row(path)
                    self.expand_to_path(path)
                    self.direccion_seleccionada = None

        elif accion == "Cortar":
            self.direccion_seleccionada_para_cortar = direccion
            self.modelo.remove(iter)
            self.direccion_seleccionada = None

        elif accion == "Crear Directorio":
            dialog = Gtk.Dialog("Crear Directorio . . .", self.get_toplevel(),
            Gtk.DialogFlags.MODAL, None)
            etiqueta = Gtk.Label("Nombre del Directorio: ")
            entry = Gtk.Entry()
            dialog.vbox.pack_start(etiqueta, True, True, 5)
            dialog.vbox.pack_start(entry, True, True, 5)
            dialog.add_button("Crear Directorio", 1)
            dialog.add_button("Cancelar", 2)
            dialog.show_all()

            if dialog.run() == 1:
                directorio_nuevo = entry.get_text()
                
                if directorio_nuevo != "" and directorio_nuevo != None:
                    if JAMF.crear_directorio(direccion, directorio_nuevo):
                        self.collapse_row(path)
                        self.expand_to_path(path)
                        
            elif dialog.run() == 2:
                pass
            
            dialog.destroy()
            
class TreeStoreModel(Gtk.TreeStore):
    
    def __init__(self):
        
        Gtk.TreeStore.__init__(self, GdkPixbuf.Pixbuf,
        GObject.TYPE_STRING, GObject.TYPE_STRING,
        GObject.TYPE_STRING)

class MenuList(Gtk.Menu):
    
    __gsignals__ = {
    "accion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING))}
    
    def __init__(self, widget, boton, pos, tiempo, path, modelo):
        
        Gtk.Menu.__init__(self)
        
        self.modelo = modelo
        self.parent_objet = widget

        lectura, escritura, ejecucion = (False, False, False)
        unidad, directorio, archivo, enlace = (False, False, False, False)
            
        iter = self.modelo.get_iter(path)
        direccion = self.modelo.get_value(iter, 2)
        
        if JAMF.describe_acceso_uri(direccion):
            lectura, escritura, ejecucion = JAMF.describe_acceso_uri(direccion)
            unidad, directorio, archivo, enlace = JAMF.describe_uri(direccion)
            
        else:
            return

        if lectura:
            copiar = Gtk.MenuItem("Copiar")
            self.append(copiar)
            copiar.connect_object("activate", self.emit_accion, path, "Copiar")
        
        if escritura and not unidad:
            borrar = Gtk.MenuItem("Borrar")
            self.append(borrar)
            borrar.connect_object("activate", self.emit_accion, path, "Borrar")
        
        if escritura and (directorio or unidad) \
            and (self.parent_objet.direccion_seleccionada != None \
            or self.parent_objet.direccion_seleccionada_para_cortar != None):
                
            pegar = Gtk.MenuItem("Pegar")
            self.append(pegar)
            pegar.connect_object("activate", self.emit_accion, path, "Pegar")

        if escritura and (directorio or archivo):
            cortar = Gtk.MenuItem("Cortar")
            self.append(cortar)
            cortar.connect_object("activate", self.emit_accion, path, "Cortar")

        if escritura and (directorio or unidad):
            nuevodirectorio = Gtk.MenuItem("Crear Directorio")
            self.append(nuevodirectorio)
            nuevodirectorio.connect_object("activate",
                self.emit_accion, path, "Crear Directorio")

        self.show_all()
        self.attach_to_widget(widget, self.null)
        
    def null(self):
        
        pass
    
    def emit_accion(self, path, accion):
        
        self.emit('accion', path, accion)
        