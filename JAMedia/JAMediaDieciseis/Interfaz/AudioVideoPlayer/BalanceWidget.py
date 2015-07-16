#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
from ..Globales import get_colors

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class BalanceWidget(gtk.EventBox):

    __gsignals__ = {
    'balance-valor': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
        (gobject.TYPE_FLOAT, gobject.TYPE_STRING))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        tabla = gtk.Table(rows=5, columns=1, homogeneous=True)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        tabla.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.brillo = ToolbarcontrolValores("Brillo")
        self.contraste = ToolbarcontrolValores("Contraste")
        self.saturacion = ToolbarcontrolValores("Saturación")
        self.hue = ToolbarcontrolValores("Matíz")
        self.gamma = ToolbarcontrolValores("Gamma")

        tabla.attach(self.brillo, 0, 1, 0, 1)
        tabla.attach(self.contraste, 0, 1, 1, 2)
        tabla.attach(self.saturacion, 0, 1, 2, 3)
        tabla.attach(self.hue, 0, 1, 3, 4)
        tabla.attach(self.gamma, 0, 1, 4, 5)

        self.add(tabla)
        self.show_all()

        self.set_size_request(150, -1)

        self.brillo.connect('valor', self.__emit_senial, 'brillo')
        self.contraste.connect('valor', self.__emit_senial, 'contraste')
        self.saturacion.connect('valor', self.__emit_senial, 'saturacion')
        self.hue.connect('valor', self.__emit_senial, 'hue')
        self.gamma.connect('valor', self.__emit_senial, 'gamma')

    def __emit_senial(self, widget, valor, tipo):
        self.emit('balance-valor', valor, tipo)

    def set_balance(self, brillo=50.0, contraste=50.0,
        saturacion=50.0, hue=50.0, gamma=10.0):
        if saturacion != None:
            self.saturacion.set_progress(saturacion)
        if contraste != None:
            self.contraste.set_progress(contraste)
        if brillo != None:
            self.brillo.set_progress(brillo)
        if hue != None:
            self.hue.set_progress(hue)
        if gamma != None:
            self.gamma.set_progress(gamma)


class ToolbarcontrolValores(gtk.Toolbar):

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self, label):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.titulo = label
        self.escala = SlicerBalance()

        item = gtk.ToolItem()
        item.set_expand(True)

        self.frame = gtk.Frame()
        self.frame.set_border_width(4)
        self.frame.set_label(self.titulo)
        self.frame.get_property("label-widget").modify_fg(
            gtk.STATE_NORMAL, get_colors("drawingplayer"))
        self.frame.set_label_align(0.5, 1.0)
        event = gtk.EventBox()
        event.set_border_width(4)
        event.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        event.add(self.escala)
        self.frame.add(event)
        self.frame.show_all()
        item.add(self.frame)
        self.insert(item, -1)

        self.show_all()

        self.escala.escala.connect("user-set-value", self.__user_set_value)

    def __user_set_value(self, widget=None, valor=None):
        if valor > 99.4:
            valor = 100.0
        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def set_progress(self, valor=0.0):
        self.escala.escala.set_value(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))


class SlicerBalance(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.escala = BalanceBar(gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))

        self.add(self.escala)
        self.show_all()


class BalanceBar(gtk.HScale):

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.set_property("adjustment", ajuste)
        self.set_digits(0)
        self.set_draw_value(False)

        self.show_all()

    def do_motion_notify_event(self, event):
        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:
            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)
            if valor >= 0.0 and valor <= 100.0:
                self.set_value(valor)
                self.emit("user-set-value", valor)
