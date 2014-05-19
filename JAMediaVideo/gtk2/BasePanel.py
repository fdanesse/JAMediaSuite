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
import gobject
import time
import datetime

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
from JAMediaWebCamVideo import JAMediaWebCamVideo
#from JAMediaInLan import JAMediaInLan

from Globales import get_video_directory

gobject.threads_init()
gtk.gdk.threads_init()


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

        self.control = True
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
        self.widget_efectos = False  #WidgetsGstreamerEfectos()

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

        self.control = False

    def __set_efecto(self, widget, efecto, propiedad=None, valor=None):
        """
        Agrega o configura efectos en la cámara de video o fotografía.
        """

        if self.control:
            return

        if propiedad == True:
            self.efectos_en_pipe.add_efecto(efecto)
            self.__re_init_video_web_cam()

        elif propiedad == False:
            self.efectos_en_pipe.remover_efecto(efecto)
            self.__re_init_video_web_cam()

        else:
            self.jamediawebcam.set_efecto(efecto, propiedad, valor)

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

    def __camara_menu_run(self):
        """
        Cámara básica del menú.
        """

        self.control = True

        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        if self.widget_efectos:
            self.widget_efectos.clear()

        self.info_label.set_text("")
        self.info_label.hide()
        self.efectos_en_pipe.clear()

        device = self.camara_setting.device

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamMenu(xid,
            device=device)

        gobject.idle_add(self.jamediawebcam.play)

        self.control = False

    def __camara_video_run(self):
        """
        Cámara básica de video.
        """

        self.control = True

        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        if self.widget_efectos:
            self.widget_efectos.clear()

        self.info_label.set_text("")
        self.info_label.hide()
        self.efectos_en_pipe.clear()

        device = self.camara_setting.device
        salida = self.video_out_setting.formato

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamVideo(
            xid, device=device, formato=salida,
            efectos=[])

        gobject.idle_add(self.jamediawebcam.play)

        self.control = False

    def __camara_foto_run(self):

        print "BasePanel: Menu de Fotografia ==> construir camara de grabacion de imagenes tomando en cuenta origen y formato segun widget de configuraciones y (tomar en cuenta configuracion de rafagas"

        self.control = True

        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        if self.widget_efectos:
            self.widget_efectos.clear()

        self.info_label.set_text("")
        self.info_label.hide()
        self.efectos_en_pipe.clear()

        device = self.camara_setting.device

        xid = self.pantalla.get_property('window').xid
        #self.jamediawebcam = JAMediaWebCamVideo(
        #    xid, device=device, formato=salida,
        #    efectos=[])

        #gobject.idle_add(self.jamediawebcam.play)

        self.control = False

    def __update_balance_toolbars(self, config):
        """
        Actualiza las toolbars de balance en video.
        """

        self.balance_config_widget.set_balance(
            brillo=config['brillo'],
            contraste=config['contraste'],
            saturacion=config['saturacion'],
            hue=config['hue'],
            gamma=config['gamma'])

    def __set_video_out(self, widget, tipo, valor):
        """
        Setea la salida de video para camara de filmación y fotografía.
        """

        self.jamediawebcam.set_formato(valor)

    def __set_camara(self, widget, tipo, valor):
        """
        Setea la entrada de video para camara de filmación y fotografía.
        """

        self.__re_init_video_web_cam(device=valor)

    def __re_init_video_web_cam(self,
        device=False, salida=False):
        """
        Cuando se agregan o quitan efectos o se cambia la fuente de video,
        se crea un nuevo objeto gstreamer que mantiene las configuraciones
        realizadas hasta el momento.
        """

        rot = self.jamediawebcam.get_rotacion()
        config = self.jamediawebcam.get_config()
        efectos = self.efectos_en_pipe.get_efectos()

        if not device:
            device = self.camara_setting.device

        if not salida:
            salida = self.video_out_setting.formato

        xid = self.pantalla.get_property('window').xid

        if "/dev/video" in device:
            if os.path.exists(device):
                self.jamediawebcam.stop()
                #del(self.jamediawebcam)
                self.jamediawebcam = False

                self.jamediawebcam = JAMediaWebCamVideo(
                    xid, device=device, formato=salida,
                    efectos=efectos)

                self.jamediawebcam.play()

                #gobject.timeout_add(1000, self.__re_config,
                #    rot, config, efectos)
                self.__re_config(rot, config, efectos)

        else:
            self.jamediawebcam.stop()
            #del(self.jamediawebcam)
            self.jamediawebcam = False

            #self.jamediawebcam = JAMediaInLan(
            self.jamediawebcam = JAMediaWebCamVideo(
                xid, device=device, formato=salida,
                efectos=efectos)

            self.jamediawebcam.play()

            #gobject.timeout_add(1000, self.__re_config,
            #    rot, config, efectos)
            self.__re_config(rot, config, efectos)

    def __re_config(self, rot, config, efectos):

        self.jamediawebcam.set_balance(
            brillo=config["brillo"],
            contraste=config["contraste"],
            saturacion=config["saturacion"],
            hue=config["hue"],
            gamma=config["gamma"])

        self.jamediawebcam.set_rotacion(rot)

        for efecto in efectos:
            self.widget_efectos.reemit_config_efecto(efecto)

        self.__update_balance_toolbars(config)

        return False

    def __update_record(self, widget, info):

        self.info_label.show()
        self.info_label.set_text(info)

    def __re_sensitive(self):

        self.get_toplevel().toolbar.set_sensitive(True)
        return False

    def nueva_camara(self, tipo):
        """
        Cuando se cambia el modo de la aplicación
        se reconstruye la camara base.
        """

        self.get_toplevel().toolbar.set_sensitive(False)

        if tipo == "visor":
            self.__camara_menu_run()

        elif tipo == "video":
            self.__camara_video_run()

        elif tipo == "foto":
            self.__camara_foto_run()

        else:
            print "BasePanel Nueva camara:", tipo

        gobject.timeout_add(1000, self.__re_sensitive)

    def set_accion(self, modo, accion):
        """
        Le pasa a la camara las ordenes seleccionadas por el
        usuario en la toolbar correspondiente de la aplicacion.
        """

        if accion == "Izquierda" or accion == "Derecha":
            self.jamediawebcam.rotar(accion)

        elif accion == "Salir":
            pass

        elif accion == "Stop":
            if modo == "video":
                self.get_toplevel().toolbar.set_sensitive(False)
                self.__re_init_video_web_cam()
                self.info_label.set_text("")
                self.info_label.hide()
                gobject.timeout_add(1000, self.__re_sensitive)

            else:
                print "BasePanel ==>", accion, "Detener Grabacion y hacer replay actualizar info_label"

        elif accion == "Filmar" and modo == "video":
            self.get_toplevel().toolbar.set_sensitive(False)
            hora = time.strftime("%H-%M-%S")
            fecha = str(datetime.date.today())
            archivo = "JV_%s_%s" % (fecha, hora)
            archivo = os.path.join(get_video_directory(), archivo)
            self.jamediawebcam.connect("update", self.__update_record)
            self.jamediawebcam.filmar(archivo)
            gobject.timeout_add(1000, self.__re_sensitive)

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

        #print "BasePanel ==> config_show", tipo

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

        #FIXME: Quizas sea mejor al final de la funcion
        if self.jamediawebcam:
            self.__update_balance_toolbars(
                self.jamediawebcam.get_config())

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

        self.widget_efectos.connect(
            "click_efecto", self.__set_efecto)
        self.widget_efectos.connect(
            "configurar_efecto", self.__set_efecto)

    def salir(self):

        if self.jamediawebcam:
            self.jamediawebcam.stop()
