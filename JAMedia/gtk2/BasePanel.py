#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BasePanel.py por:
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

import gtk
import gobject
import threading

from Widgets import DialogoDescarga
from Izquierda import Izquierda
from Derecha import Derecha
from Globales import get_colors
from Globales import get_ip
from JAMediaReproductor.JAMediaReproductor import JAMediaReproductor


class BasePanel(gtk.HPaned):

    __gsignals__ = {
    "show-controls": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "accion-list": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    "menu_activo": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "add_stream": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "video": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,)),
    'stop-record': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_border_width(2)

        self._thread = False
        self.player = False

        self.izquierda = Izquierda()
        self.derecha = Derecha()

        self.pack1(self.izquierda, resize=True, shrink=True)
        self.pack2(self.derecha, resize=False, shrink=False)

        self.show_all()

        self.derecha.connect("cargar-reproducir", self.__cargar_reproducir)
        self.derecha.connect("accion-list", self.__emit_accion_list)
        self.derecha.connect("menu_activo", self.__emit_menu_activo)
        self.derecha.connect("add_stream", self.__emit_add_stream)
        self.derecha.connect("accion-controls", self.__accion_controls)
        self.derecha.connect("balance-valor", self.__accion_balance)
        #self.derecha.connect("add_remove_efecto", self.__add_remove_efecto)
        #self.derecha.connect("configurar_efecto", self.__config_efecto)

        self.izquierda.connect("show-controls", self.__emit_show_controls)
        self.izquierda.connect("rotar", self.__rotar)
        self.izquierda.connect("stop-record", self.__stop_record)
        self.izquierda.connect("seek", self.__user_set_progress)
        self.izquierda.connect("volumen", self.__set_volumen)
        self.izquierda.connect("actualizar_streamings",
            self.__actualizar_streamings)

        gobject.timeout_add(5000, self.__check_ip)

    def __stop_record(self, widget):
        self.__emit_menu_activo()
        self.emit("stop-record")

    def __actualizar_streamings(self, widget):
        self.__emit_menu_activo()
        dialog = DialogoDescarga(parent=self.get_toplevel(), force=True)
        dialog.run()
        dialog.destroy()
        # FIXME: Recargar Lista actual

    #def __add_remove_efecto(self, widget, efecto, valor):
    #    # Agrega o quita efecto de video.
    #    self.__emit_menu_activo()
    #    print self.__add_remove_efecto, efecto, valor
    #    # agregar el efecto en el bin y en el widget

    #def __config_efecto(self, widget, efecto, propiedad, valor):
    #    # Configurar efecto de video.
    #    self.__emit_menu_activo()
    #    print self.__config_efecto, efecto, propiedad, valor

    def __accion_balance(self, widget, valor, prop):
        # Setea valores de Balance en el reproductor.
        self.__emit_menu_activo()
        if prop == "saturacion":
            self.player.set_balance(saturacion=valor)
        elif prop == "contraste":
            self.player.set_balance(contraste=valor)
        elif prop == "brillo":
            self.player.set_balance(brillo=valor)
        elif prop == "hue":
            self.player.set_balance(hue=valor)
        elif prop == "gamma":
            self.player.set_balance(gamma=valor)

    def __emit_add_stream(self, widget, title):
        # El usuario agregará una dirección de streaming
        self.emit("add_stream", title)

    def __emit_menu_activo(self, widget=False):
        # hay un menu contextual presente
        self.emit("menu_activo")
        self.izquierda.buffer_info.hide()

    def __emit_accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.emit("accion-list", lista, accion, _iter)

    def __accion_controls(self, widget, accion):
        # anterior, siguiente, pausa, play, stop
        self.__emit_menu_activo()
        if accion == "atras":
            self.derecha.lista.seleccionar_anterior()
        elif accion == "siguiente":
            self.derecha.lista.seleccionar_siguiente()
        elif accion == "stop":
            if self.player:
                self.player.stop()
        elif accion == "pausa-play":
            if self.player:
                self.player.pause_play()

    def __set_volumen(self, widget, valor):
        self.__emit_menu_activo()
        if self.player:
            self.player.set_volumen(valor)

    def __user_set_progress(self, widget, valor):
        self.__emit_menu_activo()
        if self.player:
            self.player.set_position(valor)

    def __emit_show_controls(self, widget, datos):
        self.emit("show-controls", datos)

    def __cargar_reproducir(self, widget, path):
        self.derecha.set_sensitive(False)

        # FIXME: Analizar mantener los siguientes valores:
        # Efectos
        # balanace
        # Gamma
        # Rotacion
        # Volumen

        volumen = 1.0
        if self.player:
            volumen = float("{:.1f}".format(
                self.izquierda.progress.volumen.get_value() * 10))
            self.player.disconnect_by_func(self.__endfile)
            self.player.disconnect_by_func(self.__state_changed)
            self.player.disconnect_by_func(self.__update_progress)
            self.player.disconnect_by_func(self.__set_video)
            self.player.disconnect_by_func(self.__loading_buffer)
            self.player.stop()
            del(self.player)
            self.player = False

        self.izquierda.progress.set_sensitive(False)
        self.__set_video(False, False)

        xid = self.izquierda.video_visor.get_property('window').xid
        self.player = JAMediaReproductor(xid)

        self.player.connect("endfile", self.__endfile)
        self.player.connect("estado", self.__state_changed)
        self.player.connect("newposicion", self.__update_progress)
        self.player.connect("video", self.__set_video)
        self.player.connect("loading-buffer", self.__loading_buffer)

        self.player.load(path)
        self._thread = threading.Thread(target=self.player.play)
        self._thread.start()
        self.player.set_volumen(volumen)
        self.izquierda.progress.volumen.set_value(volumen / 10)
        self.derecha.set_sensitive(True)

    def __loading_buffer(self, player, buf):
        self.izquierda.buffer_info.set_progress(float(buf))

    def __rotar(self, widget, valor):
        if self.player:
            self.__emit_menu_activo()
            self.player.rotar(valor)

    def __set_video(self, widget, valor):
        self.izquierda.toolbar_info.set_video(valor)
        self.emit("video", valor)

    def __update_progress(self, objetoemisor, valor):
        self.izquierda.progress.set_progress(float(valor))

    def __state_changed(self, widget=None, valor=None):
        if "playing" in valor:
            self.derecha.player_controls.set_playing()
            self.izquierda.progress.set_sensitive(True)
            gobject.idle_add(self.__update_balance)
        elif "paused" in valor or "None" in valor:
            self.derecha.player_controls.set_paused()
            gobject.idle_add(self.__update_balance)
        else:
            print "Estado del Reproductor desconocido:", valor

    def __update_balance(self):
        config = {}
        if self.player:
            config = self.player.get_balance()
        self.derecha.balance.set_balance(
            brillo=config.get('brillo', 50.0),
            contraste=config.get('contraste', 50.0),
            saturacion=config.get('saturacion', 50.0),
            hue=config.get('hue', 50.0),
            gamma=config.get('gamma', 10.0))
        return False

    def __check_ip(self):
        valor = get_ip()
        self.izquierda.set_ip(valor)
        self.derecha.set_ip(valor)
        return True

    def __endfile(self, widget=None, senial=None):
        self.derecha.player_controls.set_paused()
        self.derecha.lista.seleccionar_siguiente()

    def setup_init(self):
        self.izquierda.setup_init()
        self.derecha.setup_init()

    def salir(self):
        if self.player:
            self.player.disconnect_by_func(self.__endfile)
            self.player.disconnect_by_func(self.__state_changed)
            self.player.disconnect_by_func(self.__update_progress)
            self.player.disconnect_by_func(self.__set_video)
            self.player.disconnect_by_func(self.__loading_buffer)
            self.player.stop()
            del(self.player)
            self.player = False

    def set_nueva_lista(self, archivos):
        self.derecha.set_nueva_lista(archivos)
