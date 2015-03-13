#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Menu.py por:
#     Cristian García    <cristian99garcia@gmail.com>
#     Ignacio Rodriguez  <nachoel01@gmail.com>
#     Flavio Danesse     <fdanesse@gmail.com>

# This program is free software; you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110 - 1301 USA

import os
import commands

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

from Widgets2 import Credits
from Help.Menu import ItemMenuInstaladores

BASE_PATH = os.path.dirname(__file__)


class Menu(Gtk.MenuBar):
    """
    Toolbar Principal.
    """

    __gtype_name__ = 'JAMediaEditorMenu'

    __gsignals__ = {
    'accion_proyecto': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    'accion_archivo': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    'accion_ver': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN)),
    'accion_codigo': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    'run_jamediapygihack': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self, accel_group):

        Gtk.MenuBar.__init__(self)

        self.dict_archivo = {}
        self.dict_proyecto = {}

        item_proyectos = Gtk.MenuItem('Proyecto')
        item_archivos = Gtk.MenuItem('Archivo')
        item_edicion = Gtk.MenuItem('Edición')
        item_ver = Gtk.MenuItem('Ver')
        item_codigo = Gtk.MenuItem('Código')
        item_ayuda = Gtk.MenuItem('Ayuda')

        menu_proyectos = Gtk.Menu()
        menu_archivos = Gtk.Menu()
        menu_edicion = Gtk.Menu()
        menu_ver = Gtk.Menu()
        menu_codigo = Gtk.Menu()
        menu_ayuda = Gtk.Menu()

        item_proyectos.set_submenu(menu_proyectos)
        item_archivos.set_submenu(menu_archivos)
        item_edicion.set_submenu(menu_edicion)
        item_ver.set_submenu(menu_ver)
        item_codigo.set_submenu(menu_codigo)
        item_ayuda.set_submenu(menu_ayuda)

        self.append(item_proyectos)
        self.append(item_archivos)
        self.append(item_edicion)
        self.append(item_ver)
        self.append(item_codigo)
        self.append(item_ayuda)

        # Items del Menú Proyectos
        item = Gtk.MenuItem('Nuevo . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Nuevo Proyecto")
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('N'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Abrir . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Abrir Proyecto")
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('O'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Editar . . .')
        item.connect("activate",
            self.__emit_accion_proyecto, "Editar Proyecto")
        self.dict_proyecto["Editar Proyecto"] = item
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('E'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Cerrar')
        item.connect("activate",
            self.__emit_accion_proyecto, "Cerrar Proyecto")
        self.dict_proyecto["Cerrar Proyecto"] = item
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('W'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Guardar')
        item.connect("activate",
            self.__emit_accion_proyecto, "Guardar Proyecto")
        self.dict_proyecto["Guardar Proyecto"] = item
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('S'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Construir . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Construir")
        self.dict_proyecto["Construir"] = item
        menu_proyectos.append(item)

        # Items del Menú Archivos
        item = Gtk.MenuItem('Nuevo')
        item.connect("activate", self.__emit_accion_archivo, "Nuevo Archivo")
        menu_archivos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('N'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Abrir . . .')
        item.connect("activate", self.__emit_accion_archivo, "Abrir Archivo")
        menu_archivos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('O'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Guardar')
        item.connect("activate", self.__emit_accion_archivo, "Guardar Archivo")
        menu_archivos.append(item)
        self.dict_archivo['Guardar'] = item
        item.add_accelerator("activate", accel_group,
            ord('S'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Guardar Como ...')
        item.connect("activate", self.__emit_accion_archivo, "Guardar Como")
        menu_archivos.append(item)

        # Items del Menú Edición
        item = Gtk.MenuItem('Deshacer')
        item.connect("activate", self.__emit_accion_archivo, "Deshacer")
        menu_edicion.append(item)
        self.dict_archivo['Deshacer'] = item
        item.add_accelerator("activate", accel_group,
            ord('Z'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Rehacer')
        item.connect("activate", self.__emit_accion_archivo, "Rehacer")
        menu_edicion.append(item)
        self.dict_archivo['Rehacer'] = item
        item.add_accelerator("activate", accel_group,
            ord('Z'), Gdk.ModifierType.CONTROL_MASK |
            Gdk.ModifierType.SHIFT_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Cortar')
        item.connect("activate", self.__emit_accion_archivo, "Cortar")
        menu_edicion.append(item)
        self.dict_archivo['Cortar'] = item
        item.add_accelerator("activate", accel_group,
            ord('X'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Copiar')
        item.connect("activate", self.__emit_accion_archivo, "Copiar")
        menu_edicion.append(item)
        self.dict_archivo['Copiar'] = item
        item.add_accelerator("activate", accel_group,
            ord('C'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Pegar')
        item.connect("activate", self.__emit_accion_archivo, "Pegar")
        self.dict_archivo['Pegar'] = item
        menu_edicion.append(item)
        item.add_accelerator("activate", accel_group,
            ord('V'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Seleccionar Todo')
        item.connect("activate",
            self.__emit_accion_archivo, "Seleccionar Todo")
        self.dict_archivo['Seleccionar Todo'] = item
        menu_edicion.append(item)
        item.add_accelerator("activate", accel_group,
            ord('A'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        # Items del menú Ver
        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()
        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.CheckButton()
        button.set_active(True)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("Numeros de línea")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_ver, "Numeracion")
        menu_ver.append(item)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()
        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.CheckButton()
        button.set_active(False)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("Panel inferior")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_ver, "Panel inferior")
        menu_ver.append(item)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()
        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.CheckButton()
        button.set_active(True)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("Panel lateral")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_ver, "Panel lateral")
        menu_ver.append(item)

        # Items del Menú Código
        item = Gtk.MenuItem('Aumentar')
        item.connect("activate", self.__emit_accion_codigo, "Aumentar")
        self.dict_archivo['Aumentar'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord("+"), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Disminuir')
        item.connect("activate", self.__emit_accion_codigo, "Disminuir")
        self.dict_archivo['Disminuir'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('-'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Formato de Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Formato")
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('T'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Identar')
        item.connect("activate", self.__emit_accion_codigo, "Identar")
        self.dict_archivo['Identar'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('I'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('De Identar')
        item.connect("activate", self.__emit_accion_codigo, "De Identar")
        self.dict_archivo['De Identar'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('I'), Gdk.ModifierType.CONTROL_MASK |
            Gdk.ModifierType.SHIFT_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Buscar Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Buscar Texto")
        self.dict_archivo['Buscar Texto'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('B'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Reemplazar Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Reemplazar Texto")
        self.dict_archivo['Reemplazar Texto'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('R'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Chequear sintaxis')
        item.connect("activate", self.__emit_accion_codigo, "Chequear")
        self.dict_archivo['Chequear'] = item
        menu_codigo.append(item)

        # Items del Menú Ayuda
        item = Gtk.MenuItem('Créditos')
        item.connect("activate", self.__run_about)
        menu_ayuda.append(item)

        item = Gtk.MenuItem('JAMediaPyGiHack')
        item.connect("activate", self.__emit_run_jamediapygihack)
        menu_ayuda.append(item)

        item = Gtk.SeparatorMenuItem()
        menu_ayuda.append(item)

        # Ayuda Sobre Construcción de Instaladores
        item = ItemMenuInstaladores()
        item.connect("help", self.__emit_help)
        menu_ayuda.append(item)

        self.show_all()

    def __emit_help(self, widget, text):
        self.emit("help", text)

    def __emit_run_jamediapygihack(self, widget):
        self.emit('run_jamediapygihack')

    def __run_about(self, widget):
        dialog = Credits(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __emit_accion_codigo(self, widget, accion):
        self.emit('accion_codigo', accion)

    def __emit_accion_ver(self, widget, accion):
        valor = not widget.get_children()[0].get_children()[0].get_active()
        widget.get_children()[0].get_children()[0].set_active(valor)
        self.emit('accion_ver', accion, valor)

    def __emit_accion_archivo(self, widget, accion):
        self.emit('accion_archivo', accion)

    def __emit_accion_proyecto(self, widget, accion):
        self.emit('accion_proyecto', accion)

    def __activar(self, option):
        if not option.get_sensitive():
            option.set_sensitive(True)

    def __desactivar(self, option):
        if option.get_sensitive():
            option.set_sensitive(False)

    def activar_proyecto(self, sensitive):
        # Activa o desactiva opciones.
        if sensitive:
            map(self.__activar, self.dict_proyecto.values())
        else:
            map(self.__desactivar, self.dict_proyecto.values())

    def update_archivos(self, _dict):
        # Activa o desactiva opciones.
        activar = []
        desactivar = []

        if _dict['rehacer']:
            activar.append(self.dict_archivo['Rehacer'])
        else:
            desactivar.append(self.dict_archivo['Rehacer'])

        if _dict['deshacer']:
            activar.append(self.dict_archivo['Deshacer'])
        else:
            desactivar.append(self.dict_archivo['Deshacer'])

        if _dict['modificado']:
            activar.append(self.dict_archivo['Guardar'])
        else:
            desactivar.append(self.dict_archivo['Guardar'])

        if _dict['clipboard_texto']:
            activar.append(self.dict_archivo['Pegar'])
        else:
            desactivar.append(self.dict_archivo['Pegar'])

        if _dict['texto_seleccionado']:
            activar.extend([
                self.dict_archivo['Cortar'],
                self.dict_archivo['Copiar'],
                ])
        else:
            desactivar.extend([
                self.dict_archivo['Cortar'],
                self.dict_archivo['Copiar'],
                ])

        if _dict['tiene_texto']:
            activar.extend([
                self.dict_archivo['Identar'],
                self.dict_archivo['De Identar'],
                self.dict_archivo['Buscar Texto'],
                self.dict_archivo['Reemplazar Texto'],
                self.dict_archivo['Seleccionar Todo'],
                self.dict_archivo['Chequear'],
                self.dict_archivo['Disminuir'],
                self.dict_archivo['Aumentar'],
                ])
        else:
            desactivar.extend([
                self.dict_archivo['Identar'],
                self.dict_archivo['De Identar'],
                self.dict_archivo['Buscar Texto'],
                self.dict_archivo['Reemplazar Texto'],
                self.dict_archivo['Seleccionar Todo'],
                self.dict_archivo['Chequear'],
                self.dict_archivo['Disminuir'],
                self.dict_archivo['Aumentar'],
                ])

        map(self.__activar, activar)
        map(self.__desactivar, desactivar)
