#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaEditor.py por:
#       Cristian García     <cristian99garcia@gmail.com>
#       Ignacio Rodriguez   <nachoel01@gmail.com>
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

'''
Cambios en setup.py:
    GTK;Development;IDE

import os

mime_path = os.path.join(os.environ["HOME"],
    ".local/share/mime/packages/")

if not os.path.exists(mime_path):
    os.mkdir(mime_path)

commands.getoutput("cp jamediaeditor.xml %s" % mime_path)
commands.getoutput('update-mime-database %s' % os.path.join(
    os.environ["HOME"], ".local/share/mime/"))
commands.getoutput('chmod 755 %s' % os.path.join(
    os.environ["HOME"], ".local/share/mime/jamediaeditor.xml"))
'''

import os

from gi.repository import Gtk
from gi.repository import Gdk

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

home = os.environ["HOME"]
BatovideWorkSpace = os.path.join(
    home, 'BatovideWorkSpace')

if not os.path.exists(BatovideWorkSpace):
    os.mkdir(BatovideWorkSpace)

PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(
    PATH, "JAMediaEditor", "Estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)


class JAMediaEditor(Gtk.Window):
    """
    Gtk.Window
        Gtk.VBox
            JAMediaEditor.Widgets.Menu
            JAMediaEditor.BasePanel.BasePanel
    """

    __gtype_name__ = 'WindowJAMediaEditor'

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("JAMediaEditor")

        self.set_icon_from_file(os.path.join(
            JAMediaObjectsPath, "Iconos",
            "JAMediaEditor2.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.CENTER)

        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)

        base_widget = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL)

        from JAMediaEditor.Widgets import Menu
        from JAMediaEditor.BasePanel import BasePanel
        from JAMediaEditor.Toolbars import ToolbarEstado
        from JAMediaPyGiHack.JAMediaPyGiHack import JAMediaPyGiHack

        self.menu = Menu(accel_group)
        self.base_panel = BasePanel()
        self.toolbar_estado = ToolbarEstado()
        self.jamediapygihack = JAMediaPyGiHack()

        base_widget.pack_start(
            self.menu, False, False, 0)
        base_widget.pack_start(
            self.base_panel, True, True, 0)
        base_widget.pack_start(
            self.jamediapygihack, True, True, 0)
        base_widget.pack_start(
            self.toolbar_estado, False, False, 0)

        self.add(base_widget)

        self.show_all()
        self.maximize()

        self.jamediapygihack.hide()

        self.menu.connect('accion_ver',
            self.__ejecutar_accion_ver)
        self.menu.connect('accion_codigo',
            self.__ejecutar_accion_codigo)
        self.menu.connect('accion_proyecto',
            self.__ejecutar_accion_proyecto)
        self.menu.connect('accion_archivo',
            self.__ejecutar_accion_archivo)
        self.menu.connect('run_jamediapygihack',
            self.__run_jamediapygihack)
        self.jamediapygihack.connect('salir',
            self.__run_editor)

        self.base_panel.connect("update",
            self.__set_toolbar_archivo_and_menu)
        self.base_panel.connect("proyecto_abierto",
            self.__set_toolbar_proyecto_and_menu)
        self.base_panel.connect("ejecucion",
            self.__set_toolbars_ejecucion)

        self.connect("delete-event", self.__exit)

    def __run_editor(self, widget):

        self.jamediapygihack.hide()
        self.menu.show()
        self.base_panel.show()

    def __run_jamediapygihack(self, widget):

        self.menu.hide()
        self.base_panel.hide()
        self.jamediapygihack.show()

    def __exit(self, widget=None, event=None):

        Gtk.main_quit()
        import sys
        sys.exit(0)

    def __ejecutar_accion_codigo(self, widget, accion):
        """
        Cuando se hace click en una opción del menú codigo.
        """

        self.base_panel.set_accion_codigo(widget, accion)

    def __ejecutar_accion_ver(self, widget, accion, valor):
        """
        Cuando se hace click en una opción del menú ver.
        """

        self.base_panel.set_accion_ver(widget, accion, valor)

    def __ejecutar_accion_archivo(self, widget, accion):
        """
        Cuando se hace click en una opción del menú que
        afecta al archivo seleccionado.
        """

        self.base_panel.set_accion_archivo(widget, accion)

    def __ejecutar_accion_proyecto(self, widget, accion):
        """
        Cuando se hace click en una opción del menú proyecto.
        """

        self.base_panel.set_accion_proyecto(widget, accion)

    def __set_toolbar_archivo_and_menu(self, widget, dict):

        self.menu.update_archivos(dict)
        self.base_panel.toolbararchivo.update(dict)

        info = {
            'renglones': dict['renglones'],
            'caracteres': dict['caracteres'],
            'archivo': dict['archivo'],
            }

        self.toolbar_estado.set_info(info)

    def __set_toolbar_proyecto_and_menu(self, widget, valor):
        """
        Activa y desactiva las opciones de proyecto en la
        toolbar y menú correspondiente cuando se abre o se
        cierra un proyecto.
        """

        self.base_panel.workpanel.detener_ejecucion()

        self.menu.activar_proyecto(valor)
        self.base_panel.toolbarproyecto.activar_proyecto(valor)

        ### Ejecuciones
        self.base_panel.toolbararchivo.activar_ejecucion(False)

        if valor:
            self.base_panel.toolbarproyecto.activar_ejecucion(False)

        else:
            self.base_panel.toolbarproyecto.activar_ejecucion(None)

    def __set_toolbars_ejecucion(self, widget, tipo, valor):
        """
        Cuando se ejecuta un archivo o proyecto, se
        actualizan las toolbars correspondientes.
        """

        if not valor:
            self.base_panel.toolbararchivo.activar_ejecucion(False)

            proyecto = self.base_panel.proyecto
            if proyecto:
                self.base_panel.toolbarproyecto.activar_ejecucion(False)

            else:
                self.base_panel.toolbarproyecto.activar_ejecucion(None)

        elif valor:
            if tipo == "proyecto":
                ### Se está ejecutando proyecto.
                self.base_panel.toolbararchivo.activar_ejecucion(None)
                self.base_panel.toolbarproyecto.activar_ejecucion(True)

            elif tipo == "archivo":
                ### Se está ejecutando archivo.
                self.base_panel.toolbarproyecto.activar_ejecucion(None)
                self.base_panel.toolbararchivo.activar_ejecucion(True)


if __name__ == "__main__":
    JAMediaEditor()
    Gtk.main()
