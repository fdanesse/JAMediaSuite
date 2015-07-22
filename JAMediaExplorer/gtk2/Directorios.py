#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Directorios.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
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
import gtk
import gobject

from JAMFileSystem import describe_acceso_uri
from JAMFileSystem import describe_archivo
from JAMFileSystem import crear_directorio
from JAMFileSystem import describe_uri
from JAMFileSystem import mover

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONOS = os.path.join(BASE_PATH, "Iconos")


class Directorios(gtk.TreeView):
    """
    TreView para estructura del directorios seleccionado.
    """

    __gsignals__ = {
    "info": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "add-leer": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "borrar": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)),
    "accion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING))
        }

    def __init__(self):

        gtk.TreeView.__init__(self,
            gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING,
                gobject.TYPE_STRING, gobject.TYPE_STRING))

        self.set_property("enable-grid-lines", True)
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        self.set_property("enable-search", True)

        self.set_tooltip_text("Click Derecho para Opciones")
        self.__construir_columnas()

        # http://developer.gnome.org/gtkmm/stable/group__gdkmmEnums.html
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.KEY_PRESS_MASK)

        self.show_all()

        self.path = False
        self.dir_select = None
        self.dict = {}
        self.actualizador = False

        self.connect("row-expanded", self.__expandir, None)
        self.connect("row-activated", self.__activar, None)
        self.connect("row-collapsed", self.__colapsar, None)

        self.connect("button-press-event", self.__handler_click)
        self.connect("key-press-event", self.__keypress)

        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

    def __keypress(self, widget, event):
        """
        Para navegar por los directorios.
        """
        tecla = str(gtk.gdk.keyval_name(event.keyval))
        model, _iter = self.get_selection().get_selected()
        path = self.get_model().get_path(_iter)
        if tecla == "Left":
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == "Right":
            if not self.row_expanded(path):
                self.expand_row(path, False)
        elif tecla == "Delete":
            # suprimir
            self.__get_accion(None, path, "Borrar")
        else:
            pass
        self.get_selection().select_iter(_iter)
        return False

    def __selecciones(self, path, column):
        """
        Cuando se selecciona un archivo o directorio.
        """
        _iter = self.get_model().get_iter(path)
        directorio = self.get_model().get_value(_iter, 2)
        if self.dir_select != directorio:
            self.dir_select = directorio
            self.emit('info', self.dir_select)
        return True

    def __construir_columnas(self):
        celda_de_imagen = gtk.CellRendererPixbuf()
        columna = gtk.TreeViewColumn(None, celda_de_imagen, pixbuf=0)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        #columna.set_sizing(gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

        celda_de_texto = gtk.CellRendererText()
        celda_de_texto.set_property('editable', True)
        celda_de_texto.connect("edited", self.__edited_item)
        columna = gtk.TreeViewColumn('Nombre', celda_de_texto, text=1)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        #columna.set_sizing(gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

        celda_de_texto = gtk.CellRendererText()
        columna = gtk.TreeViewColumn(None, celda_de_texto, text=2)
        columna.set_property('resizable', False)
        columna.set_property('visible', False)
        #columna.set_sizing(gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

        celda_de_texto = gtk.CellRendererText()
        columna = gtk.TreeViewColumn('Tamaño', celda_de_texto, text=3)
        columna.set_property('resizable', True)
        columna.set_property('visible', True)
        #columna.set_sizing(gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

    def __edited_item(self, widget, path, newtext):
        _iter = self.get_model().get_iter(path)
        oldpath = self.get_model().get_value(_iter, 2)
        uno = os.path.dirname(oldpath)
        newpath = os.path.join(uno, newtext)
        if newpath != oldpath:
            if mover(oldpath, newpath):
                self.get_model().set_value(_iter, 2, newpath)
                self.get_model().set_value(_iter, 1, newtext)

    def __leer(self, dire):
        archivo = ""
        try:
            directorio = dire[0]
            path = dire[1]
            if path:
                iter_ = self.get_model().get_iter(path)
            else:
                iter_ = self.get_model().get_iter_first()
            archivos = []
            listdir = os.listdir(os.path.join(directorio))
            listdir.sort()
            for archivo in listdir:
                direccion = os.path.join(directorio, archivo)
                if not self.get_parent().get_parent().ver_ocultos:
                    if archivo.startswith('.'):
                        continue
                if os.path.isdir(direccion):
                    icono = None
                    lectura, escritura, ejecucion = describe_acceso_uri(
                        direccion)
                    if not lectura:
                        icono = os.path.join(ICONOS, "button-cancel.svg")
                    else:
                        icono = os.path.join(ICONOS, "document-open.svg")
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                        icono, -1, 30)
                    iteractual = self.get_model().append(
                        iter_, [pixbuf, archivo, direccion, ""])
                    self.__agregar_nada(iteractual)
                elif os.path.isfile(direccion):
                    archivos.append(direccion)
            for x in archivos:
                archivo = os.path.basename(x)
                icono = None
                tipo = describe_archivo(x)
                if 'video' in tipo:
                    icono = os.path.join(ICONOS, "video.svg")
                elif 'audio' in tipo:
                    icono = os.path.join(ICONOS, "sonido.svg")
                elif 'image' in tipo and not 'iso' in tipo:
                    #icono = os.path.join(x) #exige en rendimiento
                    icono = os.path.join(ICONOS, "edit-select-all.svg")
                elif 'pdf' in tipo:
                    icono = os.path.join(ICONOS, "pdf.svg")
                elif 'zip' in tipo or 'rar' in tipo:
                    icono = os.path.join(ICONOS, "edit-select-all.svg")
                else:
                    icono = os.path.join(ICONOS, "edit-select-all.svg")
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 30)
                self.get_model().append(iter_, [pixbuf, archivo,
                    x, str(os.path.getsize(x)) + " bytes"])
            self.dict[directorio] = str(listdir)
        except:
            print "**** Error de acceso:", dire, archivo
        iter_ = self.get_model().get_iter_first()
        if iter_:
            self.get_selection().select_iter(iter_)

    def __agregar_nada(self, iterador):
        self.get_model().append(iterador, [None,
            "(Vacío, Sin Permisos o link)", None, None])

    def __expandir(self, treeview, iter_, path, user_param1):
        iterdelprimerhijo = self.get_model().iter_children(iter_)
        valordelprimerhijoenlafila = self.get_model().get_value(
            iterdelprimerhijo, 1)
        valor = self.get_model().get_value(iter_, 2)
        dire = (valor, path)
        if os.path.islink(os.path.join(valor)):
            return
        try:
            if os.listdir(os.path.join(valor)) \
                and valordelprimerhijoenlafila == \
                "(Vacío, Sin Permisos o link)":
                self.__leer(dire)
                self.get_model().remove(iterdelprimerhijo)
            else:
                #print "Esta direccion está vacía o ya fue llenada."
                pass
        except:
                #print "No tienes permisos de lectura sobre este directorio."
                pass

    def __activar(self, treeview, path, view_column, user_param1):
        iter_ = self.get_model().get_iter(path)
        valor = self.get_model().get_value(iter_, 2)
        try:
            if os.path.isdir(os.path.join(valor)):
                if treeview.row_expanded(path):
                    treeview.collapse_row(path)
                elif not treeview.row_expanded(path):
                    treeview.expand_to_path(path)
        except:
            pass

    def __colapsar(self, treeview, iter_, path, user_param1):
        valor = self.get_model().get_value(iter_, 2)
        if self.dict.get(valor, False):
            del (self.dict[valor])
        while self.get_model().iter_n_children(iter_):
            iterdelprimerhijo = self.get_model().iter_children(iter_)
            self.get_model().remove(iterdelprimerhijo)
        self.__agregar_nada(iter_)

    def __handler_click(self, widget, event):
        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)
        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(
                int(pos[0]), int(pos[1]))
        except:
            return
        if boton == 1:
            return
        elif boton == 3:
            menu = MenuList(
                widget, boton, pos, tiempo, path, self.get_model())
            menu.connect('accion', self.__get_accion)
            gtk.Menu.popup(menu, None, None, None, boton, tiempo)
        elif boton == 2:
            return

    def __get_accion(self, widget, path, accion):
        iter_ = self.get_model().get_iter(path)
        direccion = self.get_model().get_value(iter_, 2)
        lectura, escritura, ejecucion = describe_acceso_uri(direccion)
        if accion == "Crear Directorio":
            dialog = gtk.Dialog("Crear Directorio . . .",
                self.get_toplevel(), gtk.DIALOG_MODAL, None)
            etiqueta = gtk.Label("Nombre del Directorio: ")
            entry = gtk.Entry()
            dialog.vbox.pack_start(etiqueta, True, True, 5)
            dialog.vbox.pack_start(entry, True, True, 5)
            dialog.add_button("Crear Directorio", 1)
            dialog.add_button("Cancelar", 2)
            dialog.vbox.show_all()
            respuesta = dialog.run()
            directorio_nuevo = entry.get_text()
            dialog.destroy()
            if respuesta == 1:
                if directorio_nuevo != "" and directorio_nuevo != None:
                    if crear_directorio(direccion, directorio_nuevo):
                        self.collapse_row(path)
                        self.expand_to_path(path)
        elif accion == "Borrar":
            self.emit('borrar', direccion, self.get_model(), iter_)
        elif accion == "new-tab":
            self.emit('add-leer', direccion)
        else:
            self.emit('accion', path, accion)

    def __handle(self):
        self.new_handle(False)
        for directorio in self.dict.keys():
            if not os.path.exists(os.path.join(directorio)):
                self.load(self.path)
                return
            listdir = os.listdir(os.path.join(directorio))
            listdir.sort()
            if not self.dict.get(directorio, False) == str(listdir):
                self.load(self.path)
                return
        self.new_handle(True)
        return False

    def load(self, directorio):
        self.dict = {}
        self.path = directorio
        self.get_model().clear()
        self.__leer((directorio, False))

    def new_handle(self, reset):
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False
        if reset:
            self.actualizador = gobject.timeout_add(1000, self.__handle)


class MenuList(gtk.Menu):

    __gsignals__ = {
    "accion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        gtk.Menu.__init__(self)

        self.modelo = modelo
        self.parent_objet = widget

        lectura, escritura, ejecucion = (False, False, False)
        unidad, directorio, archivo, enlace = (False, False, False, False)

        iter_ = self.modelo.get_iter(path)
        direccion = self.modelo.get_value(iter_, 2)

        if describe_acceso_uri(direccion):
            lectura, escritura, ejecucion = describe_acceso_uri(direccion)
            unidad, directorio, archivo, enlace = describe_uri(direccion)
        else:
            return

        if lectura:
            item = gtk.MenuItem("Copiar")
            self.append(item)
            item.connect_object("activate", self.__emit_accion, path, "Copiar")

        if escritura and not unidad:
            borrar = gtk.MenuItem("Borrar")
            self.append(borrar)
            borrar.connect_object("activate",
                self.__emit_accion, path, "Borrar")

        notebook = self.parent_objet.get_parent().get_parent()
        if escritura and (directorio or unidad) and \
            (notebook.copiando or notebook.cortando):
            pegar = gtk.MenuItem("Pegar")
            self.append(pegar)
            pegar.connect_object("activate",
                self.__emit_accion, path, "Pegar")

        if escritura and (directorio or archivo):
            cortar = gtk.MenuItem("Cortar")
            self.append(cortar)
            cortar.connect_object("activate",
                self.__emit_accion, path, "Cortar")

        if escritura and (directorio or unidad):
            abrir_pestania = gtk.MenuItem("Abrir en Pestaña Nueva")
            self.append(abrir_pestania)
            abrir_pestania.connect_object("activate",
                self.__emit_accion, path, "new-tab")

            nuevodirectorio = gtk.MenuItem("Crear Directorio")
            self.append(nuevodirectorio)
            nuevodirectorio.connect_object("activate",
                self.__emit_accion, path, "Crear Directorio")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __emit_accion(self, path, accion):
        self.emit('accion', path, accion)
