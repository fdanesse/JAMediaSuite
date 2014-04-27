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
from Widgets import Video_out_Config
from Widgets import Rafagas_Config
from Widgets import Efectos_en_Pipe
from Widgets import Info_Label
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
        self.info_label = Info_Label()
        self.efectos_en_pipe = Efectos_en_Pipe()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_NEVER)
        scroll.add_with_viewport(
            self.efectos_en_pipe)
        scroll.get_child().modify_bg(
            0, get_colors("drawingplayer"))

        vbox = gtk.VBox()
        vbox.pack_start(self.info_label, False, False, 0)
        vbox.pack_start(self.pantalla, True, True, 0)
        vbox.pack_start(scroll, False, False, 0)
        self.pack1(vbox, resize=True, shrink=True)

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
        self.video_out_setting = Video_out_Config()
        self.rafagas_setting = Rafagas_Config()
        self.balance_config_widget = ToolbarConfig()
        self.widget_efectos = False #WidgetsGstreamerEfectos()

        self.vbox_config.pack_start(
            self.camara_setting, False, False, 0)
        self.vbox_config.pack_start(
            self.video_out_setting, False, False, 0)
        self.vbox_config.pack_start(
            self.rafagas_setting, False, False, 0)
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
        self.video_out_setting.connect(
            "set_video_out", self.__set_video_out)

    def __set_efecto(self, widget, efecto, propiedad=None, valor=None):

        if propiedad == True:
            self.efectos_en_pipe.add_efecto(efecto)
            print "BasePanel: Menu video ==> agregar efecto en la camara", efecto

        elif propiedad == False:
            self.efectos_en_pipe.remover_efecto(efecto)
            print "BasePanel: Menu video ==> quitar efecto de la camara", efecto

        else:
            print "BasePanel: Menu video ==> configurar efecto en la camara", efecto, propiedad, valor

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

        print "BasePanel: Menu video ==> configurar", valor, tipo

    def __camara_menu_run(self):

        if self.widget_efectos:
            self.widget_efectos.clear()

        self.info_label.set_text("")
        self.info_label.hide()
        self.efectos_en_pipe.clear()

        if self.jamediawebcam:
            self.jamediawebcam.reset()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamMenu(xid,
            self.camara_setting.device)
        gobject.idle_add(self.jamediawebcam.play)

    def __camara_video_run(self):

        print "BasePanel: Menu de Video ==> construir camara de grabacion de video tomando en cuenta origen y formato segun widget de configuraciones (tomar en cuenta configuracion de rafagas)"

        if self.jamediawebcam:
            self.jamediawebcam.reset()
            del(self.jamediawebcam)
            self.jamediawebcam = False

    def __camara_foto_run(self):

        print "BasePanel: Menu de Fotografia ==> construir camara de grabacion de imagenes tomando en cuenta origen y formato segun widget de configuraciones"

        if self.jamediawebcam:
            self.jamediawebcam.reset()
            del(self.jamediawebcam)
            self.jamediawebcam = False

    def __update_balance_toolbars(self):
        """
        Actualiza las toolbars de balance en video.
        """

        if not self.jamediawebcam: return

        config = self.jamediawebcam.get_balance()

        self.balance_config_widget.set_balance(
            brillo=config['brillo'],
            contraste=config['contraste'],
            saturacion=config['saturacion'],
            hue=config['hue'],
            gamma=config['gamma'])

    def __set_video_out(self, widget, tipo, valor):

        print "BasePanel ==> Reconfigurar formato de salida de video", tipo, valor

    def __set_camara(self, widget, tipo, valor):

        print "BasePanel ==> Reconfigurar camara de video", tipo, valor

    def nueva_camara(self, tipo):

        if tipo == "visor":
            self.__camara_menu_run()

        elif tipo == "video":
            self.__camara_video_run()

        elif tipo == "foto":
            self.__camara_foto_run()

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
            print "BasePanel ==>", accion, "Detener Grabacion y hacer replay actualizar info_label"

        elif accion == "Filmar":
            print "BasePanel ==>", accion, "Comenzar a Filmar"

        elif accion == "Fotografiar":
            print "BasePanel ==>", accion, "Comenzar a Fotografiar, tomando en cuenta las rafagas" #self.rafagas_setting.get_rafaga

        else:
            print "BasePanel ==>", accion, "falta definir"

    def config_show(self, tipo):
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

        print "BasePanel ==> config_show", tipo

        if tipo:
            if self.box_config.get_visible():
                self.box_config.hide()

            else:
                self.box_config.show()

        else:
            self.box_config.hide()
            return

        video_widgets = [
            self.camara_setting,
            self.video_out_setting,
            self.balance_config_widget,
            self.widget_efectos]

        foto_widgets = [
            self.camara_setting,
            #self.video_out_setting,
            self.rafagas_setting,
            self.balance_config_widget,
            self.widget_efectos]

        self.__update_balance_toolbars()

        map(ocultar, video_widgets)
        map(ocultar, foto_widgets)

        if tipo == "camara":
            map(mostrar, video_widgets)

        elif tipo == "foto":
            # ráfagas
            # formato de salida de imágenes
            map(mostrar, foto_widgets)

        #elif "video" in datos:

        #elif "audio" in datos:
            # Configuración de audio

    def pack_efectos(self):
        """
        Empaqueta los widgets de efectos gstreamer.
        """

        self.widget_efectos = WidgetsGstreamerEfectos()

        self.vbox_config.pack_start(
            self.widget_efectos, False, False, 0)

        gobject.idle_add(self.__cargar_efectos,
            list(get_jamedia_video_efectos()))

        self.widget_efectos.connect("click_efecto", self.__set_efecto)
        self.widget_efectos.connect("configurar_efecto", self.__set_efecto)

    def salir(self):

        if self.jamediawebcam:
            self.jamediawebcam.reset()
