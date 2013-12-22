#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Navegador.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM - Uruguay
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
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

from NoteBookDirectorios import NoteBookDirectorios

import JAMediaObjects
from JAMediaObjects.JAMFileSystem import DeviceManager
from JAMediaObjects.JAMFileSystem import describe_uri
from JAMediaObjects.JAMediaGlobales import get_pixels

ICONOS = os.path.join(JAMediaObjects.__path__[0], "Iconos")

HOME = os.environ["HOME"]
ACTIVITIES = os.path.join(HOME, "Activities")
DIARIO = os.path.join(HOME, ".sugar/default")
LOGS = os.path.join(DIARIO, "logs")
ROOT = "/"
JAMEDIA = os.path.join(HOME, "JAMediaDatos")


class Navegador(Gtk.Paned):
    """
    Navegador de Archivos.
    """

    __gtype_name__ = 'JAMediaExplorerNavegador'

    __gsignals__ = {
    "info": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "cargar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    "borrar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.Paned.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.unidades = None
        self.notebookdirectorios = NoteBookDirectorios()
        self.infowidget = None

        self.pack1(self.__area_izquierda_del_panel(),
            resize=False, shrink=True)
        self.pack2(self.notebookdirectorios,
            resize=True, shrink=True)

        self.show_all()

        self.unidades.connect('leer', self.__leer)
        self.unidades.get_selection().select_path(0)
        self.unidades.connect('info', self.__emit_info)

        self.notebookdirectorios.connect('info', self.__emit_info)
        self.notebookdirectorios.connect('borrar', self.__emit_borrar)

        self.infowidget.connect('cargar', self.__emit_cargar)

    def __emit_borrar(self, widget, direccion, modelo, iter):
        """
        Cuando se selecciona borrar en el menu de un item.
        """

        self.emit('borrar', direccion, modelo, iter)

    def __emit_cargar(self, widget, tipo):
        """
        Cuando se hace click en infowidget se pasa
        los datos a la ventana principal.
        """

        self.emit('cargar', tipo)

    def __emit_info(self, widget, path):
        """
        Cuando el usuario selecciona un archivo
        o directorio en la estructura de directorios,
        pasa la informacion del mismo a la ventana principal.
        """

        self.emit('info', path)

    def __area_izquierda_del_panel(self):

        self.unidades = Unidades()

        panel_izquierdo = Gtk.Paned(
            orientation=Gtk.Orientation.VERTICAL)

        panel_izquierdo.pack1(
            self.unidades, resize=False, shrink=True)

        self.infowidget = InfoWidget()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scrolled_window.add_with_viewport(self.infowidget)

        panel_izquierdo.pack2(
            scrolled_window, resize=True, shrink=True)

        return panel_izquierdo

    def __leer(self, widget, directorio):
        """
        Cuando se selecciona una unidad en el panel izquierdo.
        """

        self.notebookdirectorios.load(directorio)


class Unidades(Gtk.TreeView):
    """
    Treview para unidades y directorios.
    """

    __gtype_name__ = 'JAMediaExplorerUnidades'

    __gsignals__ = {
    "leer": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "info": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GdkPixbuf.Pixbuf,
            GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(False)
        self.set_headers_visible(False)

        self.dir_select = None

        self.demonio_unidades = DeviceManager()

        self.__setear_columnas()
        self.__Llenar_ListStore()

        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()

        self.demonio_unidades.connect(
            'nueva_unidad_conectada',
            self.__nueva_unidad_conectada)

        self.demonio_unidades.connect(
            'nueva_unidad_desconectada',
            self.__nueva_unidad_desconectada)

    def __nueva_unidad_conectada(self, widget, unidad):
        """
        Cuando se conecta una unidad, se agrega a la lista.
        """

        icono = os.path.join(ICONOS,
            "drive-removable-media-usb.svg")

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, get_pixels(0.8), -1)

        self.get_model().append([
            pixbuf, unidad['label'],
            unidad['mount_path']])

    def __nueva_unidad_desconectada(self, widget, unidad):
        """
        Cuando se desconecta una unidad, se quita de la lista.
        """

        iter = self.get_model().get_iter_first()
        self.remover_unidad(iter, unidad)

    def __remover_unidad(self, iter, unidad):
        """
        Cuando se desconecta una unidad, se quita de la lista.
        """

        directorio = self.get_model().get_value(iter, 2)

        if directorio == unidad['mount_path']:
            self.get_model().remove(iter)

        else:
            iter = self.get_model().iter_next(iter)
            self.remover_unidad(iter, unidad)

    def __selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se hace click sobre una unidad de almacenamiento.
        """

        # model y listore son ==
        iter = model.get_iter(path)
        directorio = model.get_value(iter, 2)

        if not is_selected and self.dir_select != directorio:
            self.dir_select = directorio
            self.emit('leer', self.dir_select)
            self.emit('info', self.dir_select)

        return True

    def __setear_columnas(self):

        self.append_column(
            self.__construir_columa_icono('Icono', 0, True))
        self.append_column(
            self.__construir_columa('Nombre', 1, True))
        self.append_column(
            self.__construir_columa('Directorio', 2, False))

    def __construir_columa(self, text, index, visible):

        render = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(text, render, text=index)
        column.set_sort_column_id(index)
        column.set_property('visible', visible)

        return column

    def __construir_columa_icono(self, text, index, visible):

        render = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn(text, render, pixbuf=index)
        column.set_property('visible', visible)

        return column

    def __Llenar_ListStore(self):

        icono = os.path.join(ICONOS, "def.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, get_pixels(0.8), -1)
        self.get_model().append([pixbuf, 'Raiz', ROOT])

        icono = os.path.join(ICONOS, "stock-home.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, get_pixels(0.8), -1)
        self.get_model().append([pixbuf, 'Usuario', HOME])

        if describe_uri(ACTIVITIES):
            icono = os.path.join(ICONOS, "stock-home.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'Actividades', ACTIVITIES])

        if describe_uri(JAMEDIA):
            icono = os.path.join(ICONOS, "JAMedia.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'JAMediaDatos', JAMEDIA])

        if describe_uri(DIARIO):
            icono = os.path.join(ICONOS, "diario.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'Diario', DIARIO])

        if describe_uri(LOGS):
            icono = os.path.join(ICONOS, "diario.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'Logs', LOGS])

        icono = os.path.join(ICONOS, "drive-removable-media-usb.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, get_pixels(0.8), -1)

        for unidad in self.demonio_unidades.get_unidades():
            self.get_model().append([
                pixbuf, unidad['label'], unidad['mount_path']])


class InfoWidget(Gtk.EventBox):
    """
    Widgets con información sobre en path
    seleccionado en la estructura de directorios y archivos.
    """

    __gtype_name__ = 'JAMediaExplorerInfoWidget'

    __gsignals__ = {
    "cargar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.normal_color = Gdk.Color(65000, 65000, 65000)
        self.select_color = Gdk.Color(61686, 65000, 48431)
        self.clicked_color = Gdk.Color(61686, 65000, 17078)

        self.modify_bg(0, self.normal_color)
        self.set_tooltip_text("Click para Ver el Archivo.")

        self.typeinfo = None

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.label = Gtk.Label("")
        self.imagen = Gtk.Image()
        self.imagen.modify_bg(0, self.normal_color)

        self.box.pack_start(self.label, False, False, 5)
        self.box.pack_start(self.imagen, True, True, 5)

        self.add(self.box)
        self.show_all()

    def set_info(self, textinfo, typeinfo):
        """
        Setea la información sobre un objeto seleccionado
        en la estructura de directorios.
        """

        # FIXME: Verificar Iconos

        self.label.set_text(textinfo)
        self.typeinfo = typeinfo
        icono = None

        if textinfo.startswith("Directorio") or \
            textinfo.startswith("Enlace"):
            icono = os.path.join(ICONOS, "document-open.svg")

        else:
            if 'video' in typeinfo:
                icono = os.path.join(ICONOS, "video.svg")

            elif 'pdf' in typeinfo:
                icono = os.path.join(ICONOS, "pdf.svg")

            elif 'audio' in typeinfo:
                icono = os.path.join(ICONOS, "sonido.svg")

            elif 'image' in typeinfo and not 'iso' in typeinfo:
                icono = os.path.join(ICONOS, "edit-select-all.svg")

            elif 'zip' in typeinfo or 'tar' in typeinfo:
                icono = os.path.join(ICONOS, "edit-select-all.svg")

            elif 'text' in typeinfo:
                icono = os.path.join(ICONOS, "edit-select-all.svg")

            else:
                icono = os.path.join(ICONOS, "edit-select-all.svg")
                self.typeinfo = None

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, 100, -1)
        self.imagen.set_from_pixbuf(pixbuf)

    def do_button_press_event(self, widget):
        """
        Cuando se hace click, se emite la señal
        cargar y se pasa el tipo de archivo para que la
        aplicacion decida si abrir o no otra aplicacion
        embebida que sepa tratar el archivo.
        """

        self.modify_bg(0, self.clicked_color)
        self.imagen.modify_bg(0, self.clicked_color)

        if self.typeinfo:
            self.emit('cargar', self.typeinfo)

    def do_button_release_event(self, widget):

        self.modify_bg(0, self.select_color)
        self.imagen.modify_bg(0, self.select_color)

    def do_enter_notify_event(self, widget):

        self.modify_bg(0, self.select_color)
        self.imagen.modify_bg(0, self.select_color)

    def do_leave_notify_event(self, widget):

        self.modify_bg(0, self.normal_color)
        self.imagen.modify_bg(0, self.normal_color)
