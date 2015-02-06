#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Widgets.py por:
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


class DialogoBuscar(Gtk.Dialog):

    __gtype_name__ = 'JAMediaEditorDialogoBuscar'

    def __init__(self, view, parent_window=None,
        title="Buscar Texto", texto=None):

        Gtk.Dialog.__init__(self, title=title, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL)

        self.set_border_width(15)

        self.view = view
        self.entrada = Gtk.Entry()

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Buscar:"), True, True, 3)
        hbox.pack_start(self.entrada, False, False, 0)
        hbox.show_all()

        self.vbox.pack_start(hbox, False, False, 3)

        self.boton_anterior = Gtk.Button('Buscar anterior')
        self.boton_siguiente = Gtk.Button('Buscar siguiente')
        self.boton_cerrar = Gtk.Button('Cerrar')

        hbox = Gtk.HBox()
        hbox.pack_start(self.boton_anterior, True, True, 3)
        hbox.pack_start(self.boton_siguiente, True, True, 3)
        hbox.pack_start(self.boton_cerrar, True, True, 0)
        hbox.show_all()

        self.vbox.pack_start(hbox, False, False, 0)

        self.boton_anterior.set_sensitive(False)
        self.boton_siguiente.set_sensitive(False)

        self.boton_anterior.connect('clicked', self.__buscar, 'Atras')
        self.boton_siguiente.connect('clicked', self.__buscar, 'Adelante')
        self.boton_cerrar.connect('clicked', self.__destroy)
        self.entrada.connect("changed", self.__changed)

        if texto:
            self.entrada.set_text(texto)
            seleccion = self.view.get_buffer().get_selection_bounds()
            GLib.idle_add(self.__update, texto, seleccion)

    def __update(self, texto, selection):
        # Cuando se abre el dialogo selecciona la primer ocurrencia.
        _buffer = self.view.get_buffer()
        start, end = _buffer.get_bounds()
        contenido = _buffer.get_text(start, end, 0)
        numero = len(contenido)
        if end.get_offset() == numero and not selection:
            # Si está al final, vuelve al principio.
            inicio = _buffer.get_start_iter()
            self.__seleccionar_texto(texto, inicio, 'Adelante')
        else:
            if selection:
                inicio, fin = selection
                _buffer.select_range(inicio, fin)
        return False

    def __changed(self, widget):
        # Habilita y deshabilita los botones de busqueda y reemplazo.
        self.boton_anterior.set_sensitive(bool(self.entrada.get_text()))
        self.boton_siguiente.set_sensitive(bool(self.entrada.get_text()))

    def __buscar(self, widget, direccion):
        # Busca el texto en el buffer.
        texto = self.entrada.get_text()
        _buffer = self.view.get_buffer()
        inicio, fin = _buffer.get_bounds()

        texto_actual = _buffer.get_text(inicio, fin, 0)
        posicion = _buffer.get_iter_at_mark(_buffer.get_insert())
        if texto:
            if texto in texto_actual:
                inicio = posicion
                if direccion == 'Adelante':
                    if inicio.get_offset() == _buffer.get_char_count():
                        inicio = _buffer.get_start_iter()

                elif direccion == 'Atras':
                    if _buffer.get_selection_bounds():
                        start, end = _buffer.get_selection_bounds()
                        contenido = _buffer.get_text(start, end, 0)
                        numero = len(contenido)
                        if end.get_offset() == numero:
                            inicio = _buffer.get_end_iter()
                        else:
                            inicio = _buffer.get_selection_bounds()[0]
                self.__seleccionar_texto(texto, inicio, direccion)
            else:
                _buffer.select_range(posicion, posicion)

    def __seleccionar_texto(self, texto, inicio, direccion):
        # Selecciona el texto solicitado, y mueve el scroll sí es necesario.
        _buffer = self.view.get_buffer()
        if direccion == 'Adelante':
            match = inicio.forward_search(texto, 0, None)
        elif direccion == 'Atras':
            match = inicio.backward_search(texto, 0, None)
        if match:
            match_start, match_end = match
            _buffer.select_range(match_end, match_start)
            self.view.scroll_to_iter(match_end, 0.1, 1, 1, 0.1)
        else:
            if direccion == 'Adelante':
                inicio = _buffer.get_start_iter()
            elif direccion == 'Atras':
                inicio = _buffer.get_end_iter()
            self.__seleccionar_texto(texto, inicio, direccion)

    def __destroy(self, widget=None):
        self.destroy()


class DialogoReemplazar(Gtk.Dialog):

    __gtype_name__ = 'JAMediaEditorDialogoReemplazar'

    def __init__(self, view, parent_window=None,
        title="Reemplazar Texto", texto=None):

        Gtk.Dialog.__init__(self, title=title, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL)

        self.set_border_width(15)
        self.view = view

        # Entries.
        self.buscar_entry = Gtk.Entry()
        self.reemplazar_entry = Gtk.Entry()

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Buscar:"), True, True, 3)
        hbox.pack_start(self.buscar_entry, False, False, 0)
        hbox.show_all()
        self.vbox.pack_start(hbox, False, False, 3)

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Reemplazar:"), True, True, 3)
        hbox.pack_start(self.reemplazar_entry, False, False, 0)
        hbox.show_all()
        self.vbox.pack_start(hbox, False, False, 10)

        # Buttons.
        cerrar = Gtk.Button("Cerrar")
        self.reemplazar = Gtk.Button("Reemplazar")
        self.button_buscar = Gtk.Button("Saltear")

        hbox = Gtk.HBox()
        hbox.pack_start(self.reemplazar, True, True, 3)
        hbox.pack_start(self.button_buscar, True, True, 3)
        hbox.pack_start(cerrar, True, True, 0)
        hbox.show_all()
        self.vbox.pack_start(hbox, False, False, 0)

        self.reemplazar.set_sensitive(False)
        self.button_buscar.set_sensitive(False)

        cerrar.connect("clicked", self.__destroy)
        self.button_buscar.connect('clicked', self.__buscar, 'Adelante')
        self.reemplazar.connect("clicked", self.__reemplazar)

        if texto:
            self.buscar_entry.set_text(texto)
            seleccion = self.view.get_buffer().get_selection_bounds()
            GLib.idle_add(self.__update, texto, seleccion)

        GLib.idle_add(self.__changed)

    def __update(self, texto, selection):
        # Cuando se abre el dialogo selecciona la primer ocurrencia.
        _buffer = self.view.get_buffer()
        start, end = _buffer.get_bounds()
        contenido = _buffer.get_text(start, end, 0)
        numero = len(contenido)
        if end.get_offset() == numero and not selection:
            inicio = _buffer.get_start_iter()
            self.__seleccionar_texto(texto, inicio, 'Adelante')
        else:
            inicio, fin = selection
            _buffer.select_range(inicio, fin)

    def __changed(self):
        # Habilita y deshabilita los botones de busqueda y reemplazo.
        self.button_buscar.set_sensitive(bool(self.buscar_entry.get_text()))
        _buffer = self.view.get_buffer()
        select = _buffer.get_selection_bounds()
        if len(select) == 2:
            select = True
        else:
            select = False
        self.reemplazar.set_sensitive(select and \
            bool(self.buscar_entry.get_text()) and \
            bool(self.reemplazar_entry.get_text()))
        return True

    def __buscar(self, widget, direccion):
        try:
            texto = self.buscar_entry.get_text()
            _buffer = self.view.get_buffer()
            inicio, fin = _buffer.get_bounds()
            texto_actual = _buffer.get_text(inicio, fin, 0)
            posicion = _buffer.get_iter_at_mark(_buffer.get_insert())
            if texto:
                if texto in texto_actual:
                    inicio = posicion
                    if direccion == 'Adelante':
                        if inicio.get_offset() == _buffer.get_char_count():
                            inicio = _buffer.get_start_iter()
                    elif direccion == 'Atras':
                        if _buffer.get_selection_bounds():
                            start, end = _buffer.get_selection_bounds()
                            contenido = _buffer.get_text(start, end, 0)
                            numero = len(contenido)
                            if end.get_offset() == numero:
                                inicio = _buffer.get_end_iter()
                            else:
                                inicio = _buffer.get_selection_bounds()[0]
                    self.__seleccionar_texto(texto, inicio, direccion)
                else:
                    buffer.select_range(posicion, posicion)
        except:
            print "FIXME: Error en:", self.__buscar
            # Cuando se reemplaza texto y llega al final del archivo,
            # al parecer no afecta en nada a la aplicación.

    def __destroy(self, widget=None, event=None):
        self.destroy()

    def __reemplazar(self, widget):
        _buffer = self.view.get_buffer()
        inicio, fin = _buffer.get_selection_bounds()
        texto_reemplazo = self.reemplazar_entry.get_text()
        _buffer.delete(inicio, fin)
        _buffer.insert_at_cursor(texto_reemplazo)
        self.button_buscar.clicked()

    def __seleccionar_texto(self, texto, inicio, direccion):
        # Selecciona el texto solicitado, y mueve el scroll sí es necesario.
        _buffer = self.view.get_buffer()
        if direccion == 'Adelante':
            match = inicio.forward_search(texto, 0, None)
        elif direccion == 'Atras':
            match = inicio.backward_search(texto, 0, None)

        if match:
            match_start, match_end = match
            _buffer.select_range(match_end, match_start)
            self.view.scroll_to_iter(match_end, 0.1, 1, 1, 0.1)
        else:
            if direccion == 'Adelante':
                inicio = _buffer.get_start_iter()
            elif direccion == 'Atras':
                inicio = _buffer.get_end_iter()
            self.__seleccionar_texto(texto, inicio, direccion)


class My_FileChooser(Gtk.FileChooserDialog):

    __gtype_name__ = 'JAMediaEditorMy_FileChooser'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, parent_window=None, action_type=None, filter_type=[],
        title=None, path=None, mime_type=[]):

        Gtk.FileChooserDialog.__init__(self, parent=parent_window,
            action=action_type, flags=Gtk.DialogFlags.MODAL, title=title)

        self.set_default_size(640, 480)
        self.set_select_multiple(False)

        if os.path.isfile(path):
            self.set_filename(path)
        else:
            self.set_current_folder_uri("file://%s" % path)

        if filter_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for fil in filter_type:
                _filter.add_pattern(fil)
            self.add_filter(_filter)

        elif mime_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for mime in mime_type:
                _filter.add_mime_type(mime)
            self.add_filter(_filter)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        texto = ""
        if action_type == Gtk.FileChooserAction.OPEN or \
            action_type == Gtk.FileChooserAction.SELECT_FOLDER:
            texto = "Abrir"

        elif action_type == Gtk.FileChooserAction.SAVE:
            texto = "Guardar"

        abrir = Gtk.Button(texto)
        salir = Gtk.Button("Salir")

        hbox.pack_end(salir, True, True, 5)
        hbox.pack_end(abrir, True, True, 5)
        self.set_extra_widget(hbox)

        salir.connect("clicked", self.__salir)
        abrir.connect("clicked", self.__abrir)
        self.show_all()
        self.connect("file-activated", self.__file_activated)

    def __file_activated(self, widget):
        # Cuando se hace doble click sobre un archivo.
        self.__abrir()

    def __abrir(self, widget=None):
        direccion = self.get_filename()
        if not direccion:
            return self.__salir()

        direccion = os.path.realpath(direccion)
        # Para abrir solo archivos, de lo contrario el filechooser
        # se está utilizando para "guardar como".
        if os.path.exists(direccion):
            if not os.path.isfile(direccion):
                return self.__salir()

        # Emite el path del archivo seleccionado.
        self.emit('load', direccion)
        self.__salir()

    def __salir(self, widget=None):
        self.destroy()


class Multiple_FileChooser(Gtk.FileChooserDialog):

    __gtype_name__ = 'JAMediaEditorMultiple_FileChooser'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, parent_window=None, filter_type=[], title=None,
        path=None, mime_type=[]):

        Gtk.FileChooserDialog.__init__(self, parent=parent_window,
            action=Gtk.FileChooserAction.OPEN, flags=Gtk.DialogFlags.MODAL,
            title=title)

        self.set_default_size(640, 480)
        self.set_select_multiple(True)

        if os.path.isfile(path):
            self.set_filename(path)
        else:
            self.set_current_folder_uri("file://%s" % path)

        if filter_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for fil in filter_type:
                _filter.add_pattern(fil)
            self.add_filter(_filter)

        elif mime_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for mime in mime_type:
                _filter.add_mime_type(mime)
            self.add_filter(_filter)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        abrir = Gtk.Button("Abrir")
        salir = Gtk.Button("Salir")

        hbox.pack_end(salir, True, True, 5)
        hbox.pack_end(abrir, True, True, 5)
        self.set_extra_widget(hbox)

        salir.connect("clicked", self.__salir)
        abrir.connect("clicked", self.__abrir)
        self.show_all()
        self.connect("file-activated", self.__file_activated)

    def __file_activated(self, widget):
        # Cuando se hace doble click sobre un archivo.
        self.__abrir()

    def __abrir(self, widget=None):
        files = self.get_filenames()
        if files:
            for _file in files:
                direccion = os.path.realpath(_file)
                if os.path.exists(direccion) and os.path.isfile(direccion):
                    # Emite el path del archivo seleccionado.
                    self.emit('load', direccion)
        self.__salir()

    def __salir(self, widget=None):
        self.destroy()


class DialogoAlertaSinGuardar(Gtk.Dialog):
    """
    Diálogo para Alertar al usuario al cerrar un archivo
    que contiene cambios sin guardar.
    """

    __gtype_name__ = 'JAMediaEditorDialogoAlertaSinGuardar'

    def __init__(self, parent_window=None):

        Gtk.Dialog.__init__(self, title="ATENCION !", parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Guardar y Continuar", Gtk.ResponseType.ACCEPT,
                "Continuar sin Guardar", Gtk.ResponseType.CLOSE,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.set_size_request(400, 150)
        self.set_border_width(15)

        label = Gtk.Label(
            "No se han guardado los ultimos cambios en el archivo.")

        label.show()
        self.vbox.add(label)


class DialogoSobreEscritura(Gtk.Dialog):
    """
    Diálogo para Alertar al usuario sobre reescritura de un archivo.
    """

    __gtype_name__ = 'JAMediaEditorDialogoSobreEscritura'

    def __init__(self, parent_window=None):

        Gtk.Dialog.__init__(self, title="ATENCION !", parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Guardar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.set_size_request(400, 150)
        self.set_border_width(15)

        label = Gtk.Label("El archivo ya axiste. ¿Deseas sobre escribirlo?")

        label.show()
        self.vbox.add(label)
