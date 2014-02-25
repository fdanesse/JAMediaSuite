#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   UbuntuRadio.py por:
#   Flavio Danesse <fdanesse@gmail.com>

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
from gi.repository import GLib

from Widgets import MenuBar
from Widgets import Lista
from Widgets import ItemPlayer

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(
    os.path.dirname(__file__), "Estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)


class UbuntuRadio(Gtk.Window):

    __gtype_name__ = 'UbuntuRadio'

    def __init__(self):

        Gtk.Window.__init__(self)

        # FIXME: Leer config
        self.config = {
            "opacity": 0.8}

        self.set_title("Ubuntu Radio")

        self.set_icon_from_file(
            os.path.join(os.path.dirname(__file__),
            "Iconos", "ubuntu_radio.svg"))

        self.set_size_request(200, 400)
        self.set_border_width(5)
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_opacity(self.config["opacity"])

        vbox = Gtk.VBox()

        menu = MenuBar()
        eventbox = Gtk.EventBox()
        self.inplay = Gtk.VBox()
        eventbox.add(self.inplay)
        self.lista = Lista()

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        self.scroll.add(self.lista)

        vbox.pack_start(menu, False, False, 0)
        vbox.pack_start(eventbox, False, False, 0)
        vbox.pack_start(self.scroll, True, True, 0)

        self.add(vbox)

        self.connect("realize", self.__load_lista)

        self.show_all()

        menu.connect("lista", self.__show_lista)
        menu.connect("actualizar", self.__actualizar_lista)
        menu.connect("salir", self.__exit)

        self.lista.connect(
            "button-press-event",
            self.__get_menu_lista)

        self.connect("delete-event", self.__exit)

    def __get_menu_lista(self, widget, event):
        """
        Despliega menu contextual de elemento en lista.
        """

        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)

        try:
            path_pos = widget.get_path_at_pos(int(pos[0]), int(pos[1]))
            path, columna, xdefondo, ydefondo = path_pos

        except:
            return

        from Widgets import MenuList

        menu = MenuList(widget, boton, pos,
            tiempo, path, widget.get_model())

        menu.connect('accion', self.__set_accion)
        menu.popup(None, None, None, None, boton, tiempo)

    def __set_accion(self, widget, lista, accion, _iter):
        """
        Responde a las selecciones en el menu contextual
        de elemento en lista.
        """

        name = lista.get_model().get_value(_iter, 1)
        uri = lista.get_model().get_value(_iter, 2)

        if accion == "play":
            self.__load_play((name, uri))

        #elif accion == "Copiar":
        #    print accion

        #elif accion == "Mover":
        #    print accion

        elif accion == "Quitar":
            items = self.inplay.get_children()

            for item in items:
                if name == item.name and uri == item.uri:
                    item.stop()
                    self.inplay.remove(item)
                    item.destroy()
                    break

            lista.get_model().remove(_iter)

        elif accion == "Borrar":
            items = self.inplay.get_children()

            for item in items:
                if name == item.name and uri == item.uri:
                    item.stop()
                    self.inplay.remove(item)
                    item.destroy()
                    break

            lista.get_model().remove(_iter)

            from Globales import eliminar_streaming

            eliminar_streaming(uri, "JAM-Radio")
            print "Streaming Eliminado:", name, uri

        elif accion == "Grabar":
            print accion

    def __actualizar_lista(self, widget):
        """
        Actualiza la Lista de Streamings desde la Web
        """

        #FIXME: Agregar control de conexión para evitar errores.
        from Widgets import DialogoDescarga

        dialog = DialogoDescarga(parent=self.get_toplevel())
        dialog.run()

        self.__load_lista()

    def __load_lista(self, widget=None):
        """
        Carga La Lista de Radios.
        """

        from Globales import set_listas_default
        from Globales import get_data_directory
        from Globales import get_streamings

        set_listas_default()

        archivo = os.path.join(
            get_data_directory(),
            'JAMediaRadio.JAMedia')

        items = get_streamings(archivo)
        self.lista.limpiar()
        self.lista.agregar_items(items)

    def __load_play(self, valor):
        """
        Reproduce un streaming.
        """

        items = self.inplay.get_children()

        for item in items:
            if item.tipo == "Reproductor":
                name, uri = valor

                if name == item.name and uri == item.uri:
                    return

                else:
                    item.stop()
                    self.inplay.remove(item)
                    item.destroy()

        self.inplay.pack_start(
            ItemPlayer(valor), False, False, 0)

    def __show_lista(self, widget):
        """
        Muestra u Oculta la Lista de Radios.
        """

        val = self.scroll.get_visible()

        if val:
            self.scroll.hide()
            self.set_size_request(200, 10)

        else:
            self.scroll.show()
            self.set_size_request(200, 400)

    def __exit(self, widget=None, event=None):

        import sys
        sys.exit(0)


if __name__ == "__main__":

    UbuntuRadio()
    Gtk.main()
