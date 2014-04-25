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

import os

import gtk
from gtk import gdk
import gobject

from Globales import get_colors

from Widgets import Visor
from Widgets import CamaraConfig
from ToolbarConfig import ToolbarConfig

from GstreamerWidgets.Widgets import WidgetsGstreamerEfectos
from GstreamerWidgets.VideoEfectos import get_jamedia_video_efectos

from JAMediaWebCamMenu import JAMediaWebCamMenu


def ocultar(objeto):

    if objeto:
        if objeto.get_visible():
            objeto.hide()


def mostrar(objeto):

    if objeto:
        if not objeto.get_visible():
            objeto.show()


class BasePanel(gtk.HPaned):
    """
    izquierda:
        visor
        barra con efectos de video que se aplican

    derecha:
        Configuración de cámara y formato de salida ==> self.camara_setting
        balance y efectos de video ==> self.video_widgets_config
        efectos de audio ==> self.audio_widgets_config
    """

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(0, get_colors("toolbars"))

        self.jamediawebcam = False

        self.pantalla = Visor()
        self.pack1(self.pantalla, resize=True, shrink=True)

        # Area Derecha del Panel
        self.box_config = gtk.EventBox()
        self.box_config.modify_bg(
            0, get_colors("window"))
        self.vbox_config = gtk.VBox()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(
            gtk.POLICY_NEVER,
            gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(
            self.vbox_config)
        scroll.get_child().modify_bg(
            0, get_colors("window"))
        self.box_config.add(scroll)

        self.camara_setting = CamaraConfig()
        self.balance_config_widget = ToolbarConfig()
        self.widget_efectos = False #WidgetsGstreamerEfectos()

        self.vbox_config.pack_start(
            self.camara_setting, False, False, 0)
        self.vbox_config.pack_start(
            self.balance_config_widget, False, False, 0)
        #self.derecha_vbox.pack_start(
        #    self.widget_efectos, True, True, 0)

        # empaquetando todo
        self.pack2(self.box_config,
            resize=False, shrink=False)

        self.show_all()

        self.pantalla.connect("button_press_event",
            self.__clicks_en_pantalla)
        self.balance_config_widget.connect(
            'valor', self.__set_balance)
        self.camara_setting.connect(
            "set_camara", self.__set_camara)

    def __set_efecto(self, widget, efecto, propiedad=None, valor=None):

        print efecto, propiedad, valor

    def __cargar_efectos(self, efectos):
        """
        Agrega los widgets con efectos a la paleta de configuración.
        """

        self.widget_efectos.cargar_efectos(efectos)
        return False

    def __clicks_en_pantalla(self, widget, event):
        """
        Hace fullscreen y unfullscreen sobre la
        ventana principal cuando el usuario hace
        doble click en el visor.
        """

        if event.type.value_name == "GDK_2BUTTON_PRESS":

            self.get_toplevel().set_sensitive(False)

            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w, h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())

            #self.__cancel_toolbars_flotantes()

            if ww == w and hh == h:
                #ventana.set_border_width(2)
                gobject.idle_add(ventana.unfullscreen)

            else:
                #ventana.set_border_width(0)
                gobject.idle_add(ventana.fullscreen)

            self.get_toplevel().set_sensitive(True)

    def __set_balance(self, widget, valor, tipo):
        """
        Setea valores en Balance de Video.
        valor es % float
        """
        '''
        if tipo == "saturacion":
            self.jamediawebcam.set_balance(saturacion=valor)

        elif tipo == "contraste":
            self.jamediawebcam.set_balance(contraste=valor)

        elif tipo == "brillo":
            self.jamediawebcam.set_balance(brillo=valor)

        elif tipo == "hue":
            self.jamediawebcam.set_balance(hue=valor)

        elif tipo == "gamma":
            self.jamediawebcam.set_balance(gamma=valor)
        '''
        print valor, tipo

    def __camara_menu_run(self):

        print "BasePanel: FIXME: Menu principal ==> quitar efectos"

        if self.jamediawebcam:
            self.jamediawebcam.reset()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamMenu(xid,
            self.camara_setting.device)
        gobject.idle_add(self.jamediawebcam.play)

    def __camara_video_run(self):

        print "BasePanel: Menu de Video ==> construir camara de grabacion de video tomando en cuenta origen y formato segun widget de configuraciones"

        if self.jamediawebcam:
            self.jamediawebcam.reset()
            del(self.jamediawebcam)
            self.jamediawebcam = False

    def __update_balance_toolbars(self):
        """
        Actualiza las toolbars de balance en video.
        """

        config = self.jamediawebcam.get_balance()

        self.balance_config_widget.set_balance(
            brillo=config['brillo'],
            contraste=config['contraste'],
            saturacion=config['saturacion'],
            hue=config['hue'],
            gamma=config['gamma'])

    def __set_camara(self, widget, tipo, valor):

        print "BasePanel ==> Reconfigurar camara de video", tipo, valor

    def nueva_camara(self, tipo):

        if tipo == "visor":
            self.__camara_menu_run()

        elif tipo == "video":
            self.__camara_video_run()

        else:
            print "BasePanel Nueva camara:", tipo

    def set_accion(self, accion):
        """
        Le pasa a la camara las ordenes seleccionadas por el usuario
        en la toolbar correspondiente de la aplicacion.
        """

        if accion == "Izquierda" or accion == "Derecha":
            #self.jamediawebcam.rotar(accion)
            print "BasePanel ==>", accion, "Rotar el Video"

        elif accion == "Salir":
            pass

        elif accion == "Stop":
            # detener grabacion
            # self.box_config.show()
            print "BasePanel ==>", accion, "Detener Grabacion y hacer replay"

        elif accion == "Filmar":
            #self.box_config.hide()
            print "BasePanel ==>", accion, "Comenzar a Filmar"

    def config_show(self, datos):
        """
        Muestra u oculta los widgets de configuración.
        """

        # si modo video:
        #   camara, formato de salida,
        #   balance, efectos de video y efectos de audio
        # si modo fotografía:
        #   camarara, formato de salida,
        #   balance y efectos de video.
        # si modo audio: formato de salida, efectos de audio.

        if datos:
            if self.box_config.get_visible():
                self.box_config.hide()

            else:
                self.box_config.show()

        else:
            self.box_config.hide()
            return

        video_widgets = [
            self.camara_setting,
            self.balance_config_widget,
            self.widget_efectos]

        self.__update_balance_toolbars()

        if "camara" in datos:
            map(mostrar, video_widgets)

        else:
            map(ocultar, video_widgets)

        #elif "video" in datos:

        #elif "audio" in datos:
            # Configuración de audio

        #elif "foto" in datos:
            # ráfagas
            # formato de salida de imágenes

    def pack_efectos(self):
        """
        Empaqueta los widgets de efectos gstreamer.
        """

        # FIXME: agregar widget para efectos que se aplican y efectos de audio

        self.widget_efectos = WidgetsGstreamerEfectos()

        self.vbox_config.pack_start(
            self.widget_efectos, False, False, 0)

        gobject.idle_add(self.__cargar_efectos,
            list(get_jamedia_video_efectos()))

        self.widget_efectos.connect("click_efecto", self.__set_efecto)
        self.widget_efectos.connect("configurar_efecto", self.__set_efecto)
