#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GLib

BASE_PATH = os.path.dirname(__file__)

#import JAMediaObjects
#from JAMediaObjects.JAMediaWidgets import JAMediaButton

from Globales import get_color
from Globales import get_separador
from Globales import get_boton


class My_FileChooser(Gtk.FileChooserDialog):
    """
    Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio.
    """

    __gtype_name__ = 'My_FileChooser'

    __gsignals__ = {
    'archivos-seleccionados': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, parent=None, action=None,
        filter=[], title=None, path=None, mime=[]):

        Gtk.FileChooserDialog.__init__(self,
            title=title,
            parent=parent,
            action=action,
            flags=Gtk.DialogFlags.MODAL)

        if not path:
            path = "file:///media"

        self.set_current_folder_uri(path)

        self.set_select_multiple(True)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        boton_abrir_directorio = Gtk.Button("Abrir")
        boton_seleccionar_todo = Gtk.Button("Seleccionar Todos")
        boton_salir = Gtk.Button("Salir")

        boton_salir.connect("clicked", self.__salir)
        boton_abrir_directorio.connect("clicked",
            self.__abrir_directorio)
        boton_seleccionar_todo.connect("clicked",
            self.__seleccionar_todos_los_archivos)

        hbox.pack_end(boton_salir, True, True, 5)
        hbox.pack_end(boton_seleccionar_todo, True, True, 5)
        hbox.pack_end(boton_abrir_directorio, True, True, 5)

        self.set_extra_widget(hbox)

        hbox.show_all()

        if filter:
            filtro = Gtk.FileFilter()
            filtro.set_name("Filtro")

            for fil in filter:
                filtro.add_pattern(fil)

            self.add_filter(filtro)

        elif mime:
            filtro = Gtk.FileFilter()
            filtro.set_name("Filtro")

            for mi in mime:
                filtro.add_mime_type(mi)

            self.add_filter(filtro)

        self.add_shortcut_folder_uri("file:///media/")

        self.resize(400, 300)

        self.connect("file-activated", self.__file_activated)

    def __file_activated(self, widget):
        """
        Cuando se hace doble click sobre un archivo.
        """

        self.emit('archivos-seleccionados', self.get_filenames())

        self.__salir(None)

    def __seleccionar_todos_los_archivos(self, widget):

        self.select_all()

    def __abrir_directorio(self, widget):
        """
        Manda una señal con la lista de archivos
        seleccionados para cargarse en el reproductor.
        """

        self.emit('archivos-seleccionados', self.get_filenames())
        self.__salir(None)

    def __salir(self, widget):

        self.destroy()


class MenuList(Gtk.Menu):
    """
    Menu con opciones para operar sobre el archivo o
    el streaming seleccionado en la lista de reproduccion
    al hacer click derecho sobre él.
    """

    __gtype_name__ = 'MenuList'

    __gsignals__ = {
    'accion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        Gtk.Menu.__init__(self)

        iter = modelo.get_iter(path)
        uri = modelo.get_value(iter, 2)

        quitar = Gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Quitar")

        from JAMediaObjects.JAMFileSystem import describe_acceso_uri
        from Globales import get_my_files_directory
        from Globales import get_data_directory
        from Globales import stream_en_archivo

        if describe_acceso_uri(uri):
            lectura, escritura, ejecucion = describe_acceso_uri(uri)

            if lectura and os.path.dirname(uri) != get_my_files_directory():
                copiar = Gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__set_accion,
                    widget, path, "Copiar")

            if escritura and os.path.dirname(uri) != get_my_files_directory():
                mover = Gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__set_accion,
                    widget, path, "Mover")

            if escritura:
                borrar = Gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.__set_accion,
                    widget, path, "Borrar")

        else:
            borrar = Gtk.MenuItem("Borrar Streaming")
            self.append(borrar)
            borrar.connect_object("activate", self.__set_accion,
                widget, path, "Borrar")

            listas = [
                os.path.join(get_data_directory(), "JAMediaTV.JAMedia"),
                os.path.join(get_data_directory(), "JAMediaRadio.JAMedia"),
                os.path.join(get_data_directory(), "MisRadios.JAMedia"),
                os.path.join(get_data_directory(), "MisTvs.JAMedia")
                ]

            if (stream_en_archivo(uri, listas[0]) and \
                not stream_en_archivo(uri, listas[3])) or \
                (stream_en_archivo(uri, listas[1]) and \
                not stream_en_archivo(uri, listas[2])):

                copiar = Gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__set_accion,
                    widget, path, "Copiar")

                mover = Gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__set_accion,
                    widget, path, "Mover")

            grabar = Gtk.MenuItem("Grabar")
            self.append(grabar)
            grabar.connect_object("activate", self.__set_accion,
                widget, path, "Grabar")

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

        iter = widget.modelo.get_iter(path)
        self.emit('accion', widget, accion, iter)

'''
class WidgetEfecto_en_Pipe(JAMediaButton):
    """
    Representa un efecto agregado al pipe de JAMediaVideo.
    Es simplemente un objeto gráfico que se agrega debajo del
    visor de video, para que el usuario tenga una referencia de
    los efectos que ha agregado y en que orden se encuentran.
    """

    __gtype_name__ = 'WidgetEfecto_en_Pipe'

    def __init__(self):

        JAMediaButton.__init__(self)

        self.show_all()

        self.set_colores(
            colornormal=get_color("NEGRO"),
            colorselect=get_color("NEGRO"),
            colorclicked=get_color("NEGRO"))

        self.modify_bg(0, self.colornormal)

    def seleccionar(self):
        pass

    def des_seleccionar(self):
        pass
'''

class DialogoDescarga(Gtk.Dialog):

    __gtype_name__ = 'DialogoDescarga'

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL)

        self.set_border_width(15)

        label = Gtk.Label("*** Descargando Streamings de JAMedia ***")
        label.show()

        self.vbox.pack_start(label, True, True, 5)

        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):

        GLib.timeout_add(500, self.__descargar)

    def __descargar(self):

        # FIXME: Agregar control de conexión para evitar errores.
        from Globales import get_streaming_default
        get_streaming_default()

        self.destroy()


class Credits(Gtk.Dialog):

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_decorated(False)
        self.set_border_width(15)

        imagen = Gtk.Image()
        imagen.set_from_file(
            os.path.join(BASE_PATH,
                "Iconos", "JAMediaCredits.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class Help(Gtk.Dialog):

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_decorated(False)
        self.set_border_width(15)

        tabla1 = Gtk.Table(columns=5, rows=2, homogeneous=False)

        vbox = Gtk.HBox()
        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.anterior = get_boton(
            archivo, flip=True,
            pixels=24,
            tooltip_text="Anterior")
        self.anterior.connect("clicked", self.__switch)
        self.anterior.show()
        vbox.pack_start(self.anterior, False, False, 0)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.siguiente = get_boton(
            archivo,
            pixels=24,
            tooltip_text="Siguiente")
        self.siguiente.connect("clicked", self.__switch)
        self.siguiente.show()
        vbox.pack_end(self.siguiente, False, False, 0)

        tabla1.attach_defaults(vbox, 0, 5, 0, 1)

        self.helps = []

        for x in range(1, 5):
            help = Gtk.Image()
            help.set_from_file(
                os.path.join(BASE_PATH,
                    "Iconos", "JAMedia-help%s.png" % x))
            tabla1.attach_defaults(help, 0, 5, 1, 2)

            self.helps.append(help)

        self.vbox.pack_start(tabla1, True, True, 0)
        self.vbox.show_all()

        self.__switch(None)

    def __ocultar(self, objeto):

        if objeto.get_visible():
            objeto.hide()

    def __switch(self, widget):

        if not widget:
            map(self.__ocultar, self.helps[1:])
            self.anterior.hide()
            self.helps[0].show()

        else:
            index = self.__get_index_visible()
            helps = list(self.helps)
            new_index = index

            if widget == self.siguiente:
                if index < len(self.helps) - 1:
                    new_index += 1

            elif widget == self.anterior:
                if index > 0:
                    new_index -= 1

            helps.remove(helps[new_index])
            map(self.__ocultar, helps)
            self.helps[new_index].show()

            if new_index > 0:
                self.anterior.show()

            else:
                self.anterior.hide()

            if new_index < self.helps.index(self.helps[-1]):
                self.siguiente.show()

            else:
                self.siguiente.hide()

    def __get_index_visible(self):

        for help in self.helps:
            if help.get_visible():
                return self.helps.index(help)
