#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Toolbars.py por:
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

from gi.repository import Gtk
from gi.repository import GObject

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

icons = os.path.join(JAMediaObjectsPath, "Iconos")

from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_separador
from JAMediaObjects.JAMediaGlobales import get_pixels


class ToolbarProyecto(Gtk.Toolbar):
    """
    Toolbar para el proyecto.
    """

    __gtype_name__ = 'JAMediaEditorToolbarProyecto'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.dict_proyecto = {}

        nuevo_proyecto = get_boton(
            os.path.join(icons, "document-new.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Nuevo Proyecto")

        abrir_proyecto = get_boton(
            os.path.join(icons, "document-open.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Abrir Proyecto")

        cerrar_proyecto = get_boton(
            os.path.join(icons, "button-cancel.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Cerrar Proyecto")

        editar_proyecto = get_boton(
            os.path.join(icons, "gtk-edit.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Editar Proyecto")

        guardar_proyecto = get_boton(
            os.path.join(icons, "document-save.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Guardar Proyecto")

        ejecutar_proyecto = get_boton(
            os.path.join(icons, "media-playback-start.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Ejecutar Proyecto")

        detener = get_boton(
            os.path.join(icons, "media-playback-stop.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Detener Ejecución")

        self.dict_proyecto["Cerrar Proyecto"] = cerrar_proyecto
        self.dict_proyecto["Editar Proyecto"] = editar_proyecto
        self.dict_proyecto["Guardar Proyecto"] = guardar_proyecto
        self.dict_proyecto["Ejecutar Proyecto"] = ejecutar_proyecto
        self.dict_proyecto["Detener Ejecución"] = detener

        self.insert(nuevo_proyecto, - 1)
        self.insert(abrir_proyecto, - 1)
        self.insert(editar_proyecto, - 1)
        self.insert(guardar_proyecto, - 1)
        self.insert(cerrar_proyecto, - 1)
        self.insert(get_separador(draw=True,
            ancho=0, expand=False), - 1)
        self.insert(ejecutar_proyecto, - 1)
        self.insert(detener, - 1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), - 1)

        self.show_all()

        botones = [
            nuevo_proyecto,
            abrir_proyecto,
            cerrar_proyecto,
            editar_proyecto,
            guardar_proyecto,
            ejecutar_proyecto,
            detener]

        for boton in botones:
            boton.connect("clicked", self.__emit_accion)

        for boton in self.dict_proyecto.keys():
            self.dict_proyecto[boton].set_sensitive(False)

    def __emit_accion(self, widget):

        self.emit("accion", widget.TOOLTIP)

    def activar(self, visibility, ejecucion):
        """
        Activa o desactiva oopciones.
        """

        submenus = []

        for option in self.dict_proyecto.keys():
            submenus.append(self.dict_proyecto[option])

        if visibility:
            map(self.__activar, submenus)

        else:
            map(self.__desactivar, submenus)

        self.dict_proyecto["Ejecutar Proyecto"].set_sensitive(
            not ejecucion)
        self.dict_proyecto["Detener Ejecución"].set_sensitive(
            ejecucion)

    def __activar(self, option):

        if not option.get_sensitive():
            option.set_sensitive(True)

    def __desactivar(self, option):

        if option.get_sensitive():
            option.set_sensitive(False)


class ToolbarArchivo(Gtk.Toolbar):
    """
    Toolbar para el archivo
    """

    __gtype_name__ = 'JAMediaEditorToolbarArchivo'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.dict_archivo = {}

        nuevo_archivo = get_boton(
            os.path.join(icons, "document-new.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Nuevo Archivo")

        abrir_archivo = get_boton(
            os.path.join(icons, "document-open.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Abrir Archivo")

        guardar_archivo = get_boton(
            os.path.join(icons, "document-save.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Guardar Archivo")

        guardar_como = get_boton(
            os.path.join(icons, "document-save-as.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Guardar Como")

        ejecutar = get_boton(
            os.path.join(icons, "media-playback-start.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Ejecutar Archivo")

        detener = get_boton(
            os.path.join(icons, "media-playback-stop.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Detener Ejecución")

        deshacer = get_boton(
            os.path.join(icons, "edit-undo.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Deshacer")

        rehacer = get_boton(
            os.path.join(icons, "edit-redo.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Rehacer")

        copiar = get_boton(
            os.path.join(icons, "edit-copy.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Copiar")

        cortar = get_boton(
            os.path.join(icons, "editcut.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Cortar")

        pegar = get_boton(
            os.path.join(icons, "editpaste.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Pegar")

        seleccionar_todo = get_boton(
            os.path.join(icons, "edit-select-all.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Seleccionar Todo")

        self.dict_archivo["Guardar"] = guardar_archivo
        self.dict_archivo["Guardar Como"] = guardar_como
        self.dict_archivo["Deshacer"] = deshacer
        self.dict_archivo["Rehacer"] = rehacer
        self.dict_archivo["Copiar"] = copiar
        self.dict_archivo["Cortar"] = cortar
        self.dict_archivo["Pegar"] = pegar
        self.dict_archivo["Seleccionar Todo"] = seleccionar_todo
        self.dict_archivo["Ejecutar Archivo"] = ejecutar
        self.dict_archivo["Detener Ejecución"] = detener

        self.insert(get_separador(draw=False,
            ancho=10, expand=False), - 1)

        self.insert(nuevo_archivo, - 1)
        self.insert(abrir_archivo, - 1)
        self.insert(guardar_archivo, - 1)
        self.insert(guardar_como, - 1)
        self.insert(get_separador(draw=True,
            ancho=0, expand=False), - 1)
        self.insert(ejecutar, - 1)
        self.insert(detener, - 1)
        self.insert(get_separador(draw=True,
            ancho=0, expand=False), - 1)
        self.insert(deshacer, - 1)
        self.insert(rehacer, - 1)
        self.insert(get_separador(draw=True,
            ancho=0, expand=False), - 1)
        self.insert(copiar, - 1)
        self.insert(cortar, - 1)
        self.insert(pegar, - 1)
        self.insert(get_separador(draw=True,
            ancho=0, expand=False), - 1)
        self.insert(seleccionar_todo, - 1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), - 1)

        self.show_all()

        botones = [
            nuevo_archivo,
            abrir_archivo,
            guardar_archivo,
            guardar_como,
            ejecutar,
            detener,
            deshacer,
            rehacer,
            copiar,
            cortar,
            pegar,
            seleccionar_todo]

        for boton in botones:
            boton.connect("clicked", self.__emit_accion)

        for boton in self.dict_archivo.keys():
            self.dict_archivo[boton].set_sensitive(False)

    def __emit_accion(self, widget):

        self.emit("accion", widget.TOOLTIP)

    def update(self, visibility, options):
        """
        Activa o desactiva oopciones.
        """

        submenus = []

        for option in options:
            if self.dict_archivo.get(option, False):
                submenus.append(self.dict_archivo[option])

        if visibility:
            map(self.__activar, submenus)

        else:
            map(self.__desactivar, submenus)

    def __activar(self, option):

        if not option.get_sensitive():
            option.set_sensitive(True)

    def __desactivar(self, option):

        if option.get_sensitive():
            option.set_sensitive(False)


class ToolbarBusquedas(Gtk.Toolbar):

    __gtype_name__ = 'JAMediaEditorToolbarBusquedas'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING)),
    "buscar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.anterior = get_boton(
            os.path.join(icons, "go-next-rtl.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Anterior")

        self.anterior.connect("clicked", self.__emit_accion)
        self.insert(self.anterior, - 1)

        item = Gtk.ToolItem()
        item.set_expand(True)

        self.entry = Gtk.Entry()
        self.entry.show()

        item.add(self.entry)
        self.insert(item, - 1)

        self.siguiente = get_boton(
            os.path.join(icons, "go-next.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Siguiente")

        self.siguiente.connect("clicked", self.__emit_accion)
        self.insert(self.siguiente, - 1)

        self.entry.connect("changed", self.__emit_buscar)
        self.show_all()

        self.anterior.set_sensitive(False)
        self.siguiente.set_sensitive(False)

    def __emit_accion(self, widget):
        """
        Cuando se hace click en anterior y siguiente.
        """

        self.emit("accion", widget.TOOLTIP, self.entry.get_text())

    def __emit_buscar(self, widget):
        """
        Cuando cambia el texto a buscar.
        """

        if widget.get_text():
            self.anterior.set_sensitive(True)
            self.siguiente.set_sensitive(True)

        else:
            self.anterior.set_sensitive(False)
            self.siguiente.set_sensitive(False)

        self.emit("buscar", widget.get_text())
