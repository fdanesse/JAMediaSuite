#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Widgets2.py por:
#     Cristian García    <cristian99garcia@gmail.com>
#     Ignacio Rodriguez  <nachoel01@gmail.com>
#     Flavio Danesse     <fdanesse@gmail.com>

# This program is free software; you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110 - 1301 USA

import os
import commands

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

BASE_PATH = os.path.dirname(__file__)


class DialogoErrores(Gtk.Dialog):
    """
    Diálogo para chequear errores
    """

    __gtype_name__ = 'JAMediaEditorDialogoErrores'

    def __init__(self, view, parent_window=None):

        Gtk.Dialog.__init__(self, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Aceptar", Gtk.ResponseType.ACCEPT])

        self.set_size_request(600, 250)
        self.set_border_width(15)

        errores = ErroresTreeview(view)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(errores)

        label = Gtk.Label("Errores")

        label.show()
        scroll.show_all()

        self.vbox.pack_start(label, False, False, 0)
        self.vbox.pack_start(scroll, True, True, 3)


class ErroresTreeview(Gtk.TreeView):

    __gtype_name__ = 'JAMediaEditorErroresTreeview'

    def __init__(self, view):

        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.view = view

        columna = Gtk.TreeViewColumn("Línea", Gtk.CellRendererText(), text=0)
        self.append_column(columna)

        columna = Gtk.TreeViewColumn("Error", Gtk.CellRendererText(), text=1)
        self.append_column(columna)

        _buffer = view.get_buffer()
        start, end = _buffer.get_bounds()
        texto = _buffer.get_text(start, end, True)

        path = os.path.join("/tmp", "check_temp.py")
        arch = open(path, "w")
        arch.write(texto)
        arch.close()

        check = os.path.join(BASE_PATH, "Check1.py")
        errores = commands.getoutput('python %s %s' % (check, path))

        for linea in errores.splitlines():
            try:
                item_str = linea.split("%s:" % path)[1]
                #if not path in item_str:
                numero = item_str.split(":")[0].strip()
                comentario = item_str.replace(item_str.split()[0], "").strip()
                item = [numero, comentario]
                self.get_model().append(item)
            except:
                pass

        check = os.path.join(BASE_PATH, "Check2.py")
        errores = commands.getoutput('python %s %s' % (check, path))

        for linea in errores.splitlines():
            try:
                item_str = linea.split("%s:" % path)[1]
                #if not path in item_str:
                numero = item_str.split(":")[0].strip()
                comentario = item_str.replace(item_str.split()[0], "").strip()
                item = [numero, comentario]
                self.get_model().append(item)
            except:
                pass

        self.show_all()
        self.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        self.get_selection().set_select_function(
            self.__clicked, self.get_model())

    def __clicked(self, treeselection,
        model, path, is_selected, listore):
        iter_sel = model.get_iter(path)
        linea = model.get_value(iter_sel, 0)
        self.view.marcar_error(int(linea))
        return True


class Credits(Gtk.Dialog):

    __gtype_name__ = 'JAMediaEditorCredits'

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self, parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_border_width(15)

        imagen = Gtk.Image()
        imagen.set_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMediaEditorCredits.svg"))

        self.vbox.pack_start(imagen, False, False, 0)
        self.vbox.show_all()


'''
class Estructura_Menu(Gtk.Menu):
    """
    Menu con opciones para treeview de Estructura.
    """

    __gtype_name__ = 'JAMediaEditorEstructura_Menu'

    __gsignals__ = {
    'accion': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos,
        tiempo, path, modelo, accion_previa):

        Gtk.Menu.__init__(self)

        iterfirst = modelo.get_iter_first()
        _iter = modelo.get_iter(path)
        filepath = modelo.get_value(_iter, 2)

        lectura, escritura, ejecucion = self.__verificar_permisos(filepath)
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                datos = commands.getoutput(
                    'file - ik %s%s%s' % ("\"", filepath, "\""))
                if "text" in datos or "x - python" in datos and lectura:
                    self.__get_item(widget, path, "abrir")
                if lectura:
                    self.__get_item(widget, path, "copiar")
                if escritura:
                    self.__get_item(widget, path, "cortar")
                if escritura:
                    self.__get_item(widget, path, "suprimir")
                if "text" in datos or "x-python" in datos and lectura:
                    self.__get_item(widget, path, "buscar")
            elif os.path.isdir(filepath):
                if filepath == modelo.get_value(iterfirst, 2):
                    self.__get_item(widget, path, "eliminar proyecto")
                    self.__get_item(widget, path, "Crear Directorio")
                    if escritura and "copiar" in accion_previa or \
                        "cortar" in accion_previa:
                        self.__get_item(widget, path, "pegar")
                    self.__get_item(widget, path, "buscar")
                else:
                    if lectura:
                        self.__get_item(widget, path, "copiar")
                    if escritura and lectura:
                        self.__get_item(widget, path, "cortar")
                    if escritura and "copiar" in accion_previa or \
                        "cortar" in accion_previa:
                        self.__get_item(widget, path, "pegar")
                    if escritura:
                        self.__get_item(widget, path, "suprimir")
                        self.__get_item(widget, path, "Crear Directorio")
                    if lectura:
                        self.__get_item(widget, path, "buscar")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __verificar_permisos(self, path):
        # verificar:
        # 1 - Si es un archivo o un directorio
        # 2 - Si sus permisos permiten la copia, escritura y borrado
        if not os.path.exists(path):
            return False, False, False
        try:
            if os.access(path, os.F_OK):
                r = os.access(path, os.R_OK)
                w = os.access(path, os.W_OK)
                x = os.access(path, os.X_OK)
                return r, w, x
            else:
                return False, False, False
        except:
            return False, False, False

    def __null(self):
        pass

    def __get_item(self, widget, path, accion):
        """
        Agrega un item al menu.
        """
        item = Gtk.MenuItem("%s%s" % (accion[0].upper(), accion[1:]))
        self.append(item)
        item.connect_object("activate", self.__set_accion, widget,
            path, accion)

    def __set_accion(self, widget, path, accion):
        """
        Responde a la seleccion del usuario sobre el menu.
        """
        _iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, _iter)


class DialogoEliminar(Gtk.Dialog):
    """
    Diálogo para confirmar la eliminación del archivo / directorio seleccionado
    """

    __gtype_name__ = 'JAMediaEditorDialogoEliminar'

    def __init__(self, tipo="Archivo", parent_window=None):

        Gtk.Dialog.__init__(self, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Si, eliminar!", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.set_size_request(300, 100)
        self.set_border_width(15)

        label = Gtk.Label(
            "Estás Seguro de que Deseas Eliminar\nel %s Seleccionado?" % tipo)

        label.show()
        self.vbox.pack_start(label, True, True, 0)


class BusquedaGrep(Gtk.Dialog):
    """
    Dialogo con un TreeView para busquedas con Grep
    """

    __gtype_name__ = 'JAMediaEditorBusquedaGrep'

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, path=None, parent_window=None):

        Gtk.Dialog.__init__(self, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Cerrar", Gtk.ResponseType.ACCEPT])

        self.path = path

        self.set_size_request(600, 250)
        self.set_border_width(15)

        self.treeview = TreeViewBusquedaGrep()
        self.entry = Gtk.Entry()
        buscar = Gtk.Button("Buscar")

        hbox = Gtk.HBox()
        hbox.pack_start(self.entry, False, False, 0)
        hbox.pack_start(buscar, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.treeview)

        scroll.show_all()
        hbox.show_all()

        self.vbox.pack_start(hbox, False, False, 0)
        self.vbox.pack_start(scroll, True, True, 0)

        buscar.connect("clicked", self.__buscar)
        self.treeview.connect("nueva-seleccion",
            self.__re_emit_nueva_seleccion)

    def __re_emit_nueva_seleccion(self, widget, valor):
        self.emit("nueva-seleccion", valor)

    def __buscar(self, widget):
        """
        Realiza la búsqueda solicitada.
        """
        text = self.entry.get_text().strip()
        if text:
            if os.path.isdir(self.path):
                result = commands.getoutput(
                    "less | grep -R -n \'%s\' %s" % (text, self.path))
                result = result.splitlines()
            elif os.path.isfile(self.path):
                result = commands.getoutput(
                    "less | grep -n \'%s\' %s" % (text, self.path))
                result = result.splitlines()
            items = []
            for line in result:
                dat = line.split(":")
                if os.path.isdir(self.path):
                    if len(dat) == 3:
                        items.append([dat[0], dat[1], dat[2].strip()])
                elif os.path.isfile(self.path):
                    if len(dat) == 2:
                        items.append([self.path, dat[0], dat[1].strip()])
            self.treeview.limpiar()
            self.treeview.agregar_items(items)


class TreeViewBusquedaGrep(Gtk.TreeView):

    __gtype_name__ = 'JAMediaEditorTreeViewBusquedaGrep'

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.ListStore(
            GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.__setear_columnas()
        self.treeselection = self.get_selection()
        self.show_all()

    def do_row_activated(self, path, treviewcolumn):
        model = self.get_model()
        _iter = model.get_iter(path)
        valor = [
            model.get_value(_iter, 0),
            model.get_value(_iter, 1),
            model.get_value(_iter, 2)]
        self.emit("nueva-seleccion", valor)

    def __setear_columnas(self):
        self.append_column(
            self.__construir_columa('Archivo', 0, True))
        self.append_column(
            self.__construir_columa('N° de línea', 1, True))
        self.append_column(
            self.__construir_columa('Línea', 2, True))

    def __construir_columa(self, text, index, visible):
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna

    def limpiar(self):
        self.get_model().clear()

    def agregar_items(self, elementos):
        self.__ejecutar_agregar_elemento(elementos)

    def __ejecutar_agregar_elemento(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """
        if not elementos:
            self.seleccionar_primero()
            return False
        self.get_model().append(elementos[0])
        elementos.remove(elementos[0])
        GLib.idle_add(self.__ejecutar_agregar_elemento, elementos)
        return False

    def seleccionar_primero(self, widget=None):
        self.treeselection.select_path(0)
'''
