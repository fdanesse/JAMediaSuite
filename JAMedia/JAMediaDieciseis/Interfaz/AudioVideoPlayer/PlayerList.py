#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
from ..Globales import describe_uri
from ..Globales import describe_archivo
from ..Globales import get_colors
from ..Globales import get_SeparatorToolItem
from ..Globales import get_boton
from ..Globales import get_ToggleToolButton
from ..Globales import describe_acceso_uri
from BalanceWidget import BalanceWidget

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONS = os.path.join(os.path.dirname(BASE_PATH), "Iconos")


class PlayerList(gtk.Frame):

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_size_request(180, -1)

        vbox = gtk.VBox()
        self.toolbar = ToolbarList()
        vbox.pack_start(self.toolbar, False, False, 0)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox1 = gtk.VBox()
        scroll.add_with_viewport(vbox1)
        scroll.get_child().modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.balance = BalanceWidget()
        vbox1.pack_start(self.balance, False, False, 0)
        self.lista = Lista()
        vbox1.pack_start(self.lista, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)
        self.add(vbox)

        self.toolbar.connect("configview", self.__show_config)
        self.toolbar.connect("load", self.__load_files)
        self.lista.connect("button-press-event", self.__click_en_lista)
        self.connect("realize", self.__realized)
        self.show_all()

    def __show_config(self, widget, valor):
        self.toolbar.show()
        if valor:
            self.lista.hide()
            self.balance.show()
        else:
            self.balance.hide()
            self.lista.show()

    def __realized(self, widget):
        self.balance.hide()
        self.toolbar.show()
        self.lista.show()

    def __click_en_lista(self, widget, event):
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
                widget, boton, pos, tiempo, path, widget.get_model())
            menu.connect('accion', self.__set_accion)
            gtk.Menu.popup(menu, None, None, None, boton, tiempo)
        elif boton == 2:
            return

    def __set_accion(self, widget, lista, accion, _iter):
        self.emit("accion", lista, accion, _iter)

    def __load_files(self, widget, items, tipo):
        if tipo == "load":
            self.lista.limpiar()
            self.toolbar.clear.set_sensitive(False)
        if items:
            self.lista.agregar_items(items)
            self.toolbar.clear.set_sensitive(True)

    def set_video(self, widget, valor):
        self.toolbar.config.set_sensitive(valor)
        if not valor and self.balance.get_visible():
            self.toolbar.config.set_active(valor)
            self.balance.hide()
            self.lista.show()


class ToolbarList(gtk.Toolbar):

    __gsignals__ = {
    "load": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING)),
    "configview": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN, ))}

    def __init__(self, mime=["audio/*", "video/*",
        "application/vnd.rn-realmedia/*"]):
        # application/vnd.rn-realmedia-vbr

        gtk.Toolbar.__init__(self)

        self.mime = mime
        self.directorio = os.environ["HOME"]

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.insert(get_SeparatorToolItem(
            draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(ICONS, "control_panel.png")
        self.config = get_ToggleToolButton(archivo, flip=False, pixels=24,
            tooltip_text="Configuraciones")
        self.config.connect("toggled", self.__toggled_button)
        self.insert(self.config, -1)
        self.config.set_sensitive(False)

        archivo = os.path.join(ICONS, "document-new.svg")
        boton = get_boton(archivo, flip=False, pixels=24,
            tooltip_text="Agregar Archivos")
        boton.connect("clicked", self.__open_files, "add")
        self.insert(boton, -1)

        archivo = os.path.join(ICONS, "document-open.svg")
        boton = get_boton(archivo, flip=False, pixels=24,
            tooltip_text="Abrir Archivos")
        boton.connect("clicked", self.__open_files, "load")
        self.insert(boton, -1)

        archivo = os.path.join(ICONS, "clear.svg")
        self.clear = get_boton(archivo, flip=False, pixels=24,
            tooltip_text="Limpiar Lista")
        self.clear.connect("clicked", self.__clear_list)
        self.insert(self.clear, -1)
        self.clear.set_sensitive(False)

        self.insert(get_SeparatorToolItem(
            draw=False, ancho=0, expand=True), -1)

        self.show_all()

    def __toggled_button(self, button):
        self.emit("configview", button.get_property("active"))

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

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.TreeView.__init__(self, gtk.ListStore(
            gtk.gdk.Pixbuf,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING))

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.permitir_select = True
        self.valor_select = False
        self.ultimo_select = False

        self.__setear_columnas()

        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()

    def __selecciones(self, path, column):
        if not self.permitir_select:
            return True
        _iter = self.get_model().get_iter(path)
        valor = self.get_model().get_value(_iter, 2)
        if self.valor_select != valor:
            self.valor_select = valor
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
        if not elementos:
            self.permitir_select = True
            modelo, _iter = self.get_selection().get_selected()
            if not _iter:
                self.seleccionar_primero()
            self.get_toplevel().set_sensitive(True)
            return False
        texto, path = elementos[0]
        descripcion = describe_uri(path)
        icono = os.path.join(ICONS, "sonido.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 24, -1)
        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = describe_archivo(path)
                if 'video' in tipo or 'application/ogg' in tipo \
                    or "application/vnd.rn-realmedia" in tipo:
                    icono = os.path.join(ICONS, "video.svg")
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
                            icono = os.path.join(ICONS, "sonido.svg")
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
        self.emit('nueva-seleccion', False)

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


class My_FileChooser(gtk.FileChooserDialog):

    __gsignals__ = {
    'archivos-seleccionados': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self, parent=None, action=None,
        filter_type=[], title=None, path=None, mime=[]):

        gtk.FileChooserDialog.__init__(self,
            title=title,
            parent=parent,
            action=action,
            )

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
        boton_seleccionar_todo.connect("clicked",
            self.__seleccionar_todos_los_archivos)

        hbox.pack_end(boton_salir, False, False, 5)
        hbox.pack_end(boton_seleccionar_todo, False, False, 5)
        hbox.pack_end(boton_abrir_directorio, False, False, 5)

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
        self.emit('archivos-seleccionados', self.get_filenames())
        self.__salir(None)

    def __seleccionar_todos_los_archivos(self, widget):
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
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Quitar")

        if describe_acceso_uri(uri):
            tipo = describe_archivo(uri)
            lectura, escritura, ejecucion = describe_acceso_uri(uri)

            if escritura:
                borrar = gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.__set_accion,
                    widget, path, "Borrar")

        tipo = describe_archivo(uri)
        if 'video' in tipo or 'application/ogg' in tipo or \
            "application/vnd.rn-realmedia" in tipo:
            subt = gtk.MenuItem("Cargar Subtitulos")
            self.append(subt)
            subt.connect_object("activate", self.__set_accion,
                widget, path, "Subtitulos")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __set_accion(self, widget, path, accion):
        _iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, _iter)
