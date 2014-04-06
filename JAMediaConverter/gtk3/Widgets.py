#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay
#
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
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import GdkPixbuf

from Globales import get_separador
from Globales import get_pixels
from Globales import describe_archivo
from Globales import describe_uri
from Globales import get_colors

BASEPATH = os.path.dirname(__file__)

#GObject.threads_init()


class Toolbar(Gtk.Toolbar):

    __gtype_name__ = 'JAMediaConverterToolbar'

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        item.set_expand(True)
        self.menu = Menu()
        self.menu.show()
        item.add(self.menu)
        self.insert(item, -1)
        '''
        archivo = os.path.join(BASEPATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)
        '''
        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.show_all()

        self.menu.connect(
            "load", self.__emit_load)

    def __emit_load(self, widget, archivos):

        self.emit('load', archivos)

    def __salir(self, widget):
        """
        Cuando se hace click en el boton salir.
        """

        self.emit('salir')


class Menu(Gtk.MenuBar):
    """
    Toolbar Principal.
    """

    __gtype_name__ = 'JAMediaConverterMenu'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        item_Procesar = Gtk.MenuItem('Cargar')
        menu_Procesar = Gtk.Menu()
        item_Procesar.set_submenu(menu_Procesar)
        self.append(item_Procesar)

        item = Gtk.MenuItem('Directorio ...')
        item.connect("activate", self.__emit_accion)
        menu_Procesar.append(item)

        item = Gtk.MenuItem('Archivos ...')
        item.connect("activate", self.__emit_accion)
        menu_Procesar.append(item)

        self.show_all()

    def __emit_accion(self, widget):

        valor = widget.get_label()

        mtype = ["audio/*", "video/*"]

        if valor == 'Directorio ...':
            filechooser = FileChooser(
                parent_window=self.get_toplevel(),
                title="Cargar Archivos",
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                #path=path,
                mime=mtype,
                )

            filechooser.connect('load', self.__emit_load)

        elif valor == 'Archivos ...':
            filechooser = FileChooser(
                parent_window=self.get_toplevel(),
                title="Cargar Archivos",
                action=Gtk.FileChooserAction.OPEN,
                #path=path,
                mime=mtype,
                )

            filechooser.connect('load', self.__emit_load)

    def __emit_load(self, widget, archivos):

        self.emit('load', archivos)


class FileChooser(Gtk.FileChooserDialog):

    __gtype_name__ = 'JAMediaConverterFileChooser'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self,
        parent_window=None,
        filter_type=[],
        title=None,
        #path=None,
        action=Gtk.FileChooserAction.OPEN,
        mime=[]):

        Gtk.FileChooserDialog.__init__(self,
            parent=parent_window,
            action=action,
            flags=Gtk.DialogFlags.MODAL,
            title=title)

        self.action = action
        self.set_default_size(640, 480)
        self.modify_bg(0, get_colors("window"))

        #if os.path.isfile(path):
        #    self.set_filename(path)

        #else:
        #    self.set_current_folder_uri("file://%s" % path)

        if self.action == Gtk.FileChooserAction.OPEN:
            self.set_select_multiple(True)

            if filter_type:
                filter = Gtk.FileFilter()
                filter.set_name("Filtro")

                for fil in filter_type:
                    filter.add_pattern(fil)

                self.add_filter(filter)

            elif mime:
                filter = Gtk.FileFilter()
                filter.set_name("Filtro")

                for m in mime:
                    filter.add_mime_type(m)

                self.add_filter(filter)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        abrir = Gtk.Button("Abrir")
        salir = Gtk.Button("Salir")

        hbox.pack_end(salir, True, True, 5)
        hbox.pack_end(abrir, True, True, 5)

        self.set_extra_widget(hbox)

        salir.connect("clicked", self.__salir)
        abrir.connect("clicked", self.__abrir)

        self.show_all()

        #self.connect("file-activated", self.__file_activated)

    #def __file_activated(self, widget):
    #    """
    #    Cuando se hace doble click sobre un archivo.
    #    """

    #    self.__abrir(None)

    def __abrir(self, widget):
        """
        Emite el path del archivo seleccionado.
        """

        files = self.get_filenames()

        if self.action == Gtk.FileChooserAction.SELECT_FOLDER:
            self.emit('load', files)

        elif self.action == Gtk.FileChooserAction.OPEN:
            if not files:
                self.__salir(None)
                return

            archivos = []
            for file in files:
                direccion = str(file).replace("//", "/")

                if os.path.exists(direccion) and os.path.isfile(direccion):
                    archivos.append(direccion)

            self.emit('load', archivos)

        self.__salir()

    def __salir(self, widget=None):

        self.destroy()


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

        descripcion = describe_uri(path)

        icono = None
        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = describe_archivo(path)

                if 'video' in tipo or 'application/ogg' in tipo or \
                    'application/octet-stream' in tipo:
                    icono = os.path.join(BASEPATH,
                        "Iconos", "video.svg")

                elif 'audio' in tipo:
                    icono = os.path.join(BASEPATH,
                        "Iconos", "sonido.svg")

                else:
                    icono = os.path.join(BASEPATH,
                        "Iconos", "sonido.svg")

        else:
            icono = os.path.join(BASEPATH,
                "Iconos", "sonido.svg")

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
