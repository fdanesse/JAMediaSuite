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

from JAMediaWebCamView import JAMediaWebCamView
#from GstreamerWidgets.Widgets import WidgetsGstreamerEfectos
from Widgets import Visor
from ToolbarConfig import ToolbarConfig


class BasePanel(gtk.HPaned):
    """
    izquierda:
        visor
        barra con efectos de video que se aplican

    derecha:
        balance y efectos de video ==> self.scroll_video_config
        efectos de audio
    """

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(0, get_colors("toolbars"))

        self.audio_widgets_config = []
        self.video_widgets_config = []

        #self.jamediawebcam = None
        self.pantalla = Visor()
        #vbox.pack_start(self.pantalla, True, True, 0)
        self.pack1(self.pantalla, resize=True, shrink=True)

        # Area Derecha del Panel
        self.derecha_vbox = gtk.VBox()

        self.balance_config_widget = ToolbarConfig()
        self.widget_efectos = False #WidgetsGstreamerEfectos()

        self.vbox_config = gtk.VBox()
        self.scroll_video_config = gtk.ScrolledWindow()
        self.scroll_video_config.set_policy(
            gtk.POLICY_NEVER,
            gtk.POLICY_AUTOMATIC)
        self.scroll_video_config.add_with_viewport(
            self.vbox_config)
        self.scroll_video_config.get_child().modify_bg(
            0, get_colors("window"))
        self.vbox_config.pack_start(
            self.balance_config_widget, False, False, 0)

        self.derecha_vbox.pack_start(
            self.scroll_video_config, True, True, 0)

        self.video_widgets_config = [
            self.balance_config_widget,
            self.scroll_video_config]

        # empaquetando todo
        self.pack2(self.derecha_vbox,
            resize=False, shrink=False)

        self.show_all()

        self.pantalla.connect("button_press_event",
            self.__clicks_en_pantalla)

    def config_show(self, datos):
        """
        Muestra u oculta los widgets de configuración.
        """

        # ocultar todas.
        # si modo video: balance, efectos de video y efectos de audio
        # si modo fotografía: balance y efectos de video.
        # si modo audio: efectos de audio.

        if "audio" in datos:
            # Configuración de audio
            pass

        if "video" in datos:
            # configuración de cámara
            # configuración de Video
            # configuración de grabación de video
            if self.video_widgets_config[0].get_visible():
                map(self.__ocultar, self.video_widgets_config)
            else:
                map(self.__mostrar, self.video_widgets_config)

        if "foto" in datos:
            # ráfagas
            # formato de salida de imágenes
            pass

    def run(self):
        """
        Estado inicial de la aplicación.
        """

        #self.derecha_vbox.hide()
        xid = self.pantalla.get_property('window').xid
        #self.jamediawebcam = JAMediaWebCamView(xid)
        #gobject.idle_add(self.jamediawebcam.play)

        map(self.__ocultar, self.video_widgets_config)
        map(self.__ocultar, self.audio_widgets_config)

    def __ocultar(self, objeto):
        """
        Esta funcion es llamada desde self.get_menu()
        """

        if objeto.get_visible():
            objeto.hide()

    def __mostrar(self, objeto):
        """
        Esta funcion es llamada desde self.get_menu()
        """

        if not objeto.get_visible():
            objeto.show()

    def pack_efectos(self):
        """
        Empaqueta los widgets de efectos gstreamer.
        """

        # FIXME: agregar widget para efectos que se aplican y efectos de audio

        from GstreamerWidgets.Widgets import WidgetsGstreamerEfectos
        from GstreamerWidgets.VideoEfectos import get_jamedia_video_efectos

        self.widget_efectos = WidgetsGstreamerEfectos()

        self.vbox_config.pack_start(
            self.widget_efectos, False, False, 0)

        gobject.idle_add(self.__cargar_efectos,
            list(get_jamedia_video_efectos()))

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
