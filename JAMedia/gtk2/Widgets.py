#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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
from multiprocessing import Process
from Globales import get_colors
from Globales import get_boton
from Globales import download_streamings
from Globales import set_listas_default
from Globales import get_ip

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class DialogoDescarga(gtk.Dialog):

    def __init__(self, parent=None, force=True):

        gtk.Dialog.__init__(self, parent=parent)

        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_border_width(15)

        self.force = force

        label = gtk.Label("*** Descargando Streamings de JAMedia ***")
        label.show()

        self.vbox.pack_start(label, True, True, 5)
        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):
        gobject.timeout_add(500, self.__descargar)

    def __descargar(self):
        if self.force:
            if get_ip():
                download_streamings()
            else:
                print "No estás conectado a Internet"
        else:
            set_listas_default()
        self.destroy()
        return False


class Credits(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self, parent=parent,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("widgetvideoitem"))
        self.set_border_width(15)

        imagen = gtk.Image()
        imagen.set_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMediaCredits.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class Help(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self, parent=parent,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("widgetvideoitem"))
        self.set_border_width(15)

        tabla1 = gtk.Table(columns=5, rows=2, homogeneous=False)

        vbox = gtk.HBox()
        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")
        self.anterior = get_boton(archivo, flip=True,
            pixels=24, tooltip_text="Anterior")

        self.anterior.connect("clicked", self.__switch)
        self.anterior.show()
        vbox.pack_start(self.anterior, False, False, 0)

        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")
        self.siguiente = get_boton(archivo, pixels=24,
            tooltip_text="Siguiente")

        self.siguiente.connect("clicked", self.__switch)
        self.siguiente.show()
        vbox.pack_end(self.siguiente, False, False, 0)

        tabla1.attach_defaults(vbox, 0, 5, 0, 1)

        self.helps = []

        for x in range(1, 5):
            try:
                help = gtk.Image()
                help.set_from_file(os.path.join(BASE_PATH,
                    "Iconos", "help-%s.svg" % x))
                tabla1.attach_defaults(help, 0, 5, 1, 2)
                self.helps.append(help)
            except:
                pass

        self.vbox.pack_start(tabla1, True, True, 0)
        self.vbox.show_all()

        self.__switch(None)

    def __ocultar(self, objeto):
        if objeto.get_visible():
            objeto.hide()

    def __switch(self, widget):
        if not widget:
            map(self.__ocultar, self.helps[1:])
            self.anterior.hide()
            self.helps[0].show()
        else:
            index = self.__get_index_visible()
            helps = list(self.helps)
            new_index = index

            if widget == self.siguiente:
                if index < len(self.helps) - 1:
                    new_index += 1
            elif widget == self.anterior:
                if index > 0:
                    new_index -= 1

            helps.remove(helps[new_index])
            map(self.__ocultar, helps)
            self.helps[new_index].show()

            if new_index > 0:
                self.anterior.show()
            else:
                self.anterior.hide()

            if new_index < self.helps.index(self.helps[-1]):
                self.siguiente.show()
            else:
                self.siguiente.hide()

    def __get_index_visible(self):
        for help in self.helps:
            if help.get_visible():
                return self.helps.index(help)


class MouseSpeedDetector(gobject.GObject, Process):
    """
    Verifica posición y movimiento del mouse.
    estado puede ser:
        fuera       (está fuera de la ventana según self.parent)
        moviendose
        detenido
    """

    __gsignals__ = {
        'estado': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, parent):

        gobject.GObject.__init__(self)
        Process.__init__(self)

        self.parent = parent

        self.actualizador = False
        self.mouse_pos = (0, 0)

    def __handler(self):
        """
        Emite la señal de estado cada 60 segundos.
        """
        try:
            display, posx, posy = gtk.gdk.display_get_default(
                ).get_window_at_pointer()
        except:
            return True
        if posx > 0 and posy > 0:
            if posx != self.mouse_pos[0] or posy != self.mouse_pos[1]:
                self.mouse_pos = (posx, posy)
                self.emit("estado", "moviendose")
            else:
                self.emit("estado", "detenido")
        else:
            self.emit("estado", "fuera")
        return True

    def new_handler(self, reset):
        """
        Resetea el controlador o lo termina según reset.
        """
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False
        if reset:
            self.actualizador = gobject.timeout_add(1000, self.__handler)
