#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetsEfectosGood.py por:
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

"""
    Widgets con controles de configuración para cada uno de
    los efectos gráficos disponibles en gstreamer.
"""

import os

import gtk
import gobject
from gtk import gdk

from Widgets import JAMediaButton
from Widgets import get_color
from Widgets import get_separador

BASE_PATH = os.path.dirname(__file__)

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


class Radioactv(gtk.VBox):
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
    "propiedad": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.VBox.__init__(self)

        frame1 = gtk.Frame()
        frame1.set_label("Color:")
        frame1.set_border_width(4)
        frame1.modify_bg(0, gdk.color_parse("#ffffff"))
        frame1.set_label_align(0.5, 1.0)
        frame1.add(self.__get_widgets_colors())

        frame2 = gtk.Frame()
        frame2.set_label("Modo:")
        frame2.set_border_width(4)
        frame2.set_label_align(0.5, 1.0)
        frame2.add(self.__get_widgets_modo())

        interval = ToolbarcontrolValores('interval')
        interval.connect('valor', self.__set_interval)

        self.pack_start(frame1, False, False, 0)
        self.pack_start(frame2, False, False, 0)
        self.pack_start(interval, False, False, 0)

        self.show_all()

    def __get_widgets_colors(self):
        """
        Cuatro botones para seleccionar el color.
        """

        color_widgets = gtk.HBox()

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
            button.set_tamanio(24, 24)
            button.set_border_width(4)
            color_widgets.pack_start(button, True, True, 0)
            button.connect('clicked', self.__clicked_color)

        return color_widgets

    def __get_widgets_modo(self):
        """
        Cuatro botones para seleccinar el modo.
        """

        modo_widgets = gtk.HBox()

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
            button.set_tamanio(24, 24)
            button.set_border_width(4)
            modo_widgets.pack_start(button, True, True, 0)
            button.connect('clicked', self.__clicked_modo)

        return modo_widgets

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
        void = <class 'gi.overrides.gdk.EventButton'>
        """

        self.emit('propiedad', 'color', color)

    def __set_modo(self, widget, void, valor):
        """
        void = <class 'gi.overrides.gdk.EventButton'>
        """

        self.emit('propiedad', 'mode', valor)


class Agingtv(gtk.VBox):
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
    "propiedad": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.VBox.__init__(self)

        interval = ToolbarcontrolValores('scratch-lines')
        interval.connect('valor', self.__set_scratch_lines)

        self.pack_start(interval, False, False, 0)
        # FIXME: Desactivo porque no funciona bien.
        #self.pack_start(self.get_toolbar_color_aging(), False, False, 0)
        self.pack_start(self.__get_toolbar_pits(), False, False, 0)
        self.pack_start(self.__get_toolbar_dusts(), False, False, 0)

        self.show_all()

    def __get_toolbar_dusts(self):

        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gdk.color_parse("#ffffff"))

        switch = gtk.CheckButton()
        switch.set_active(True)
        switch.show()
        item = gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        label = gtk.Label("dusts")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        switch.connect('button-press-event', self.__set_dusts)

        return toolbar

    def __get_toolbar_pits(self):

        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gdk.color_parse("#ffffff"))

        switch = gtk.CheckButton()
        switch.set_active(True)
        switch.show()
        item = gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        label = gtk.Label("pits")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        switch.connect('button-press-event', self.__set_pits)

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


class ToolbarcontrolValores(gtk.Toolbar):
    """
    Toolbar con escala para modificar
    valores de balance en video, utilizada
    por ToolbarBalanceConfig.
    """

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self, label):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, gdk.color_parse("#ffffff"))

        self.titulo = label

        self.escala = SlicerBalance()

        item = gtk.ToolItem()
        item.set_expand(True)

        self.frame = gtk.Frame()
        self.frame.set_label(self.titulo)
        self.frame.modify_bg(0, gdk.color_parse("#ffffff"))
        self.frame.set_border_width(4)
        self.frame.set_label_align(0.5, 1.0)
        self.frame.add(self.escala)
        self.frame.show()
        item.add(self.frame)
        self.insert(item, -1)

        self.show_all()

        self.escala.connect("user-set-value", self.__user_set_value)

    def __user_set_value(self, widget=None, valor=None):
        """
        Recibe la posicion en la barra de
        progreso (en % float), y re emite los valores.
        """

        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def set_progress(self, valor):
        """
        Establece valores en la escala.
        """

        self.escala.set_progress(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))


class SlicerBalance(gtk.EventBox):
    """
    Barra deslizable para cambiar valores de Balance en Video.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gdk.color_parse("#ffffff"))

        self.escala = BalanceBar(gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))

        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)

    def set_progress(self, valor=0.0):
        """
        El reproductor modifica la escala.
        """

        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()

    def __emit_valor(self, widget, valor):
        """
        El usuario modifica la escala.
        Y se emite la señal con el valor (% float).
        """

        self.emit("user-set-value", valor)


class BalanceBar(gtk.HScale):
    """
    Escala de SlicerBalance.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(0, gdk.color_parse("#ffffff"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (7, 10)

        icono = os.path.join(os.path.dirname(BASE_PATH),
            "Iconos", "iconplay.svg")
        pixbuf = gdk.pixbuf_new_from_file_at_size(icono,
            16, 16)
        self.pixbuf = pixbuf.rotate_simple(
            gdk.PIXBUF_ROTATE_CLOCKWISE)

        self.connect("expose_event", self.__expose)

        self.show_all()

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """

        if event.state == gdk.MOD2_MASK | \
            gdk.BUTTON1_MASK:

            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)
            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

    def __expose(self, widget, event):
        """
        Dibuja el estado de la barra de progreso.
        """

        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        gc.set_rgb_fg_color(gdk.color_parse("#ffffff"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        gc.set_rgb_fg_color(gdk.Color(0, 0, 0))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(gdk.Color(65000, 26000, 0))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True
