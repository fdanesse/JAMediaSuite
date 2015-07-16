#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
from ..Globales import get_colors
from ..Globales import get_SeparatorToolItem
from ..Globales import get_boton
from ..Globales import get_radios

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

        vbox = gtk.VBox()
        self.toolbar = ToolbarList()
        vbox.pack_start(self.toolbar, False, False, 0)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.lista = Lista()
        scroll.add(self.lista)
        scroll.get_child().modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        vbox.pack_end(scroll, True, True, 0)
        self.add(vbox)

        self.toolbar.connect("load", self.__load)
        self.toolbar.connect("buscar", self.lista.buscar)
        self.lista.connect("button-press-event", self.__click_en_lista)
        self.show_all()

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
        print accion
        #self.emit("accion", lista, accion, _iter)

    def __load(self, widget, items, tipo):
        if tipo == "load":
            self.lista.limpiar()
            # Fixme: si hay internet
            items = get_radios()
            self.lista.agregar_items(items)
        elif tipo == "add":
            dialog = Dialog_add_Streaming(parent=self.get_toplevel())
            resp = dialog.run()
            if resp == gtk.RESPONSE_ACCEPT:
                print dialog.get_datos()
            dialog.destroy()


class ToolbarList(gtk.Toolbar):

    __gsignals__ = {
    "load": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING)),
    "buscar": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.insert(get_SeparatorToolItem(
            draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(ICONS, "document-new.svg")
        boton = get_boton(archivo, flip=False, pixels=24,
            tooltip_text="Agregar Emisora")
        boton.connect("clicked", self.__open_files, "add")
        self.insert(boton, -1)

        archivo = os.path.join(ICONS, "document-open.svg")
        boton = get_boton(archivo, flip=False, pixels=24,
            tooltip_text="Cargar Lista de Emisoras")
        boton.connect("clicked", self.__open_files, "load")
        self.insert(boton, -1)

        self.insert(get_SeparatorToolItem(
            draw=False, ancho=10, expand=False), -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        self.entry = gtk.Entry()
        self.entry.connect("activate", self.__buscar)
        item.add(self.entry)
        self.insert(item, -1)

        self.insert(get_SeparatorToolItem(
            draw=False, ancho=10, expand=False), -1)

        archivo = os.path.join(ICONS, "buscar.svg")
        boton = get_boton(archivo, flip=False, pixels=24,
            tooltip_text="Buscar")
        boton.connect("clicked", self.__buscar)
        self.insert(boton, -1)

        self.insert(get_SeparatorToolItem(
            draw=False, ancho=3, expand=False), -1)

        self.show_all()

    def __buscar(self, widget):
        self.emit("buscar", self.entry.get_text().strip().lower())

    def __open_files(self, widget, tipo):
        self.emit("load", [], tipo)


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
        #render.set_property("cell-background", get_colors("toolbars"))
        columna = gtk.TreeViewColumn(text, render, pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        return columna

    def __ejecutar_agregar_elemento(self, elementos):
        if not elementos:
            self.permitir_select = True
            modelo, _iter = self.get_selection().get_selected()
            #if not _iter:
            #    self.seleccionar_primero()
            self.get_toplevel().set_sensitive(True)
            return False
        texto, path = elementos[0]
        icono = os.path.join(ICONS, "Music-Radio-1-icon.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 24, -1)
        self.get_model().append([pixbuf, texto, path])
        elementos.remove(elementos[0])
        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)
        return False

    def __buscar_delante(self, texto, _iter):
        if not _iter:
            return False
        model = self.get_model()
        while _iter:
            contenido = model.get_value(_iter, 1).lower()
            if texto in contenido:
                self.get_selection().select_iter(_iter)
                self.scroll_to_cell(model.get_path(_iter))
                return True
            _iter = model.iter_next(_iter)

    def buscar(self, widget, texto):
        model, _iter = self.get_selection().get_selected()
        inicio = _iter
        if not _iter:
            _iter = model.get_iter_first()
            inicio = _iter
        else:
            _iter = model.iter_next(_iter)
        if not self.__buscar_delante(texto, _iter):
            if inicio != _iter:
                self.__buscar_delante(texto, model.get_iter_first())

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


class MenuList(gtk.Menu):

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        gtk.Menu.__init__(self)

        quitar = gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Quitar")

        quitar = gtk.MenuItem("Eliminar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Borrar")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __set_accion(self, widget, path, accion):
        _iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, _iter)


class Dialog_add_Streaming(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self, parent=parent,
                title="Agregar Streaming",
                buttons=("Guardar", gtk.RESPONSE_ACCEPT,
                "Cancelar", gtk.RESPONSE_CANCEL))

        self.set_border_width(15)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        frame = gtk.Frame()
        frame.set_property("label", " Nombre: ")
        event = gtk.EventBox()
        event.set_border_width(8)
        self.nombre = gtk.Entry()
        event.add(self.nombre)
        frame.add(event)
        self.vbox.pack_start(frame, True, True, 0)

        frame = gtk.Frame()
        frame.set_property("label", " URL: ")
        event = gtk.EventBox()
        event.set_border_width(8)
        self.url = gtk.Entry()
        event.add(self.url)
        frame.add(event)
        self.vbox.pack_start(frame, True, True, 0)
        self.vbox.show_all()

    def get_datos(self):
        return [self.nombre.get_text().strip(), self.url.get_text().strip()]
