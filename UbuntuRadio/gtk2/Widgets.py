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

import gtk
from gtk import gdk
import gobject
from gtk.gdk import Pixbuf


class MenuBar(gtk.MenuBar):

    __gtype_name__ = 'UbuntuRadioMenu'

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'lista': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'actualizar': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'configurar': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
        }

    def __init__(self):

        gtk.MenuBar.__init__(self)

        item1 = gtk.MenuItem('Menú')
        menu = gtk.Menu()
        item1.set_submenu(menu)

        item = gtk.MenuItem('Radios')
        item.connect("activate", self.__listar_radios)
        menu.append(item)

        item = gtk.MenuItem('Configurar...')
        item.connect("activate", self.__configurar)
        menu.append(item)

        item = gtk.MenuItem('Creditos...')
        item.connect("activate", self.__creditos)
        menu.append(item)

        item = gtk.MenuItem('Actualizar Lista')
        item.connect("activate", self.__emit_actualizar)
        menu.append(item)

        item = gtk.MenuItem('Salir')
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

        self.emit("configurar")

    def __listar_radios(self, widget):

        self.emit("lista")

    def __emit_salir(self, widget):

        self.emit("salir")


class Lista(gtk.TreeView):

    __gtype_name__ = 'UbuntuRadioLista'

    def __init__(self):

        gtk.TreeView.__init__(self,
            gtk.ListStore(
                Pixbuf,
                gobject.TYPE_STRING,
                gobject.TYPE_STRING))

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

        render = gtk.CellRendererText()

        columna = gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TreeViewColumnSizing.AUTOSIZE)

        return columna

    def __construir_columa_icono(self, text, index, visible):

        render = gtk.CellRendererPixbuf()

        columna = gtk.TreeViewColumn(text, render, pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TreeViewColumnSizing.AUTOSIZE)

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
                    pixbuf = Pixbuf.new_from_file_at_size(
                        icono, 24, -1)

                break

        self.get_model().append([pixbuf, texto, path])

        elementos.remove(elementos[0])

        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)

        return False

    def limpiar(self):

        self.get_model().clear()

    def agregar_items(self, elementos):

        gobject.idle_add(
            self.__ejecutar_agregar_elemento,
            elementos)


class Volumen(gtk.VolumeButton):

    __gtype_name__ = 'UbuntuRadioVolumen'

    __gsignals__ = {
    "volumen": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.VolumeButton.__init__(self)

        self.show_all()

    def do_value_changed(self, valor):

        self.emit('volumen', valor)


class ItemPlayer(gtk.Frame):

    __gtype_name__ = 'UbuntuRadioItemPlayer'

    def __init__(self, valor):

        gtk.Frame.__init__(self)

        self.tipo = "Reproductor"
        self.player_estado = "None"
        self.name, self.uri = valor

        self.set_label(" Reproduciendo . . . ")

        eventbox = gtk.EventBox()
        eventbox.set_border_width(5)

        hbox = gtk.HBox()
        self.control_volumen = Volumen()

        self.stop_button = gtk.Button()
        self.image_button = gtk.Image()
        self.image_button.set_from_stock(
                gtk.STOCK_MEDIA_PLAY, gtk.IconSize.BUTTON)
        self.stop_button.set_image(self.image_button)

        hbox.pack_start(gtk.Label(self.name),
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
        self.player.connect("estado", self.__update_estado)
        self.player.connect("endfile", self.__endfile)
        self.player.play()

    def __endfile(self, player):

        self.image_button.set_from_stock(
            gtk.STOCK_MEDIA_PLAY, gtk.IconSize.BUTTON)

        gobject.idle_add(self.get_toplevel().queue_draw)

    def __update_estado(self, player, valor):

        self.player_estado = valor

        if valor == "playing":
            self.image_button.set_from_stock(
                gtk.STOCK_MEDIA_STOP, gtk.IconSize.BUTTON)

        else:
            self.image_button.set_from_stock(
                gtk.STOCK_MEDIA_PLAY, gtk.IconSize.BUTTON)

        gobject.idle_add(self.get_toplevel().queue_draw)

    def __set_volume(self, widget, valor):

        self.player.set_volumen(valor)

    def stop(self, widget=False):

        if self.player_estado == "playing":
            self.player.stop()

        else:
            self.player.play()


class ItemRecord(gtk.Frame):

    __gtype_name__ = 'UbuntuRadioItemRecord'

    def __init__(self, valor, formato):

        gtk.Frame.__init__(self)

        self.tipo = "Grabador"
        self.player_estado = "None"
        self.name, self.uri = valor

        self.set_label(" Grabando . . . ")
        self.label_info = gtk.Label("Grabación Detenida")

        eventbox = gtk.EventBox()
        eventbox.set_border_width(5)

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        self.stop_button = gtk.Button()
        self.image_button = gtk.Image()
        self.image_button.set_from_stock(
                gtk.STOCK_MEDIA_RECORD, gtk.IconSize.BUTTON)
        self.stop_button.set_image(self.image_button)

        hbox.pack_start(gtk.Label(self.name),
            False, False, 0)
        hbox.pack_end(self.stop_button,
            False, False, 0)

        vbox.pack_start(hbox,
            False, False, 0)
        vbox.pack_start(self.label_info,
            False, False, 0)

        eventbox.add(vbox)
        self.add(eventbox)

        self.show_all()

        self.stop_button.connect(
            "clicked", self.stop)

        from Record import MyPlayBin

        self.player = MyPlayBin(self.uri, formato)
        self.player.connect("estado", self.__update_estado)
        self.player.connect("endfile", self.__endfile)
        self.player.connect("update", self.__update_info)
        self.player.play(self.name)

    def __update_info(self, player, info):

        self.label_info.set_text(info)

    def __endfile(self, player):

        self.image_button.set_from_stock(
            gtk.STOCK_MEDIA_RECORD, gtk.IconSize.BUTTON)

        self.label_info.set_text("Grabación Detenida")

        gobject.idle_add(self.get_toplevel().queue_draw)

    def __update_estado(self, player, valor):

        self.player_estado = valor

        if valor == "playing":
            self.image_button.set_from_stock(
                gtk.STOCK_MEDIA_STOP, gtk.IconSize.BUTTON)

        else:
            self.image_button.set_from_stock(
                gtk.STOCK_MEDIA_RECORD, gtk.IconSize.BUTTON)
            self.label_info.set_text("Grabación Detenida")

        gobject.idle_add(self.get_toplevel().queue_draw)

    def stop(self, widget=False):

        if self.player_estado == "playing":
            self.player.stop()

        else:
            self.player.play(self.name)


class MenuList(gtk.Menu):

    __gtype_name__ = 'UbuntuRadioMenuList'

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        gtk.Menu.__init__(self)

        iter = modelo.get_iter(path)
        uri = modelo.get_value(iter, 2)

        from Globales import get_data_directory
        from Globales import stream_en_archivo

        play = gtk.MenuItem("Reproducir")
        self.append(play)
        play.connect_object("activate", self.__set_accion,
            widget, path, "play")

        '''
        listas = [
            os.path.join(get_data_directory(), "JAMediaRadio.JAMedia"),
            ]

        if stream_en_archivo(uri, listas[0]):

            copiar = gtk.MenuItem("Copiar a JAMedia")
            self.append(copiar)
            copiar.connect_object("activate", self.__set_accion,
                widget, path, "Copiar")

            mover = gtk.MenuItem("Mover a JAMedia")
            self.append(mover)
            mover.connect_object("activate", self.__set_accion,
                widget, path, "Mover")
        '''

        quitar = gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Quitar")

        borrar = gtk.MenuItem("Borrar Streaming")
        self.append(borrar)
        borrar.connect_object(
            "activate", self.__set_accion,
            widget, path, "Borrar")

        grabar = gtk.MenuItem("Grabar")
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


class DialogoDescarga(gtk.Dialog):

    __gtype_name__ = 'UbuntuRadioDialogoDescarga'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            flags=gtk.DIALOG_MODAL)

        self.set_border_width(15)
        self.set_decorated(False)
        self.set_resizable(False)

        label = gtk.Label("*** Descargando Streamings ***")
        label.show()

        self.vbox.pack_start(label, True, True, 5)

        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):

        gobject.timeout_add(500, self.__descargar)

    def __descargar(self):

        from Globales import get_streaming_default
        get_streaming_default()

        self.destroy()


class Creditos(gtk.Dialog):

    __gtype_name__ = 'UbuntuRadioCreditos'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            flags=gtk.DIALOG_MODAL,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_border_width(15)
        self.set_decorated(False)
        self.set_resizable(False)

        imagen = gtk.Image()
        imagen.set_from_file(
            os.path.join(os.path.dirname(__file__),
                "Iconos", "creditos.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class DialogoConfig(gtk.Dialog):

    __gtype_name__ = 'UbuntuRadioDialogoConfig'

    def __init__(self, parent=None, config={}):

        gtk.Dialog.__init__(self,
            parent=parent,
            flags=gtk.DIALOG_MODAL,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_border_width(15)
        self.set_decorated(False)
        self.set_resizable(False)

        self.config = config

        frame_formatos = self.__get_frame_formatos()
        frame_colores = self.__get_frame_colores()
        frame_opacidad = self.__get_frame_opacidad()

        self.vbox.pack_start(
            frame_formatos, True, True, 5)
        self.vbox.pack_start(
            frame_colores, True, True, 5)
        self.vbox.pack_start(
            frame_opacidad, True, True, 5)

        self.vbox.show_all()

    def __get_frame_opacidad(self):

        frame = gtk.Frame()
        frame.set_border_width(5)
        frame.set_label(" Opacidad de Interfaz: ")

        escala = gtk.Scale()
        escala.set_adjustment(
            gtk.Adjustment(0.5, 0.5, 1.1, 0.1, 0.1, 0.1))
        escala.set_digits(1)
        #escala.set_draw_value(False)

        frame.add(escala)

        escala.set_value(self.config["opacidad"])
        escala.connect("value-changed", self.__set_opacidad)

        return frame

    def __get_frame_formatos(self):

        frame = gtk.Frame()
        frame.set_border_width(5)
        frame.set_label(" Formato de Grabación: ")

        hbox = gtk.HBox()

        botones = [
            gtk.RadioButton("ogg"),
            gtk.RadioButton("mp3"),
            gtk.RadioButton("wav"),
            ]

        for boton in botones:
            boton.connect("toggled", self.__set_formato)
            hbox.pack_start(boton, True, True, 0)

        for boton in botones[1:]:
            boton.join_group(botones[0])
            if boton.get_label() == self.config["formato"]:
                boton.set_active(True)

        frame.add(hbox)

        return frame

    def __get_frame_colores(self):

        frame = gtk.Frame()
        frame.set_border_width(5)
        frame.set_label(" Colores de la Aplicación: ")

        vbox = gtk.VBox()

        hbox1 = gtk.HBox()
        boton_ventana = gtk.ColorButton()
        boton_ventana.set_title("color_ventana")
        boton_ventana.set_color(
            gdk.color_parse(self.config["color_ventana"]))
        boton_ventana.connect("color-set", self.__set_config)
        hbox1.pack_start(boton_ventana, False, False, 3)
        hbox1.pack_start(gtk.Label("Ventana"), False, False, 3)

        hbox2 = gtk.HBox()
        boton_ventana = gtk.ColorButton()
        boton_ventana.set_title("color_fuente_ventana")
        boton_ventana.set_color(
            gdk.color_parse(self.config["color_fuente_ventana"]))
        boton_ventana.connect("color-set", self.__set_config)
        hbox2.pack_start(boton_ventana, False, False, 3)
        hbox2.pack_start(gtk.Label("Fuentes"), False, False, 3)

        hbox3 = gtk.HBox()
        boton_menu = gtk.ColorButton()
        boton_menu.set_title("color_menu")
        boton_menu.set_color(
            gdk.color_parse(self.config["color_menu"]))
        boton_menu.connect("color-set", self.__set_config)
        hbox3.pack_start(boton_menu, False, False, 3)
        hbox3.pack_start(gtk.Label("Fondo del Menú"), False, False, 3)

        hbox4 = gtk.HBox()
        boton_texto = gtk.ColorButton()
        boton_texto.set_title("color_fuente_menu")
        boton_texto.set_color(
            gdk.color_parse(self.config["color_fuente_menu"]))
        boton_texto.connect("color-set", self.__set_config)
        hbox4.pack_start(boton_texto, False, False, 3)
        hbox4.pack_start(gtk.Label("Fuente del Menú"), False, False, 3)

        hbox5 = gtk.HBox()
        boton_texto = gtk.ColorButton()
        boton_texto.set_title("color_descarga")
        boton_texto.set_color(
            gdk.color_parse(self.config["color_descarga"]))
        boton_texto.connect("color-set", self.__set_config)
        hbox5.pack_start(boton_texto, False, False, 3)
        hbox5.pack_start(gtk.Label("Item en Descargas"), False, False, 3)

        hbox6 = gtk.HBox()
        boton_texto = gtk.ColorButton()
        boton_texto.set_title("color_fuente_descarga")
        boton_texto.set_color(
            gdk.color_parse(self.config["color_fuente_descarga"]))
        boton_texto.connect("color-set", self.__set_config)
        hbox6.pack_start(boton_texto, False, False, 3)
        hbox6.pack_start(gtk.Label("Fuente en Descargas"), False, False, 3)

        cajas = [hbox1, hbox2, hbox3, hbox4, hbox5, hbox6]

        for caja in cajas:
            vbox.pack_start(caja, True, True, 3)

        frame.add(vbox)

        return frame

    def __set_config(self, widget):
        """
        Setea los colores y escribe la configuración
        en el archivo css.
        """

        if widget:
            color = widget.get_color().to_string().replace("#", "")
            color = "#%s%s%s" % (color[0:2], color[4:6], color[8:10])
            self.config[widget.get_title()] = color

        dict_colors = {
            "opacidad": self.config["opacidad"],
            "formato": self.config["formato"],
            "color1": self.config["color_ventana"],
            "color2": self.config["color_fuente_ventana"],
            "color3": self.config["color_menu"],
            "color4": self.config["color_fuente_menu"],
            "color5": self.config["color_descarga"],
            "color6": self.config["color_fuente_descarga"],
            }

        from Globales import set_estilo
        set_estilo(dict_colors)

    def __set_formato(self, widget):
        """
        Setea el formato de grabación y
        manda a guardar la configuración.
        """

        if widget.get_active():
            self.config["formato"] = widget.get_label()
            self.__set_config(False)

    def __set_opacidad(self, widget):
        """
        Setea la opacidad de la ventana y
        manda a guardar la configuración.
        """

        self.config["opacidad"] = float(
            "%.1f" % widget.get_value())
        self.__set_config(False)
        self.get_toplevel().set_opacity(
            self.config["opacidad"])
