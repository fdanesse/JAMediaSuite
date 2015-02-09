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
import glob

from gi.repository import Gtk
from gi.repository import GdkX11

BASE_PATH = os.path.dirname(__file__)
ICONOS = os.path.join(BASE_PATH, "Iconos")

#from Globales import get_boton

LICENCIAS = ['GPL2', 'GPL3', 'LGPL 2.1', 'LGPL 3', 'BSD', 'MIT X11']
screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()


class DialogoProyecto(Gtk.Window):
    """
    Diálogo para crear un nuevo proyecto.
    """

    __gtype_name__ = 'JAMediaEditorDialogoProyecto'

    def __init__(self, parent_window=None,
        title="Proyecto Nuevo", accion="nuevo"):

        Gtk.Window.__init__(self)

        self.parent_window = parent_window
        self.set_title(title)
        self.set_transient_for(self.parent_window)
        self.set_border_width(15)

        tabla = Gtk.Table(rows=10, columns=2, homogeneous=True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(tabla)

        # Fila 1
        self.nombre = Gtk.Entry()
        box = self.__pack_entry("Nombre:", self.nombre)
        tabla.attach(box, 0, 1, 0, 1)
        # self.nombre.connect("key_release_event", self.__check_nombre)

        self.version = Gtk.Entry()
        box = self.__pack_entry("Version:", self.version)
        tabla.attach(box, 1, 2, 0, 1)
        # self.version.connect("changed", self.__check_version)

        # Fila 3
        self.categories = Gtk.Entry()
        box = self.__pack_entry("Categoría:", self.categories)
        tabla.attach(box, 0, 2, 1, 2)
        # self.version.connect("changed", self.__check_version)

        # Fila 4
        self.mimetypes = Gtk.Entry()
        box = self.__pack_entry("MimeTypes:", self.mimetypes)
        tabla.attach(box, 0, 2, 2, 3)
        # self.nombre.connect("key_release_event", self.__check_nombre)

        # Fila 5
        self.url = Gtk.Entry()
        box = self.__pack_entry("Sitio Web:", self.url)
        tabla.attach(box, 0, 2, 3, 4)
        # self.nombre.connect("key_release_event", self.__check_nombre)

        # Fila 6
        self.licencia = Gtk.ComboBoxText()
        for licencia in LICENCIAS:
            self.licencia.append_text(licencia)
        self.licencia.set_active(0)
        box = self.__pack_entry("Licencia:", self.licencia)
        tabla.attach(box, 0, 1, 4, 5)
        # self.nombre.connect("key_release_event", self.__check_nombre)

        '''
        # Entradas de datos.
        self.main = Gtk.ComboBoxText()
        self.path = Gtk.Label()
        self.descripcion = Gtk.TextView()
        self.descripcion.set_editable(True)
        self.descripcion.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scroll_descripcion = Gtk.ScrolledWindow()
        scroll_descripcion.set_policy(Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
        scroll_descripcion.add_with_viewport(self.descripcion)
        scroll_descripcion.set_size_request(200, 100)
        self.icon_path = Gtk.Label()
        # Autores
        self.autores = WidgetAutores()
        # Si se abre para editar, no se le puede cambiar el nombre.
        if accion == "editar":
            self.nombre.set_sensitive(False)
        '''

        self.resize(w/3, h-40)
        self.move(w-w/3, 40)

        self.add(scroll)
        self.show_all()

    def __pack_entry(self, text, entry):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(Gtk.Label(text), False, False, 5)
        box.pack_start(entry, True, True, 5)
        return box
    '''
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
        return Gtk.Label(text)

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

        nombre = unicode(self.nombre.get_text(), "utf-8")
        main = self.main.get_active_text()
        if main:
            main = unicode(main, "utf-8")
        path = unicode(self.path.get_text(), "utf-8")
        mimetypes = unicode(self.mimetypes.get_text(), "utf-8")
        categories = unicode(self.categories.get_text(), "utf-8")
        descripcion = unicode(_buffer.get_text(_buffer.get_start_iter(),
            _buffer.get_end_iter(), True), "utf-8")
        version = unicode(self.version.get_text(), "utf-8")
        licencia = unicode(self.licencia.get_active_text(), "utf-8")
        url = unicode(self.url.get_text(), "utf-8")

        if nombre:
            nombre = nombre.strip()
        if main:
            main = main.strip()
        if path:
            path = path.strip()
        if mimetypes:
            mimetypes = mimetypes.replace("\n", " ").strip()
        if categories:
            categories = categories.replace("\n", " ").strip()
        if descripcion:
            descripcion = descripcion.replace("\n", " ").strip()
        if version:
            version = version.strip()
        if licencia:
            licencia = licencia.strip()
        if url:
            url = url.replace("\n", " ").strip()
        _dict = {
            "nombre": nombre,
            "main": main,
            "path": path,
            "descripcion": descripcion,
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
            arch = glob.glob("%s/*.py" % diccionario["path"])
            self.main.remove_all()
            for archivo in arch:
                self.main.append_text(
                    unicode(os.path.basename(archivo), "utf-8"))

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
                if self.nombre.get_text().strip():
                    button.set_sensitive(True)
                else:
                    button.set_sensitive(False)
                break
    '''
'''
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

        remover = get_boton(os.path.join(ICONOS, "list-remove.svg"),
            pixels=37, tooltip_text="Eliminar")

        agregar = get_boton(os.path.join(ICONOS, "gtk-add.svg"),
            pixels=37, tooltip_text="Agregar")

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
            nombre = nombre.get_text().strip()
            mail = mail.get_text().strip()
            autores.append((unicode(nombre, "utf-8"), unicode(mail, "utf-8")))
        return autores

    def set_autores(self, autores):
        for x in range(len(autores) - 1):
            self.__agregar(None)
        for autor in autores:
            nombre, mail = autor
            linea = self.get_children()[autores.index(autor)]
            linea.get_children()[0].get_child().set_text(nombre)
            linea.get_children()[1].get_child().set_text(mail)
'''
