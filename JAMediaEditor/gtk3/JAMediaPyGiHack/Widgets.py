#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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
import commands
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

BASE_PATH = os.path.dirname(__file__)
ICONOS = os.path.join(BASE_PATH, "Iconos")

from Globales import get_dict
from Globales import get_separador
from Globales import get_boton


class Toolbar(Gtk.Toolbar):

    __gtype_name__ = 'PygiHackToolbar'

    __gsignals__ = {
    'import': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING)),
    'accion-menu': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_BOOLEAN)),
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "zoom": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    "accion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING)),
    "informe": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        item.set_expand(False)
        self.menu = Menu()
        self.menu.connect("import", self.__emit_import)
        self.menu.connect("accion-menu", self.__emit_accion_menu)
        self.menu.show()
        item.add(self.menu)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=10, expand=False), -1)

        item = Gtk.ToolItem()
        item.set_expand(True)
        self.toolbarbusquedas = ToolbarBusquedas()
        item.add(self.toolbarbusquedas)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(ICONOS, "Zoomout.svg")
        boton = get_boton(archivo, flip=False, pixels=18,
            tooltip_text="Alejar")
        boton.connect("clicked", self.__emit_zoom)
        self.insert(boton, -1)

        archivo = os.path.join(ICONOS, "Zoomin.svg")
        boton = get_boton(archivo, flip=False, pixels=18,
            tooltip_text="Acercar")
        boton.connect("clicked", self.__emit_zoom)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=10, expand=False), -1)

        archivo = os.path.join(ICONOS, "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=32, tooltip_text="Salir")
        boton.connect("clicked", self.__emit_salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        self.toolbarbusquedas.connect("accion", self.__re_emit_accion)
        self.toolbarbusquedas.connect("informe", self.__re_emit_informe)

        self.show_all()

    def __emit_zoom(self, widget):
        self.emit('zoom', widget.TOOLTIP)

    def __emit_salir(self, widget):
        self.emit('salir')

    def __emit_accion_menu(self, widget, menu, wid_lab, valor):
        self.emit("accion-menu", menu, wid_lab, valor)

    def __emit_import(self, widget, paquete, modulo):
        self.emit("import", paquete, modulo)

    def __re_emit_informe(self, widget):
        self.emit("informe")

    def __re_emit_accion(self, widget, accion, text):
        """
        Cuando se hace click en anterior y siguiente de toolbarbusquedas.
        """
        self.emit("accion", accion, text)

    def update(self, view):
        self.menu.update(view)

    def activar_busquedas(self, valor):
        self.toolbarbusquedas.activar(valor)


class ToolbarTry(Gtk.Statusbar):

    __gtype_name__ = 'PygiHackToolbarTry'

    def __init__(self):

        Gtk.Statusbar.__init__(self)
        self.show_all()

    def set_info(self, info):
        self.push(0, "Info: %s" % info)


class Menu(Gtk.MenuBar):
    """
    Toolbar Principal.
    """

    __gtype_name__ = 'PygiHackMenu'

    __gsignals__ = {
     'import': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING)),
    'accion-menu': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_BOOLEAN))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        _dict = get_dict()

        ### Items del Menú Abrir
        self.item_abrir = Gtk.MenuItem('Importar')
        menu_abrir = Gtk.Menu()
        self.item_abrir.set_submenu(menu_abrir)
        self.append(self.item_abrir)

        item = Gtk.MenuItem('python')
        menu_abrir.append(item)
        if _dict.get('python', False):
            m = Gtk.Menu()
            item.set_submenu(m)
            for key in _dict.get('python', []):
                i = Gtk.MenuItem(key)
                i.connect("activate", self.__emit_import, 'python')
                m.append(i)

        item = Gtk.MenuItem('python-gi')
        menu_abrir.append(item)
        if _dict.get('python-gi', False):
            m = Gtk.Menu()
            item.set_submenu(m)
            for key in _dict.get('python-gi', []):
                i = Gtk.MenuItem(key)
                i.connect("activate", self.__emit_import, 'python-gi')
                m.append(i)

        item = Gtk.MenuItem('Otros')
        menu_abrir.append(item)
        if _dict.get('Otros', False):
            m = Gtk.Menu()
            item.set_submenu(m)
            for key in _dict.get('Otros', []):
                i = Gtk.MenuItem(key)
                i.connect("activate", self.__emit_import, 'Otros')
                m.append(i)

        ### Items del Menú Ver
        item_ver = Gtk.MenuItem('Ver')
        menu_ver = Gtk.Menu()
        item_ver.set_submenu(menu_ver)
        self.append(item_ver)

        item = Gtk.MenuItem('Apis PyGiHack')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton1 = Gtk.RadioButton()
        boton1.set_active(False)
        hbox.pack_start(boton1, False, False, 0)
        label = Gtk.Label("Apis PyGiHack")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_menu2, "ver")
        menu_ver.append(item)
        self.show_all()

        item = Gtk.MenuItem('inspect1.0')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton2 = Gtk.RadioButton()
        boton2.set_active(True)
        boton2.join_group(boton1)
        hbox.pack_start(boton2, False, False, 0)
        label = Gtk.Label("Gstreamer - Inspect 1.0")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_menu2, "ver")
        menu_ver.append(item)

        self.show_all()

    def __emit_accion_menu(self, widget, menu):
        valor = not widget.get_children()[0].get_children()[0].get_active()
        widget.get_children()[0].get_children()[0].set_active(valor)
        label = widget.get_children()[0].get_children()[1]
        self.emit("accion-menu", menu, label.get_text(), valor)

    def __emit_accion_menu2(self, widget, menu):
        valor = not widget.get_children()[0].get_children()[0].get_active()
        if valor:
            widget.get_children()[0].get_children()[0].set_active(valor)
            label = widget.get_children()[0].get_children()[1]
            self.emit("accion-menu", menu, label.get_text(), valor)

    def __emit_import(self, widget, menu):
        disponible = False
        if menu == "python-gi":
            if widget.get_label() == "gi":
                ejecutable = os.path.join(
                    BASE_PATH, "SpyderHack", "Check.py")
            else:
                ejecutable = os.path.join(BASE_PATH,
                    "SpyderHack", "Gi_Check.py")
        elif menu == "python":
            ejecutable = os.path.join(BASE_PATH,
                "SpyderHack", "Check.py")
        elif menu == "Otros":
            ejecutable = os.path.join(BASE_PATH,
                "SpyderHack", "Check.py")
        else:
            return

        ret = commands.getoutput('python %s %s' % (
            ejecutable, widget.get_label()))

        if 'True' in ret:
            disponible = True
        else:
            disponible = False

        if disponible:
            self.emit("import", menu, widget.get_label())
        else:
            dialog = Gtk.Dialog(parent=self.get_toplevel(),
                flags=Gtk.DialogFlags.MODAL,
                buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

            dialog.set_border_width(15)
            dialog.vbox.pack_start(Gtk.Label(
                "%s no se Encuentra Disponible" % widget.get_label()),
                True, True, 0)

            dialog.vbox.show_all()
            dialog.run()
            dialog.destroy()
            widget.destroy()

    def __set_add_menu(self, widget):
        print "Agregar un Item en:", widget.get_label()

    def update(self, view):
        if view == "Gstreamer - Inspect 1.0":
            self.item_abrir.set_sensitive(False)
        elif view == "Apis PyGiHack":
            self.item_abrir.set_sensitive(True)


class ToolbarBusquedas(Gtk.EventBox):

    __gtype_name__ = 'JAMediaEditorToolbarBusquedas'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING)),
    "informe": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.set_border_width(5)

        self.activo = False

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.entry = Gtk.Entry()
        self.entry.show()
        self.entry.connect("changed", self.__check_sensitive)
        self.entry.connect("activate", self.__emit_accion_buscar)
        hbox.pack_start(self.entry, False, False, 0)

        self.anterior = get_boton(os.path.join(ICONOS, "go-next.svg"),
            pixels=18, tooltip_text="Buscar Anterior",
            rotacion=GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)
        self.anterior.connect("clicked", self.__emit_accion)
        hbox.pack_start(self.anterior, False, False, 0)

        self.siguiente = get_boton(os.path.join(ICONOS, "go-next.svg"),
            pixels=18, tooltip_text="Buscar Siguiente",
            rotacion=GdkPixbuf.PixbufRotation.CLOCKWISE)
        self.siguiente.connect("clicked", self.__emit_accion)
        hbox.pack_start(self.siguiente, False, False, 0)

        self.informe = get_boton(os.path.join(ICONOS, "document-new.svg"),
            pixels=18, tooltip_text="Obtener Estructura")
        self.informe.connect("clicked", self.__emit_informe)
        hbox.pack_start(self.informe, False, False, 0)

        self.add(hbox)
        self.show_all()

        self.anterior.set_sensitive(self.activo)
        self.siguiente.set_sensitive(self.activo)
        self.informe.set_sensitive(self.activo)
        self.set_sensitive(self.activo)

    def __emit_informe(self, widget):
        self.emit("informe")

    def __emit_accion_buscar(self, widget):
        text = self.entry.get_text().strip()
        if text:
            self.emit("accion", "Buscar Siguiente", text)

    def __emit_accion(self, widget):
        """
        Cuando se hace click en anterior y siguiente.
        """
        text = self.entry.get_text().strip()
        if text:
            self.emit("accion", widget.TOOLTIP, text)

    def __check_sensitive(self, entry):
        """
        Cuando cambia el texto a buscar.
        """
        if self.entry.get_text().strip():
            self.anterior.set_sensitive(True)
            self.siguiente.set_sensitive(True)
            #self.emit("buscar", self.entry.get_text().strip())
        else:
            self.anterior.set_sensitive(False)
            self.siguiente.set_sensitive(False)

    def activar(self, valor):
        self.activo = valor
        if not self.activo:
            self.entry.set_text("")
        self.informe.set_sensitive(self.activo)
        self.set_sensitive(self.activo)
