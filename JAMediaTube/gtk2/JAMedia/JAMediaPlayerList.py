#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPlayerList.py por:
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

from Globales import get_colors
from Globales import get_separador
from Globales import get_boton

from Globales import describe_uri
from Globales import describe_archivo
from Globales import describe_acceso_uri
from Globales import get_streamings
from Globales import stream_en_archivo

from Globales import get_JAMedia_Directory
from Globales import get_data_directory
from Globales import get_my_files_directory
from Globales import get_tube_directory
from Globales import get_audio_directory
from Globales import get_video_directory

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def ocultar(objeto):
    if objeto.get_visible():
        objeto.hide()


def mostrar(objeto):
    if not objeto.get_visible():
        objeto.show()


class PlayerList(gtk.Frame):

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "accion-list": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    "menu_activo": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "add_stream": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "len_items": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT, ))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.directorio = get_JAMedia_Directory()
        self.mime = ['audio/*', 'video/*']

        vbox = gtk.VBox()

        self.toolbar = JAMediaToolbarList()
        self.lista = Lista()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(self.lista)

        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)

        self.add(vbox)
        self.show_all()

        self.set_size_request(150, -1)

        self.toolbar.connect("cargar_lista", self.cargar_lista)
        self.toolbar.connect("add_stream", self.__emit_add_stream)
        self.toolbar.connect("menu_activo", self.__emit_menu_activo)

        self.lista.connect("nueva-seleccion", self.__emit_nueva_seleccion)
        self.lista.connect("button-press-event", self.__click_derecho_en_lista)
        self.lista.connect("len_items", self.__re_emit_len_items)

    def __re_emit_len_items(self, widget, items):
        self.emit("len_items", items)

    def __emit_add_stream(self, widget):
        # El usuario agregará una dirección de streaming
        self.emit("add_stream", self.toolbar.label.get_text())

    def __emit_menu_activo(self, widget=False):
        # hay un menu contextual presente
        self.emit("menu_activo")

    def __emit_accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.emit("accion-list", lista, accion, _iter)

    def __emit_nueva_seleccion(self, widget, pista):
        # item seleccionado en la lista
        self.emit('nueva-seleccion', pista)

    def __seleccionar_lista_de_stream(self, archivo, titulo):
        items = get_streamings(archivo)
        self.__load_list(items, "load", titulo)

    def __seleccionar_lista_de_archivos(self, directorio, titulo):
        archivos = sorted(os.listdir(directorio))
        lista = []
        for path in archivos:
            archivo = os.path.join(directorio, path)
            if os.path.isfile(archivo):
                lista.append(archivo)
        self.__load_files(False, lista, titulo)

    def __load_files(self, widget, archivos, titulo=False):
        items = []
        archivos.sort()
        for path in archivos:
            if not os.path.isfile(path):
                continue
            archivo = os.path.basename(path)
            items.append([archivo, path])
            self.directorio = os.path.dirname(path)
        self.__load_list(items, "load", titulo)
        # FIXME: Mostrar clear y add para agregar archivos a la lista

    def __load_list(self, items, tipo, titulo=False):
        if tipo == "load":
            self.lista.limpiar()
            self.emit("accion-list", False, "limpiar", False)
        if items:
            self.lista.agregar_items(items)
        else:
            self.emit('nueva-seleccion', False)
        if titulo != False:
            self.toolbar.label.set_text(titulo)

    def __click_derecho_en_lista(self, widget, event):
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
        if boton == 1 or boton == 2:
            return
        elif boton == 3:
            self.__emit_menu_activo()
            menu = MenuList(
                widget, boton, pos, tiempo, path, widget.get_model())
            menu.connect('accion', self.__emit_accion_list)
            gtk.Menu.popup(menu, None, None, None, boton, tiempo)

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
        self.mime = mime

    def get_selected_path(self):
        modelo, _iter = self.lista.get_selection().get_selected()
        valor = self.lista.get_model().get_value(_iter, 2)
        return valor

    def get_items_paths(self):
        filepaths = []
        model = self.lista.get_model()
        item = model.get_iter_first()
        self.lista.get_selection().select_iter(item)
        while item:
            filepaths.append(model.get_value(item, 2))
            item = model.iter_next(item)
        return filepaths

    def setup_init(self):
        ocultar(self.toolbar.boton_agregar)

    def cargar_lista(self, widget, indice):
        data = get_data_directory()
        _dict = {
            0: os.path.join(data, 'JAMediaRadio.JAMedia'),
            1: os.path.join(data, 'JAMediaTV.JAMedia'),
            2: os.path.join(data, 'MisRadios.JAMedia'),
            3: os.path.join(data, 'MisTvs.JAMedia'),
            4: os.path.join(data, 'JAMediaWebCams.JAMedia'),
            5: get_my_files_directory(),
            6: get_tube_directory(),
            7: get_audio_directory(),
            8: get_video_directory(),
            }
        ocultar(self.toolbar.boton_agregar)
        if indice == 0:
            self.__seleccionar_lista_de_stream(_dict[0], "JAM-Radio")
        elif indice == 1:
            self.__seleccionar_lista_de_stream(_dict[1], "JAM-TV")
        elif indice == 2:
            self.__seleccionar_lista_de_stream(_dict[2], "Radios")
            mostrar(self.toolbar.boton_agregar)
        elif indice == 3:
            self.__seleccionar_lista_de_stream(_dict[3], "TVs")
            mostrar(self.toolbar.boton_agregar)
        elif indice == 4:
            self.__seleccionar_lista_de_stream(_dict[4], "WebCams")
        elif indice == 5:
            self.__seleccionar_lista_de_archivos(_dict[indice], "Archivos")
        elif indice == 6:
            self.__seleccionar_lista_de_archivos(_dict[indice], "JAM-Tube")
        elif indice == 7:
            self.__seleccionar_lista_de_archivos(_dict[indice], "JAM-Audio")
        elif indice == 8:
            self.__seleccionar_lista_de_archivos(_dict[indice], "JAM-Video")
        elif indice == 9:
            selector = My_FileChooser(parent=self.get_toplevel(),
                filter_type=[], action=gtk.FILE_CHOOSER_ACTION_OPEN,
                mime=self.mime, title="Abrir Archivos", path=self.directorio)
            selector.connect('load-files', self.__load_files, "Archivos")
            selector.run()
            if selector:
                selector.destroy()

    def set_ip(self, valor):
        self.toolbar.ip = valor

    def set_nueva_lista(self, archivos):
        self.__load_files(False, archivos, titulo="Archivos")


class Lista(gtk.TreeView):

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "len_items": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT, ))}

    def __init__(self):

        gtk.TreeView.__init__(self, gtk.ListStore(gtk.gdk.Pixbuf,
            gobject.TYPE_STRING, gobject.TYPE_STRING))

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.len_items = 0
        self.permitir_select = True
        self.valor_select = False

        self.__setear_columnas()

        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()

    def __selecciones(self, path, column):
        if not self.permitir_select:
            return True
        self.permitir_select = False
        _iter = self.get_model().get_iter(path)
        valor = self.get_model().get_value(_iter, 2)
        if self.valor_select != valor:
            gobject.timeout_add(3, self.__select, _iter, valor)
        return True

    def __select(self, _iter, valor):
        self.valor_select = valor
        self.emit('nueva-seleccion', self.valor_select)
        self.scroll_to_cell(self.get_model().get_path(_iter))
        self.permitir_select = True
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
        self.permitir_select = False
        self.set_sensitive(False)
        if not elementos:
            self.permitir_select = True
            self.seleccionar_primero()
            self.set_sensitive(True)
            return False

        texto, path = elementos[0]
        descripcion = describe_uri(path)
        icono = os.path.join(BASE_PATH, "Iconos", "sonido.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 24, -1)

        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = describe_archivo(path)
                if 'video' in tipo or 'application/ogg' in tipo:
                    icono = os.path.join(BASE_PATH, "Iconos", "video.svg")
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                        icono, 24, -1)
                elif 'audio' in tipo or 'application/octet-stream' in tipo:
                    pass
                else:
                    if "image" in tipo:
                        icono = path
                        try:
                            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                icono, 50, -1)
                        except:
                            icono = os.path.join(BASE_PATH,
                                "Iconos", "sonido.svg")
                            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                icono, 24, -1)

        self.get_model().append([pixbuf, texto, path])
        elementos.remove(elementos[0])
        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)
        return False

    def limpiar(self):
        self.permitir_select = False
        self.get_model().clear()
        self.valor_select = False
        self.ultimo_select = False
        self.permitir_select = True
        self.len_items = 0
        self.emit("len_items", 0)

    def agregar_items(self, elementos):
        self.len_items = len(elementos)
        self.emit("len_items", self.len_items)
        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)

    def seleccionar_siguiente(self, widget=None):
        modelo, _iter = self.get_selection().get_selected()
        try:
            self.get_selection().select_iter(
                self.get_model().iter_next(_iter))
        except:
            if self.len_items == 1:
                self.emit('nueva-seleccion', self.valor_select)
            else:
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

    __gsignals__ = {
    'load-files': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self, parent=None, action=None,
        filter_type=[], title=None, path=None, mime=[]):

        gtk.FileChooserDialog.__init__(self, title=title, parent=parent,
            action=action)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_resizable(True)
        self.set_size_request(320, 240)

        self.set_current_folder_uri("file://%s" % path)
        self.set_select_multiple(True)

        hbox = gtk.HBox()

        boton_abrir_directorio = gtk.Button("Abrir")
        boton_seleccionar_todo = gtk.Button("Seleccionar Todos")
        boton_salir = gtk.Button("Salir")
        boton_salir.connect("clicked", self.__salir)

        boton_abrir_directorio.connect("clicked", self.__file_activated)
        boton_seleccionar_todo.connect("clicked", self.__select_all)

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
        self.emit('load-files', self.get_filenames())
        self.__salir(None)

    def __select_all(self, widget):
        self.select_all()

    def __salir(self, widget):
        self.destroy()


class MenuList(gtk.Menu):

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
        quitar.connect_object("activate", self.__emit_accion,
            widget, path, "Quitar")

        my_files_directory = get_my_files_directory()

        if describe_acceso_uri(uri):
            lectura, escritura, ejecucion = describe_acceso_uri(uri)
            if lectura and os.path.dirname(uri) != my_files_directory:
                copiar = gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__emit_accion,
                    widget, path, "Copiar")
            if escritura and os.path.dirname(uri) != my_files_directory:
                mover = gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__emit_accion,
                    widget, path, "Mover")
            if escritura:
                borrar = gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.__emit_accion,
                    widget, path, "Borrar")
            #tipo = describe_archivo(uri)
            #if "audio" in tipo or "video" in tipo or
            # "application/ogg" in tipo:
            #    editar = gtk.MenuItem("Editar o Convertir Archivo")
            #    self.append(editar)
            #    editar.connect_object("activate", self.__emit_accion,
            #        widget, path, "Editar")
        else:
            borrar = gtk.MenuItem("Borrar Streaming")
            self.append(borrar)
            borrar.connect_object("activate", self.__emit_accion,
                widget, path, "Borrar")
            listas = [
                os.path.join(get_data_directory(), "JAMediaTV.JAMedia"),
                os.path.join(get_data_directory(), "JAMediaRadio.JAMedia"),
                os.path.join(get_data_directory(), "MisRadios.JAMedia"),
                os.path.join(get_data_directory(), "MisTvs.JAMedia"),
                os.path.join(get_data_directory(), "JAMediaWebCams.JAMedia"),
                ]
            jtv = stream_en_archivo(uri, listas[0])
            jr = stream_en_archivo(uri, listas[1])
            r = stream_en_archivo(uri, listas[2])
            tv = stream_en_archivo(uri, listas[3])
            #webcam = stream_en_archivo(uri, listas[4])

            if (jtv and not tv) or (jr and not r):
                copiar = gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__emit_accion,
                    widget, path, "Copiar")
                mover = gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__emit_accion,
                    widget, path, "Mover")

            grabar = gtk.MenuItem("Grabar")
            self.append(grabar)
            grabar.connect_object("activate", self.__emit_accion,
                widget, path, "Grabar")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __emit_accion(self, widget, path, accion):
        _iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, _iter)


class JAMediaToolbarList(gtk.EventBox):

    __gsignals__ = {
    "cargar_lista": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "add_stream": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "menu_activo": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.ip = False

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Selecciona una Lista")
        boton.connect("clicked", self.__get_menu)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("")
        self.label.modify_fg(0, get_colors("drawingplayer"))
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "agregar.svg")
        self.boton_agregar = get_boton(archivo, flip=False, pixels=24)
        self.boton_agregar.set_tooltip_text("Agregar Streaming")
        self.boton_agregar.connect("clicked", self.__emit_add_stream)
        toolbar.insert(self.boton_agregar, -1)

        self.add(toolbar)
        self.show_all()

    def __get_menu(self, widget):
        self.emit("menu_activo")
        menu = gtk.Menu()

        if self.ip:
            item = gtk.MenuItem("JAMedia Radio")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 0)

            item = gtk.MenuItem("JAMedia TV")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 1)

            item = gtk.MenuItem("Mis Emisoras")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 2)

            item = gtk.MenuItem("Mis Canales")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 3)

            item = gtk.MenuItem("Web Cams")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 4)

        item = gtk.MenuItem("Mis Archivos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 5)

        item = gtk.MenuItem("JAMediaTube")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 6)

        item = gtk.MenuItem("Audio-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 7)

        item = gtk.MenuItem("Video-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 8)

        item = gtk.MenuItem("Archivos Externos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 9)

        menu.show_all()
        menu.attach_to_widget(widget, self.__null)
        gtk.Menu.popup(menu, None, None, None, 1, 0)

    def __null(self):
        pass

    def __emit_load_list(self, indice):
        self.emit("cargar_lista", indice)

    def __emit_add_stream(self, widget):
        self.emit("add_stream")
