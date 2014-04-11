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

import gtk
from gtk import gdk
import gobject


BASE_PATH = os.path.dirname(__file__)


class Lista(gtk.TreeView):
    """
    Lista generica.
    """

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.TreeView.__init__(self, gtk.ListStore(
            gdk.Pixbuf,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.permitir_select = True
        self.valor_select = False
        self.ultimo_select = False
        self.timer_select = False

        self.__setear_columnas()

        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()

    def __selecciones(self, path, column):
        """
        Cuando se selecciona un item en la lista.
        """

        if not self.permitir_select:
            return True

        _iter = self.get_model().get_iter(path)
        valor = self.get_model().get_value(_iter, 2)

        if self.valor_select != valor:
            self.valor_select = valor

            if self.timer_select:
                gobject.source_remove(self.timer_select)
                self.timer_select = False

            gobject.timeout_add(3, self.__select)
            self.scroll_to_cell(self.get_model().get_path(_iter))

        return True

    def __select(self):

        if self.ultimo_select != self.valor_select:
            self.emit('nueva-seleccion', self.valor_select)
            self.ultimo_select = self.valor_select

        return False

    def __setear_columnas(self):

        self.append_column(self.__construir_columa_icono('', 0, True))
        self.append_column(self.__construir_columa('Nombre', 1, True))
        self.append_column(self.__construir_columa('', 2, False))

    def __construir_columa(self, text, index, visible):

        render = gtk.CellRendererText()

        columna = gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        return columna

    def __construir_columa_icono(self, text, index, visible):

        render = gtk.CellRendererPixbuf()

        columna = gtk.TreeViewColumn(text, render, pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        return columna

    def limpiar(self):

        self.permitir_select = False
        self.get_model().clear()
        self.permitir_select = True

    def agregar_items(self, elementos):
        """
        Recibe lista de: [texto para mostrar, path oculto] y
        Comienza secuencia de agregado a la lista.
        """

        self.get_toplevel().set_sensitive(False)
        self.permitir_select = False

        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)

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
                    icono = os.path.join(BASE_PATH,
                        "Iconos", "video.svg")

                elif 'audio' in tipo:
                    icono = os.path.join(BASE_PATH,
                        "Iconos", "sonido.svg")

                else:
                    icono = os.path.join(BASE_PATH,
                        "Iconos", "sonido.svg")
        else:
            icono = os.path.join(BASE_PATH,
                "Iconos", "sonido.svg")

        pixbuf = gdk.pixbuf_new_from_file_at_size(icono,
            24, -1)
        self.get_model().append([pixbuf, texto, path])

        elementos.remove(elementos[0])

        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)

        return False

    def seleccionar_siguiente(self, widget=None):

        modelo, _iter = self.get_selection().get_selected()

        try:
            self.get_selection().select_iter(
                self.get_model().iter_next(_iter))

        except:
            self.seleccionar_primero()

        return False

    def seleccionar_anterior(self, widget=None):

        modelo, _iter = self.get_selection().get_selected()

        try:
            # HACK porque: model no tiene iter_previous
            #self.get_selection().select_iter(
            #    self.get_model().iter_previous(_iter))
            path = self.get_model().get_path(_iter)
            path = (path[0] - 1, )

            self.get_selection().select_iter(
                self.get_model().get_iter(path))

        except:
            self.seleccionar_ultimo()

        return False

    def seleccionar_primero(self, widget=None):

        self.get_selection().select_path(0)

    def seleccionar_ultimo(self, widget=None):

        model = self.get_model()
        item = model.get_iter_first()

        _iter = None

        while item:
            _iter = item
            item = model.iter_next(item)

        if _iter:
            self.get_selection().select_iter(_iter)
            #path = model.get_path(iter)
