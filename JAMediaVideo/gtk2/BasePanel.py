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

from JAMediaConvert.WidgetConvert import WidgetConvert

from JAMedia.PlayerList import PlayerList
from JAMedia.ToolbarConfig import ToolbarConfig
from JAMedia.PlayerControls import PlayerControl
from JAMedia.ProgressPlayer import ProgressPlayer
from JAMedia.JAMediaReproductor.JAMediaReproductor import JAMediaReproductor

from JAMediaImagenes.ImagePlayer import ImagePlayer

from Widgets import Visor
from Widgets import CamaraConfig
from Widgets import Video_out_Config
from Widgets import Rafagas_Config
from Widgets import Efectos_en_Pipe
from Widgets import Info_Label

from GstreamerWidgets.WidgetsGstreamerVideoEfectos import WidgetsGstreamerVideoEfectos
from GstreamerWidgets.VideoEfectos import get_jamedia_video_efectos

from GstreamerBins.JAMediaWebCamMenu import JAMediaWebCamMenu
from GstreamerBins.JAMediaWebCamVideo import JAMediaWebCamVideo

from Globales import get_video_directory
from Globales import get_imagenes_directory
from Globales import get_ip

PR = False


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

    __gsignals__ = {
    "accion-list": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    "in-run": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN, )),
    "cancel-toolbars": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, ()),
    "pendientes": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(0, get_colors("toolbars"))

        self.control = True
        self.jamediawebcam = False
        self.player = False
        self.imageplayer = False

        self.pantalla = Visor()
        self.info_label = Info_Label()
        self.efectos_en_pipe = Efectos_en_Pipe()
        self.progressplayer = ProgressPlayer()
        self.jamediaconvert = WidgetConvert()

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
        vbox.pack_start(self.jamediaconvert, True, True, 0)
        vbox.pack_start(scroll, False, False, 0)
        vbox.pack_start(self.progressplayer, False, False, 0)
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
        self.playerlist = PlayerList()
        self.player_control = PlayerControl()
        self.widget_efectos = False  # WidgetsGstreamerEfectos()

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

        self.vbox_config.pack_start(
            self.playerlist, True, True, 0)

        self.vbox_config.pack_end(
            self.player_control, False, True, 0)

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

        self.player_control.connect(
            "activar", self.__accion_player)
        self.playerlist.connect(
            "nueva-seleccion", self.__play_item)
        self.playerlist.connect(
            "accion", self.__re_emit_accion_list)
        self.progressplayer.connect(
            "user-set-value", self.__user_set_progress)
        self.progressplayer.connect(
            "volumen", self.__set_volumen)

        self.jamediaconvert.connect(
            "accion-list", self.__re_emit_accion_list)
        self.jamediaconvert.connect(
            "in-run", self.__jamediaconvert_in_run)
        self.jamediaconvert.connect(
            "pendientes", self.__jamediaconvert_info)

        self.control = False

    def __jamediaconvert_info(self, widget, info):
        self.emit("pendientes", info)

    def __jamediaconvert_in_run(self, widget, valor):
        self.emit("in-run", valor)

    def __re_emit_accion_list(self, widget, lista, accion, _iter):
        self.emit("accion-list", lista, accion, _iter)

    def __set_volumen(self, widget, valor):
        """
        REPRODUCTOR:
            Cuando el usuario cambia el volumen.
        """

        if self.player:
            self.player.set_volumen(valor)

        self.emit("cancel-toolbars")

    def __user_set_progress(self, widget=None, valor=None):
        """
        REPRODUCTOR:
            Recibe la posicion en la barra de progreso cuando
            el usuario la desplaza y hace "seek" sobre el reproductor.
        """

        if self.player:
            self.player.set_position(valor)

        self.emit("cancel-toolbars")

    def __accion_player(self, widget, senial):
        """
        REPRODUCTOR:
            Acciones sobre pistas en lista de reproducción.
        """

        if senial == "atras":
            self.playerlist.seleccionar_anterior()

        elif senial == "siguiente":
            self.playerlist.seleccionar_siguiente()

        elif senial == "stop":
            if self.player:
                self.player.stop()

        elif senial == "pausa-play":
            if self.player:
                self.player.pause_play()

        self.emit("cancel-toolbars")

    def __play_item(self, widget, path):
        """
        REPRODUCTOR y VISOR de IMAGENES:
        """

        if self.player:
            volumen = 1.0

            volumen = float("{:.1f}".format(
                self.progressplayer.volumen.get_value() * 10))
            self.player.stop()
            del(self.player)

            xid = self.pantalla.get_property('window').xid
            self.player = JAMediaReproductor(xid)

            self.player.connect(
                "endfile", self.__endfile)
            self.player.connect(
                "estado", self.__cambioestadoreproductor)
            self.player.connect(
                "newposicion", self.__update_progress)
            #self.player.connect(
            #    "video", self.__set_video)

            if path:
                self.player.load(path)

            self.player.set_volumen(volumen)
            self.progressplayer.volumen.set_value(volumen / 10)

        elif self.imageplayer:
            self.imageplayer.load(path)

        else:
            print self.__play_item, path

    def __endfile(self, widget=None, senial=None):
        """
        REPRODUCTOR:
            Recibe la señal de fin de archivo desde el reproductor
            y llama a seleccionar_siguiente en la lista de reproduccion.
        """

        self.player_control.set_paused()
        gobject.idle_add(
            self.playerlist.seleccionar_siguiente)

    def __cambioestadoreproductor(self, widget=None, valor=None):
        """
        REPRODUCTOR:
            Recibe los cambios de estado del reproductor (paused y playing)
            y actualiza la imagen del boton play en la toolbar de reproduccion.
        """

        if "playing" in valor:
            self.player_control.set_playing()

        elif "paused" in valor or "None" in valor:
            self.player_control.set_paused()

        else:
            print "Estado del Reproductor desconocido:", valor

    def __update_progress(self, objetoemisor, valor):
        """
        REPRODUCTOR:
            Recibe el progreso de la reproduccion desde el reproductor
            y actualiza la barra de progreso.
        """

        self.progressplayer.set_progress(float(valor))

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

        self.emit("cancel-toolbars")

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

            ventana = self.get_toplevel()
            ventana.set_sensitive(False)
            screen = ventana.get_screen()
            w, h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())

            ventana.toolbar_salir.hide()
            color = get_colors("toolbars")

            if ww == w and hh == h:
                ventana.set_border_width(4)
                color = get_colors("toolbars")
                gobject.idle_add(ventana.unfullscreen)

            else:
                ventana.set_border_width(0)
                color = get_colors("drawingplayer")
                gobject.idle_add(ventana.fullscreen)

            ventana.modify_bg(0, color)
            ventana.toolbar.modify_bg(0, color)
            ventana.toolbar.toolbar_principal.modify_bg(0, color)
            ventana.toolbar.toolbar_video.modify_bg(0, color)
            ventana.toolbar.toolbar_fotografia.modify_bg(0, color)
            ventana.toolbar.toolbar_jamedia.modify_bg(0, color)
            ventana.toolbar.toolbar_jamediaimagenes.modify_bg(0, color)

            ventana.set_sensitive(True)

        self.emit("cancel-toolbars")

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

        self.emit("cancel-toolbars")

    def __jamediaconvert_run(self):
        """
        Cambia a modo Conversor y Extractor.
        """

        if PR:
            print "__jamediaconvert_run"
        self.pantalla.hide()
        self.box_config.hide()
        self.jamediaconvert.show()
        self.emit("in-run", False)

    def __jamediaimagenes_run(self):
        """
        Cambia a modo visor de imágenes.
        """

        if PR:
            print "__jamediaimagenes_run"
        self.imageplayer = ImagePlayer(self.pantalla)
        self.playerlist.set_mime_types(["image/*"])

    def __jamedia_run(self):
        """
        Cambia a modo reproductor.
        """

        if PR:
            print "__jamedia_run"
        xid = self.pantalla.get_property('window').xid
        self.player = JAMediaReproductor(xid)

        self.playerlist.set_mime_types(["audio/*", "video/*"])
        self.progressplayer.show()

    def __camara_menu_run(self):
        """
        Cambia a modo Cámara básica del menú.
        """

        if PR:
            print "__camara_menu_run"

        self.control = True

        device = self.camara_setting.device

        #FIXME: No debiera ser necesario
        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamMenu(xid,
            device=device)

        self.jamediawebcam.play()

        self.control = False

    def __camara_video_run(self):
        """
        Cambia modo Cámara de video.
        """

        if PR:
            print "__camara_video_run"

        self.control = True

        device = self.camara_setting.device
        salida = self.video_out_setting.formato

        #FIXME: No debiera ser necesario
        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamVideo(
            xid, device=device, formato=salida,
            efectos=[])

        self.jamediawebcam.connect("update",
            self.__update_record)
        self.jamediawebcam.connect("stop-rafaga",
            self.__recibe_stop_rafaga)
        self.jamediawebcam.connect("endfile",
            self.__control_grabacion_end)

        if "Escritorio" in device:
            self.get_toplevel().toolbar.permitir_filmar(True)

        else:
            if "/dev/video" in device:
                self.get_toplevel().toolbar.permitir_filmar(True)

            else:
                self.get_toplevel().toolbar.permitir_filmar(False)

        self.jamediawebcam.play()

        self.control = False

    def __control_grabacion_end(self, widget):
        self.mode_change("video")

    def __camara_foto_run(self):
        """
        Cambia a modo Cámara de Fotografía.
        """

        if PR:
            print "__camara_foto_run"

        self.control = True

        device = self.camara_setting.device
        salida = self.video_out_setting.formato

        #FIXME: No debiera ser necesario
        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamVideo(
            xid, device=device, formato=salida,
            efectos=[])

        self.jamediawebcam.connect("update",
            self.__update_record)
        self.jamediawebcam.connect("stop-rafaga",
            self.__recibe_stop_rafaga)

        gobject.idle_add(self.jamediawebcam.play)

        self.control = False

    def __recibe_stop_rafaga(self, widget):
        """
        Cuando la camara dejará de fotografiar.
        """

        self.info_label.set_text("")
        self.info_label.hide()

        gobject.timeout_add(500, self.__resensitive_foto)

    def __resensitive_foto(self):
        toolbar = self.get_toplevel().toolbar
        toolbar.toolbar_fotografia.set_estado("Stop")
        return False

    def __update_balance_toolbars(self, config):
        """
        Actualiza las toolbars de balance en video.
        """

        self.balance_config_widget.set_balance(
            brillo=config.get('brillo', False),
            contraste=config.get('contraste', False),
            saturacion=config.get('saturacion', False),
            hue=config.get('hue', False),
            gamma=config.get('gamma', False))

    def __set_video_out(self, widget, tipo, formato):
        """
        Setea la salida de video para camara de filmación y fotografía.
        """

        self.jamediawebcam.set_formato(formato)
        self.emit("cancel-toolbars")

    def __set_camara(self, widget, tipo, device):
        """
        Setea la entrada de video para camara de filmación y fotografía.
        Si la entrada de video es la red lan, deshabilita el volcado a la
        red y la grabación.
        """

        if "Escritorio" in device:
            self.video_out_setting.set_sensitive(True)
            self.get_toplevel().toolbar.permitir_filmar(True)

        else:
            if "/dev/video" in device:
                self.video_out_setting.set_sensitive(True)
                self.get_toplevel().toolbar.permitir_filmar(True)

            else:
                #FIXME: Anular Grabación para cámara Remota:
                self.video_out_setting.set_sensitive(False)
                self.get_toplevel().toolbar.permitir_filmar(False)

        self.__re_init_video_web_cam(device=device)
        self.emit("cancel-toolbars")

    def __re_init_video_web_cam(self, device=False, salida=False):
        """
        Cuando se agregan o quitan efectos o se cambia la fuente de video,
        se crea un nuevo objeto gstreamer que mantiene las configuraciones
        realizadas hasta el momento.
        """

        if PR:
            print "__re_init_video_web_cam", device, salida

        rot = 0
        config = {}

        if self.jamediawebcam:
            rot = self.jamediawebcam.get_rotacion()
            config = self.jamediawebcam.get_config()

        efectos = self.efectos_en_pipe.get_efectos()

        if not device:
            device = self.camara_setting.device

        if not salida:
            salida = self.video_out_setting.formato

        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        time.sleep(3)

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamVideo(
            xid, device=device, formato=salida,
            efectos=efectos)

        self.jamediawebcam.connect("update",
            self.__update_record)
        self.jamediawebcam.connect("stop-rafaga",
            self.__recibe_stop_rafaga)
        self.jamediawebcam.connect("endfile",
            self.__control_grabacion_end)

        self.jamediawebcam.play()
        self.__re_config(rot, config, efectos)

    def __re_config(self, rot, config, efectos):

        if PR:
            print "__re_config", rot, config, efectos

        self.jamediawebcam.set_balance(
            brillo=config.get("brillo", False),
            contraste=config.get("contraste", False),
            saturacion=config.get("saturacion", False),
            hue=config.get("hue", False),
            gamma=config.get("gamma", False))

        if rot:
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

    def update_accions(self, accion, uri):
        """
        Cuando se quita un archivo de su lugar a través de la lista,
        se detienen los reproductores y se quita la tarea de ese
        archivo en el conversor.
        """

        if accion in ["Quitar", "Borrar", "Mover"]:
            if self.player:
                self.player.stop()

            if self.imageplayer:
                self.imageplayer.stop()

            self.jamediaconvert.quitar(uri)

    def mode_change(self, tipo):
        """
        Cambia el modo de la aplicación.
        """

        if PR:
            print "Mode_Change:", tipo

        self.get_toplevel().toolbar.set_sensitive(False)

        self.jamediaconvert.reset()
        self.jamediaconvert.hide()
        self.pantalla.show()

        if self.jamediawebcam:
            self.jamediawebcam.stop()
            del(self.jamediawebcam)
            self.jamediawebcam = False

        if self.player:
            self.player.stop()
            del(self.player)
            self.player = False

        if self.imageplayer:
            self.imageplayer.stop()
            del(self.imageplayer)
            self.imageplayer = False

        if self.widget_efectos:
            self.widget_efectos.clear()

        self.info_label.set_text("")
        self.info_label.hide()
        self.efectos_en_pipe.clear()
        self.playerlist.limpiar()
        self.progressplayer.hide()

        if tipo == "menu":
            self.__camara_menu_run()

        elif tipo == "video":
            self.__camara_video_run()

        elif tipo == "foto":
            self.__camara_foto_run()

        elif tipo == "jamedia":
            self.__jamedia_run()

        elif tipo == "jamediaimagenes":
            self.__jamediaimagenes_run()

        elif tipo == "converter":
            self.__jamediaconvert_run()

        else:
            print "BasePanel Nuevo Modo:", tipo

        gobject.timeout_add(1000, self.__re_sensitive)

    def set_accion(self, modo, accion):
        """
        Le pasa a la camara las ordenes seleccionadas por el
        usuario en la toolbar correspondiente de la aplicacion.
        """

        self.emit("cancel-toolbars")

        if accion == "Izquierda" or accion == "Derecha":
            if self.jamediawebcam:
                self.jamediawebcam.rotar(accion)

            elif self.player:
                self.player.rotar(accion)

            elif self.imageplayer:
                self.imageplayer.rotar(accion)

            else:
                print "Accion sin definir:", self.set_accion, modo, accion

        elif accion == "Stop":
            if modo == "video":
                self.get_toplevel().toolbar.set_sensitive(False)
                self.__re_init_video_web_cam()
                self.info_label.set_text("")
                self.info_label.hide()
                gobject.timeout_add(1000, self.__re_sensitive)

            elif modo == "foto":
                self.get_toplevel().toolbar.set_sensitive(False)
                self.__re_init_video_web_cam()
                self.info_label.set_text("")
                self.info_label.hide()
                gobject.timeout_add(300, self.__re_sensitive)

            elif modo == "jamediaconverter":
                self.jamediaconvert.tareas_pendientes = []
                # FIXME: Considerar detener la conversíon en progreso

            else:
                print "Accion sin definir:", self.set_accion, modo, accion

        elif accion == "Filmar":  # and modo == "video":
            self.get_toplevel().toolbar.set_sensitive(False)
            hora = time.strftime("%H-%M-%S")
            fecha = str(datetime.date.today())
            archivo = "JV_%s_%s" % (fecha, hora)
            archivo = os.path.join(get_video_directory(), archivo)
            self.jamediawebcam.filmar(archivo)
            gobject.timeout_add(1000, self.__re_sensitive)

        elif accion == "Fotografiar":
            self.get_toplevel().toolbar.set_sensitive(False)
            rafaga = self.rafagas_setting.get_rafaga()
            self.jamediawebcam.fotografiar(get_imagenes_directory(), rafaga)
            gobject.timeout_add(300, self.__re_sensitive)

        # FIXME: Desactivadas por ahora
        #elif accion == "Centrar" or accion == "Acercar" or accion == "Alejar":
        #    self.imageplayer.set_zoom(accion)

        else:
            print "Accion sin definir:", self.set_accion, modo, accion

    def config_show(self, tipo):
        """
        Muestra u oculta los widgets de configuración.
        """

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

        jamedia_widgets = [
            #self.camara_setting,
            #self.video_out_setting,
            #self.rafagas_setting,
            #self.balance_config_widget,
            #self.widget_efectos,
            self.playerlist,
            self.player_control]

        jamediaimagenes_widgets = [
            #self.camara_setting,
            #self.video_out_setting,
            #self.rafagas_setting,
            #self.balance_config_widget,
            #self.widget_efectos,
            self.playerlist,
            #self.player_control,
            ]

        map(ocultar, video_widgets)
        map(ocultar, foto_widgets)
        map(ocultar, jamedia_widgets)
        map(ocultar, jamediaimagenes_widgets)

        if tipo == "camara":
            map(mostrar, video_widgets)
            self.camara_setting.label_ip.set_text(get_ip())

        elif tipo == "foto":
            map(mostrar, foto_widgets)
            self.camara_setting.label_ip.set_text(get_ip())

        elif tipo == "jamedia":
            map(mostrar, jamedia_widgets)

        elif tipo == "jamediaimagenes":
            map(mostrar, jamediaimagenes_widgets)

        else:
            print self.config_show, "Falta definir:", tipo

        if self.jamediawebcam:
            self.__update_balance_toolbars(
                self.jamediawebcam.get_config())

        self.emit("cancel-toolbars")

    def pack_efectos(self):
        """
        Empaqueta los widgets de efectos gstreamer.
        """

        self.widget_efectos = WidgetsGstreamerVideoEfectos()

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
            del(self.jamediawebcam)
            self.jamediawebcam = False

        if self.player:
            self.player.stop()
            del(self.player)
            self.player = False

        if self.imageplayer:
            self.imageplayer.stop()
            del(self.imageplayer)
            self.imageplayer = False

        self.jamediaconvert.reset()
