#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaVideoEfectos.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
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

"""
    Para probar los efectos gráficos de gstreamer y sus diferentes
    configuraciones.
"""

import os

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gst
from gi.repository import GstVideo

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

GObject.threads_init()
Gst.init([])

class Ventana(Gtk.Window):

    def __init__(self):

        super(Ventana, self).__init__()

        self.set_title("JAMediaVideoEfectos.")
        #self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
        #    "Iconos", "ver.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        hpanel = Gtk.HPaned()

        from JAMediaObjects.JAMediaWidgets import Visor

        # plugins Good
        from WidgetsEfectosGood import Radioactv
        from WidgetsEfectosGood import Agingtv

        pantalla = Visor()
        self.widget_efecto = Radioactv()
        #self.widget_efecto = Agingtv()

        hpanel.pack1(pantalla, resize = True, shrink = True)
        hpanel.pack2(self.widget_efecto, resize = False, shrink = True)

        self.add(hpanel)

        self.show_all()
        self.realize()

        from gi.repository import GdkX11

        xid = pantalla.get_property('window').get_xid()
        self.efecto = EfectoBin('radioactv', xid)
        #self.efecto = EfectoBin('agingtv', xid)

        self.widget_efecto.connect('propiedad', self.set_efecto)
        self.connect("destroy", self.salir)

        GLib.idle_add(self.efecto.play)

    def set_efecto(self, widget, propiedad, valor):
        """
        Setea propieades en el efecto, según las señales
        que envía widget_efecto.
        """

        self.efecto.set_efecto(propiedad, valor)

    def salir(self, widget = False, senial = False):

        import sys
        sys.exit(0)

class EfectoBin(GObject.GObject):
    """
    Pipeline genérico para efecto de video,
    para explorar configuraciones.
    """

    def __init__(self, nombre, ventana_id):
        """
        Recibe el nombre del efecto y el id del widget
        donde debe dibujar gstreamer.
        """

        GObject.GObject.__init__(self)

        self.ventana_id = ventana_id

        self.pipeline = Gst.Pipeline()

        camara = Gst.ElementFactory.make('v4l2src', "webcam")
        videoconvert1 = Gst.ElementFactory.make('videoconvert', "videoconvert1")
        self.efecto = Gst.ElementFactory.make('%s' % (nombre), "efecto")
        videoconvert2 = Gst.ElementFactory.make('videoconvert', "videoconvert2")
        pantalla = Gst.ElementFactory.make('xvimagesink', "pantalla")

        self.pipeline.add(camara)
        self.pipeline.add(videoconvert1)
        self.pipeline.add(self.efecto)
        self.pipeline.add(videoconvert2)
        self.pipeline.add(pantalla)

        camara.link(videoconvert1)
        videoconvert1.link(self.efecto)
        self.efecto.link(videoconvert2)
        videoconvert2.link(pantalla)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_mensaje)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.sync_message)

    def set_efecto(self, propiedad, valor):

        self.efecto.set_property(propiedad, valor)
        print propiedad, valor

    def sync_message(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        try:
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

        except:
            pass

    def on_mensaje(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "***", 'on_mensaje'
            print err, debug
            self.pipeline.set_state(Gst.State.READY)

    def pause(self, widget = False, event = False):

        self.pipeline.set_state(Gst.State.PAUSED)

    def play(self, widget = False, event = False):

        self.pipeline.set_state(Gst.State.PLAYING)

        return False

    def stop(self, widget = False, event = False):

        self.pipeline.set_state(Gst.State.PAUSED)
        self.pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":

    Ventana()
    Gtk.main()

