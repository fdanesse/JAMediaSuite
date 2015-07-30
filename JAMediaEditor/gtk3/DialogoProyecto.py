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
import json
import glob
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GdkX11
import Licencias as Lic

HOME = os.environ["HOME"]
BASE_PATH = os.path.dirname(__file__)
ICONOS = os.path.join(BASE_PATH, "Iconos")
BatovideWorkSpace = os.path.join(HOME, 'BatovideWorkSpace')

LICENCIAS = ['GPL2', 'GPL3', 'LGPL 2.1', 'LGPL 3', 'BSD', 'MIT X11']

screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()

TRUE_CHAR = range(65, 91)  # Letras Mayúsculas
TRUE_CHAR.append(95)  # _
for x in range(97, 123):
    TRUE_CHAR.append(x)  # Letras Minúsculas

TRUE_VER = range(48, 58)


def pack_entry(text, entry):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    box.pack_start(Gtk.Label(text), False, False, 5)
    box.pack_start(entry, True, True, 5)
    return box


class DialogoProyecto(Gtk.Window):
    """
    Diálogo para crear un nuevo proyecto.
    """

    __gtype_name__ = 'JAMediaEditorDialogoProyecto'

    __gsignals__ = {
        'load': (GObject.SIGNAL_RUN_LAST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self, parent_window=None, title="Proyecto Nuevo"):

        Gtk.Window.__init__(self)

        self.parent_window = parent_window
        self.set_title(title)
        self.set_transient_for(self.parent_window)
        self.set_border_width(15)

        hbox = Gtk.HBox()
        image = Gtk.Image()
        arch = os.path.join(BASE_PATH, "Help", "Iconos", "constructortux.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(arch, 100, 100)
        image.set_from_pixbuf(pixbuf)
        hbox.pack_start(image, False, False, 0)
        label = Gtk.Label("Constructor de Proyectos")
        hbox.pack_start(label, True, True, 3)
        label.modify_font(Pango.FontDescription("%s %s" % ("Monospace", 12)))
        #label.modify_fg(0, Gdk.Color(0, 0, 65000))

        vbox = Gtk.VBox()
        vbox.pack_start(hbox, False, False, 0)

        tabla = Gtk.Table(rows=11, columns=2, homogeneous=True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(tabla)

        self.path = Gtk.Label()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(Gtk.Label(" path: "), False, False, 0)
        box.pack_start(self.path, False, False, 0)
        tabla.attach(box, 0, 2, 0, 1)

        self.nombre = Gtk.Entry()
        self.nombre.set_sensitive(False)
        box = pack_entry("Nombre:", self.nombre)
        tabla.attach(box, 0, 1, 1, 2)
        self.nombre.connect("changed", self.__check_nombre)

        self.version = Gtk.Entry()
        box = pack_entry("Version:", self.version)
        tabla.attach(box, 1, 2, 1, 2)
        self.version.connect("changed", self.__check_version)

        self.categories = Gtk.Entry()
        box = pack_entry("Categoría:", self.categories)
        tabla.attach(box, 0, 2, 2, 3)

        self.mimetypes = Gtk.Entry()
        box = pack_entry("MimeTypes:", self.mimetypes)
        tabla.attach(box, 0, 2, 3, 4)

        self.url = Gtk.Entry()
        box = pack_entry("Sitio Web:", self.url)
        tabla.attach(box, 0, 2, 4, 5)

        self.licencia = Gtk.ComboBoxText()
        box = pack_entry("Licencia:", self.licencia)
        tabla.attach(box, 0, 1, 5, 6)

        self.main = Gtk.ComboBoxText()
        self.main.set_active(0)
        box = pack_entry("Ejecutable:", self.main)
        tabla.attach(box, 1, 2, 5, 6)

        frame1 = Gtk.Frame()
        frame1.set_border_width(5)
        frame1.set_label(" Autores: ")
        self.autores = Gtk.TextView()
        self.autores.set_border_width(5)
        self.autores.set_editable(True)
        self.autores.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scroll1 = Gtk.ScrolledWindow()
        scroll1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll1.add(self.autores)
        frame1.add(scroll1)
        tabla.attach(frame1, 0, 2, 6, 8)

        frame2 = Gtk.Frame()
        frame2.set_border_width(5)
        frame2.set_label(" Descripción: ")
        self.descripcion = Gtk.TextView()
        self.descripcion.set_border_width(5)
        self.descripcion.set_editable(True)
        self.descripcion.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scroll2 = Gtk.ScrolledWindow()
        scroll2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll2.add(self.descripcion)
        frame2.add(scroll2)
        tabla.attach(frame2, 0, 2, 8, 10)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button_crear = Gtk.Button("Crear")
        self.button_crear.connect("clicked", self.__crear_cargar_proyecto)
        self.button_cancelar = Gtk.Button("Cancelar")
        self.button_cancelar.connect("clicked", self.__salir)
        box.pack_start(self.button_crear, True, True, 0)
        box.pack_start(self.button_cancelar, True, True, 0)
        tabla.attach(box, 0, 2, 10, 11)

        self.resize(w / 3, h - 40)
        self.move(w - w / 3, 40)

        vbox.pack_start(scroll, True, True, 0)
        self.add(vbox)
        self.show_all()

    def __crear_cargar_proyecto(self, widget):
        _dict = self.__get_proyecto()
        if widget.get_label() == "Crear":
            self.__guardar_proyecto(_dict)
            nombre = _dict.get("nombre", "")
            path = os.path.join(BatovideWorkSpace, nombre)
            self.emit("load", os.path.join(path, "proyecto.ide"))
        elif widget.get_label() == "Guardar":
            self.__actualizar_proyecto(_dict)
            self.parent_window.base_panel.proyecto = _dict
        self.__salir()

    def __actualizar_proyecto(self, _dict):
        path = _dict["path"]
        # Seteo automático de licencia
        licencia_path = os.path.join(path, "COPYING")
        arch = open(licencia_path, "w")
        arch.write(Lic.dict[_dict["licencia"]])
        arch.close()
        # Seteo automático de autores.
        autores_path = os.path.join(path, "AUTHORS")
        arch = open(autores_path, "w")
        arch.write(_dict["autores"])
        arch.close()
        # Guardar archivo de Proyecto.
        proyecto_file = os.path.join(path, "proyecto.ide")
        archivo = open(proyecto_file, "w")
        archivo.write(
            json.dumps(
                _dict,
                indent=4,
                ensure_ascii=False,
                separators=(", ", ":"),
                encoding="utf-8"))
        archivo.close()

    def __guardar_proyecto(self, _dict):
        """
        Los proyectos siempre se crean en BatovideWorkSpace
        """
        nombre = _dict.get("nombre", "")
        if nombre:
            if nombre in os.listdir(BatovideWorkSpace):
                print "FIXME: Ya existe un Proyecto con este Nombre"
                return
            else:
                # verificar, guardar, ocultar y mandar cargar.
                path = os.path.join(BatovideWorkSpace, nombre)
                os.mkdir(path)
                _dict["path"] = path
                # Seteo automático de licencia
                licencia_path = os.path.join(path, "COPYING")
                arch = open(licencia_path, "w")
                arch.write(Lic.dict[_dict["licencia"]])
                arch.close()
                # Seteo automático de autores.
                autores_path = os.path.join(path, "AUTHORS")
                arch = open(autores_path, "w")
                arch.write(_dict["autores"])
                arch.close()
                # Seteo automático de main.
                if not _dict["main"]:
                    _dict["main"] = "main.py"
                # Guardar archivo de Proyecto.
                proyecto_file = os.path.join(path, "proyecto.ide")
                archivo = open(proyecto_file, "w")
                archivo.write(
                    json.dumps(
                        _dict,
                        indent=4,
                        ensure_ascii=False,
                        separators=(", ", ":"),
                        encoding="utf-8"))
                archivo.close()

    def __check_nombre(self, widget):
        nombre = self.nombre.get_text().strip()
        if nombre:
            if ord(nombre[-1]) not in TRUE_CHAR:
                nombre = str(nombre[:-1])
            self.nombre.set_text(nombre)
        if nombre:
            self.button_crear.set_sensitive(True)
        else:
            self.button_crear.set_sensitive(False)

    def __salir(self, widget=None):
        self.destroy()

    def __check_version(self, widget):
        version = self.version.get_text().strip()
        if version:
            if ord(version[-1]) not in TRUE_VER:
                version = str(version[:-1])
            self.version.set_text(version)
        else:
            self.version.set_text("0")

    def __get_proyecto(self):
        nombre = self.nombre.get_text()
        main = self.main.get_active_text()
        mimetypes = self.mimetypes.get_text()
        categories = self.categories.get_text()
        descripcion = self.descripcion.get_buffer().get_text(
            self.descripcion.get_buffer().get_start_iter(),
            self.descripcion.get_buffer().get_end_iter(), True)
        version = self.version.get_text()
        licencia = self.licencia.get_active_text()
        url = self.url.get_text()
        autores = self.autores.get_buffer().get_text(
            self.autores.get_buffer().get_start_iter(),
            self.autores.get_buffer().get_end_iter(), True)
        path = self.path.get_text()
        if nombre:
            nombre = nombre.strip()
        if main:
            main = main.strip()
        if mimetypes:
            mimetypes = mimetypes.replace("\n", "").strip()
        if categories:
            categories = categories.replace("\n", "").strip()
        if descripcion:
            descripcion = descripcion.replace("\n", "").strip()
        if version:
            version = version.strip()
        if licencia:
            licencia = licencia.strip()
        if url:
            url = url.replace("\n", "").strip()
        _dict = {
            "nombre": nombre,
            "path": path,
            "main": main,
            "descripcion": descripcion,
            "mimetypes": mimetypes,
            "categoria": categories,
            "version": version,
            "licencia": licencia,
            "url": url,
            "autores": autores,
            }
        return _dict

    def __limpiar(self):
        self.nombre.set_text("")
        self.version.set_text("0")
        self.mimetypes.set_text("")
        self.categories.set_text("")
        self.descripcion.get_buffer().set_text("")
        self.main.remove_all()
        self.licencia.remove_all()
        self.url.set_text("")
        self.autores.get_buffer().set_text("")
        for licencia in LICENCIAS:
            self.licencia.append_text(licencia)
        self.licencia.set_active(0)
        self.path.set_text("")
        self.button_crear.set_sensitive(False)

    def __set_dialogo(self, _dict):
        self.nombre.set_text(_dict["nombre"])
        self.version.set_text(_dict["version"])
        self.mimetypes.set_text(_dict["mimetypes"])
        self.categories.set_text(_dict["categoria"])
        self.descripcion.get_buffer().set_text(_dict["descripcion"])
        self.licencia.set_active(LICENCIAS.index(_dict["licencia"]))
        self.url.set_text(_dict["url"])
        self.autores.get_buffer().set_text(_dict["autores"])
        self.path.set_text(_dict["path"])
        arch = glob.glob("%s/*.py" % _dict["path"])
        for archivo in arch:
            self.main.append_text(os.path.basename(archivo))
        model = self.main.get_model()
        item = model.get_iter_first()
        count = 0
        while item:
            if model.get_value(item, 0) == _dict["main"]:
                self.main.set_active(count)
                break
            item = model.iter_next(item)
            count += 1

    def setting(self, title, path):
        self.__limpiar()
        self.set_title(title)
        if title == "Nuevo Proyecto":
            self.button_crear.set_label("Crear")
            self.nombre.set_sensitive(True)
        elif title == "Editar Proyecto":
            self.button_crear.set_label("Guardar")
            self.nombre.set_sensitive(False)
            arch = open(os.path.join(path, "proyecto.ide"), "r")
            _dict = json.load(arch, "utf-8")
            arch.close()
            self.__set_dialogo(_dict)
        self.show_all()
