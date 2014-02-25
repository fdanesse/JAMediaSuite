#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import GdkPixbuf


class MenuBar(Gtk.MenuBar):

    __gtype_name__ = 'UbuntuRadioMenu'

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'lista': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'actualizar': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    #'accion_archivo': (GObject.SIGNAL_RUN_FIRST,
    #    GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
        }

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        item1 = Gtk.MenuItem('Menú')
        menu = Gtk.Menu()
        item1.set_submenu(menu)

        item = Gtk.MenuItem('Radios')
        item.connect("activate", self.__listar_radios)
        menu.append(item)
        '''
        item = Gtk.MenuItem('Configurar...')
        item.connect("activate", self.__configurar)
        menu.append(item)
        '''
        item = Gtk.MenuItem('Creditos...')
        item.connect("activate", self.__creditos)
        menu.append(item)

        item = Gtk.MenuItem('Actualizar Lista')
        item.connect("activate", self.__emit_actualizar)
        menu.append(item)

        item = Gtk.MenuItem('Salir')
        item.connect("activate", self.__emit_salir)
        menu.append(item)

        self.append(item1)

        self.show_all()

    def __creditos(self, widget):

        dialog = Creditos(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __emit_actualizar(self, widget):

        self.emit("actualizar")

    def __configurar(self, widget):

        print "Configurar"

    def __listar_radios(self, widget):

        '''
        dialog = Dialogo_Radios(self.get_toplevel())
        dialog.run()
        dialog.destroy()
        '''

        self.emit("lista")

    def __emit_salir(self, widget):

        self.emit("salir")


class Lista(Gtk.TreeView):

    __gtype_name__ = 'UbuntuRadioLista'

    def __init__(self):

        Gtk.TreeView.__init__(self,
            Gtk.ListStore(
                GdkPixbuf.Pixbuf,
                GObject.TYPE_STRING,
                GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.__setear_columnas()

        self.get_selection().set_select_function(
            self.__selecciones, self.get_model())

        self.show_all()

    '''
    def keypress(self, widget, event):
        # derecha 114 izquierda 113 suprimir 119
        # backspace 22 (en xo no existe suprimir)
        tecla = event.get_keycode()[1]
        model, iter = self.treeselection.get_selected()
        valor = self.modelo.get_value(iter, 2)
        path = self.modelo.get_path(iter)
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        elif tecla == 119:
            # suprimir
            print valor, path
        else:
            pass
        return False'''

    def __selecciones(self, treeselection,
        model, path, is_selected, listore):

        _iter = model.get_iter(path)
        self.scroll_to_cell(model.get_path(_iter))

        return True

    def __setear_columnas(self):

        self.append_column(self.__construir_columa_icono('', 0, True))
        self.append_column(self.__construir_columa('Emisora', 1, True))
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

    def __ejecutar_agregar_elemento(self, elementos):

        if not elementos:
            self.get_selection().select_path(0)
            return False

        texto, path = elementos[0]
        pixbuf = None
        paises = [
            "uruguay", "rusia",
            "alemania", "colombia",
            "libano", "venezuela",
            "eeuu"]

        for pais in paises:
            if pais in texto.lower().replace(
                "(", "").replace(")", "").split():

                icono = os.path.join(os.path.dirname(__file__),
                    "Iconos", "%s.svg" % pais)

                if os.path.exists(icono):
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                        icono, 24, -1)

                break

        self.get_model().append([pixbuf, texto, path])

        elementos.remove(elementos[0])

        GLib.idle_add(self.__ejecutar_agregar_elemento, elementos)

        return False

    def limpiar(self):

        self.get_model().clear()

    def agregar_items(self, elementos):

        GLib.idle_add(
            self.__ejecutar_agregar_elemento,
            elementos)


class Volumen(Gtk.VolumeButton):

    __gtype_name__ = 'UbuntuRadioVolumen'

    __gsignals__ = {
    "volumen": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}

    def __init__(self):

        Gtk.VolumeButton.__init__(self)

        self.show_all()

    def do_value_changed(self, valor):

        self.emit('volumen', valor)


class ItemPlayer(Gtk.Frame):

    __gtype_name__ = 'UbuntuRadioItemPlayer'

    def __init__(self, valor):

        Gtk.Frame.__init__(self)

        self.tipo = "Reproductor"
        self.player_estado = "None"
        self.name, self.uri = valor

        self.set_label("Reproduciendo . . .")

        eventbox = Gtk.EventBox()
        eventbox.set_border_width(5)

        hbox = Gtk.HBox()
        self.control_volumen = Volumen()

        self.stop_button = Gtk.Button()
        self.image_button = Gtk.Image()
        self.image_button.set_from_stock(
                Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
        self.stop_button.set_image(self.image_button)

        hbox.pack_start(Gtk.Label(self.name),
            False, False, 0)
        hbox.pack_end(self.stop_button,
            False, False, 0)
        hbox.pack_end(self.control_volumen,
            False, False, 0)

        eventbox.add(hbox)
        self.add(eventbox)

        self.control_volumen.set_value(0.10)

        self.show_all()

        self.control_volumen.connect(
            "volumen", self.__set_volume)
        self.stop_button.connect(
            "clicked", self.stop)

        from Player import MyPlayBin

        self.player = MyPlayBin(self.uri, 0.10)
        self.player.connect("estado", self.__update)
        self.player.play()

    def __update(self, player, valor):

        self.player_estado = valor

        if valor == "playing":
            self.image_button.set_from_stock(
                Gtk.STOCK_MEDIA_STOP, Gtk.IconSize.BUTTON)

        else:
            self.image_button.set_from_stock(
                Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)

        GLib.idle_add(self.get_toplevel().queue_draw)

    def __set_volume(self, widget, valor):

        self.player.set_volumen(valor)

    def stop(self, widget=False):

        if self.player_estado == "playing":
            self.player.stop()

        else:
            self.player.play()


class MenuList(Gtk.Menu):

    __gtype_name__ = 'UbuntuRadioMenuList'

    __gsignals__ = {
    'accion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        Gtk.Menu.__init__(self)

        iter = modelo.get_iter(path)
        uri = modelo.get_value(iter, 2)

        from Globales import get_data_directory
        from Globales import stream_en_archivo

        play = Gtk.MenuItem("Reproducir")
        self.append(play)
        play.connect_object("activate", self.__set_accion,
            widget, path, "play")

        '''
        listas = [
            os.path.join(get_data_directory(), "JAMediaRadio.JAMedia"),
            ]

        if stream_en_archivo(uri, listas[0]):

            copiar = Gtk.MenuItem("Copiar a JAMedia")
            self.append(copiar)
            copiar.connect_object("activate", self.__set_accion,
                widget, path, "Copiar")

            mover = Gtk.MenuItem("Mover a JAMedia")
            self.append(mover)
            mover.connect_object("activate", self.__set_accion,
                widget, path, "Mover")
        '''

        quitar = Gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Quitar")

        borrar = Gtk.MenuItem("Borrar Streaming")
        self.append(borrar)
        borrar.connect_object(
            "activate", self.__set_accion,
            widget, path, "Borrar")

        grabar = Gtk.MenuItem("Grabar")
        self.append(grabar)
        grabar.connect_object("activate", self.__set_accion,
            widget, path, "Grabar")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __set_accion(self, widget, path, accion):

        iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, iter)


class DialogoDescarga(Gtk.Dialog):

    __gtype_name__ = 'UbuntuRadioDialogoDescarga'

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL)

        self.set_border_width(15)

        label = Gtk.Label("*** Descargando Streamings ***")
        label.show()

        self.vbox.pack_start(label, True, True, 5)

        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):

        GLib.timeout_add(500, self.__descargar)

    def __descargar(self):

        from Globales import get_streaming_default
        get_streaming_default()

        self.destroy()


class Creditos(Gtk.Dialog):

    __gtype_name__ = 'UbuntuRadioCreditos'

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_border_width(15)
        self.set_decorated(False)
        self.set_resizable(False)

        imagen = Gtk.Image()
        imagen.set_from_file(
            os.path.join(os.path.dirname(__file__),
                "Iconos", "creditos.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()