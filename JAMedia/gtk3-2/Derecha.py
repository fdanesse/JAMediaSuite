#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Derecha.py por:
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
from gi.repository import Gtk
from gi.repository import GObject

from BalanceWidget import BalanceWidget
#from GstWidgets.Widgets import VideoEfectos
#from GstWidgets.VideoEfectos import get_jamedia_video_efectos
from JAMediaPlayerList import PlayerList
from PlayerControls import PlayerControls
from Globales import get_colors


def ocultar(objeto):
    if objeto.get_visible():
        objeto.hide()


def mostrar(objeto):
    if not objeto.get_visible():
        objeto.show()


class Derecha(Gtk.EventBox):

    __gsignals__ = {
    "cargar-reproducir": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    "accion-list": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT)),
    "menu_activo": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    "add_stream": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    "accion-controls": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'balance-valor': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,
        GObject.TYPE_STRING)),
    "add_remove_efecto": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN)),
    'configurar_efecto': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("window"))

        vbox = Gtk.VBox()
        conf_box = Gtk.VBox()

        self.balance = BalanceWidget()
        #self.efectos = VideoEfectos()
        self.lista = PlayerList()
        self.lista.set_mime_types(["audio/*", "video/*"])
        self.player_controls = PlayerControls()

        conf_box.pack_start(self.balance, False, False, 0)
        #conf_box.pack_start(self.efectos, True, True, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(conf_box)
        scroll.get_child().modify_bg(Gtk.StateType.NORMAL, get_colors("window"))

        vbox.pack_start(scroll, True, True, 0)
        vbox.pack_start(self.lista, True, True, 0)
        vbox.pack_end(self.player_controls, False, False, 0)

        self.add(vbox)

        self.show_all()

        self.balance.connect("balance-valor", self.__emit_balance)
        #self.efectos.connect("click_efecto", self.__emit_add_remove_efecto)
        #self.efectos.connect("configurar_efecto", self.__emit_config_efecto)

        self.lista.connect("nueva-seleccion", self.__emit_cargar_reproducir)
        self.lista.connect("accion-list", self.__emit_accion_list)
        self.lista.connect("menu_activo", self.__emit_menu_activo)
        self.lista.connect("add_stream", self.__emit_add_stream)

        self.player_controls.connect("accion-controls",
            self.__emit_accion_controls)

        self.set_size_request(150, -1)

    #def __emit_config_efecto(self, widget, efecto, propiedad, valor):
    #    # Configurar efecto de video.
    #    self.emit("configurar_efecto", efecto, propiedad, valor)

    #def __emit_add_remove_efecto(self, widget, efecto, valor):
    #    # Agrega o quita efecto de video.
    #    self.emit("add_remove_efecto", efecto, valor)

    def __emit_balance(self, widget, valor, prop):
        # brillo, contraste, saturación, hue, gamma
        self.emit('balance-valor', valor, prop)

    def __emit_accion_controls(self, widget, accion):
        # anterior, siguiente, pausa, play, stop
        self.emit("accion-controls", accion)

    def __emit_add_stream(self, widget, title):
        # El usuario agregará una dirección de streaming
        self.emit("add_stream", title)

    def __emit_menu_activo(self, widget=False):
        # hay un menu contextual presente
        self.emit("menu_activo")

    def __emit_accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.emit("accion-list", lista, accion, _iter)

    def __emit_cargar_reproducir(self, widget, path):
        if path:
            self.player_controls.activar(True)
        else:
            self.player_controls.activar(False)

        self.emit("cargar-reproducir", path)

    def show_config(self):
        objs = self.get_child().get_children()
        valor = objs[0].get_visible()

        if valor:
            ocultar(objs[0])
            map(mostrar, objs[1:])

        else:
            mostrar(objs[0])
            map(ocultar, objs[1:])

    def setup_init(self):
        ocultar(self.get_child().get_children()[0])
        self.lista.setup_init()
        self.player_controls.activar(False)
        #self.efectos.cargar_efectos(list(get_jamedia_video_efectos()))
