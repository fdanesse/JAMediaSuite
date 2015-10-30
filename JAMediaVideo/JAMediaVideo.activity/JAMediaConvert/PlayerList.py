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
from Globales import describe_acceso_uri
from Globales import get_my_files_directory

BASE_PATH = os.path.dirname(__file__)
BASE_PATH = os.path.dirname(BASE_PATH)


class PlayerList(gtk.Frame):

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "accion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.modify_bg(0, get_colors("window"))

        vbox = gtk.VBox()

        self.toolbar = ToolbarList()
        self.lista = Lista()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(self.lista)

        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)

        self.add(vbox)
        self.show_all()

        self.set_size_request(250, -1)

        self.toolbar.connect("load", self.__load_files)
        self.lista.connect("nueva-seleccion", self.__re_emit_nueva_seleccion)
        self.lista.connect("button-press-event", self.__click_derecho_en_lista)

    def __click_derecho_en_lista(self, widget, event):
        """
        Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista de reproduccion, permitiendo copiar, mover y
        borrar el archivo o streaming o simplemente quitarlo
        de la lista.
        """

        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)

        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(
                int(pos[0]), int(pos[1]))

        except:
            return

        # TreeView.get_path_at_pos(event.x, event.y) devuelve:
        # * La ruta de acceso en el punto especificado (x, y),
        # en relación con las coordenadas widget
        # * El gtk.TreeViewColumn en ese punto
        # * La coordenada X en relación con el fondo de la celda
        # * La coordenada Y en relación con el fondo de la celda

        if boton == 1:
            return

        elif boton == 3:
            menu = MenuList(
                widget, boton, pos, tiempo, path, widget.get_model())
            menu.connect('accion', self.__set_accion)
            gtk.Menu.popup(menu, None, None, None, boton, tiempo)

        elif boton == 2:
            return

    def __set_accion(self, widget, lista, accion, _iter):
        """
        Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.

        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar.
        """
        self.emit("accion", lista, accion, _iter)

    def __re_emit_nueva_seleccion(self, widget, pista):
        self.emit('nueva-seleccion', pista)

    def __load_files(self, widget, items, tipo):
        if tipo == "load":
            self.lista.limpiar()
            self.emit("accion", False, "limpiar", False)

        if items:
            self.lista.agregar_items(items)

        else:
            self.emit('nueva-seleccion', False)

    def seleccionar_primero(self):
        self.lista.seleccionar_primero()

    def seleccionar_ultimo(self):
        self.lista.seleccionar_ultimo()

    def seleccionar_anterior(self):
        self.lista.seleccionar_anterior()

    def seleccionar_siguiente(self):
        self.lista.seleccionar_siguiente()

    def select_valor(self, path_origen):
        self.lista.select_valor(path_origen)

    def limpiar(self):
        self.lista.limpiar()

    def set_mime_types(self, mime):
        """
        Setea el tipo de elementos admitidos en la lista.
        """
        self.toolbar.mime = mime

    def get_selected_path(self):
        """
        Devuelve el valor del path seleccionado.
        """
        modelo, _iter = self.lista.get_selection().get_selected()
        valor = self.lista.get_model().get_value(_iter, 2)
        return valor

    def get_items_paths(self):
        """
        Devuelve la lista de archivos en la lista.
        """
        filepaths = []
        model = self.lista.get_model()
        item = model.get_iter_first()

        self.lista.get_selection().select_iter(item)
        first_path = model.get_path(item)

        while item:
            filepaths.append(model.get_value(item, 2))
            item = model.iter_next(item)

        return filepaths


class ToolbarList(gtk.EventBox):

    __gsignals__ = {
    "load": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING))}

    def __init__(self, mime=["audio/*", "video/*", "image/*"]):

        gtk.EventBox.__init__(self)

        self.mime = mime
        self.directorio = get_JAMedia_Directory()

        toolbar = gtk.Toolbar()

        self.modify_bg(0, get_colors("toolbars"))
        toolbar.modify_bg(0, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "document-open.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Abrir Archivos")
        boton.connect("clicked", self.__open_files, "load")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "document-new.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Agregar Archivos")
        boton.connect("clicked", self.__open_files, "add")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "clear.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Limpiar Lista")
        boton.connect("clicked", self.__clear_list)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

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
            path=self.directorio)

        selector.connect('archivos-seleccionados',
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

        self.directorio = os.path.dirname(path)
        self.emit("load", items, tipo)


class Lista(gtk.TreeView):
    """
    Lista generica.
    """

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.TreeView.__init__(self, gtk.ListStore(
            gdk.Pixbuf,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING))

        self.modify_bg(0, get_colors("window"))
        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.permitir_select = True
        self.valor_select = False
        self.ultimo_select = False
        #self.timer_select = False

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

            #if self.timer_select:
            #    gobject.source_remove(self.timer_select)
            #    self.timer_select = False

            gobject.timeout_add(3, self.__select,
                self.get_model().get_path(_iter))

        return True

    def __select(self, path):
        if self.ultimo_select != self.valor_select:
            self.emit('nueva-seleccion', self.valor_select)
            self.ultimo_select = self.valor_select

        self.scroll_to_cell(path)
        return False

    def __setear_columnas(self):
        self.append_column(self.__construir_columa_icono('', 0, True))
        self.append_column(self.__construir_columa('Archivo', 1, True))
        self.append_column(self.__construir_columa('', 2, False))

    def __construir_columa(self, text, index, visible):
        render = gtk.CellRendererText()
        render.set_property("background", get_colors("window"))
        render.set_property("foreground", get_colors("drawingplayer"))

        columna = gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        return columna

    def __construir_columa_icono(self, text, index, visible):
        render = gtk.CellRendererPixbuf()
        render.set_property("cell-background", get_colors("toolbars"))

        columna = gtk.TreeViewColumn(text, render, pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        return columna

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
        pixbuf = ""
        icono = None

        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = describe_archivo(path)

                if 'video' in tipo or 'application/ogg' in tipo:
                    icono = os.path.join(BASE_PATH, "Iconos", "video.svg")
                    pixbuf = gdk.pixbuf_new_from_file_at_size(icono, 24, -1)

                elif 'audio' in tipo or 'application/octet-stream' in tipo:
                    icono = os.path.join(BASE_PATH, "Iconos", "sonido.svg")
                    pixbuf = gdk.pixbuf_new_from_file_at_size(icono, 24, -1)

                else:
                    icono = path
                    if "image" in tipo:
                        pixbuf = gdk.pixbuf_new_from_file_at_size(
                            icono, 50, -1)

                    else:
                        try:
                            pixbuf = gdk.pixbuf_new_from_file_at_size(
                                icono, 24, -1)
                        except:
                            icono = os.path.join(BASE_PATH,
                                "Iconos", "sonido.svg")
                            pixbuf = gdk.pixbuf_new_from_file_at_size(
                                icono, 24, -1)

        else:
            icono = os.path.join(BASE_PATH, "Iconos", "sonido.svg")
            pixbuf = gdk.pixbuf_new_from_file_at_size(icono, 24, -1)

        self.get_model().append([pixbuf, texto, path])
        elementos.remove(elementos[0])
        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)
        return False

    def limpiar(self):
        self.permitir_select = False
        self.get_model().clear()
        self.valor_select = False
        self.ultimo_select = False
        #self.timer_select = False
        self.permitir_select = True

    def agregar_items(self, elementos):
        """
        Recibe lista de: [texto para mostrar, path oculto] y
        Comienza secuencia de agregado a la lista.
        """
        self.get_toplevel().set_sensitive(False)
        self.permitir_select = False

        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)

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

    def select_valor(self, path_origen):
        model = self.get_model()
        _iter = model.get_iter_first()
        valor = model.get_value(_iter, 2)

        while valor != path_origen:
            _iter = model.iter_next(_iter)
            valor = model.get_value(_iter, 2)

        if _iter:
            self.get_selection().select_iter(_iter)


class My_FileChooser(gtk.FileChooserDialog):
    """
    Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio.
    """

    __gsignals__ = {
    'archivos-seleccionados': (gobject.SIGNAL_RUN_LAST,
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
        boton_abrir_directorio.connect("clicked", self.__file_activated)
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


class MenuList(gtk.Menu):
    """
    Menu con opciones para operar sobre el archivo o
    el streaming seleccionado en la lista de reproduccion
    al hacer click derecho sobre él.
    """

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        gtk.Menu.__init__(self)

        _iter = modelo.get_iter(path)
        uri = modelo.get_value(_iter, 2)

        quitar = gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Quitar")

        my_files_directory = get_my_files_directory()

        if describe_acceso_uri(uri):
            tipo = describe_archivo(uri)
            lectura, escritura, ejecucion = describe_acceso_uri(uri)

            if lectura and os.path.dirname(uri) != my_files_directory:
                copiar = gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__set_accion,
                    widget, path, "Copiar")

            if escritura and os.path.dirname(uri) != my_files_directory:
                mover = gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__set_accion,
                    widget, path, "Mover")

            if escritura:
                borrar = gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.__set_accion,
                    widget, path, "Borrar")

            #if "audio" in tipo or "video" in tipo or "application/ogg" in tipo:
            #    editar = gtk.MenuItem("Editar o Convertir Archivo")
            #    self.append(editar)
            #    editar.connect_object("activate", self.__set_accion,
            #        widget, path, "Editar")

        #else:
        #    borrar = gtk.MenuItem("Borrar Streaming")
        #    self.append(borrar)
        #    borrar.connect_object("activate", self.__set_accion,
        #        widget, path, "Borrar")

        #    data_directory = get_data_directory()

        #    listas = [
        #        os.path.join(data_directory, "JAMediaTV.JAMedia"),
        #        os.path.join(data_directory, "JAMediaRadio.JAMedia"),
        #        os.path.join(data_directory, "MisRadios.JAMedia"),
        #        os.path.join(data_directory, "MisTvs.JAMedia")
        #        ]

        #    if (stream_en_archivo(uri, listas[0]) and \
        #        not stream_en_archivo(uri, listas[3])) or \
        #        (stream_en_archivo(uri, listas[1]) and \
        #        not stream_en_archivo(uri, listas[2])):

        #        copiar = gtk.MenuItem("Copiar a JAMedia")
        #        self.append(copiar)
        #        copiar.connect_object("activate", self.__set_accion,
        #            widget, path, "Copiar")

        #        mover = gtk.MenuItem("Mover a JAMedia")
        #        self.append(mover)
        #        mover.connect_object("activate", self.__set_accion,
        #            widget, path, "Mover")

        #    grabar = gtk.MenuItem("Grabar")
        #    self.append(grabar)
        #    grabar.connect_object("activate", self.__set_accion,
        #        widget, path, "Grabar")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __set_accion(self, widget, path, accion):
        """
        Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.

        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar.
        """
        _iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, _iter)
