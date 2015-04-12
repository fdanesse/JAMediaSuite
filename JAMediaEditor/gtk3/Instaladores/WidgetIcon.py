#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetIcon.py por:
#       Flavio Danesse      <fdanesse@gmail.com>

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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject


def get_boton(stock, tooltip):
    boton = Gtk.ToolButton.new_from_stock(stock)
    boton.set_tooltip_text(tooltip)
    boton.TOOLTIP = tooltip
    return boton


def get_separador(draw=False, ancho=0, expand=False):
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


class WidgetIcon(Gtk.Frame):
    """
    Widget que permite al usuario seleccionar el ícono de la aplicación.
    """

    __gtype_name__ = 'JAMediaEditorWidgetIcon'

    __gsignals__ = {
    'iconpath': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'make': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, tipo, proyecto_path):

        Gtk.Frame.__init__(self)

        self.set_label(" Selecciona un Icono para Tu Aplicación ")
        self.set_border_width(15)

        self.tipo = tipo
        self.proyecto_path = proyecto_path

        toolbar = Gtk.Toolbar()
        toolbar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#edf5ff'))

        self.image = Gtk.Image()
        self.image.set_size_request(50, 50)

        boton = get_boton(Gtk.STOCK_OPEN, "Buscar Archivo")
        self.aceptar = Gtk.Button("Construir Instalador")
        self.aceptar.set_sensitive(False)

        toolbar.insert(get_separador(draw=False, ancho=10, expand=False), -1)

        item = Gtk.ToolItem()
        item.add(self.image)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=10, expand=False), -1)
        toolbar.insert(boton, -1)
        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        item.add(self.aceptar)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=10, expand=False), -1)

        self.add(toolbar)
        self.show_all()

        boton.connect("clicked", self.__open_filechooser)
        self.aceptar.connect("clicked", self.__emit_construir)

    def __emit_construir(self, widget):
        self.emit("make")

    def __open_filechooser(self, widget):
        mimes = ["image/*"]
        if self.tipo == "sugar":
            mimes = ["image/svg+xml"]
        filechooser = FileChooser(self.get_toplevel(),
            mimes, self.proyecto_path)
        ret = filechooser.run()
        if ret == Gtk.ResponseType.ACCEPT:
            path = u'%s'.encode('utf8') % filechooser.get_filename()
            self.__set_icon_path(path)
        filechooser.destroy()

    def __set_icon_path(self, iconpath):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(iconpath, 50, 50)
        self.image.set_from_pixbuf(pixbuf)
        self.aceptar.set_sensitive(True)
        self.emit("iconpath", iconpath)


class FileChooser(Gtk.FileChooserDialog):

    def __init__(self, window, mimes, path):

        Gtk.FileChooserDialog.__init__(self, parent=window,
            action=Gtk.FileChooserAction.OPEN,
            title="Seleccionar Icono . . .",
            buttons=[
                "Aceptar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])
        self.set_select_multiple(False)
        self.set_current_folder_uri("file://%s" % path)
        _filter = Gtk.FileFilter()
        _filter.set_name("Filtro")
        for m in mimes:
            _filter.add_mime_type(m)
        self.add_filter(_filter)
        self.connect("realize", self.__realize)
        self.set_size_request(640, 480)

    def __realize(self, widget):
        self.resize(640, 480)
