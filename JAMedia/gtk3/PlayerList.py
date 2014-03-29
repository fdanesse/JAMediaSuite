#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PlayerList.py por:
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

import os

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GLib

BASE_PATH = os.path.dirname(__file__)

#import JAMediaObjects
#from JAMediaObjects.JAMediaWidgets import JAMediaButton

from Globales import get_color
from Globales import get_separador
from Globales import get_boton


class Lista(Gtk.TreeView):
    """
    Lista generica.
    """

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.TreeView.__init__(self)

        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.permitir_select = True
        self.valor_select = None

        self.modelo = Gtk.ListStore(
            GdkPixbuf.Pixbuf,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING)

        self.__setear_columnas()

        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(
            self.__selecciones, self.modelo)

        self.set_model(self.modelo)
        self.show_all()

    """
    def keypress(self, widget, event):
        # derecha 114 izquierda 113 suprimir 119
        # backspace 22 (en xo no existe suprimir)
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
            print valor, path
        else:
            pass
        return False
        """

    def __selecciones(self, treeselection,
        model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """

        if not self.permitir_select:
            return True

        # model y listore son ==
        _iter = model.get_iter(path)
        valor = model.get_value(_iter, 2)

        if not is_selected and self.valor_select != valor:
            self.scroll_to_cell(model.get_path(_iter))
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)

        return True

    def __setear_columnas(self):

        self.append_column(self.__construir_columa_icono('', 0, True))
        self.append_column(self.__construir_columa('Nombre', 1, True))
        self.append_column(self.__construir_columa('', 2, False))

    def __construir_columa(self, text, index, visible):

        render = Gtk.CellRendererText()

        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        return columna

    def __construir_columa_icono(self, text, index, visible):

        render = Gtk.CellRendererPixbuf()

        columna = Gtk.TreeViewColumn(text, render, pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        return columna

    def limpiar(self):

        self.permitir_select = False
        self.modelo.clear()
        self.permitir_select = True

    def agregar_items(self, elementos):
        """
        Recibe lista de: [texto para mostrar, path oculto] y
        Comienza secuencia de agregado a la lista.
        """

        self.get_toplevel().set_sensitive(False)
        self.permitir_select = False

        GLib.idle_add(self.__ejecutar_agregar_elemento, elementos)

    def __ejecutar_agregar_elemento(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """

        if not elementos:
            self.permitir_select = True
            self.seleccionar_primero()
            self.get_toplevel().set_sensitive(True)
            return False

        texto, path = elementos[0]

        from Globales import describe_uri
        from Globales import describe_archivo

        descripcion = describe_uri(path)

        icono = None
        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = describe_archivo(path)

                if 'video' in tipo or 'application/ogg' in tipo or \
                    'application/octet-stream' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "video.svg")

                elif 'audio' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "sonido.svg")

                elif 'image' in tipo and not 'iso' in tipo:
                    icono = os.path.join(path)  # exige rendimiento
                    #icono = os.path.join(JAMediaWidgetsBASE,
                    #    "Iconos", "imagen.png")

                elif 'pdf' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "pdf.svg")

                elif 'zip' in tipo or 'rar' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "edit-select-all.svg")

                else:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "edit-select-all.svg")
        else:
            icono = os.path.join(JAMediaWidgetsBASE,
                "Iconos", "edit-select-all.svg")

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
                get_pixels(0.8), -1)
            self.modelo.append([pixbuf, texto, path])

        except:
            pass

        elementos.remove(elementos[0])

        GLib.idle_add(self.__ejecutar_agregar_elemento, elementos)

        return False

    def seleccionar_siguiente(self, widget=None):

        modelo, _iter = self.treeselection.get_selected()

        try:
            self.treeselection.select_iter(modelo.iter_next(_iter))

        except:
            self.seleccionar_primero()

        return False

    def seleccionar_anterior(self, widget=None):

        modelo, _iter = self.treeselection.get_selected()

        try:
            self.treeselection.select_iter(modelo.iter_previous(_iter))

        except:
            self.seleccionar_ultimo()

        return False

    def seleccionar_primero(self, widget=None):

        self.treeselection.select_path(0)

    def seleccionar_ultimo(self, widget=None):

        model = self.get_model()
        item = model.get_iter_first()

        _iter = None

        while item:
            _iter = item
            item = model.iter_next(item)

        if _iter:
            self.treeselection.select_iter(_iter)
            #path = model.get_path(iter)
