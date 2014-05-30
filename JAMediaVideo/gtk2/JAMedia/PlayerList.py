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

from Globales import describe_uri
from Globales import describe_archivo
from Globales import get_colors
from Globales import get_separador
from Globales import get_boton
from Globales import get_JAMedia_Directory

BASE_PATH = os.path.dirname(__file__)


class PlayerList(gtk.ScrolledWindow):

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.ScrolledWindow.__init__(self)

        #FIXME: Scroll debe contener solo la lista
        vbox = gtk.VBox()

        self.toolbar = ToolbarList()
        self.lista = Lista()

        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(self.lista, True, True, 0)

        self.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)
        self.add_with_viewport(vbox)

        self.get_child().modify_bg(
            0, get_colors("window"))

        self.show_all()

        self.set_size_request(150, -1)

        self.toolbar.connect("load", self.__load_files)
        self.lista.connect("nueva-seleccion",
            self.__re_emit_nueva_seleccion)

    def __re_emit_nueva_seleccion(self, widget, pista):

        self.emit('nueva-seleccion', pista)

    def __load_files(self, widget, items, tipo):

        if tipo == "load":
            self.lista.limpiar()

        if items:
            self.lista.agregar_items(items)

        else:
            self.emit('nueva-seleccion', False)

    def seleccionar_anterior(self):

        self.lista.seleccionar_anterior()

    def seleccionar_siguiente(self):

        self.lista.seleccionar_siguiente()

    def limpiar(self):

        self.lista.limpiar()

    def set_mime_types(self, mime):

        self.toolbar.mime = mime


class ToolbarList(gtk.EventBox):

    __gsignals__ = {
    "load": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING))}

    def __init__(self, mime=["audio/*", "video/*", "image/*"]):

        gtk.EventBox.__init__(self)

        self.mime = mime
        toolbar = gtk.Toolbar()

        self.modify_bg(0, get_colors("window"))
        toolbar.modify_bg(0, get_colors("window"))

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "document-open.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Abrir Archivos")
        boton.connect("clicked", self.__open_files, "load")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "document-new.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Agregar Archivos")
        boton.connect("clicked", self.__open_files, "add")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "clear.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Limpiar Lista")
        boton.connect("clicked", self.__clear_list)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def __clear_list(self, widget):

        self.emit("load", [], "load")

    def __open_files(self, widget, tipo):

        selector = My_FileChooser(
            parent=self.get_toplevel(),
            filter_type=[],
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            mime=self.mime,
            title="Abrir Archivos",
            path=get_JAMedia_Directory())

        selector.connect(
            'archivos-seleccionados',
            self.__cargar_directorio, tipo)

        selector.run()

        if selector:
            selector.destroy()

    def __cargar_directorio(self, widget, archivos, tipo):
        """
        Recibe una lista de archivos y setea la lista
        de reproduccion con ellos.
        """

        if not archivos:
            return

        items = []
        archivos.sort()

        for archivo in archivos:
            path = archivo
            archivo = os.path.basename(path)
            items.append([archivo, path])

        self.emit("load", items, tipo)


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
        self.append_column(self.__construir_columa('Archivo', 1, True))
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

            if path > -1:
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


class My_FileChooser(gtk.FileChooserDialog):
    """
    Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio.
    """

    __gsignals__ = {
    'archivos-seleccionados': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self, parent=None, action=None,
        filter_type=[], title=None, path=None, mime=[]):

        gtk.FileChooserDialog.__init__(self,
            title=title,
            parent=parent,
            action=action,
            #flags=gtk.DIALOG_MODAL,
            )

        self.modify_bg(0, get_colors("window"))
        self.set_resizable(True)
        self.set_size_request(320, 240)

        #if not path:
        #    path = "file:///media"

        self.set_current_folder_uri("file://%s" % path)
        self.set_select_multiple(True)

        hbox = gtk.HBox()

        boton_abrir_directorio = gtk.Button("Abrir")
        boton_seleccionar_todo = gtk.Button("Seleccionar Todos")
        boton_salir = gtk.Button("Salir")

        boton_salir.connect("clicked", self.__salir)
        boton_abrir_directorio.connect("clicked",
            self.__file_activated)
        boton_seleccionar_todo.connect("clicked",
            self.__seleccionar_todos_los_archivos)

        hbox.pack_end(boton_salir, True, True, 5)
        hbox.pack_end(boton_seleccionar_todo, True, True, 5)
        hbox.pack_end(boton_abrir_directorio, True, True, 5)

        self.set_extra_widget(hbox)

        hbox.show_all()

        if filter_type:
            filtro = gtk.FileFilter()
            filtro.set_name("Filtro")

            for fil in filter_type:
                filtro.add_pattern(fil)

            self.add_filter(filtro)

        elif mime:
            filtro = gtk.FileFilter()
            filtro.set_name("Filtro")

            for mi in mime:
                filtro.add_mime_type(mi)

            self.add_filter(filtro)

        self.add_shortcut_folder_uri("file:///media/")
        self.connect("file-activated", self.__file_activated)
        self.connect("realize", self.__resize)

    def __resize(self, widget):

        self.resize(437, 328)

    def __file_activated(self, widget):
        """
        Cuando se hace doble click sobre un archivo.
        """

        self.emit('archivos-seleccionados', self.get_filenames())
        self.__salir(None)

    def __seleccionar_todos_los_archivos(self, widget):

        self.select_all()

    def __salir(self, widget):

        self.destroy()
