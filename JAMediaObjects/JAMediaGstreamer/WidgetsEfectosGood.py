#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetsEfectosGood.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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
    Widgets con controles de configuración para cada uno de
    los efectos gráficos disponibles en gstreamer.
"""

from gi.repository import Gtk
from gi.repository import GObject

from JAMediaObjects.JAMediaGlobales import get_color
from JAMediaObjects.JAMediaGlobales import get_pixels
from JAMediaObjects.JAMediaGlobales import get_separador

"""
Contiene:
    Radioactv
    Agingtv

No Contiene (Debido a que no son configurables):
    edgetv
    warptv
    shagadelictv

    dicetv          (Solo se puede configurar square-bits de 0-5)
    rippletv        (Solo se puede configurar el modo 0-1)
    vertigotv       (Solo se puede configurar speed y zoom-speed)
    streaktv        (Solo se puede configurar feedback true-false)

    optv            Es bien feo
    revtv           Feo
"""


class Radioactv(Gtk.VBox):
    """
    Element Properties:
        name                : The name of the object
                            flags: legible, escribible
                            String. Default: "radioactv0"
        parent              : The parent of the object
                            flags: legible, escribible
                            Object of type "GstObject"
        qos                 : Handle Quality-of-Service events
                            flags: legible, escribible
                            Boolean. Default: true
        mode                : Mode
                            flags: legible, escribible
                            Enum "GstRadioacTVMode" Default: 0, "normal"
                               (0): normal           - Normal
                               (1): strobe1          - Strobe 1
                               (2): strobe2          - Strobe 2
                               (3): trigger          - Trigger
        color               : Color
                            flags: legible, escribible, controlable
                            Enum "GstRadioacTVColor" Default: 3, "white"
                               (0): red              - Red
                               (1): green            - Green
                               (2): blue             - Blue
                               (3): white            - White
        interval            : Snapshot interval (in strobe mode)
                            flags: legible, escribible, controlable
                            Unsigned Integer. Range: 0 - 2147483647 Default: 3
        trigger             : Trigger (in trigger mode)
                            flags: legible, escribible, controlable
                            Boolean. Default: false
    """

    __gsignals__ = {
    "propiedad": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.VBox.__init__(self)

        frame1 = Gtk.Frame()
        frame1.set_label("Color:")
        frame1.set_label_align(0.5, 1.0)
        frame1.add(self.__get_widgets_colors())

        frame2 = Gtk.Frame()
        frame2.set_label("Modo:")
        frame2.set_label_align(0.5, 1.0)
        frame2.add(self.__get_widgets_modo())

        from JAMediaObjects.JAMediaWidgets import ToolbarcontrolValores

        interval = ToolbarcontrolValores('interval')
        interval.connect('valor', self.__set_interval)

        self.pack_start(frame1, False, False, 0)
        self.pack_start(frame2, False, False, 0)
        self.pack_start(interval, False, False, 0)
        self.pack_start(self.__get_toolbar_on_off(), False, False, 0)

        self.show_all()

    def __get_widgets_colors(self):
        """
        Cuatro botones para seleccionar el color.
        """

        from JAMediaObjects.JAMediaWidgets import JAMediaButton

        color_widgets = Gtk.HBox()

        white = JAMediaButton()
        white.connect('clicked', self.__set_color, 3)
        white.set_colores(colornormal=get_color("BLANCO"))
        white.set_tooltip('Blanco')

        red = JAMediaButton()
        red.connect('clicked', self.__set_color, 0)
        red.set_colores(colornormal=get_color("ROJO"))
        red.set_tooltip('Rojo')

        green = JAMediaButton()
        green.connect('clicked', self.__set_color, 1)
        green.set_colores(colornormal=get_color("VERDE"))
        green.set_tooltip('Verde')

        blue = JAMediaButton()
        blue.connect('clicked', self.__set_color, 2)
        blue.set_colores(colornormal=get_color("AZUL"))
        blue.set_tooltip('Azul')

        self.botones_colores = [
            white,
            red,
            green,
            blue]

        for button in self.botones_colores:
            button.set_tamanio(get_pixels(1.0), get_pixels(1.0))
            color_widgets.pack_start(button, True, True, 1)
            button.connect('clicked', self.__clicked_color)

        return color_widgets

    def __get_widgets_modo(self):
        """
        Cuatro botones para seleccinar el modo.
        """

        from JAMediaObjects.JAMediaWidgets import JAMediaButton

        modo_widgets = Gtk.HBox()

        white = JAMediaButton()
        white.connect('clicked', self.__set_modo, 0)
        white.set_label(0)
        white.set_tooltip('normal')

        red = JAMediaButton()
        red.connect('clicked', self.__set_modo, 1)
        red.set_label(1)
        red.set_tooltip('strobe1')

        green = JAMediaButton()
        green.connect('clicked', self.__set_modo, 2)
        green.set_label(2)
        green.set_tooltip('strobe2')

        blue = JAMediaButton()
        blue.connect('clicked', self.__set_modo, 3)
        blue.set_label(3)
        blue.set_tooltip('trigger')

        self.botones_modo = [
            white,
            red,
            green,
            blue]

        for button in self.botones_modo:
            button.set_tamanio(get_pixels(1.0), get_pixels(1.0))
            modo_widgets.pack_start(button, True, True, 1)
            button.connect('clicked', self.__clicked_modo)

        return modo_widgets

    def __get_toolbar_on_off(self):
        """
        En modo 3, se puede desactivar y activar el efecto.
        switch activa y desactiva el efecto si modo == 3.
        """

        toolbar = Gtk.Toolbar()

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        label = Gtk.Label("on:")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.switch = Gtk.Switch()
        self.switch.set_active(True)
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(self.switch)
        toolbar.insert(item, -1)

        self.switch.connect('button-press-event', self.__set_trigger)

        return toolbar

    def __clicked_color(self, widget, void):

        for boton in self.botones_colores:

            if not boton == widget:
                boton.des_seleccionar()

    def __clicked_modo(self, widget, void):

        for boton in self.botones_modo:

            if not boton == widget:
                boton.des_seleccionar()

    def __set_interval(self, widget, valor):
        """
        Setea el intervalo.
        """

        interval = int(3 * valor / 100.0)
        self.emit('propiedad', 'interval', interval)

    def __set_color(self, widget, void, color):
        """
        void = <class 'gi.overrides.Gdk.EventButton'>
        """

        self.emit('propiedad', 'color', color)

    def __set_modo(self, widget, void, valor):
        """
        void = <class 'gi.overrides.Gdk.EventButton'>
        """

        self.emit('propiedad', 'mode', valor)

    def __set_trigger(self, widget, valor):
        """
        Activa y desactiva el efecto.
        """

        self.emit("propiedad", 'trigger', not widget.get_active())


class Agingtv(Gtk.VBox):
    """
    Element Properties:
          name                : The name of the object
                                flags: legible, escribible
                                String. Default: "agingtv0"
          parent              : The parent of the object
                                flags: legible, escribible
                                Object of type "GstObject"
          qos                 : Handle Quality-of-Service events
                                flags: legible, escribible
                                Boolean. Default: true
          scratch-lines       : Number of scratch lines
                                flags: legible, escribible, controlable
                                Unsigned Integer. Range: 0 - 20 Default: 7
          color-aging         : Color Aging
                                flags: legible, escribible, controlable
                                Boolean. Default: true
          pits                : Pits
                                flags: legible, escribible, controlable
                                Boolean. Default: true
          dusts               : Dusts
                                flags: legible, escribible, controlable
                                Boolean. Default: true
    """

    __gsignals__ = {
    "propiedad": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.VBox.__init__(self)

        from JAMediaObjects.JAMediaWidgets import ToolbarcontrolValores

        interval = ToolbarcontrolValores('scratch-lines')
        interval.connect('valor', self.__set_scratch_lines)

        self.pack_start(interval, False, False, 0)
        # FIXME: Desactivo porque no funciona bien.
        #self.pack_start(self.get_toolbar_color_aging(), False, False, 0)
        self.pack_start(self.__get_toolbar_pits(), False, False, 0)
        self.pack_start(self.__get_toolbar_dusts(), False, False, 0)

        self.show_all()

    def __get_toolbar_dusts(self):

        toolbar = Gtk.Toolbar()

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        label = Gtk.Label("dusts:")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        switch = Gtk.Switch()
        switch.set_active(True)
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar.insert(item, -1)

        switch.connect('button-press-event', self.__set_dusts)

        return toolbar

    def __get_toolbar_pits(self):

        toolbar = Gtk.Toolbar()

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        label = Gtk.Label("pits:")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        switch = Gtk.Switch()
        switch.set_active(True)
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar.insert(item, -1)

        switch.connect('button-press-event', self.__set_pits)

        return toolbar

    def __get_toolbar_color_aging(self):

        toolbar = Gtk.Toolbar()

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        label = Gtk.Label("color-aging:")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        switch = Gtk.Switch()
        switch.set_active(True)
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar.insert(item, -1)

        switch.connect('button-press-event', self.__set_color_aging)

        return toolbar

    def __set_scratch_lines(self, widget, valor):
        """
        Setea el intervalo.
        """

        interval = int(20 * valor / 100.0)
        self.emit('propiedad', 'scratch-lines', interval)

    def __set_color_aging(self, widget, valor):

        self.emit("propiedad", 'color-aging', not widget.get_active())

    def __set_pits(self, widget, valor):

        self.emit("propiedad", 'pits', not widget.get_active())

    def __set_dusts(self, widget, valor):

        self.emit("propiedad", 'dusts', not widget.get_active())
