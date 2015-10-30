#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaExplorer.py por:
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
import sys
import gtk

from sugar.activity import activity

from Toolbars import ToolbarSalir
from Toolbars import Toolbar
from Toolbars import ToolbarTry
from Toolbars import ToolbarAccion
from Navegador import Navegador

from JAMFileSystem import get_tamanio
from JAMFileSystem import describe_archivo
from JAMFileSystem import describe_uri
from JAMFileSystem import describe_acceso_uri
from JAMFileSystem import borrar

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONOS = os.path.join(BASE_PATH, "Iconos")


class Ventana(activity.Activity):

    def __init__(self, handle):

        activity.Activity.__init__(self, handle, False)

        self.set_title("JAMediaExplorer")
        self.set_icon_from_file(os.path.join(ICONOS, "JAMediaExplorer.svg"))
        self.modify_bg(0, gtk.gdk.Color(65000, 65000, 65000))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_border_width(3)

        vbox = gtk.VBox()

        self.toolbar = Toolbar()
        self.toolbar_accion = ToolbarAccion()
        self.toolbar_salir = ToolbarSalir()
        self.navegador = Navegador()
        self.toolbar_try = ToolbarTry()

        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(self.toolbar_accion, False, False, 0)
        vbox.pack_start(self.toolbar_salir, False, False, 0)
        vbox.pack_start(self.navegador, True, True, 0)
        vbox.pack_end(self.toolbar_try, False, False, 0)

        self.set_canvas(vbox)
        self.show_all()
        self.realize()

        self.toolbar_accion.hide()
        self.toolbar_salir.hide()

        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar.connect('accion_ver', self.__set_accion)
        self.toolbar_accion.connect('borrar', self.__ejecutar_borrar)
        self.toolbar_salir.connect('salir', self.__salir)
        self.connect("delete-event", self.__salir)

        self.navegador.connect('info', self.__get_info)
        self.navegador.connect('borrar', self.__set_borrar)

    def __set_accion(self, widget, accion, valor):
        """
        Cuando se hace click en ver ocultos del menu.
        """
        self.get_toplevel().set_sensitive(False)
        self.navegador.notebookdirectorios.recargar(valor)
        self.get_toplevel().set_sensitive(True)

    def __ejecutar_borrar(self, widget, direccion, modelo, iter_):
        """
        Ejecuta borrar un archivo o directorio.
        """
        self.get_toplevel().set_sensitive(False)
        if borrar(direccion):
            modelo.remove(iter_)
            self.navegador.notebookdirectorios.copiando = False
            self.navegador.notebookdirectorios.cortando = False
        self.get_toplevel().set_sensitive(True)

    def __set_borrar(self, widget, direccion, modelo, iter_):
        """
        Setea borrar un archivo en toolbaraccion.
        """
        self.toolbar_salir.hide()
        self.toolbar_accion.set_accion(direccion, modelo, iter_)

    def __confirmar_salir(self, widget=None, senial=None):
        self.toolbar_accion.hide()
        self.toolbar_salir.run("JAMediaExplorer")

    def __ocultar(self, objeto):
        if objeto.get_visible():
            objeto.hide()

    def __mostrar(self, objeto):
        if not objeto.get_visible():
            objeto.show()

    def __get_items(self, directorio, tipo):
        if not os.path.exists(directorio) \
            or not os.path.isdir(directorio):
                return []
        items = []
        for archivo in os.listdir(directorio):
            path = os.path.join(directorio, archivo)
            descripcion = describe_archivo(path)
            if tipo in descripcion and not 'iso' in descripcion:
                items.append([archivo, path])
        return items

    def __get_info(self, widget, path):
        """
        Recibe el path seleccionado en la estructura
        de directorios, obtiene información sobre el mismo
        y la pasa a infowidget para ser mostrada.
        """
        if not path:
            return
        if not os.path.exists(path):
            return

        self.toolbar_try.label.set_text(path)
        # FIXME: Falla si se movió y no se actualiza
        unidad, directorio, archivo, enlace = describe_uri(path)
        lectura, escritura, ejecucion = describe_acceso_uri(path)

        texto = ""
        typeinfo = ""

        if enlace:
            texto = "Enlace.\n"
        else:
            if directorio:
                texto = "Directorio.\n"

            elif archivo:
                texto = "Archivo.\n"
                texto += "Tipo:\n"

                for dato in describe_archivo(path).split(";"):
                    texto += "\t%s\n" % (dato.strip())
                    typeinfo += dato

                texto += "Tamaño:\n"
                texto += "\t%s bytes\n" % (get_tamanio(path))

        texto += "Permisos: \n"
        texto += "\tLactura: %s\n" % (lectura)
        texto += "\tEscritura: %s\n" % (escritura)
        texto += "\tEjecución: %s\n" % (ejecucion)

        self.navegador.infowidget.set_info(texto, typeinfo)

    def __salir(self, widget=None, senial=None):
        notebook = self.navegador.notebookdirectorios
        paginas = notebook.get_n_pages()
        pags = notebook.get_children()
        for indice in range(paginas):
            pags[indice].get_child().new_handle(False)
        sys.exit(0)
        gtk.main_quit()
