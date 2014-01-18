#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMedia.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(
    PATH, "JAMediaConverter", "Estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)

GObject.threads_init()


def get_data(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    """

    import commands

    datos = commands.getoutput(
        'file -ik %s%s%s' % ("\"", archivo, "\""))

    retorno = ""

    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)

    return retorno


class Ventana(Gtk.Window):

    __gtype_name__ = 'Ventana'

    def __init__(self):

        super(Ventana, self).__init__()

        self.set_title("JAMedia Converter")

        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaConvert.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        from JAMediaConverter.Widgets import Toolbar
        from JAMediaObjects.JAMediaWidgets import Lista
        from JAMediaConverter.WidgetTareas import WidgetTareas

        vbox = Gtk.VBox()
        base_panel = Gtk.HPaned()
        vbox2 = Gtk.VBox()

        self.toolbar = Toolbar()
        self.lista = Lista()
        self.widgettareas = WidgetTareas()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.lista)

        base_panel.pack1(scroll, resize=False, shrink=False)
        base_panel.pack2(vbox2, resize=False, shrink=False)

        vbox.pack_start(
            self.toolbar, False, False, 0)
        vbox.pack_start(
            base_panel, True, True, 0)

        vbox2.pack_start(self.widgettareas, True, True, 0)

        self.add(vbox)

        self.show_all()
        self.realize()

        self.toolbar.connect(
            'salir', self.__salir)
        self.toolbar.connect(
            'load', self.__load_files)
        self.lista.connect(
            "nueva-seleccion", self.__selecction_file)
        self.widgettareas.connect(
            'copy_tarea', self.__copy_tarea)

        self.connect("delete-event", self.__salir)

    def __copy_tarea(self, widget, tarea):
        """
        Extiende la tarea configurada a todos
        los archivos en la lista, siempre que estos
        sean del mismo tipo (audio o video) y si su formato
        actual lo permite (ejemplo: no se convierte mp3 a mp3).
        """

        model = self.lista.get_model()
        item = model.get_iter_first()

        it = None

        while item:
            it = item
            item = model.iter_next(item)

            if it:
                path = model.get_value(it, 2)
                widtarea = self.widgettareas.tareas.get(path, False)

                if not widtarea:
                    self.widgettareas.go_tarea(path)

        for key in self.widgettareas.tareas.keys():
            widtarea = self.widgettareas.tareas[key]

            if not widtarea.estado:
                widtarea.setear(tarea)

    def __selecction_file(self, widget, path):

        self.widgettareas.go_tarea(path)

    def __load_files(self, widget, lista):
        """
        Agrega archivos a la lista a procesar.
        """

        items = []

        for origen in lista:
            if os.path.isdir(origen):
                for archivo in os.listdir(origen):
                    arch = os.path.join(origen, archivo)
                    datos = get_data(arch)

                    if 'audio' in datos or \
                        'video' in datos or \
                        'application/ogg' in datos or \
                        'application/octet-stream' in datos:
                        items.append([os.path.basename(arch), arch])

            elif os.path.isfile(origen):
                datos = get_data(origen)

                if 'audio' in datos or \
                    'video' in datos or \
                    'application/ogg' in datos or \
                    'application/octet-stream' in datos:
                    items.append([os.path.basename(origen), origen])

        self.lista.limpiar()

        if items:
            self.lista.agregar_items(items)

    def __salir(self, widget=None, senial=None):

        for key in self.widgettareas.tareas.keys():
            widtarea = self.widgettareas.tareas[key]
            widtarea.stop()

        import sys
        sys.exit(0)


if __name__ == "__main__":
    Ventana()
    Gtk.main()
