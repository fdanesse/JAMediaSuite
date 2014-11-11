#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMedia.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

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
import sys
import threading

from Toolbars import Toolbar
from Toolbars import ToolbarSalir
from Toolbars import ToolbarAccion
from Toolbars import ToolbarAddStream

from Widgets import MouseSpeedDetector
from BasePanel import BasePanel

from JAMediaReproductor.JAMediaGrabador import JAMediaGrabador

from Globales import get_colors
from Globales import eliminar_streaming
from Globales import add_stream
from Globales import get_my_files_directory
from Globales import describe_archivo

gobject.threads_init()

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))


def ocultar(objeto):
    if objeto.get_visible():
        objeto.hide()


def mostrar(objeto):
    if not objeto.get_visible():
        objeto.show()


BASE_PATH = os.path.dirname(__file__)


"""
Necesita:
    python-gst0.10
    gstreamer0.10-ffmpeg
    gstreamer0.10-plugins-base
    gstreamer0.10-plugins-good
    gstreamer0.10-plugins-ugly
    gstreamer0.10-plugins-bad
    gstreamer0.10-tools
"""


class JAMedia(gtk.EventBox):

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_sensitive(False)
        #self.set_title("JAMedia")
        #self.set_icon_from_file(os.path.join(BASE_PATH,
        #    "Iconos", "JAMedia.svg"))
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        #self.set_resizable(True)
        self.set_border_width(2)
        #self.set_position(gtk.WIN_POS_CENTER)

        self.archivos = []
        self.grabador = False
        self.mouse_in_visor = False
        self.cursor_root = False

        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.toolbar_accion = ToolbarAccion()
        self.add_stream = ToolbarAddStream()

        self.base_panel = BasePanel()

        vbox = gtk.VBox()
        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(self.toolbar_salir, False, False, 0)
        vbox.pack_start(self.toolbar_accion, False, False, 0)
        vbox.pack_start(self.add_stream, False, False, 0)
        vbox.pack_start(self.base_panel, True, True, 0)

        self.add(vbox)
        self.show_all()
        #self.realize()

        # Controlador del mouse.
        #   http://www.pygtk.org/pygtk2reference/class-gdkdisplay.html
        #   #function-gdk--display-get-default
        icono = os.path.join(BASE_PATH, "Iconos", "jamedia_cursor.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 24)
        self.jamedia_cursor = gtk.gdk.Cursor(
            gtk.gdk.display_get_default(), pixbuf, 0, 0)

        #self.cursor_root = self.get_property("window").get_cursor()
        #self.get_property("window").set_cursor(self.jamedia_cursor)

        self.mouse_listener = MouseSpeedDetector(self)
        self.mouse_listener.new_handler(True)

        self.toolbar.connect("accion", self.__accion_toolbar)

        self.base_panel.connect("show-controls", self.__ocultar_controles)
        self.base_panel.connect("accion-list", self.__accion_list)
        self.base_panel.connect("menu_activo", self.__cancel_toolbars)
        self.base_panel.connect("add_stream", self.__run_add_stream)
        self.base_panel.connect("stop-record", self.__detener_grabacion)

        self.toolbar_accion.connect("accion-stream", self.__accion_stream)
        self.toolbar_accion.connect("grabar", self.__grabar)
        self.toolbar_salir.connect("salir", self.__salir)

        self.add_stream.connect("add-stream", self.__add_stream)

        self.mouse_listener.connect("estado", self.__set_mouse)
        self.connect("hide", self.__hide_show)
        self.connect("show", self.__hide_show)
        #self.connect("delete-event", self.__salir)
        self.connect("realize", self.__realize)

        #self.resize(640, 480)
        gobject.idle_add(self.__setup_init)
        print "JAMedia process:", os.getpid()

    def __realize(self, widget):
        self.cursor_root = self.get_property("window").get_cursor()
        self.get_property("window").set_cursor(self.jamedia_cursor)

    def __add_stream(self, widget, tipo, nombre, url):
        add_stream(tipo, [nombre, url])
        if "Tv" in tipo or "TV" in tipo:
            indice = 3
        elif "Radio" in tipo:
            indice = 2
        else:
            return
        self.base_panel.derecha.lista.cargar_lista(None, indice)

    def __run_add_stream(self, widget, title):
        self.add_stream.set_accion(title)

    def __grabar(self, widget, uri):
        self.set_sensitive(False)
        self.__detener_grabacion()

        tipo = "video"
        label = self.base_panel.derecha.lista.toolbar.label.get_text()
        if label == "JAM-TV" or label == "TVs" or label == "WebCams":
            tipo = "video"
        else:
            tipo = "audio"

        hora = time.strftime("%H-%M-%S")
        fecha = str(datetime.date.today())
        archivo = "%s-%s" % (fecha, hora)
        archivo = os.path.join(get_my_files_directory(), archivo)

        self.grabador = JAMediaGrabador(uri, archivo, tipo)

        self.grabador.connect('update', self.__update_grabador)
        self.grabador.connect('endfile', self.__detener_grabacion)

        _thread = threading.Thread(target=self.grabador.play)
        _thread.start()

        self.set_sensitive(True)

    def __update_grabador(self, widget, datos):
        self.base_panel.izquierda.toolbar_record.set_info(datos)

    def __detener_grabacion(self, widget=None):
        if self.grabador:
            self.grabador.disconnect_by_func(self.__update_grabador)
            self.grabador.disconnect_by_func(self.__detener_grabacion)
            self.grabador.stop()
            del(self.grabador)
            self.grabador = False

        self.base_panel.izquierda.toolbar_record.stop()

    def __accion_stream(self, widget, accion, url):
        lista = self.base_panel.derecha.lista.toolbar.label.get_text()

        if accion == "Borrar":
            eliminar_streaming(url, lista)
            print "Streaming Eliminado:", url

        elif accion == "Copiar":
            modelo, _iter = self.base_panel.derecha.lista.lista.get_selection(
                ).get_selected()
            nombre = modelo.get_value(_iter, 1)
            url = modelo.get_value(_iter, 2)
            tipo = self.base_panel.derecha.lista.toolbar.label.get_text()
            add_stream(tipo, [nombre, url])

        elif accion == "Mover":
            modelo, _iter = self.base_panel.derecha.lista.lista.get_selection(
                ).get_selected()
            nombre = modelo.get_value(_iter, 1)
            url = modelo.get_value(_iter, 2)
            tipo = self.base_panel.derecha.lista.toolbar.label.get_text()
            add_stream(tipo, [nombre, url])
            eliminar_streaming(url, lista)

        else:
            print "accion_stream desconocido:", accion

    def __setup_init(self):
        self.__cancel_toolbars()
        self.toolbar.configurar.set_sensitive(False)
        self.base_panel.setup_init()
        if self.archivos:
            self.base_panel.set_nueva_lista(self.archivos)
            self.archivos = []
        self.set_sensitive(True)
        return False

    def __accion_toolbar(self, widget, accion):
        self.__cancel_toolbars()
        if accion == "salir":
            #self.toolbar_salir.run("JAMedia")
            self.emit('salir')
        elif accion == "show-config":
            self.base_panel.derecha.show_config()
        else:
            print self.__accion_toolbar, accion

    def __hide_show(self, widget):
        """
        Controlador del mouse funcionará solo si JAMedia es Visible.
        """
        self.mouse_listener.new_handler(widget.get_visible())

    def __set_mouse(self, widget, estado):
        """
        Muestra u oculta el mouse de jamedia según su posición.
        """
        win = self.get_property("window")

        if self.mouse_in_visor:  # Solo cuando el mouse está sobre el Visor.
            if estado == "moviendose":
                if win.get_cursor() != self.jamedia_cursor:
                    win.set_cursor(self.jamedia_cursor)
                    return

            elif estado == "detenido":
                if win.get_cursor() != gtk.gdk.BLANK_CURSOR:
                    win.set_cursor(gtk.gdk.Cursor(gtk.gdk.BLANK_CURSOR))
                    return

            elif estado == "fuera":
                if win.get_cursor() != self.cursor_root:
                    win.set_cursor(self.cursor_root)
                    return

        else:
            if estado == "moviendose" or estado == "detenido":
                if win.get_cursor() != self.jamedia_cursor:
                    win.set_cursor(self.jamedia_cursor)
                    return

            elif estado == "fuera":
                if win.get_cursor() != self.cursor_root:
                    win.set_cursor(self.cursor_root)
                    return

    def __ocultar_controles(self, widget, datos):
        zona, ocultar = datos
        self.mouse_in_visor = zona

        if zona and ocultar:
            self.__cancel_toolbars()
            self.set_border_width(0)
            self.base_panel.set_border_width(0)
            self.toolbar.hide()
            self.base_panel.derecha.hide()
            self.base_panel.izquierda.toolbar_info.hide()
            self.base_panel.izquierda.progress.hide()

        elif not zona and ocultar:
            self.toolbar.show()
            self.set_border_width(2)
            self.base_panel.set_border_width(2)
            self.base_panel.derecha.show()
            self.base_panel.izquierda.toolbar_info.show()
            self.base_panel.izquierda.progress.show()

            #if not self.hbox_efectos_en_pipe.get_children():
            #    self.hbox_efectos_en_pipe.get_parent().get_parent(
            #        ).get_parent().hide()

        elif not zona and not ocultar:
            pass

        elif zona and not ocultar:
            pass

    def __salir(self, widget=None, senial=None):
        self.__detener_grabacion()
        self.base_panel.salir()
        gtk.main_quit()
        sys.exit(0)

    def __cancel_toolbars(self, widget=False):
        map(ocultar, self.get_child().get_children()[1:-1])

    def __accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.toolbar_accion.set_accion(lista, accion, _iter)

    def set_archivos(self, archivos):
        self.archivos = archivos


def check_path(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            datos = describe_archivo(path)
            if 'audio' in datos or 'video' in datos or \
                'application/ogg' in datos or \
                'application/octet-stream' in datos:
                    return path
    return False
