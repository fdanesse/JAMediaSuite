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

#from JAMediaWebCamView import JAMediaWebCamView
#from GstreamerWidgets.Widgets import WidgetsGstreamerEfectos
from Widgets import Visor
from ToolbarConfig import ToolbarConfig


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

        #self.jamediawebcam = None
        self.pantalla = Visor()
        #vbox.pack_start(self.pantalla, True, True, 0)
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

        self.camara_setting = gtk.Label("Camara Setting")
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

    def __set_balance(self, widget, valor, tipo):
        """
        Setea valores en Balance de Video.
        valor es % float
        """

        print valor, tipo
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

    def set_accion(self, accion):
        """
        Le pasa a la camara las ordenes seleccionadas por el usuario
        en la toolbar correspondiente de la aplicacion.
        """

        self.jamediawebcam.set_accion(accion)

        if accion == "Salir":
            # resetear camara y volver a poner en play, sin efectos.
            self.jamediawebcam.reset()
            self.run()

        elif accion == "Stop":
            # detener grabacion
            pass

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

        print "config_show", datos

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

        if "camara" in datos:
            map(self.__mostrar, video_widgets)

        else:
            map(self.__ocultar, video_widgets)

        #elif "video" in datos:

        #elif "audio" in datos:
            # Configuración de audio

        #elif "foto" in datos:
            # ráfagas
            # formato de salida de imágenes

    def run(self):
        """
        Estado inicial de la aplicación.
        """

        from JAMediaWebCam import JAMediaWebCam

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCam(xid)
        gobject.idle_add(self.jamediawebcam.play)

        map(self.__ocultar, [self.box_config])

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

        self.widget_efectos.connect("click_efecto", self.__set_efecto)
        self.widget_efectos.connect("configurar_efecto", self.__set_efecto)

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
