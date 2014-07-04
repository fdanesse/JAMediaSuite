#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DialogoProyecto.py por:
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

BASE_PATH = os.path.dirname(__file__)

icons = os.path.join(BASE_PATH, "Iconos")

from Globales import get_boton
from Globales import get_pixels

LICENCIAS = ['GPL2', 'GPL3', 'LGPL 2.1', 'LGPL 3', 'BSD', 'MIT X11']


class DialogoProyecto(Gtk.Dialog):
    """
    Diálogo para crear un nuevo proyecto.
    """

    __gtype_name__ = 'JAMediaEditorDialogoProyecto'

    def __init__(self, parent_window=None,
        title="Crear Proyecto Nuevo", accion="nuevo"):

        Gtk.Dialog.__init__(self, title=title,
            parent=parent_window, flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Guardar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.sizes = [(600, 150), (600, 450)]

        if accion == "nuevo":
            self.set_size_request(600, 150)
        else:
            self.set_size_request(600, 450)

        self.set_border_width(15)

        # Entradas de datos.
        self.nombre = Gtk.Entry()
        self.main = Gtk.ComboBoxText()
        self.path = Gtk.Label()
        self.mimetypes = Gtk.Entry()
        self.categories = Gtk.Entry()

        self.version = Gtk.Entry()
        self.version.connect("changed", self.__check_version)
        self.version.set_text("0.0.1")

        self.descripcion = Gtk.TextView()
        self.descripcion.set_editable(True)
        self.descripcion.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

        scroll_descripcion = Gtk.ScrolledWindow()
        scroll_descripcion.set_policy(Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
        scroll_descripcion.add_with_viewport(self.descripcion)
        scroll_descripcion.set_size_request(200, 100)

        self.licencia = Gtk.ComboBoxText()
        self.url = Gtk.Entry()
        self.icon_path = Gtk.Label()

        # Box para despues agregarlo a un scroll
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Scroll
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.box)

        self.vbox.pack_start(scroll, True, True, 0)

        # Autores
        self.autores = WidgetAutores()

        if accion == "nuevo":
            boton = Gtk.Button("Ver más Opciones...")

        else:
            boton = Gtk.Button("Ocultar Opciones...")

        boton.connect("clicked", self.__show_options)

        self.internal_widgets = [
            self.__get_pack_box(
                [self.__get_label('Nombre:'), self.nombre]),
            self.__get_pack_box(
                [boton]),
            self.__get_pack_box(
                [self.__get_label('Archivo Principal:'),
                self.main]),
            self.__get_pack_box(
                [self.__get_label('Directorio del proyecto:'),
                self.path]),
            self.__get_pack_box(
                [self.__get_label('MimeTypes:'), self.mimetypes]),
            self.__get_pack_box(
                [self.__get_label('Categoría:'), self.categories]),
            self.__get_pack_box(
                [self.__get_label('Versión:'), self.version]),
            self.__get_pack_box(
                [self.__get_label('Licencia:'), self.licencia]),
            self.__get_pack_box(
                [self.__get_label('Web:'), self.url]),
            self.__get_pack_box(
                [self.__get_label("Autores:"),
                self.autores]),
            self.__get_pack_box(
                [self.__get_label('Descripción:'), scroll_descripcion])]

        for widget in self.internal_widgets:
            self.box.pack_start(widget, False, False, 3)

        for licencia in LICENCIAS:
            self.licencia.append_text(licencia)

        self.licencia.set_active(0)
        self.show_all()

        if accion == "nuevo":
            for widget in self.internal_widgets[2:]:
                widget.hide()

        self.nombre.connect("key_release_event", self.__check_nombre)

        # Si se abre para editar, no se le puede cambiar el nombre.
        if accion == "editar":
            self.nombre.set_sensitive(False)

        for button in self.get_action_area().get_children():
            if self.get_response_for_widget(button) == Gtk.ResponseType.ACCEPT:
                button.set_sensitive(False)
                break

    def __show_options(self, button):
        options = False
        for widget in self.internal_widgets[2:]:
            if widget.get_visible():
                widget.hide()
                options = False

            else:
                widget.show()
                options = True

        if options:
            self.resize(self.sizes[1][0], self.sizes[1][1])
            self.set_size_request(self.sizes[1][0], self.sizes[1][1])
            button.set_label("Ocultar Opciones...")

        else:
            self.resize(self.sizes[0][0], self.sizes[0][1])
            self.set_size_request(self.sizes[0][0], self.sizes[0][1])
            button.set_label("Ver más Opciones...")

    def __check_version(self, widget):
        """
        En el campo versión solo pueden haber numeros y puntos.
        """
        text = widget.get_text()
        items = text.split(".")
        valores = []

        for item in items:
            item = item.strip()
            try:
                valores.append(int(item))

            except:
                valores.append(0)

        while len(valores) < 3:
            valores.append(0)

        version = "%s.%s.%s" % (valores[0], valores[1], valores[2])
        self.version.set_text(version)

    def __check_nombre(self, widget, event):
        """
        Activa y Desactiva el boton aceptar, según
        tenga nombre el proyecto o no.
        """

        boton = None

        for button in self.get_action_area().get_children():
            if self.get_response_for_widget(button) == Gtk.ResponseType.ACCEPT:
                boton = button
                break

        nombre = self.nombre.get_text()
        if nombre:
            nombre = nombre.strip()

        if nombre:
            boton.set_sensitive(True)

        else:
            boton.set_sensitive(False)

    def __get_label(self, text):
        label = Gtk.Label(text)
        return label

    def __get_pack_box(self, widgets):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(widgets[0], False, False, 5)
        for widget in widgets[1:]:
            box.pack_start(widget, True, True, 5)
        return box

    def get_proyecto(self):
        """
        Devuelve un diccionario con la definición del proyecto.
        """
        _buffer = self.descripcion.get_buffer()

        nombre = self.nombre.get_text()
        main = self.main.get_active_text()
        path = self.path.get_text()
        mimetypes = self.mimetypes.get_text()
        categories = self.categories.get_text()

        text = _buffer.get_text(_buffer.get_start_iter(),
            _buffer.get_end_iter(), True)

        version = self.version.get_text()
        licencia = self.licencia.get_active_text()
        url = self.url.get_text()

        if nombre:
            nombre = nombre.strip()

        if main:
            main = main.strip()

        if path:
            path = path.strip()

        if mimetypes:
            mimetypes = mimetypes.strip()

        if categories:
            categories = categories.strip()

        if text:
            text = text.strip()

        if version:
            version = version.strip()

        if licencia:
            licencia = licencia.strip()

        if url:
            url = url.strip()

        _dict = {
            "nombre": nombre,
            "main": main,
            "path": path,
            "descripcion": text,
            "mimetypes": mimetypes,
            "categoria": categories,
            "version": version,
            "licencia": licencia,
            "url": url,
            "autores": self.autores.get_autores()
            }

        return _dict

    def set_proyecto(self, diccionario):
        """
        Establece los datos del diccionario introducido
        """

        self.nombre.set_text(diccionario["nombre"])
        self.path.set_text(diccionario["path"])
        self.version.set_text(diccionario["version"])
        self.mimetypes.set_text(diccionario["mimetypes"])
        self.categories.set_text(diccionario["categoria"])
        self.descripcion.get_buffer().set_text(diccionario["descripcion"])
        self.licencia.set_active(LICENCIAS.index(diccionario["licencia"]))
        self.url.set_text(diccionario["url"])
        self.autores.set_autores(diccionario["autores"])

        # Setear Combo para archivo Main.
        if diccionario.get("path", False):
            import glob
            arch = glob.glob("%s/*.py" % diccionario["path"])
            self.main.remove_all()

            for archivo in arch:
                self.main.append_text(os.path.basename(archivo))

        model = self.main.get_model()
        item = model.get_iter_first()

        count = 0
        while item:
            if model.get_value(item, 0) == diccionario["main"]:
                self.main.set_active(count)
                break

            item = model.iter_next(item)
            count += 1

        # Setear sensibilidad en el boton aceptar.
        for button in self.get_action_area().get_children():
            if self.get_response_for_widget(button) == Gtk.ResponseType.ACCEPT:
                nombre = self.nombre.get_text()
                if nombre:
                    nombre.strip()

                if not nombre:
                    button.set_sensitive(False)

                else:
                    button.set_sensitive(True)

                break


class WidgetAutores(Gtk.Box):
    """
    Box para agregar datos de los Autores
    """

    __gtype_name__ = 'JAMediaEditorWidgetAutores'

    def __init__(self):

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.__agregar(None)
        self.show_all()

    def __agregar(self, widget):
        """
        Función para agregar información de un autor.
        """
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        entry1 = Gtk.Entry()
        entry2 = Gtk.Entry()

        remover = get_boton(os.path.join(icons, "list-remove.svg"),
            pixels=get_pixels(1.0), tooltip_text="Eliminar")

        agregar = get_boton(os.path.join(icons, "gtk-add.svg"),
            pixels=get_pixels(1.0), tooltip_text="Agregar")

        frame1 = Gtk.Frame()
        frame1.set_label("Nombre")
        frame2 = Gtk.Frame()
        frame2.set_label("Mail")

        frame1.add(entry1)
        frame2.add(entry2)

        box.pack_start(frame1, False, False, 5)
        box.pack_start(frame2, False, False, 0)
        box.pack_start(remover, False, False, 0)
        box.pack_start(agregar, False, False, 0)

        self.pack_start(box, False, False, 0)

        agregar.connect("clicked", self.__agregar)
        remover.connect("clicked", self.__quitar)
        self.show_all()

    def __quitar(self, widget):
        """
        Función para eliminar informacion de un autor.
        """
        if len(self.get_children()) == 1:
            widget.get_parent().get_children()[0].get_child().set_text("")
            widget.get_parent().get_children()[1].get_child().set_text("")

        else:
            widget.get_parent().destroy()

    def get_autores(self):
        """
        Devuelve una lista de tuplas (nombre, mail),
        con todos los autores definidos.
        """
        autores = []

        for autor in self.get_children():
            nombre = autor.get_children()[0].get_child()
            mail = autor.get_children()[1].get_child()

            nombre = nombre.get_text()
            nombre = nombre.strip()

            mail = mail.get_text()
            mail = mail.strip()

            autores.append((nombre, mail))

        return autores

    def set_autores(self, autores):
        for x in range(len(autores) - 1):
            self.__agregar(None)

        for autor in autores:
            nombre, mail = autor
            linea = self.get_children()[autores.index(autor)]
            linea.get_children()[0].get_child().set_text(nombre)
            linea.get_children()[1].get_child().set_text(mail)
