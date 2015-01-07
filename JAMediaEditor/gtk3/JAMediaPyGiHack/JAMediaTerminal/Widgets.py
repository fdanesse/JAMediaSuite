#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay

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
from gi.repository import Pango
from gi.repository import GLib

from Globales import get_pixels
from Globales import get_separador
from Globales import get_boton

BASE_PATH = os.path.dirname(__file__)

Width_Button = 0.5

FAMILIES = Gtk.Window().get_pango_context().list_families()


class ToolbarTerminal(Gtk.Toolbar):
    """
    Toolbar de JAMediaTerminal.
    """

    __gtype_name__ = 'ToolbarTerminal2'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "reset": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "formato": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        ### Interpretes disponibles.
        bash_path = None
        python_path = None

        paths = os.environ["PATH"].split(':')
        for path in paths:
            if 'bash' in os.listdir(path):
                bash_path = os.path.join(path, 'bash')

            if 'python' in os.listdir(path):
                python_path = os.path.join(path, 'python')

            if bash_path and python_path:
                break

        for path in paths:
            if 'ipython' in os.listdir(path):
                python_path = os.path.join(path, 'ipython')

        ### Construcción.
        archivo = os.path.join(BASE_PATH, "Iconos", "edit-copy.svg")
        boton = get_boton(archivo,
            pixels=get_pixels(Width_Button), tooltip_text="Copiar")
        boton.connect("clicked", self.__emit_accion, "copiar")
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "editpaste.svg")
        boton = get_boton(archivo,
            pixels=get_pixels(Width_Button), tooltip_text="Pegar")
        boton.connect("clicked", self.__emit_accion, "pegar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        ### Botón Formato.
        archivo = os.path.join(BASE_PATH, "Iconos", "font.svg")
        boton = get_boton(archivo,
            pixels=get_pixels(Width_Button), tooltip_text="Fuente")
        boton.connect("clicked", self.__emit_formato)
        self.insert(boton, -1)

        ### Botón Agregar.
        archivo = os.path.join(BASE_PATH, "Iconos", "tab-new.svg")
        boton = get_boton(archivo,
            pixels=get_pixels(Width_Button), tooltip_text="Nueva Terminal")
        boton.connect("clicked", self.__emit_accion, "agregar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=10, expand=False), -1)
        ### Botón bash.
        archivo = os.path.join(BASE_PATH, "Iconos", "bash.svg")
        boton = get_boton(archivo,
            pixels=get_pixels(Width_Button), tooltip_text="Terminal bash")
        boton.connect("clicked", self.__emit_reset, bash_path)
        self.insert(boton, -1)

        ### Botón python.
        archivo = os.path.join(BASE_PATH, "Iconos", "python.svg")
        boton = get_boton(archivo,
            pixels=get_pixels(Width_Button), tooltip_text="Terminal python")
        boton.connect("clicked", self.__emit_reset, python_path)
        self.insert(boton, -1)

        self.show_all()

    def __emit_formato(self, widget):
        self.emit('formato')

    def __emit_reset(self, widget, path):
        self.emit('reset', path)

    def __emit_accion(self, widget, accion):
        self.emit('accion', accion)


class DialogoFormato(Gtk.Dialog):
    """
    Selector de fuente y tamaño.
    """

    __gtype_name__ = 'DialogoFormato2'

    def __init__(self, parent_window=False, fuente="Monospace", tamanio=10):

        Gtk.Dialog.__init__(self, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Aceptar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.fuente = fuente
        self.tamanio = tamanio

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        ### Lista de Fuentes.
        treeview_fuentes = TreeViewFonts(self.fuente)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(treeview_fuentes)

        box.pack_start(scroll, True, True, 0)

        ### Tamaños.
        treeview_tamanios = TreeViewTamanio(self.tamanio)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(treeview_tamanios)

        box.pack_start(scroll, True, True, 0)
        self.vbox.pack_start(box, True, True, 0)

        ### Preview.
        self.preview = Gtk.Label("Texto")
        self.preview.modify_font(
            Pango.FontDescription("%s %s" % (self.fuente, self.tamanio)))

        eventbox = Gtk.EventBox()
        eventbox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
        eventbox.add(self.preview)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(eventbox)
        scroll.set_size_request(-1, 100)
        self.vbox.pack_start(scroll, False, False, 2)

        self.set_size_request(400, 400)
        self.set_border_width(15)

        self.show_all()

        treeview_fuentes.connect("nueva-seleccion", self.__set_font)
        treeview_tamanios.connect("nueva-seleccion", self.__set_tamanio)

    def __set_font(self, widget, fuente):
        """
        Cuando se cambia la fuente.
        """
        if self.fuente != fuente:
            self.fuente = fuente
            self.preview.modify_font(Pango.FontDescription(
                "%s %s" % (self.fuente, self.tamanio)))

    def __set_tamanio(self, widget, tamanio):
        """
        Cuando se cambia el tamaño.
        """
        if self.tamanio != tamanio:
            self.tamanio = tamanio
            self.preview.modify_font(Pango.FontDescription(
                "%s %s" % (self.fuente, self.tamanio)))

    def get_font(self):
        """
        Devuelve fuente y tamaño seleccionados.
        """
        return (self.fuente, self.tamanio)


class TreeViewFonts(Gtk.TreeView):

    __gtype_name__ = 'TreeViewFonts2'

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self, fuente):

        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.fuente = fuente

        self.__setear_columnas()

        self.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()
        GLib.idle_add(self.__init)

    def __setear_columnas(self):
        columna = Gtk.TreeViewColumn("Fuente",
            Gtk.CellRendererText(), markup=0)
        columna.set_sort_column_id(0)
        columna.set_property('visible', True)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

        columna = Gtk.TreeViewColumn("Nombre",
            Gtk.CellRendererText(), text=1)
        columna.set_sort_column_id(1)
        columna.set_property('visible', False)
        columna.set_property('resizable', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

    def __init(self):
        self.get_model().clear()

        ### Cargar las fuentes.
        fuentes = []
        for family in FAMILIES:
            name = family.get_name()
            fuentes.append(name)

        for fuente in sorted(fuentes):
            texto = '<span font="%s">%s</span>' % (fuente, fuente)
            self.get_model().append([texto, fuente])

        ### Seleccionar la fuente inicial.
        item = self.get_model().get_iter_first()
        while item:
            if self.get_model().get_value(item, 1) == self.fuente:
                self.get_selection().select_path(
                    self.get_model().get_path(item))
                self.scroll_to_cell(self.get_model().get_path(item))
                return False

            item = self.get_model().iter_next(item)

        return False

    def __selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """
        _iter = self.get_model().get_iter(path)
        fuente = self.get_model().get_value(_iter, 1)

        if self.fuente != fuente:
            self.fuente = fuente
            self.scroll_to_cell(path)
            self.emit('nueva-seleccion', self.fuente)

        return True


class TreeViewTamanio(Gtk.TreeView):

    __gtype_name__ = 'TreeViewTamanio2'

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT, ))}

    def __init__(self, tamanio):

        Gtk.TreeView.__init__(self, Gtk.ListStore(GObject.TYPE_INT))

        self.__setear_columnas()
        self.tamanio = tamanio

        self.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()
        GLib.idle_add(self.__init)

    def __setear_columnas(self):
        columna = Gtk.TreeViewColumn("Tamaño",
            Gtk.CellRendererText(), text=0)
        columna.set_sort_column_id(0)
        columna.set_property('visible', True)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

    def __init(self):
        self.get_model().clear()
        for num in range(8, 21):
            self.get_model().append([num])

        ### Seleccionar el tamaño inicial.
        item = self.get_model().get_iter_first()
        while item:
            if self.get_model().get_value(item, 0) == self.tamanio:
                self.get_selection().select_path(
                    self.get_model().get_path(item))
                self.scroll_to_cell(self.get_model().get_path(item))
                return False

            item = self.get_model().iter_next(item)

        return False

    def __selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """
        _iter = self.get_model().get_iter(path)
        tamanio = self.get_model().get_value(_iter, 0)

        if self.tamanio != tamanio:
            self.tamanio = tamanio
            self.scroll_to_cell(path)
            self.emit('nueva-seleccion', self.tamanio)

        return True
