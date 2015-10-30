#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   NoteBookDirectorios.py por:
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
import gobject

from Globales import get_boton
from Directorios import Directorios
from JAMFileSystem import mover
from JAMFileSystem import copiar

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONOS = os.path.join(BASE_PATH, "Iconos")


class NoteBookDirectorios(gtk.Notebook):

    __gsignals__ = {
    "info": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "borrar": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)),
    "montaje": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "no-paginas": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Notebook.__init__(self)

        self.set_scrollable(True)

        self.copiando = False
        self.cortando = False
        self.ver_ocultos = False

        self.show_all()
        self.connect('switch_page', self.__switch_page)

    def __switch_page(self, widget, widget_child, indice):
        paginas = self.get_children()
        for pagina in paginas:
            directorio = pagina.get_child()
            if paginas.index(pagina) != indice:
                model, iter_ = directorio.get_selection().get_selected()
                if iter_:
                    path = model.get_value(iter_, 2)
                    self.emit('info', path)
                    self.emit('montaje', directorio.path)
                directorio.new_handle(True)
            else:
                directorio.new_handle(False)

    def __action_add_leer(self, widget, path):
        self.add_leer(path)

    def __emit_info(self, widget, path):
        """
        Cuando el usuario selecciona un archivo
        o directorio en la estructura de directorios,
        pasa la informacion del mismo a la ventana principal.
        """
        self.emit('info', path)

    def __set_accion(self, widget, path, accion):
        iter_ = widget.get_model().get_iter(path)
        direccion = widget.get_model().get_value(iter_, 2)
        if accion == "Copiar":
            self.copiando = direccion
            self.cortando = False
        elif accion == "Pegar":
            if self.cortando:
                dire, wid, it = self.cortando
                if mover(dire, direccion):
                    if wid:
                        if wid != widget:
                            wid.get_model().remove(it)
                    widget.collapse_row(path)
                    widget.expand_to_path(path)
                    self.cortando = False
            else:
                if self.copiando:
                    if copiar(self.copiando, direccion):
                        widget.collapse_row(path)
                        widget.expand_to_path(path)
                        self.cortando = False
        elif accion == "Cortar":
            self.cortando = (direccion, widget, iter_)
            self.copiando = False

    def __emit_borrar(self, widget, direccion, modelo, iter_):
        """
        Cuando se selecciona borrar en el menu de un item.
        """
        self.emit('borrar', direccion, modelo, iter_)

    def __cerrar(self, widget):
        """
        Cerrar la lengüeta seleccionada.
        """
        notebook = widget.get_parent().get_parent()
        paginas = notebook.get_n_pages()
        for indice in range(paginas):
            boton = self.get_tab_label(
                self.get_children()[indice]).get_children()[1]
            if boton == widget:
                self.get_children()[indice].get_child().new_handle(False)
                self.remove_page(indice)
                break

    def add_leer(self, path):
        """
        Carga un Directorio y Agrega una Lengüeta para él.
        """
        directorios = Directorios()
        hbox = gtk.HBox()
        texto = path
        if len(texto) > 15:
            texto = " . . . " + str(path[-15:])
        label = gtk.Label(texto)
        boton = get_boton(
            os.path.join(ICONOS, "button-cancel.svg"),
            pixels=18,
            tooltip_text="Cerrar")

        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(boton, False, False, 0)

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(directorios)
        self.append_page(scroll, hbox)

        label.show()
        boton.show()
        self.show_all()

        directorios.connect('info', self.__emit_info)
        directorios.connect('borrar', self.__emit_borrar)
        directorios.connect('accion', self.__set_accion)
        directorios.connect('add-leer', self.__action_add_leer)

        directorios.load(path)
        boton.connect("clicked", self.__cerrar)
        self.set_current_page(-1)
        self.set_tab_reorderable(scroll, True)
        return False

    def load(self, path):
        paginas = self.get_children()
        if not paginas:
            self.add_leer(path)
        else:
            scrolled = paginas[self.get_current_page()]
            scrolled.get_children()[0].load(path)
            label = self.get_tab_label(scrolled).get_children()[0]
            texto = path
            if len(texto) > 15:
                texto = " . . . " + str(path[-15:])
            label.set_text(texto)

    def do_page_removed(self, scroll, num):
        paginas = self.get_children()
        if not paginas:
            self.emit('no-paginas')

    def recargar(self, valor):
        """
        Recarga todas las lengüetas.
        """
        self.ver_ocultos = valor
        paginas = self.get_children()
        for pagina in paginas:
            directorio = pagina.get_child()
            directorio.load(directorio.path)
