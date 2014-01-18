#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Previews.py por:
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
#from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

from Widgets import ToolbarPreviews
from Widgets import ToolbarTry

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaObjects.JAMFileSystem import describe_archivo


class Previews (Gtk.EventBox):
    """
    Vista Preview de directorios con imágenes y albumes.
    """

    __gtype_name__ = 'JAMediaImagenesPreviews'

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'switch_to': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'camara': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, path):

        Gtk.EventBox.__init__(self)

        self.path = path  # Directorio

        base_box = Gtk.VBox()

        self.toolbar = ToolbarPreviews(path)
        self.iconview = IconView(path)
        self.toolbartry = ToolbarTry()

        base_box.pack_start(self.toolbar, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.iconview)

        base_box.pack_start(scroll, True, True, 0)
        base_box.pack_end(self.toolbartry, False, False, 0)

        self.add(base_box)

        self.show_all()

        self.iconview.connect('switch_to', self.__emit_switch)

        self.toolbar.connect('camara', self.__emit_camara)
        self.toolbar.connect('switch_to', self.__emit_switch)
        self.toolbar.connect('salir', self.__salir)
        self.toolbar.connect('open', self.__emit_switch)

        ### Activar botón atras solo si no se está en home del usuario.
        if os.path.dirname(self.path) == os.path.dirname(os.environ["HOME"]):
            self.toolbar.hide_button_back()

        self.connect("motion-notify-event",
            self.__do_motion_notify_event)
        self.iconview.connect('motion',
            self.__do_motion_notify_event)
        self.iconview.connect("button-press-event",
            self.__click_derecho_en_lista)

    def __click_derecho_en_lista(self, widget, event):
        """
        Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista de imágenes, permitiendo copiar, mover y
        borrar el archivo o simplemente quitarlo
        de la lista.
        """

        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time

        if boton == 1:
            return

        elif boton == 3:

            path = widget.get_path_at_pos(
                int(pos[0]), int(pos[1]))
            #iter = widget.get_model().get_iter(path)

            from Widgets import MenuList

            menu = MenuList(
                widget, boton, pos,
                tiempo, path, widget.get_model(),
                self.path)

            menu.connect('accion', self.__set_menu_accion)
            menu.popup(None, None, None, None, boton, tiempo)

        elif boton == 2:
            return

    def __set_menu_accion(self, widget, widget_item, accion, iter, file_path):

        if accion == "Quitar":
            widget_item.get_model().remove(iter)

        elif accion == "Borrar":
            from JAMediaObjects.JAMFileSystem import borrar
            widget_item.get_model().remove(iter)

            borrar(file_path)

        elif accion == "Copiar":
            from Globales import get_imagenes_directory
            from JAMediaObjects.JAMFileSystem import copiar

            copiar(file_path, get_imagenes_directory())

        elif accion == "Mover":
            from Globales import get_imagenes_directory
            from JAMediaObjects.JAMFileSystem import mover
            widget_item.get_model().remove(iter)

            mover(file_path, get_imagenes_directory())

    def __do_motion_notify_event(self, widget, event):
        """
        Cuando se mueve el mouse sobre la ventana se
        muestran u ocultan las toolbars.
        """

        rect = self.toolbar.get_allocation()
        arriba = range(0, rect.height)

        root_rect = self.get_toplevel().get_allocation()
        rect = self.toolbartry.get_allocation()
        abajo = range(root_rect.height - rect.height, root_rect.height)
        x, y = self.get_toplevel().get_pointer()

        if y in arriba or y in abajo:
            self.toolbar.show()
            self.toolbartry.show()
            return

        else:
            self.toolbar.hide()
            self.toolbartry.hide()
            return

    def __emit_camara(self, widget):

        self.emit("camara")

    def __emit_switch(self, widget, path):

        self.emit("switch_to", path)

    def __salir(self, widget):

        self.emit("salir")

    def run(self):

        self.iconview.load_previews(self.path)
        self.toolbartry.set_info("Directorio: %s" % self.path)


class IconView(Gtk.IconView):
    """
    http://python-gtk-3-tutorial.readthedocs.org/en/latest/iconview.html

    Widget Contenedor de portadas para directorios
    con imágenes o imágenes.
    """

    __gtype_name__ = 'JAMediaImagenesIconView'

    __gsignals__ = {
    'switch_to': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'motion': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}

    def __init__(self, path):

        Gtk.IconView.__init__(self)

        self.path = path

        self.previews = Gtk.ListStore(
            GdkPixbuf.Pixbuf,
            GObject.TYPE_STRING)

        self.set_model(self.previews)
        self.set_pixbuf_column(0)
        self.set_text_column(1)

        self.set_margin(10)
        self.set_column_spacing(10)
        self.set_row_spacing(10)
        self.set_item_padding(10)

        self.set_columns(-1)
        self.set_item_width(-1)

        self.set_selection_mode(Gtk.SelectionMode.SINGLE)

        self.show_all()

        self.connect("motion-notify-event",
            self.__do_motion_notify_event)

    def __do_motion_notify_event(self, widget, event):
        """
        Cuando se mueve el mouse sobre la ventana.
        """

        self.emit("motion", event)

    def load_previews(self, basepath):
        """
        Crea y carga los previews de imagen de los archivos
        contenidos en basepath.
        """

        imagen_en_path = False

        self.get_toplevel().set_sensitive(False)

        self.path = basepath

        for temp_path in os.listdir(self.path):
            path = os.path.join(self.path, temp_path)

            if not os.access(path, os.R_OK):
                continue

            if os.path.isdir(path):

                for archivo in os.listdir(path):
                    new_path = os.path.join(path, archivo)

                    if os.path.isfile(new_path):
                        descripcion = describe_archivo(new_path)

                        if 'image' in descripcion and not 'iso' in descripcion:
                            try:
                                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                    new_path, 200, -1)
                                self.previews.append(
                                    [pixbuf, path.split("/")[-1]])

                                while Gtk.events_pending():
                                    Gtk.main_iteration()

                            except:
                                pass

                            break

            elif os.path.isfile(path):
                descripcion = describe_archivo(path)

                if 'image' in descripcion and not 'iso' in descripcion:
                    try:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                            path, 200, -1)
                        self.previews.append([pixbuf, path.split("/")[-1]])

                        imagen_en_path = True

                        while Gtk.events_pending():
                            Gtk.main_iteration()

                    except:
                        pass

        self.get_toplevel().set_sensitive(True)
        return imagen_en_path

    def do_selection_changed(self):
        """
        Cuando se selecciona un item.
        """

        self.get_toplevel().set_sensitive(False)

        try:
            path = self.get_selected_items()[0].to_string()

        except:
            return

        iter = self.get_model().get_iter(path)
        valor = self.get_model().get_value(iter, 1)

        self.emit("switch_to", os.path.join(self.path, valor))
    '''
    def do_motion_notify_event(self, event):
        """
        Cuando se mueve el mouse sobre la ventana.
        """

        pass'''
