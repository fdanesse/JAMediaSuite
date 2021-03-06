#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaVideo.py por:
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
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import GObject
from gi.repository import GLib

from Globales import get_audio_directory
from Globales import get_imagenes_directory
from Globales import get_video_directory
from Globales import get_colors

BASE_PATH = os.path.dirname(__file__)

GObject.threads_init()
Gdk.threads_init()


class JAMediaVideo(Gtk.Window):

    def __init__(self):

        super(JAMediaVideo, self).__init__()

        self.set_title("JAMediaVideo")
        self.set_icon_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMediaVideo.svg"))
        self.set_resizable(True)
        self.set_default_size(640, 480)
        self.modify_bg(0, get_colors("drawingplayer"))
        self.set_position(Gtk.WindowPosition.CENTER)

        self.jamediawebcam = None

        self.toolbar = None
        self.toolbar_salir = None
        self.toolbarprincipal = None

        # Sockets para Aplicaciones Embebidas
        #self.socketjamediavideo = None
        #self.socketjamediafotografia = None
        #self.socketjamediaaudio = None
        #self.socketjamedia = None
        #self.socketjamimagenes = None

        # Aplicaciones Embebidas
        #self.jamediavideo = None
        #self.jamediafotografia = None
        #self.jamediaaudio = None
        #self.jamediaplayer = None
        #self.jamimagenes = None

        self.pantalla = None

        self.controlesdinamicos = None

        self.pistas = []

        self.__setup_init()

    def __setup_init(self):
        """
        Genera y empaqueta toda la interfaz.
        """

        from Widgets import Visor
        from Widgets import ToolbarSalir
        from Widgets import Toolbar
        from Widgets import ToolbarPrincipal
        #from JAMediaVideoAplicaciones import JAMediaVideoWidget
        #from JAMediaVideoAplicaciones import JAMediaFotografiaWidget
        #from JAMediaVideoAplicaciones import JAMediaAudioWidget

        #from JAMedia.JAMedia import JAMediaPlayer
        #from JAMImagenes2.JAMImagenes import JAMImagenes

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)
        self.show_all()

        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.toolbarprincipal = ToolbarPrincipal()

        #self.socketjamediavideo = Gtk.Socket()
        #self.socketjamediafotografia = Gtk.Socket()
        #self.socketjamediaaudio = Gtk.Socket()
        #self.socketjamedia = Gtk.Socket()
        #self.socketjamimagenes = Gtk.Socket()

        self.pantalla = Visor()

        vbox.pack_start(self.toolbar, False, True, 0)
        vbox.pack_start(self.toolbar_salir, False, True, 0)
        vbox.pack_start(self.toolbarprincipal, False, True, 0)

        #vbox.pack_start(self.socketjamediavideo, True, True, 0)
        #vbox.pack_start(self.socketjamediafotografia, True, True, 0)
        #vbox.pack_start(self.socketjamediaaudio, True, True, 0)
        #vbox.pack_start(self.socketjamedia, True, True, 0)
        #vbox.pack_start(self.socketjamimagenes, True, True, 0)

        vbox.pack_start(self.pantalla, True, True, 0)

        #self.jamediavideo = JAMediaVideoWidget()
        #self.socketjamediavideo.add_id(self.jamediavideo.get_id())

        #self.jamediafotografia = JAMediaFotografiaWidget()
        #self.socketjamediafotografia.add_id(self.jamediafotografia.get_id())

        #self.jamediaaudio = JAMediaAudioWidget()
        #self.socketjamediaaudio.add_id(self.jamediaaudio.get_id())

        #self.jamediaplayer = JAMediaPlayer()
        #self.socketjamedia.add_id(self.jamediaplayer.get_id())

        #self.jamimagenes = JAMImagenes()
        #self.socketjamimagenes.add_id(self.jamimagenes.get_id())

        self.show_all()
        self.realize()

        GLib.idle_add(self.__setup_init2)

    def __setup_init2(self):
        """
        Inicializa la aplicación a su estado fundamental.
        """

        from JAMediaWebCam import JAMediaWebCam

        #self.jamediaplayer.setup_init()
        #self.jamediaplayer.switch_reproductor(None, "JAMediaReproductor")

        #self.jamediavideo.setup_init()
        #self.jamediafotografia.setup_init()
        #self.jamediaaudio.setup_init()

        #self.controlesdinamicos = [
        #    self.toolbar,
        #    self.toolbar_salir,
        #    self.toolbarprincipal,
        #    self.socketjamediavideo,
        #    self.socketjamediafotografia,
        #    self.socketjamediaaudio,
        #    self.socketjamedia,
        #    self.socketjamimagenes]

        #map(self.__ocultar, self.controlesdinamicos)
        #map(self.__mostrar, [self.toolbar, self.toolbarprincipal])

        #from gi.repository import GdkX11

        #xid = self.pantalla.get_property('window').get_xid()
        #self.jamediawebcam = JAMediaWebCam(xid)

        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar_salir.connect('salir', self.__salir)
        self.toolbarprincipal.connect("menu", self.__get_menu)

        #self.jamediavideo.connect('salir', self.__get_menu_base)
        #self.jamediafotografia.connect('salir', self.__get_menu_base)
        #self.jamediaaudio.connect('salir', self.__get_menu_base)
        #self.jamediaplayer.connect('salir', self.__get_menu_base)
        #self.jamimagenes.connect('salir', self.__get_menu_base)

        self.pantalla.connect("button_press_event", self.__clicks_en_pantalla)

        self.connect("delete-event", self.__salir)

        #self.fullscreen()

        #from JAMediaObjects.JAMediaGlobales import get_video_efectos
        #from JAMediaObjects.JAMediaGlobales import get_visualizadores

        #self.jamediavideo.cargar_efectos(list(get_video_efectos()))
        #self.jamediafotografia.cargar_efectos(list(get_video_efectos()))
        #self.jamediaaudio.cargar_efectos(list(get_video_efectos()))
        #self.jamediaaudio.cargar_visualizadores(list(get_visualizadores()))

        #GLib.idle_add(self.jamediawebcam.reset)

        #if self.pistas:
        #    # FIXME: Agregar reconocer tipo de archivo para cargar
        #    # la lista en jamedia o jamediaimagenes.
        #    map(self.__ocultar, self.controlesdinamicos)
        #    self.jamediawebcam.stop()
        #    map(self.__ocultar, [self.pantalla])
        #    map(self.__mostrar, [self.socketjamedia])
        #    self.jamediaplayer.set_nueva_lista(self.pistas)

    def __clicks_en_pantalla(self, widget, event):
        """
        Hace fullscreen y unfullscreen sobre la
        ventana principal cuando el usuario hace
        doble click en el visor.
        """

        if event.type.value_name == "GDK_2BUTTON_PRESS":
            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w, h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())

            if ww == w and hh == h:
                ventana.unfullscreen()

            else:
                ventana.fullscreen()

    def __get_menu_base(self, widget):
        """
        Cuando se sale de un menú particular,
        se vuelve al menú principal.
        """
        pass
        #map(self.__ocultar, self.controlesdinamicos)
        #map(self.__mostrar, [self.toolbar,
        #    self.toolbarprincipal, self.pantalla])

        #GLib.idle_add(self.jamediawebcam.reset)

    def __get_menu(self, widget, menu):
        """
        Cuando se hace click en algún botón de
        la toolbar principal, se entra en el menú
        correspondiente o se ejecuta determinada acción.
        """
        pass
        #map(self.__ocultar, self.controlesdinamicos)

        #if menu == "Filmar":
        #    self.jamediawebcam.stop()
        #    map(self.__ocultar, [self.pantalla])
        #    map(self.__mostrar, [self.socketjamediavideo])
        #    self.jamediavideo.play()

        #elif menu == "Fotografiar":
        #    self.jamediawebcam.stop()
        #    map(self.__ocultar, [self.pantalla])
        #    map(self.__mostrar, [self.socketjamediafotografia])
        #    self.jamediafotografia.play()

        #elif menu == "Grabar":
        #    self.jamediawebcam.stop()
        #    map(self.__ocultar, [self.pantalla])
        #    map(self.__mostrar, [self.socketjamediaaudio])
        #    self.jamediaaudio.play()

        #elif menu == "Reproducir":
        #    self.jamediawebcam.stop()
        #    map(self.__ocultar, [self.pantalla])
        #    map(self.__mostrar, [self.socketjamedia])
        #    archivos = []

        #    for arch in os.listdir(get_audio_directory()):
        #        ar = os.path.join(get_audio_directory(), arch)
        #        archivos.append([arch, ar])

        #    for arch in os.listdir(get_video_directory()):
        #        ar = os.path.join(get_video_directory(), arch)
        #        archivos.append([arch, ar])

        #    GLib.idle_add(self.jamediaplayer.set_nueva_lista, archivos)

        #elif menu == "Ver":
        #    self.jamediawebcam.stop()
        #    map(self.__ocultar, [self.pantalla])
        #    map(self.__mostrar, [self.socketjamimagenes])

        #    self.jamimagenes.switch_to(None, get_imagenes_directory())

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

    def set_pistas(self, pistas):

        self.pistas = pistas

    def __confirmar_salir(self, widget=None, senial=None):
        """
        Recibe salir y lo pasa a la toolbar de confirmación.
        """

        self.toolbar_salir.run("JAMediaVideo")

    def __salir(self, widget=None, senial=None):
        """
        Reconfigurar la cámara y salir.
        """

        #self.jamediawebcam.reset()
        #self.jamediawebcam.stop()

        import sys
        Gtk.main_quit()
        sys.exit(0)


def get_item_list(path):

    if os.path.exists(path):
        if os.path.isfile(path):

            from JAMediaObjects.JAMFileSystem import describe_archivo

            archivo = os.path.basename(path)
            datos = describe_archivo(path)

            if 'audio' in datos or \
                'video' in datos or \
                'application/ogg' in datos or \
                'application/octet-stream' in datos:
                    return [archivo, path]

    return False

if __name__ == "__main__":

    items = []
    import sys

    if len(sys.argv) > 1:

        for campo in sys.argv[1:]:
            path = os.path.join(campo)

            if os.path.isfile(path):
                item = get_item_list(path)

                if item:
                    items.append(item)

            elif os.path.isdir(path):

                for arch in os.listdir(path):
                    newpath = os.path.join(path, arch)

                    if os.path.isfile(newpath):
                        item = get_item_list(newpath)

                        if item:
                            items.append(item)

        if items:
            jamediavideo = JAMediaVideo()
            jamediavideo.set_pistas(items)

        else:
            jamediavideo = JAMediaVideo()

    else:
        jamediavideo = JAMediaVideo()

    Gtk.main()
