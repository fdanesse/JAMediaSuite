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

import gtk
from gtk import gdk
import gobject

from Globales import get_audio_directory
from Globales import get_imagenes_directory
from Globales import get_video_directory
from Globales import get_colors

from Toolbars import Toolbar
from Toolbars import ToolbarSalir
from Widgets import Visor

from JAMediaWebCamView import JAMediaWebCamView

BASE_PATH = os.path.dirname(__file__)

gobject.threads_init()
gdk.threads_init()


class JAMediaVideo(gtk.Window):

    def __init__(self):

        super(JAMediaVideo, self).__init__()

        self.set_title("JAMediaVideo")
        self.set_icon_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMediaVideo.svg"))
        self.set_resizable(True)
        self.set_default_size(640, 480)
        self.modify_bg(0, get_colors("window"))
        self.set_position(gtk.WIN_POS_CENTER)

        self.jamediawebcam = None
        self.pistas = []

        vbox = gtk.VBox()
        self.add(vbox)
        self.show_all()

        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.pantalla = Visor()

        vbox.pack_start(self.toolbar, False, True, 0)
        vbox.pack_start(self.toolbar_salir, False, True, 0)
        vbox.pack_start(self.pantalla, True, True, 0)

        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar_salir.connect('salir', self.__salir)
        self.pantalla.connect("button_press_event",
            self.__clicks_en_pantalla)

        self.connect("delete-event", self.__salir)

        self.show_all()
        self.realize()

        gobject.idle_add(self.__run)

    def __run(self):

        self.toolbar_salir.hide()

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamView(xid)

        #if self.pistas:
        #    # FIXME: Agregar reconocer tipo de archivo para cargar
        #    # la lista en jamedia o jamediaimagenes.
        #    map(self.__ocultar, self.controlesdinamicos)
        #    self.jamediawebcam.stop()
        #    map(self.__ocultar, [self.pantalla])
        #    map(self.__mostrar, [self.socketjamedia])
        #    self.jamediaplayer.set_nueva_lista(self.pistas)

        #self.fullscreen()
        self.toolbar.switch("menu")
        gobject.idle_add(self.jamediawebcam.play)

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

    #def __get_menu_base(self, widget):
    #    """
    #    Cuando se sale de un menú particular,
    #    se vuelve al menú principal.
    #    """

    #    # detener camaras
    #    self.toolbar.switch("Ver")

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
        gtk.main_quit()
        sys.exit(0)


def get_item_list(path):

    if os.path.exists(path):
        if os.path.isfile(path):

            from Globales import describe_archivo

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

    gtk.main()
