#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay

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
from gi.repository import GObject
from gi.repository import GLib
from Widgets import Toolbar
from BaseBox import BaseBox
from InformeWidget import InformeWidget

BASE_PATH = os.path.dirname(__file__)


class JAMediaPyGiHack(Gtk.Box):

    __gtype_name__ = 'JAMediaPyGiHack'

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "abrir": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.toolbar = Toolbar()
        self.pack_start(self.toolbar, False, False, 0)

        self.basebox = BaseBox()
        self.pack_start(self.basebox, True, True, 0)

        self.informewidget = False

        # FIXME: Activar para obtener informe de módulos
        #self.connect("realize", self.__realize)
        self.show_all()

        self.toolbar.connect("import", self.__import)
        self.toolbar.connect("accion-menu", self.__set_accion)
        self.toolbar.connect("salir", self.__emit_salir)
        self.toolbar.connect("zoom", self.__zoom)
        self.toolbar.connect("accion", self.__buscar_mas)
        self.toolbar.connect("informe", self.__informar)

        self.basebox.connect("update", self.__update)
        self.basebox.connect('abrir', self.__open_file)
        self.basebox.connect("nobusquedas", self.__desactivar_busquedas)
        
    """
    def __realize(self, widget):
        GLib.timeout_add(1000, self.__informe_pygihack)

    def __informe_pygihack(self):
        self.get_toplevel().set_sensitive(False)
        dialog = Gtk.Dialog(parent=self.get_toplevel(),
        flags=Gtk.DialogFlags.MODAL,
        buttons=["Aceptar", Gtk.ResponseType.ACCEPT])
        dialog.set_border_width(15)
        dialog.set_size_request(250, 400)
        textview = Gtk.TextView()
        textview.set_editable(False)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(textview)
        textview.get_buffer().set_text(self.toolbar.menu.informe)
        dialog.vbox.pack_start(scroll, True, True, 0)
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()
        self.get_toplevel().set_sensitive(True)
        return False
    """
    
    def __open_file(self, widget, modulo_path):
        self.emit("abrir", modulo_path)

    def __zoom(self, widget, zoom):
        self.basebox.zoom(zoom)

    def __informar(self, widget):
        """
        Abre nueva lengueta en Workpanel con la información de Introspección
        del archivo seleccionado.
        """
        if self.informewidget:
            self.informewidget.destroy()
        self.informewidget = InformeWidget(self.get_toplevel())
        text = self.basebox.get_estructura()
        self.informewidget.setting(text)

    def __buscar_mas(self, widget, accion, text):
        self.basebox.buscar_mas(accion, text)

    def __emit_salir(self, widget):
        self.emit('salir')

    def __update(self, widget, view):
        self.toolbar.update(view)
        self.toolbar.activar_busquedas(self.basebox.check_busquedas())

    def __desactivar_busquedas(self, widget):
        self.toolbar.activar_busquedas(False)

    def __set_accion(self, widget, menu, wid_lab, valor):
        self.basebox.set_accion(menu, wid_lab, valor)

    def __import(self, widget, paquete, modulo):
        self.basebox.import_modulo(paquete, modulo)


class Ventana(Gtk.Window):

    __gtype_name__ = 'VentanaJAMediaPyGiHack'

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("JAMediaPygiHack")

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.maximize()
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        jamediapygihack = JAMediaPyGiHack()
        self.add(jamediapygihack)

        self.show_all()
        self.realize()

        jamediapygihack.connect("salir", self.__salir)
        self.connect("delete-event", self.__salir)

    def __salir(self, widget=None, senial=None):
        import sys
        sys.exit(0)


if __name__ == "__main__":
    Ventana()
    Gtk.main()
