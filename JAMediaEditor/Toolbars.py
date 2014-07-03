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
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

from Globales import get_pixels
from Globales import get_separador
from Globales import get_boton
from Globales import make_icon_active

BASE_PATH = os.path.dirname(__file__)
icons = os.path.join(BASE_PATH, "Iconos")


class ToolbarProyecto(Gtk.EventBox):
    """
    Toolbar para el proyecto.
    """

    __gtype_name__ = 'JAMediaEditorToolbarProyecto'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        from collections import OrderedDict
        self.dict_proyecto = OrderedDict()
        toolbar = Gtk.Toolbar()

        icon_path = make_icon_active(os.path.join(icons, "document-new.svg"))
        nuevo_proyecto = get_boton(icon_path, pixels=get_pixels(0.5),
            tooltip_text="Nuevo Proyecto")
        self.dict_proyecto["Nuevo Proyecto"] = [nuevo_proyecto,
            "document-new.svg"]

        icon_path = make_icon_active(os.path.join(icons, "document-open.svg"))
        abrir_proyecto = get_boton(icon_path, pixels=get_pixels(0.5),
            tooltip_text="Abrir Proyecto")
        self.dict_proyecto["Abrir Proyecto"] = [abrir_proyecto,
            "document-open.svg"]

        cerrar_proyecto = get_boton(os.path.join(icons, "button-cancel.svg"),
            pixels=get_pixels(0.5), tooltip_text="Cerrar Proyecto")
        self.dict_proyecto["Cerrar Proyecto"] = [cerrar_proyecto,
            "button-cancel.svg"]

        editar_proyecto = get_boton(os.path.join(icons, "gtk-edit.svg"),
            pixels=get_pixels(0.5), tooltip_text="Editar Proyecto")
        self.dict_proyecto["Editar Proyecto"] = [editar_proyecto,
            "gtk-edit.svg"]

        guardar_proyecto = get_boton(os.path.join(icons, "document-save.svg"),
            pixels=get_pixels(0.5), tooltip_text="Guardar Proyecto")
        self.dict_proyecto["Guardar Proyecto"] = [guardar_proyecto,
            "document-save.svg"]

        ejecutar_proyecto = get_boton(
            os.path.join(icons, "media-playback-start.svg"),
            pixels=get_pixels(0.5), tooltip_text="Ejecutar Proyecto")
        self.dict_proyecto["Ejecutar Proyecto"] = [ejecutar_proyecto,
            "media-playback-start.svg"]

        detener_ejecucion = get_boton(
            os.path.join(icons, "media-playback-stop.svg"),
            pixels=get_pixels(0.5), tooltip_text="Detener Ejecución")
        self.dict_proyecto["Detener Ejecución"] = [detener_ejecucion,
            "media-playback-stop.svg"]

        toolbar.insert(nuevo_proyecto, - 1)
        toolbar.insert(abrir_proyecto, - 1)
        toolbar.insert(editar_proyecto, - 1)
        toolbar.insert(guardar_proyecto, - 1)
        toolbar.insert(cerrar_proyecto, - 1)

        toolbar.insert(get_separador(draw=True, ancho=0, expand=False), - 1)

        toolbar.insert(ejecutar_proyecto, - 1)
        toolbar.insert(detener_ejecucion, - 1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), - 1)

        self.add(toolbar)
        self.show_all()

        for key in self.dict_proyecto.keys():
            self.dict_proyecto[key][0].connect("clicked", self.__emit_accion)

        self.activar_proyecto(False)
        self.activar_ejecucion(None)

        self.set_size_request(240, -1)

    def __emit_accion(self, widget):
        self.emit("accion", widget.TOOLTIP)

    def activar_ejecucion(self, ejecucion):
        """
        Activa y desactiva opción de ejecución de proyecto.
        """
        if ejecucion == None:
            map(self.__desactivar, self.dict_proyecto.keys()[-2:])

        elif ejecucion == False:
            map(self.__activar, [self.dict_proyecto.keys()[-2]])
            map(self.__desactivar, [self.dict_proyecto.keys()[-1]])

        elif ejecucion == True:
            map(self.__desactivar, [self.dict_proyecto.keys()[-2]])
            map(self.__activar, [self.dict_proyecto.keys()[-1]])

    def activar_proyecto(self, sensitive):
        """
        Activa o desactiva opciones básicas de proyecto.
        """
        if sensitive:
            map(self.__activar, self.dict_proyecto.keys()[2:])
        else:
            map(self.__desactivar, self.dict_proyecto.keys()[2:])

    def __activar(self, key):
        option, icon = self.dict_proyecto[key]
        if not option.get_sensitive():
            icon_path = make_icon_active(os.path.join(icons, icon))
            pixels = get_pixels(0.5)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icon_path, pixels, pixels)
            imagen = option.get_icon_widget()
            imagen.set_from_pixbuf(pixbuf)
            option.set_sensitive(True)

    def __desactivar(self, key):
        option, icon = self.dict_proyecto[key]
        if option.get_sensitive():
            icon_path = os.path.join(icons, icon)
            pixels = get_pixels(0.5)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icon_path, pixels, pixels)
            imagen = option.get_icon_widget()
            imagen.set_from_pixbuf(pixbuf)
            option.set_sensitive(False)


class ToolbarArchivo(Gtk.EventBox):
    """
    Toolbar para el archivo
    """

    __gtype_name__ = 'JAMediaEditorToolbarArchivo'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        from collections import OrderedDict
        self.dict_archivo = OrderedDict()
        toolbar = Gtk.Toolbar()

        icon_path = make_icon_active(os.path.join(icons, "document-new.svg"))
        nuevo_archivo = get_boton(os.path.join(icons, icon_path),
            pixels=get_pixels(0.5), tooltip_text="Nuevo Archivo")
        self.dict_archivo["Nuevo Archivo"] = [nuevo_archivo,
            "document-new.svg"]

        icon_path = make_icon_active(os.path.join(icons, "document-open.svg"))
        abrir_archivo = get_boton(os.path.join(icons, icon_path),
            pixels=get_pixels(0.5), tooltip_text="Abrir Archivo")
        self.dict_archivo["Abrir Archivo"] = [abrir_archivo,
            "document-open.svg"]

        guardar_archivo = get_boton(os.path.join(icons, "document-save.svg"),
            pixels=get_pixels(0.5), tooltip_text="Guardar Archivo")
        self.dict_archivo["Guardar Archivo"] = [guardar_archivo,
            "document-save.svg"]

        icon_path = make_icon_active(
            os.path.join(icons, "document-save-as.svg"))
        guardar_como = get_boton(os.path.join(icons, icon_path),
            pixels=get_pixels(0.5), tooltip_text="Guardar Como")
        self.dict_archivo["Guardar Como"] = [guardar_como,
            "document-save-as.svg"]

        icon_path = make_icon_active(
            os.path.join(icons, "media-playback-start.svg"))
        ejecutar = get_boton(os.path.join(icons, icon_path),
            pixels=get_pixels(0.5), tooltip_text="Ejecutar Archivo")
        self.dict_archivo["Ejecutar Archivo"] = [ejecutar,
            "media-playback-start.svg"]

        detener = get_boton(
            os.path.join(icons, "media-playback-stop.svg"),
            pixels=get_pixels(0.5), tooltip_text="Detener Ejecución")
        self.dict_archivo["Detener Ejecución"] = [detener,
            "media-playback-stop.svg"]

        deshacer = get_boton(os.path.join(icons, "edit-undo.svg"),
            pixels=get_pixels(0.5), tooltip_text="Deshacer")
        self.dict_archivo["Deshacer"] = [deshacer, "edit-undo.svg"]

        rehacer = get_boton(os.path.join(icons, "edit-redo.svg"),
            pixels=get_pixels(0.5), tooltip_text="Rehacer")
        self.dict_archivo["Rehacer"] = [rehacer, "edit-redo.svg"]

        copiar = get_boton(os.path.join(icons, "edit-copy.svg"),
            pixels=get_pixels(0.5), tooltip_text="Copiar")
        self.dict_archivo["Copiar"] = [copiar, "edit-copy.svg"]

        cortar = get_boton(os.path.join(icons, "editcut.svg"),
            pixels=get_pixels(0.5), tooltip_text="Cortar")
        self.dict_archivo["Cortar"] = [cortar, "editcut.svg"]

        pegar = get_boton(os.path.join(icons, "editpaste.svg"),
            pixels=get_pixels(0.5), tooltip_text="Pegar")
        self.dict_archivo["Pegar"] = [pegar, "editpaste.svg"]

        seleccionar_todo = get_boton(
            os.path.join(icons, "edit-select-all.svg"),
            pixels=get_pixels(0.5), tooltip_text="Seleccionar Todo")
        self.dict_archivo["Seleccionar Todo"] = [seleccionar_todo,
            "edit-select-all.svg"]

        toolbar.insert(get_separador(draw=False, ancho=10, expand=False), - 1)

        toolbar.insert(nuevo_archivo, - 1)
        toolbar.insert(abrir_archivo, - 1)
        toolbar.insert(guardar_archivo, - 1)
        toolbar.insert(guardar_como, - 1)
        toolbar.insert(get_separador(draw=True, ancho=0, expand=False), - 1)
        toolbar.insert(ejecutar, - 1)
        toolbar.insert(detener, - 1)
        toolbar.insert(get_separador(draw=True, ancho=0, expand=False), - 1)
        toolbar.insert(deshacer, - 1)
        toolbar.insert(rehacer, - 1)
        toolbar.insert(get_separador(draw=True, ancho=0, expand=False), - 1)
        toolbar.insert(copiar, - 1)
        toolbar.insert(cortar, - 1)
        toolbar.insert(pegar, - 1)
        toolbar.insert(get_separador(draw=True, ancho=0, expand=False), - 1)
        toolbar.insert(seleccionar_todo, - 1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), - 1)
        self.add(toolbar)
        self.show_all()

        for key in self.dict_archivo.keys():
            boton = self.dict_archivo[key][0]
            boton.connect("clicked", self.__emit_accion)

    def __emit_accion(self, widget):
        self.emit("accion", widget.TOOLTIP)

    def activar_ejecucion(self, ejecucion):
        """
        Activa y desactiva opción de ejecución de proyecto.
        """
        if ejecucion == None:
            map(self.__desactivar, [
                self.dict_archivo["Ejecutar Archivo"],
                self.dict_archivo["Detener Ejecución"],
                ])

        elif ejecucion == False:
            map(self.__activar, [self.dict_archivo["Ejecutar Archivo"]])
            map(self.__desactivar, [self.dict_archivo["Detener Ejecución"]])

        elif ejecucion == True:
            map(self.__desactivar, [self.dict_archivo["Ejecutar Archivo"]])
            map(self.__activar, [self.dict_archivo["Detener Ejecución"]])

    def update(self, _dict):
        """
        Activa o desactiva opciones.
        """
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
            activar.append(self.dict_archivo['Guardar Archivo'])
        else:
            desactivar.append(self.dict_archivo['Guardar Archivo'])

        if _dict['clipboard_texto']:
            activar.append(self.dict_archivo["Pegar"])
        else:
            desactivar.append(self.dict_archivo["Pegar"])

        if _dict['tiene_texto']:
            activar.append(self.dict_archivo["Seleccionar Todo"])
        else:
            desactivar.append(self.dict_archivo["Seleccionar Todo"])

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

        map(self.__activar, activar)
        map(self.__desactivar, desactivar)

    def __activar(self, item):
        option, icon = item
        if not option.get_sensitive():
            icon_path = make_icon_active(os.path.join(icons, icon))
            pixels = get_pixels(0.5)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icon_path, pixels, pixels)
            imagen = option.get_icon_widget()
            imagen.set_from_pixbuf(pixbuf)
            option.set_sensitive(True)

    def __desactivar(self, item):
        option, icon = item
        if option.get_sensitive():
            icon_path = os.path.join(icons, icon)
            pixels = get_pixels(0.5)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icon_path, pixels, pixels)
            imagen = option.get_icon_widget()
            imagen.set_from_pixbuf(pixbuf)
            option.set_sensitive(False)


class ToolbarBusquedas(Gtk.EventBox):

    __gtype_name__ = 'JAMediaEditorToolbarBusquedas'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING)),
    "buscar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        toolbar = Gtk.Toolbar()

        self.anterior = get_boton(os.path.join(icons, "go-next-rtl.svg"),
            pixels=get_pixels(0.5), tooltip_text="Anterior")

        self.anterior.connect("clicked", self.__emit_accion)
        toolbar.insert(self.anterior, - 1)

        item = Gtk.ToolItem()
        item.set_expand(True)

        self.entry = Gtk.Entry()
        self.entry.show()

        item.add(self.entry)
        toolbar.insert(item, - 1)

        self.siguiente = get_boton(os.path.join(icons, "go-next.svg"),
            pixels=get_pixels(0.5), tooltip_text="Siguiente")

        self.siguiente.connect("clicked", self.__emit_accion)
        toolbar.insert(self.siguiente, - 1)

        self.entry.connect("changed", self.__emit_buscar)
        self.add(toolbar)
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


class ToolbarEstado(Gtk.EventBox):
    """
    Barra de estado.
    """

    __gtype_name__ = 'JAMediaEditorToolbarEstado'

    def __init__(self):

        Gtk.EventBox.__init__(self)

        toolbar = Gtk.Toolbar()
        toolbar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#000000'))
        toolbar.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse('#ffffff'))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("")
        self.label.set_alignment(0.0, 0.5)
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        #self.insert(get_separador(draw=False, ancho=0, expand=True), -1)
        self.add(toolbar)
        self.show_all()

    def set_info(self, _dict):
        reng = _dict['renglones']
        carac = _dict['caracteres']
        arch = _dict['archivo']

        text = self.label.get_text()
        new_text = u"Archivo: %s  Lineas: %s  Caracteres: %s" % (
            arch, reng, carac)

        try:
            if text != new_text:
                self.label.set_text(new_text)
        except:
            pass
