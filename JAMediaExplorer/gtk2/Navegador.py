#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Navegador.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
#
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
import gtk
import gobject
import commands

from NoteBookDirectorios import NoteBookDirectorios
from JAMFileSystem import DeviceManager
from JAMFileSystem import describe_uri

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONOS = os.path.join(BASE_PATH, "Iconos")

HOME = os.environ["HOME"]
ACTIVITIES = os.path.join(HOME, "Activities")
JAMEDIA = os.path.join(HOME, "JAMediaDatos")
DIARIO = os.path.join(HOME, ".sugar/default")
LOGS = os.path.join(DIARIO, "logs")
ROOT = "/"


class Navegador(gtk.HPaned):
    """
    Navegador de Archivos.
    """

    __gsignals__ = {
    "info": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "cargar": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "borrar": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(0, gtk.gdk.color_parse("#e3f2f2"))

        # Izquierda
        panel_izquierdo = gtk.VPaned()
        self.unidades = Unidades()
        panel_izquierdo.pack1(self.unidades, resize=False, shrink=True)
        self.infowidget = InfoWidget()
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.add_with_viewport(self.infowidget)
        panel_izquierdo.pack2(scrolled_window, resize=True, shrink=True)
        self.pack1(panel_izquierdo, resize=False, shrink=True)

        # Derecha
        self.notebookdirectorios = NoteBookDirectorios()
        self.pack2(self.notebookdirectorios, resize=True, shrink=True)

        self.show_all()

        self.unidades.connect('leer', self.__leer)
        self.unidades.connect('add-leer', self.__add)
        self.unidades.connect('info', self.__emit_info)
        self.unidades.connect('remove_explorers', self.__remove_explorers)

        self.notebookdirectorios.connect('info', self.__emit_info)
        self.notebookdirectorios.connect('borrar', self.__emit_borrar)
        self.notebookdirectorios.connect('montaje', self.__select_montaje)
        self.notebookdirectorios.connect('no-paginas', self.__select_home)

    def __select_home(self, widget):
        gobject.idle_add(self.unidades.select_home)

    def __select_montaje(self, widget, montaje):
        """
        Cuando se hace switch en el notebook, se selecciona
        la unidad de montaje a la cual refiere.
        """
        model = self.unidades.get_model()
        item = model.get_iter_first()
        while item:
            if model.get_value(item, 2) == montaje:
                self.unidades.get_selection().select_iter(item)
                break
            item = model.iter_next(item)

    def __remove_explorers(self, widget, remove_explorers):
        """
        Cuando se desmonta una unidad, se cierran las lenguetas
        que refieren a ella y se verifican los paths en cortar y copiar.
        """
        paginas = self.notebookdirectorios.get_children()
        pags = []
        for pagina in paginas:
            directorio = pagina.get_child()
            for path in remove_explorers:
                if path in directorio.path:
                    pags.append(paginas.index(pagina))
                    break

        pags.reverse()
        for pag in pags:
            self.notebookdirectorios.remove_page(pag)

        copiando = self.notebookdirectorios.copiando
        cortando = self.notebookdirectorios.cortando

        for path in remove_explorers:
            if copiando:
                if path in copiando:
                    self.notebookdirectorios.copiando = False
            if cortando:
                path_cortando = self.notebookdirectorios.cortando[0]
                if path in path_cortando:
                    self.notebookdirectorios.cortando = False

    def __emit_borrar(self, widget, direccion, modelo, iter):
        self.emit('borrar', direccion, modelo, iter)

    def __emit_info(self, widget, path):
        self.emit('info', path)

    def __leer(self, widget, directorio):
        self.get_toplevel().set_sensitive(False)
        self.notebookdirectorios.load(directorio)
        self.get_toplevel().set_sensitive(True)

    def __add(self, widget, directorio):
        self.get_toplevel().set_sensitive(False)
        self.notebookdirectorios.add_leer(directorio)
        self.get_toplevel().set_sensitive(True)


class Unidades(gtk.TreeView):
    """
    Treview para unidades y directorios.
    """

    __gsignals__ = {
    "leer": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "add-leer": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "info": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "remove_explorers": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.TreeView.__init__(self,
            gtk.ListStore(gtk.gdk.Pixbuf,
            gobject.TYPE_STRING, gobject.TYPE_STRING))

        self.modify_bg(0, gtk.gdk.color_parse("#e3f2f2"))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(False)
        self.set_headers_visible(False)

        self.dir_select = None
        self.demonio_unidades = DeviceManager()

        self.__setear_columnas()
        self.__Llenar_ListStore()

        self.connect("button-press-event", self.__handler_click)
        self.show_all()
        self.demonio_unidades.connect('update', self.__update_unidades)
        gobject.idle_add(self.select_home)

    def __handler_click(self, widget, event):
        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)
        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(
                int(pos[0]), int(pos[1]))
        except:
            return
        if boton == 1:
            iter_ = self.get_model().get_iter(path)
            directorio = self.get_model().get_value(iter_, 2)
            self.dir_select = directorio
            self.emit('leer', self.dir_select)
            self.emit('info', self.dir_select)
            return
        elif boton == 3:
            menu = MenuListUnidades(
                widget, boton, pos, tiempo, path, self.get_model())
            menu.connect('accion', self.__get_accion)
            gtk.Menu.popup(menu, None, None, None, boton, tiempo)
        elif boton == 2:
            return

    def __get_accion(self, widget, path, accion):
        iter_ = self.get_model().get_iter(path)
        direccion = self.get_model().get_value(iter_, 2)
        if accion == "Abrir":
            self.dir_select = direccion
            self.emit('add-leer', self.dir_select)
            self.emit('info', self.dir_select)

    def __update_unidades(self, widget):
        """
        Cuando se Conecta o Desconecta una Unidad.
        """
        unidades = self.demonio_unidades.get_unidades()
        lista = {}
        for unidad in unidades.keys():
            dic = unidades.get(unidad, False)
            if dic:
                mount_path = dic.get('mount_path', "")
                lista[mount_path.split("/")[-1]] = mount_path
        gobject.timeout_add(1000, self.__update_unidades2, lista)

    def __update_unidades2(self, lista):
        """
        Actualizar lista de unidades.
        """
        model = self.get_model()
        item = model.get_iter_first()
        mounts = []
        remove_explorers = []
        while item:
            # Remover Unidades desmontadas.
            item_remove = False
            if not os.path.exists(model.get_value(item, 2)):
                remove_explorers.append(model.get_value(item, 2))
                item_remove = item
            else:
                mounts.append(model.get_value(item, 1))
            item = model.iter_next(item)
            if item_remove:
                model.remove(item_remove)
        for it in lista.keys():
            # Agregar Unidades nuevas.
            if not it in mounts:
                icono = os.path.join(ICONOS, "drive-removable-media-usb.svg")
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)
                model.append([pixbuf, it, lista[it]])
        if remove_explorers:
            self.emit('remove_explorers', remove_explorers)
        return False

    def __setear_columnas(self):
        self.append_column(self.__construir_columa_icono('Icono', 0, True))
        self.append_column(self.__construir_columa('Nombre', 1, True))
        self.append_column(self.__construir_columa('Directorio', 2, False))

    def __construir_columa(self, text, index, visible):
        render = gtk.CellRendererText()
        column = gtk.TreeViewColumn(text, render, text=index)
        column.set_sort_column_id(index)
        column.set_property('visible', visible)
        return column

    def __construir_columa_icono(self, text, index, visible):
        render = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn(text, render, pixbuf=index)
        column.set_property('visible', visible)
        return column

    def __Llenar_ListStore(self):
        self.get_toplevel().set_sensitive(False)

        icono = os.path.join(ICONOS, "def.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)
        self.get_model().append([pixbuf, 'Raiz', ROOT])

        icono = os.path.join(ICONOS, "stock-home.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)
        self.get_model().append([pixbuf, commands.getoutput('whoami'), HOME])

        if describe_uri(ACTIVITIES):
            icono = os.path.join(ICONOS, "stock-home.svg")
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)
            self.get_model().append([pixbuf, 'Actividades', ACTIVITIES])

        if describe_uri(JAMEDIA):
            icono = os.path.join(ICONOS, "JAMedia.svg")
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)
            self.get_model().append([pixbuf, 'JAMediaDatos', JAMEDIA])

        if describe_uri(DIARIO):
            icono = os.path.join(ICONOS, "diario.svg")
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)
            self.get_model().append([pixbuf, 'Diario', DIARIO])

        if describe_uri(LOGS):
            icono = os.path.join(ICONOS, "diario.svg")
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)
            self.get_model().append([pixbuf, 'Logs', LOGS])

        icono = os.path.join(ICONOS, "drive-removable-media-usb.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 30, -1)

        unidades = self.demonio_unidades.get_unidades()
        for unidad in unidades.keys():
            dic = unidades.get(unidad, False)
            if dic:
                mount_path = dic.get('mount_path', "")
                self.get_model().append([
                    pixbuf, mount_path.split("/")[-1], mount_path])
        self.get_toplevel().set_sensitive(True)

    def select_home(self):
        self.get_toplevel().set_sensitive(False)
        self.get_selection().select_path(1)
        modelo, iter_ = self.get_selection().get_selected()
        if iter_:
            self.get_selection().select_iter(iter_)
            self.dir_select = self.get_model().get_value(iter_, 2)
            self.emit('leer', self.dir_select)
            self.emit('info', self.dir_select)
        self.get_toplevel().set_sensitive(True)
        return False


class MenuListUnidades(gtk.Menu):

    __gsignals__ = {
    "accion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        gtk.Menu.__init__(self)

        self.modelo = modelo
        self.parent_objet = widget

        abrir_pestania = gtk.MenuItem("Abrir en Pestaña Nueva")
        self.append(abrir_pestania)
        abrir_pestania.connect_object("activate",
            self.__emit_accion, path, "Abrir")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __emit_accion(self, path, accion):
        self.emit('accion', path, accion)


class InfoWidget(gtk.EventBox):
    """
    Widgets con información sobre en path
    seleccionado en la estructura de directorios y archivos.
    """

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.normal_color = gtk.gdk.Color(65000, 65000, 65000)
        self.select_color = gtk.gdk.Color(61686, 65000, 48431)
        self.clicked_color = gtk.gdk.Color(61686, 65000, 17078)

        self.modify_bg(0, self.normal_color)
        self.typeinfo = None

        self.box = gtk.VBox()
        self.label = gtk.Label("")
        self.imagen = gtk.Image()
        self.imagen.modify_bg(0, self.normal_color)

        self.box.pack_start(self.label, False, False, 5)
        self.box.pack_start(self.imagen, False, False, 5)

        self.add(self.box)
        self.show_all()

    def set_info(self, textinfo, typeinfo):
        """
        Setea la información sobre un objeto seleccionado
        en la estructura de directorios.
        """
        # FIXME: Verificar Iconos
        self.label.set_text(textinfo)
        self.typeinfo = typeinfo
        icono = None

        if textinfo.startswith("Directorio") or \
            textinfo.startswith("Enlace"):
            icono = os.path.join(ICONOS, "document-open.svg")
        else:
            if 'video' in typeinfo:
                icono = os.path.join(ICONOS, "video.svg")
            elif 'pdf' in typeinfo:
                icono = os.path.join(ICONOS, "pdf.svg")
            elif 'audio' in typeinfo:
                icono = os.path.join(ICONOS, "sonido.svg")
            elif 'image' in typeinfo and not 'iso' in typeinfo:
                icono = os.path.join(ICONOS, "edit-select-all.svg")
            elif 'zip' in typeinfo or 'tar' in typeinfo:
                icono = os.path.join(ICONOS, "edit-select-all.svg")
            elif 'text' in typeinfo:
                icono = os.path.join(ICONOS, "edit-select-all.svg")
            else:
                icono = os.path.join(ICONOS, "edit-select-all.svg")
                self.typeinfo = None

        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 100, -1)
        self.imagen.set_from_pixbuf(pixbuf)

    def do_button_release_event(self, widget):
        self.modify_bg(0, self.select_color)
        self.imagen.modify_bg(0, self.select_color)

    def do_enter_notify_event(self, widget):
        self.modify_bg(0, self.select_color)
        self.imagen.modify_bg(0, self.select_color)

    def do_leave_notify_event(self, widget):
        self.modify_bg(0, self.normal_color)
        self.imagen.modify_bg(0, self.normal_color)
