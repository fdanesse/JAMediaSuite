#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Navegador.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM - Uruguay
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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

from NoteBookDirectorios import NoteBookDirectorios

import JAMediaObjects
from JAMediaObjects.JAMFileSystem import DeviceManager
from JAMediaObjects.JAMFileSystem import describe_uri
from JAMediaObjects.JAMediaGlobales import get_pixels

ICONOS = os.path.join(JAMediaObjects.__path__[0], "Iconos")

HOME = os.environ["HOME"]
ACTIVITIES = os.path.join(HOME, "Activities")
DIARIO = os.path.join(HOME, ".sugar/default")
LOGS = os.path.join(DIARIO, "logs")
ROOT = "/"
JAMEDIA = os.path.join(HOME, "JAMediaDatos")


class Navegador(Gtk.Paned):
    """
    Navegador de Archivos.
    """

    __gtype_name__ = 'JAMediaExplorerNavegador'

    __gsignals__ = {
    "info": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "cargar": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    "borrar": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.Paned.__init__(
            self, orientation=Gtk.Orientation.HORIZONTAL)

        self.unidades = None
        self.notebookdirectorios = NoteBookDirectorios()
        self.infowidget = None

        self.pack1(self.__area_izquierda_del_panel(),
            resize=False, shrink=True)
        self.pack2(self.notebookdirectorios,
            resize=True, shrink=True)

        self.show_all()

        self.unidades.connect(
            'leer', self.__leer)
        self.unidades.connect(
            'add-leer', self.__add)
        self.unidades.connect(
            'info', self.__emit_info)
        self.unidades.connect(
            'remove_explorers', self.__remove_explorers)

        self.notebookdirectorios.connect(
            'info', self.__emit_info)
        self.notebookdirectorios.connect(
            'borrar', self.__emit_borrar)
        self.notebookdirectorios.connect(
            'montaje', self.__select_montaje)
        self.notebookdirectorios.connect(
            'no-paginas', self.__select_home)

        self.infowidget.connect(
            'cargar', self.__emit_cargar)

    def __select_home(self, widget):

        from gi.repository import GLib
        GLib.idle_add(self.unidades.select_home)

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
        """
        Cuando se selecciona borrar en el menu de un item.
        """

        self.emit('borrar', direccion, modelo, iter)

    def __emit_cargar(self, widget, tipo):
        """
        Cuando se hace click en infowidget se pasa
        los datos a la ventana principal.
        """

        self.emit('cargar', tipo)

    def __emit_info(self, widget, path):
        """
        Cuando el usuario selecciona un archivo
        o directorio en la estructura de directorios,
        pasa la informacion del mismo a la ventana principal.
        """

        self.emit('info', path)

    def __area_izquierda_del_panel(self):

        self.unidades = Unidades()

        panel_izquierdo = Gtk.Paned(
            orientation=Gtk.Orientation.VERTICAL)

        panel_izquierdo.pack1(
            self.unidades, resize=False, shrink=True)

        self.infowidget = InfoWidget()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scrolled_window.add_with_viewport(self.infowidget)

        panel_izquierdo.pack2(
            scrolled_window, resize=True, shrink=True)

        return panel_izquierdo

    def __leer(self, widget, directorio):
        """
        Cuando se selecciona una unidad en el panel izquierdo.
        """

        self.get_toplevel().set_sensitive(False)
        self.notebookdirectorios.load(directorio)
        self.get_toplevel().set_sensitive(True)

    def __add(self, widget, directorio):
        """
        Cuando se selecciona una unidad en el panel izquierdo.
        """

        self.get_toplevel().set_sensitive(False)
        self.notebookdirectorios.add_leer(directorio)
        self.get_toplevel().set_sensitive(True)


class Unidades(Gtk.TreeView):
    """
    Treview para unidades y directorios.
    """

    __gtype_name__ = 'JAMediaExplorerUnidades'

    __gsignals__ = {
    "leer": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "add-leer": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "info": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "remove_explorers": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GdkPixbuf.Pixbuf,
            GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(False)
        self.set_headers_visible(False)

        self.dir_select = None

        self.demonio_unidades = DeviceManager()

        self.__setear_columnas()
        self.__Llenar_ListStore()

        self.connect("button-press-event",
            self.__handler_click)

        self.show_all()

        self.demonio_unidades.connect('update',
            self.__update_unidades)

        from gi.repository import GLib
        GLib.idle_add(self.select_home)

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

        # TreeView.get_path_at_pos(event.x, event.y) devuelve:
        # * La ruta de acceso en el punto especificado (x, y),
        # en relación con las coordenadas widget
        # * El gtk.TreeViewColumn en ese punto
        # * La coordenada X en relación con el fondo de la celda
        # * La coordenada Y en relación con el fondo de la celda

        if boton == 1:
            iter_ = self.get_model().get_iter(path)
            directorio = self.get_model().get_value(iter_, 2)

            #if self.dir_select != directorio:
            self.dir_select = directorio
            self.emit('leer', self.dir_select)
            self.emit('info', self.dir_select)

            return

        elif boton == 3:
            menu = MenuListUnidades(
                widget, boton, pos, tiempo, path, self.get_model())
            menu.connect('accion', self.__get_accion)
            menu.popup(None, None, None, None, boton, tiempo)

        elif boton == 2:
            return

    def __get_accion(self, widget, path, accion):

        iter_ = self.get_model().get_iter(path)
        direccion = self.get_model().get_value(iter_, 2)
        #lectura, escritura, ejecucion = describe_acceso_uri(direccion)

        if accion == "Abrir":
            self.dir_select = direccion
            self.emit('add-leer', self.dir_select)
            self.emit('info', self.dir_select)

        '''
        if accion == "Copiar":
            self.copiando = direccion

        elif accion == "Borrar":
            self.copiando = direccion

            self.emit('borrar',
                self.copiando,
                self.get_model(), iter_)

            self.copiando = None

        elif accion == "Pegar":
            if self.cortando:
                if mover(self.cortando, direccion):
                    self.collapse_row(path)
                    self.expand_to_path(path)
                    self.cortando = None

            else:
                if copiar(self.copiando, direccion):
                    self.collapse_row(path)
                    self.expand_to_path(path)
                    self.copiando = None

        elif accion == "Cortar":
            self.cortando = direccion
            self.get_model().remove(iter_)
            self.copiando = None

        elif accion == "Crear Directorio":
            dialog = Gtk.Dialog(
                "Crear Directorio . . .",
                self.get_toplevel(),
                Gtk.DialogFlags.MODAL, None)

            etiqueta = Gtk.Label("Nombre del Directorio: ")
            entry = Gtk.Entry()
            dialog.vbox.pack_start(etiqueta, True, True, 5)
            dialog.vbox.pack_start(entry, True, True, 5)
            dialog.add_button("Crear Directorio", 1)
            dialog.add_button("Cancelar", 2)

            dialog.show_all()

            if dialog.run() == 1:
                directorio_nuevo = entry.get_text()

                if directorio_nuevo != "" and directorio_nuevo != None:
                    if crear_directorio(direccion, directorio_nuevo):
                        self.collapse_row(path)
                        self.expand_to_path(path)

            elif dialog.run() == 2:
                pass

            dialog.destroy()
    '''

    def __update_unidades(self, widget):
        """
        Cuando se Conecta o Desconecta una Unidad.
        """

        unidades = self.demonio_unidades.get_unidades()

        lista = {}
        for unidad in unidades.keys():
            dic = unidades.get(unidad, False)

            if dic:
                #label = dic.get('label', "")
                mount_path = dic.get('mount_path', "")
                lista[mount_path.split("/")[-1]] = mount_path

        from gi.repository import GLib

        GLib.timeout_add(
            1000, self.__update_unidades2, lista)

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
                icono = os.path.join(ICONOS,
                    "drive-removable-media-usb.svg")
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    icono, get_pixels(0.8), -1)

                model.append([pixbuf, it, lista[it]])

        if remove_explorers:
            self.emit('remove_explorers', remove_explorers)

        return False

    def __setear_columnas(self):

        self.append_column(
            self.__construir_columa_icono('Icono', 0, True))
        self.append_column(
            self.__construir_columa('Nombre', 1, True))
        self.append_column(
            self.__construir_columa('Directorio', 2, False))

    def __construir_columa(self, text, index, visible):

        render = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(text, render, text=index)
        column.set_sort_column_id(index)
        column.set_property('visible', visible)

        return column

    def __construir_columa_icono(self, text, index, visible):

        render = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn(text, render, pixbuf=index)
        column.set_property('visible', visible)

        return column

    def __Llenar_ListStore(self):

        self.get_toplevel().set_sensitive(False)

        import commands

        icono = os.path.join(ICONOS, "def.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, get_pixels(0.8), -1)
        self.get_model().append([pixbuf, 'Raiz', ROOT])

        icono = os.path.join(ICONOS, "stock-home.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, get_pixels(0.8), -1)
        self.get_model().append([pixbuf,
            commands.getoutput('whoami'), HOME])

        if describe_uri(ACTIVITIES):
            icono = os.path.join(ICONOS, "stock-home.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'Actividades', ACTIVITIES])

        if describe_uri(JAMEDIA):
            icono = os.path.join(ICONOS, "JAMedia.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'JAMediaDatos', JAMEDIA])

        if describe_uri(DIARIO):
            icono = os.path.join(ICONOS, "diario.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'Diario', DIARIO])

        if describe_uri(LOGS):
            icono = os.path.join(ICONOS, "diario.svg")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                icono, get_pixels(0.8), -1)
            self.get_model().append([pixbuf, 'Logs', LOGS])

        icono = os.path.join(ICONOS, "drive-removable-media-usb.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, get_pixels(0.8), -1)

        unidades = self.demonio_unidades.get_unidades()

        for unidad in unidades.keys():
            dic = unidades.get(unidad, False)

            if dic:
                #label = dic.get('label', "")
                mount_path = dic.get('mount_path', "")

                self.get_model().append([
                    pixbuf, mount_path.split("/")[-1], mount_path])

        self.get_toplevel().set_sensitive(True)

    def select_home(self):

        self.get_toplevel().set_sensitive(False)

        self.get_selection().select_path(1)
        modelo, iter_ = self.get_selection().get_selected()

        if iter_:
            #iter_ = self.get_model().iter_next(iter_)
            self.get_selection().select_iter(iter_)

            #if self.dir_select != directorio:
            self.dir_select = self.get_model().get_value(iter_, 2)
            self.emit('leer', self.dir_select)
            self.emit('info', self.dir_select)

        self.get_toplevel().set_sensitive(True)

        return False


class MenuListUnidades(Gtk.Menu):

    __gtype_name__ = 'JAMediaExplorerMenuListUnidades'

    __gsignals__ = {
    "accion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        Gtk.Menu.__init__(self)

        self.modelo = modelo
        self.parent_objet = widget

        #lectura, escritura, ejecucion = (False, False, False)
        #unidad, directorio, archivo, enlace = (False, False, False, False)

        #iter_ = self.modelo.get_iter(path)
        #direccion = self.modelo.get_value(iter_, 2)

        #if describe_acceso_uri(direccion):
        #    lectura, escritura, ejecucion = describe_acceso_uri(direccion)
        #    unidad, directorio, archivo, enlace = describe_uri(direccion)

        #else:
        #    return

        abrir_pestania = Gtk.MenuItem("Abrir en Pestaña Nueva")
        self.append(abrir_pestania)
        abrir_pestania.connect_object("activate",
            self.__emit_accion, path, "Abrir")

        '''
        if lectura:
            copiar = Gtk.MenuItem("Copiar")
            self.append(copiar)
            copiar.connect_object("activate",
                self.__emit_accion, path, "Copiar")

        if escritura and not unidad:
            borrar = Gtk.MenuItem("Borrar")
            self.append(borrar)
            borrar.connect_object("activate",
                self.__emit_accion, path, "Borrar")

        if escritura and (directorio or unidad) \
            and (self.parent_objet.copiando != None \
            or self.parent_objet.cortando != None):

            pegar = Gtk.MenuItem("Pegar")
            self.append(pegar)
            pegar.connect_object("activate",
                self.__emit_accion, path, "Pegar")

        if escritura and (directorio or archivo):
            cortar = Gtk.MenuItem("Cortar")
            self.append(cortar)
            cortar.connect_object("activate",
                self.__emit_accion, path, "Cortar")

        if escritura and (directorio or unidad):
            nuevodirectorio = Gtk.MenuItem("Crear Directorio")
            self.append(nuevodirectorio)
            nuevodirectorio.connect_object("activate",
                self.__emit_accion, path, "Crear Directorio")
        '''

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):

        pass

    def __emit_accion(self, path, accion):

        self.emit('accion', path, accion)


class InfoWidget(Gtk.EventBox):
    """
    Widgets con información sobre en path
    seleccionado en la estructura de directorios y archivos.
    """

    __gtype_name__ = 'JAMediaExplorerInfoWidget'

    __gsignals__ = {
    "cargar": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.normal_color = Gdk.Color(65000, 65000, 65000)
        self.select_color = Gdk.Color(61686, 65000, 48431)
        self.clicked_color = Gdk.Color(61686, 65000, 17078)

        self.modify_bg(0, self.normal_color)
        #self.set_tooltip_text("Click para Ver el Archivo.")

        self.typeinfo = None

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.label = Gtk.Label("")
        self.imagen = Gtk.Image()
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

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, 100, -1)
        self.imagen.set_from_pixbuf(pixbuf)

    def do_button_press_event(self, widget):
        """
        Cuando se hace click, se emite la señal
        cargar y se pasa el tipo de archivo para que la
        aplicacion decida si abrir o no otra aplicacion
        embebida que sepa tratar el archivo.
        """

        self.modify_bg(0, self.clicked_color)
        self.imagen.modify_bg(0, self.clicked_color)

        if self.typeinfo:
            self.emit('cargar', self.typeinfo)

    def do_button_release_event(self, widget):

        self.modify_bg(0, self.select_color)
        self.imagen.modify_bg(0, self.select_color)

    def do_enter_notify_event(self, widget):

        self.modify_bg(0, self.select_color)
        self.imagen.modify_bg(0, self.select_color)

    def do_leave_notify_event(self, widget):

        self.modify_bg(0, self.normal_color)
        self.imagen.modify_bg(0, self.normal_color)
