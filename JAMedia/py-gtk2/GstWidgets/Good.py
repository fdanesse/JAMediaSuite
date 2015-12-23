#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Good.py por:
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
Widgets con controles de configuración para cada uno de los efectos gráficos
    disponibles en gstreamer.

    Contiene:
        Radioactv
        Agingtv

    Debido a que no son configurables No Contiene:
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

import os
import gtk
import gobject

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.dirname(BASE_PATH)


def get_separador(draw=False, ancho=0, expand=False):
    """
    Devuelve un separador generico.
    """
    separador = gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


def get_color(color):
    """
    Devuelve Colores predefinidos.
    """
    colors = {
        "GRIS": gtk.gdk.Color(60156, 60156, 60156),
        "AMARILLO": gtk.gdk.Color(65000, 65000, 40275),
        "NARANJA": gtk.gdk.Color(65000, 26000, 0),
        "BLANCO": gtk.gdk.Color(65535, 65535, 65535),
        "NEGRO": gtk.gdk.Color(0, 0, 0),
        "ROJO": gtk.gdk.Color(65000, 0, 0),
        "VERDE": gtk.gdk.Color(0, 65000, 0),
        "AZUL": gtk.gdk.Color(0, 0, 65000),
        }
    return colors.get(color, None)


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
    "propiedad": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.VBox.__init__(self)

        self.control = True

        frame1 = gtk.Frame()
        frame1.set_label("Color:")
        frame1.set_border_width(4)
        frame1.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
        frame1.set_label_align(0.5, 1.0)
        frame1.add(self.__get_widgets_colors())

        frame2 = gtk.Frame()
        frame2.set_label("Modo:")
        frame2.set_border_width(4)
        frame2.set_label_align(0.5, 1.0)
        frame2.add(self.__get_widgets_modo())

        #self.interval = ToolbarcontrolValores('interval')
        #self.interval.connect('valor', self.__set_interval)

        self.pack_start(frame1, False, False, 0)
        self.pack_start(frame2, False, False, 0)
        #self.pack_start(self.interval, False, False, 0)

        self.show_all()

        self.control = False

    def __get_widgets_colors(self):
        """
        Cuatro botones para seleccionar el color.
        """

        hbox = gtk.HBox()

        self.white = gtk.RadioButton()
        self.white.set_label("W")
        self.white.connect('toggled', self.__set_color, 3)
        self.white.modify_bg(0, get_color("BLANCO"))
        self.white.set_tooltip_text('Blanco')
        hbox.pack_start(self.white, False, False, 0)

        self.red = gtk.RadioButton()
        self.red.set_label("R")
        self.red.connect('toggled', self.__set_color, 0)
        self.red.modify_bg(0, get_color("ROJO"))
        self.red.set_tooltip_text('Rojo')
        hbox.pack_start(self.red, False, False, 0)
        self.red.set_group(self.white)

        self.green = gtk.RadioButton()
        self.green.set_label("G")
        self.green.connect('toggled', self.__set_color, 1)
        self.green.modify_bg(0, get_color("VERDE"))
        self.green.set_tooltip_text('VERDE')
        hbox.pack_start(self.green, False, False, 0)
        self.green.set_group(self.white)

        self.blue = gtk.RadioButton()
        self.blue.set_label("B")
        self.blue.connect('toggled', self.__set_color, 2)
        self.blue.modify_bg(0, get_color("AZUL"))
        self.blue.set_tooltip_text('AZUL')
        hbox.pack_start(self.blue, False, False, 0)
        self.blue.set_group(self.white)

        return hbox

    def __get_widgets_modo(self):
        """
        Cuatro botones para seleccinar el modo.
        """

        hbox = gtk.HBox()

        self.modo0 = gtk.RadioButton()
        self.modo0.set_label("0")
        self.modo0.set_tooltip_text('normal')
        self.modo0.connect('toggled', self.__set_modo, 0)
        hbox.pack_start(self.modo0, False, False, 0)

        self.modo1 = gtk.RadioButton()
        self.modo1.set_label("1")
        self.modo1.set_tooltip_text('strobe1')
        self.modo1.connect('toggled', self.__set_modo, 1)
        self.modo1.set_group(self.modo0)
        hbox.pack_start(self.modo1, False, False, 0)

        self.modo2 = gtk.RadioButton()
        self.modo2.set_label("2")
        self.modo2.set_tooltip_text('strobe2')
        self.modo2.connect('toggled', self.__set_modo, 2)
        self.modo2.set_group(self.modo0)
        hbox.pack_start(self.modo2, False, False, 0)

        self.modo3 = gtk.RadioButton()
        self.modo3.set_label("3")
        self.modo3.set_tooltip_text('strobe3')
        self.modo3.connect('toggled', self.__set_modo, 3)
        self.modo3.set_group(self.modo0)
        hbox.pack_start(self.modo3, False, False, 0)

        return hbox

    #def __set_interval(self, widget, valor):
    #    if self.control:
    #        return
    #    interval = long(2147483647 * valor / 100.0)
    #    self.emit('propiedad', 'interval', interval)

    def __set_color(self, widget, color):
        if self.control:
            return
        if widget.get_active():
            self.emit('propiedad', 'color', color)

    def __set_modo(self, widget, mode):
        if self.control:
            return
        if widget.get_active():
            self.emit('propiedad', 'mode', mode)

    def reemit_config(self):
        widgets = [self.red, self.green, self.blue, self.white]
        for widget in widgets:
            if widget.get_active():
                widget.set_active(True)
                self.__set_color(widget, widgets.index(widget))
                break
        for widget in [self.modo0, self.modo1, self.modo2, self.modo3]:
            if widget.get_active():
                widget.set_active(True)
                self.__set_modo(widget, int(widget.get_label()))
                break

    def reset(self):
        self.control = True
        #self.interval.set_progress(0.0)
        self.white.set_active(True)
        self.modo0.set_active(True)
        self.control = False


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
    "propiedad": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.VBox.__init__(self)

        self.control = True

        self.switch_dusts = False
        self.switch_pits = False
        self.scratch_lines = ToolbarcontrolValores('scratch-lines')
        self.scratch_lines.connect('valor', self.__set_scratch_lines)

        self.pack_start(self.scratch_lines, False, False, 0)
        self.pack_start(self.__get_toolbar_pits(), False, False, 0)
        self.pack_start(self.__get_toolbar_dusts(), False, False, 0)

        self.reset()
        self.show_all()

        self.control = False

    def __get_toolbar_dusts(self):
        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        self.switch_dusts = gtk.CheckButton()
        self.switch_dusts.set_active(True)
        self.switch_dusts.show()
        item = gtk.ToolItem()
        item.set_expand(False)
        item.add(self.switch_dusts)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        label = gtk.Label("dusts")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        self.switch_dusts.connect('toggled', self.__set_dusts)

        return toolbar

    def __get_toolbar_pits(self):
        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        self.switch_pits = gtk.CheckButton()
        self.switch_pits.set_active(True)
        self.switch_pits.show()
        item = gtk.ToolItem()
        item.set_expand(False)
        item.add(self.switch_pits)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        label = gtk.Label("pits")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        self.switch_pits.connect('toggled', self.__set_pits)

        return toolbar

    def __set_scratch_lines(self, widget, valor):
        if self.control:
            return
        interval = int(20.0 * valor / 100.0)
        self.emit('propiedad', 'scratch-lines', interval)

    def __set_pits(self, widget, x=False):
        if self.control:
            return
        self.emit("propiedad", 'pits', widget.get_active())

    def __set_dusts(self, widget, x=False):
        if self.control:
            return
        self.emit("propiedad", 'dusts', widget.get_active())

    def reemit_config(self):
        self.__set_scratch_lines(False, self.scratch_lines.get_progress())
        self.switch_dusts.set_active(self.switch_dusts.get_active())
        self.__set_dusts(self.switch_dusts)
        self.switch_pits.set_active(self.switch_pits.get_active())
        self.__set_pits(self.switch_pits)

    def reset(self):
        self.control = True
        self.scratch_lines.set_progress(35.0)
        self.switch_dusts.set_active(True)
        self.switch_pits.set_active(True)
        self.control = False


class ToolbarcontrolValores(gtk.Toolbar):
    """
    Toolbar con escala para modificar
    valores de balance en video, utilizada
    por ToolbarBalanceConfig.
    """

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self, label):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        self.titulo = label

        self.escala = SlicerBalance()

        item = gtk.ToolItem()
        item.set_expand(True)

        self.frame = gtk.Frame()
        self.frame.set_label(self.titulo)
        self.frame.modify_bg(0, gtk.gdk.color_parse("#ffffff"))
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
        if valor > 99.4:
            valor = 100.0
        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def set_progress(self, valor):
        """
        Establece valores en la escala.
        """
        self.escala.set_progress(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def get_progress(self):
        return self.escala.get_progress()


class SlicerBalance(gtk.EventBox):
    """
    Barra deslizable para cambiar valores de Balance en Video.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        self.escala = BalanceBar(gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))

        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)

    def set_progress(self, valor=0.0):
        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()

    def get_progress(self):
        return self.escala.ajuste.get_value()

    def __emit_valor(self, widget, valor):
        self.emit("user-set-value", valor)


class BalanceBar(gtk.HScale):
    """
    Escala de SlicerBalance.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(0, gtk.gdk.color_parse("#ffffff"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (7, 10)

        icono = os.path.join(BASE_PATH, "Iconos", "controlslicer.svg")
        self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 16, 16)

        self.connect("expose_event", self.__expose)

        self.show_all()

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """
        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:
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

        gc.set_rgb_fg_color(gtk.gdk.color_parse("#ffffff"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        gc.set_rgb_fg_color(gtk.gdk.Color(0, 0, 0))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(gtk.gdk.Color(65000, 26000, 0))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True
