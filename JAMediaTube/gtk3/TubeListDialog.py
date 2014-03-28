#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   TubeListDialog.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

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
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import GLib

BASE_PATH = os.path.dirname(__file__)


class TubeListDialog(Gtk.Dialog):

    __gtype_name__ = 'TubeListDialog'

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_border_width(15)
        rect = parent.get_allocation()
        self.set_size_request(rect.width - 15, rect.height - 25)

        self.actualizando = False

        self.panel = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)

        self.listas = Lista()
        self.videos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        scroll = self.__get_scroll()
        scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.listas)
        self.panel.pack1(scroll, resize=False, shrink=True)

        scroll = self.__get_scroll()
        scroll.add_with_viewport(self.videos)
        self.panel.pack2(scroll, resize=True, shrink=False)

        self.label = Gtk.Label("")
        self.vbox.pack_start(self.label, False, False, 0)
        self.vbox.pack_start(self.panel, True, True, 0)
        self.vbox.show_all()

        self.listas.connect("nueva-seleccion", self.__select_list)
        self.listas.connect("button-press-event",
            self.__click_derecho_en_lista)
        self.connect("realize", self.__do_realize)

    def __click_derecho_en_lista(self, widget, event):
        """
        Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista.
        """

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
            return

        elif boton == 3:
            menu = Gtk.Menu()
            borrar = Gtk.MenuItem("Eliminar")
            menu.append(borrar)

            borrar.connect_object(
                "activate", self.__eliminar,
                widget, path)

            menu.show_all()
            menu.attach_to_widget(widget, self.__null)

            menu.popup(None, None, None, None, boton, tiempo)

        elif boton == 2:
            return

    def __null(self):
        pass

    def __eliminar(self, widget, path):
        """
        Elimina una lista del archivo shelve.
        """

        if self.actualizando:
            return

        for child in self.videos.get_children():
            self.videos.remove(child)
            child.destroy()

        new_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        new_box.show_all()
        self.videos.pack_start(
            new_box,
            True, True, 0)

        iter = widget.get_model().get_iter(path)
        key = widget.get_model().get_value(iter, 2)

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        del(dict_tube[key])

        keys = dict_tube.keys()

        dict_tube.close()

        widget.get_model().remove(iter)

        if not keys:
            dialog = Gtk.Dialog(
                parent=self.get_toplevel(),
                flags=Gtk.DialogFlags.MODAL,
                buttons=["OK", Gtk.ResponseType.ACCEPT])

            dialog.set_border_width(15)

            label = Gtk.Label("Todas las Listas han sido Eliminadas.")
            dialog.vbox.pack_start(label, True, True, 0)
            dialog.vbox.show_all()

            dialog.run()

            dialog.destroy()

            self.destroy()

    def __select_list(self, widget, valor):
        """
        Cuando se selecciona una lista, se cargan
        los videos que contiene en self.videos.
        """

        self.actualizando = True

        self.panel.set_sensitive(False)

        for child in self.videos.get_children():
            self.videos.remove(child)
            child.destroy()

        new_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        new_box.show_all()
        self.videos.pack_start(
            new_box,
            True, True, 0)

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        videos = []
        for item in dict_tube[valor].keys():
            videos.append(dict_tube[valor][item])

        dict_tube.close()

        GLib.idle_add(self.__add_videos, videos)

    def __add_videos(self, videos):
        """
        Se crean los video_widgets de videos y
        se agregan al panel, segun destino.
        """

        if not videos:
            self.label.set_text("%s Videos Listados." % len(
                self.videos.get_children()[0].get_children()))
            self.panel.set_sensitive(True)
            self.actualizando = False
            return False

        self.label.set_text("Listando Videos . . .  Quedan %s" % len(videos))

        video = videos[0]

        from Widgets import WidgetVideoItem
        videowidget = WidgetVideoItem(video)
        videowidget.connect("click_derecho", self.__clicked_videowidget)

        videowidget.show_all()
        videos.remove(video)

        try:
            self.videos.get_children()[0].pack_start(
                videowidget, False, False, 1)

        except:
            return False

        GLib.idle_add(self.__add_videos, videos)

    def __clicked_videowidget(self, widget, event):
        """
        Cuando se hace click derecho sobre un video item.
        """

        boton = event.button
        #pos = (event.x, event.y)
        tiempo = event.time

        menu = Gtk.Menu()
        borrar = Gtk.MenuItem("Eliminar")
        menu.append(borrar)

        borrar.connect_object(
            "activate", self.__eliminar_video,
            widget)

        menu.show_all()
        menu.attach_to_widget(widget, self.__null)

        menu.popup(None, None, None, None, boton, tiempo)

    def __eliminar_video(self, widget):

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        if len(dict_tube[self.listas.valor_select].keys()) == 1:
            modelo, iter = self.listas.treeselection.get_selected()
            path = modelo.get_path(iter)
            self.__eliminar(self.listas, path)

        else:
            videos = {}
            for id in dict_tube[self.listas.valor_select].keys():
                if id != widget.videodict["id"]:
                    videos[id] = dict_tube[self.listas.valor_select][id]

            dict_tube[self.listas.valor_select] = videos

            widget.destroy()
            self.label.set_text("%s Videos Listados." % len(
                self.videos.get_children()[0].get_children()))

        dict_tube.close()

    def __do_realize(self, widget):
        """
        Carga la lista de Albums de Descargas en self.listas.
        """

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        keys = dict_tube.keys()

        dict_tube.close()

        lista = []
        for key in keys:
            lista.append([key, key])

        self.listas.agregar_items(lista)

    def __get_scroll(self):

        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        return scroll


class Lista(Gtk.TreeView):
    """
    Lista generica.
    """

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.TreeView.__init__(self,Gtk.ListStore(
            GdkPixbuf.Pixbuf,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.permitir_select = True
        self.valor_select = None

        self.__setear_columnas()

        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()

    def __selecciones(self, treeselection,
        model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """

        if not self.permitir_select:
            return True

        # model y listore son ==
        _iter = model.get_iter(path)
        valor = model.get_value(_iter, 2)

        if not is_selected and self.valor_select != valor:
            self.scroll_to_cell(model.get_path(_iter))
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)

        return True

    def __setear_columnas(self):

        self.append_column(self.__construir_columa_icono('', 0, True))
        self.append_column(self.__construir_columa('Nombre', 1, True))
        self.append_column(self.__construir_columa('', 2, False))

    def __construir_columa(self, text, index, visible):

        render = Gtk.CellRendererText()

        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        return columna

    def __construir_columa_icono(self, text, index, visible):

        render = Gtk.CellRendererPixbuf()

        columna = Gtk.TreeViewColumn(text, render, pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        return columna

    def limpiar(self):

        self.permitir_select = False
        self.get_model().clear()
        self.permitir_select = True

    def agregar_items(self, elementos):
        """
        Recibe lista de: [texto para mostrar, path oculto] y
        Comienza secuencia de agregado a la lista.
        """

        self.get_toplevel().set_sensitive(False)
        self.permitir_select = False

        GLib.idle_add(self.__ejecutar_agregar_elemento, elementos)

    def __ejecutar_agregar_elemento(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """

        if not elementos:
            self.permitir_select = True
            self.seleccionar_primero()
            self.get_toplevel().set_sensitive(True)
            return False

        texto, path = elementos[0]

        icono = os.path.join(BASE_PATH,
            "Iconos", "video.svg")

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
                24, -1)
            self.get_model().append([pixbuf, texto, path])

        except:
            pass

        elementos.remove(elementos[0])

        GLib.idle_add(self.__ejecutar_agregar_elemento, elementos)

        return False

    def seleccionar_primero(self, widget=None):

        self.get_selection().select_path(0)
