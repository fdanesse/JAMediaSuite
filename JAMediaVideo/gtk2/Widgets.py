#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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

from Globales import get_separador
from Globales import get_boton
from Globales import get_color
from Globales import get_colors

BASE_PATH = os.path.dirname(__file__)


class Info_Label(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.label = gtk.Label("Info Grabador")
        self.label.modify_bg(0, get_colors("drawingplayer"))
        self.label.modify_fg(0, get_colors("window"))

        self.add(self.label)
        self.show_all()

    def set_text(self, text):

        self.label.set_text(text)


class Efectos_en_Pipe(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.box = gtk.HBox()

        self.add(self.box)
        self.show_all()

        #self.set_size_request(-1, 15)

    def clear(self):

        for child in self.box.get_children():
            self.box.remove(child)
            child.destroy()

        self.hide()

    def add_efecto(self, efecto):

        button = gtk.Button(efecto)
        button.set_tooltip_text(efecto)
        self.box.pack_start(button, False, False, 0)
        self.show_all()

    def remover_efecto(self, efecto):

        for button in self.box.get_children():
            if button.get_tooltip_text() == efecto:
                self.box.remove(button)
                button.destroy()
                break

        if not self.box.get_children():
            self.hide()


class Visor(gtk.DrawingArea):
    """
    Visor generico para utilizar como area de
    reproduccion de videos o dibujar.
    """

    __gsignals__ = {
    "ocultar_controles": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.add_events(
            gdk.KEY_PRESS_MASK |
            gdk.KEY_RELEASE_MASK |
            gdk.POINTER_MOTION_MASK |
            gdk.POINTER_MOTION_HINT_MASK |
            gdk.BUTTON_MOTION_MASK |
            gdk.BUTTON_PRESS_MASK |
            gdk.BUTTON_RELEASE_MASK
        )

        self.show_all()

    def do_motion_notify_event(self, event):
        """
        Cuando se mueve el mouse sobre el visor.
        """

        x, y = (int(event.x), int(event.y))
        rect = self.get_allocation()
        xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)

        if x in range(ww - 60, ww) or y in range(yy, yy + 60) \
            or y in range(hh - 60, hh):

            self.emit("ocultar_controles", False)
            return

        else:
            self.emit("ocultar_controles", True)
            return


class Credits(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            #flags=gtk.DIALOG_MODAL,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        imagen = gtk.Image()
        #imagen.set_from_file(
        #    os.path.join(BASE_PATH,
        #    "Iconos", "JAMediaCredits.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class Help(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            #flags=gtk.DIALOG_MODAL,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        tabla1 = gtk.Table(columns=5, rows=2, homogeneous=False)

        vbox = gtk.HBox()
        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.anterior = get_boton(
            archivo, flip=True,
            pixels=24,
            tooltip_text="Anterior")
        self.anterior.connect("clicked", self.__switch)
        self.anterior.show()
        vbox.pack_start(self.anterior, False, False, 0)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.siguiente = get_boton(
            archivo,
            pixels=24,
            tooltip_text="Siguiente")
        self.siguiente.connect("clicked", self.__switch)
        self.siguiente.show()
        vbox.pack_end(self.siguiente, False, False, 0)

        tabla1.attach_defaults(vbox, 0, 5, 0, 1)

        self.helps = []

        for x in range(1, 5):
            try:
                help = gtk.Image()
                #help.set_from_file(
                #    os.path.join(BASE_PATH,
                #    "Iconos", "help-%s.svg" % x))
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


class CamaraConfig(gtk.EventBox):

    __gsignals__ = {
    'set_camara': (gobject.SIGNAL_RUN_CLEANUP, gobject.TYPE_NONE,
        (gobject.TYPE_STRING, gobject.TYPE_STRING))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.device = "/dev/video0"

        self.modify_bg(0, get_colors("window"))
        self.set_border_width(4)

        # Camara Origen
        frame = gtk.Frame()
        frame.set_label(" Fuente de Video: ")
        box = gtk.VBox()
        frame.add(box)

        boton1 = gtk.RadioButton()
        boton1.set_label("Camara 1")
        boton1.connect("clicked", self.__set_camara)
        box.pack_start(boton1, False, False, 0)

        boton2 = gtk.RadioButton()
        boton2.set_group(boton1)
        boton2.connect("clicked", self.__set_camara)
        boton2.set_label("Camara 2")
        box.pack_start(boton2, False, False, 0)

        boton3 = gtk.RadioButton()
        boton3.set_group(boton1)
        boton3.set_label("Estación Remota")
        boton3.connect("clicked", self.__set_camara)
        box.pack_start(boton3, False, False, 0)

        self.add(frame)
        self.show_all()

        boton1.set_active(True)

    def __set_camara(self, widget):

        if widget.get_active():
            if widget.get_label() == "Estación Remota":
                self.device = "Estación Remota"

            else:
                self.device = "/dev/video%s" % str(int(
                    widget.get_label().split()[-1])-1)

            self.emit("set_camara",
                "device", self.device)


class Video_out_Config(gtk.EventBox):

    __gsignals__ = {
    'set_video_out': (gobject.SIGNAL_RUN_CLEANUP, gobject.TYPE_NONE,
        (gobject.TYPE_STRING, gobject.TYPE_STRING))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.formato = "ogv"

        self.modify_bg(0, get_colors("window"))
        self.set_border_width(4)

        # Formato
        frame = gtk.Frame()
        frame.set_label(" Formato de Salida: ")
        box = gtk.VBox()
        frame.add(box)

        #vbox.pack_start(gtk.Label("Resolucion"))
        boton3 = gtk.RadioButton()
        boton3.set_label("ogv")
        boton3.connect("clicked", self.__set_formato)
        box.pack_start(boton3, False, False, 0)

        boton4 = gtk.RadioButton()
        boton4.set_group(boton3)
        boton4.set_label("avi")
        boton4.connect("clicked", self.__set_formato)
        box.pack_start(boton4, False, False, 0)

        boton5 = gtk.RadioButton()
        boton5.set_group(boton3)
        boton5.set_label("mpeg")
        boton5.connect("clicked", self.__set_formato)
        box.pack_start(boton5, False, False, 0)

        boton6 = gtk.RadioButton()
        boton6.set_group(boton3)
        boton6.set_label("Estación Remota")
        boton6.connect("clicked", self.__set_formato)
        box.pack_start(boton6, False, False, 0)

        hbox = gtk.HBox()
        self.ip_text = gtk.Entry()
        self.ip_text.set_size_request(100, -1)
        self.ip_text.set_text("192.168.1.2")
        hbox.pack_start(gtk.Label("Ip:"), False, False, 5)
        hbox.pack_end(self.ip_text, True, True, 5)
        box.pack_start(hbox, False, False, 5)

        self.add(frame)
        self.show_all()

        boton3.set_active(True)

    def __set_formato(self, widget):

        if widget.get_active():
            if widget.get_label() == "Estación Remota":
                self.formato = self.ip_text.get_text()

            else:
                self.formato = widget.get_label()

            self.emit("set_video_out",
                "formato", self.formato)


class Rafagas_Config(gtk.EventBox):

    __gsignals__ = {
    'set_video_out': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("window"))
        self.set_border_width(4)

        frame = gtk.Frame()
        frame.set_label("Ráfaga:")
        box = gtk.HBox()
        frame.add(box)

        button = gtk.Button("-")
        button.connect("clicked", self.__set)
        box.pack_start(button, True, True, 5)
        self.label = gtk.Label("1.0")
        box.pack_start(self.label, False, False, 5)
        button = gtk.Button("+")
        button.connect("clicked", self.__set)
        box.pack_start(button, True, True, 5)
        self.rafaga = gtk.CheckButton()
        self.rafaga.set_label("on")
        box.pack_start(self.rafaga, True, True, 5)

        self.add(frame)
        self.show_all()

    def __set(self, widget):

        signo = widget.get_label()
        valor = float(self.label.get_text())

        if signo == "-":
            if valor > 1.0:
                valor -= 0.1

        elif signo == "+":
            valor += 0.1

        self.label.set_text(str(valor))

    def get_rafaga(self):

        if self.rafaga.get_active():
            return float(self.label.get_text())

        else:
            return 0


'''
class JAMediaButton(gtk.EventBox):
    """
    Un Boton a medida.
    """

    __gsignals__ = {
    "clicked": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    "click_derecho": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.cn = get_color("BLANCO")
        self.cs = get_color("AMARILLO")
        self.cc = get_color("NARANJA")
        self.text_color = get_color("NEGRO")
        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.set_visible_window(True)
        self.modify_bg(0, self.colornormal)
        self.modify_fg(0, self.text_color)
        self.set_border_width(1)

        self.estado_select = False

        self.add_events(
            gdk.BUTTON_PRESS_MASK |
            gdk.BUTTON_RELEASE_MASK |
            gdk.POINTER_MOTION_MASK |
            gdk.ENTER_NOTIFY_MASK |
            gdk.LEAVE_NOTIFY_MASK)

        self.connect("button_press_event", self.button_press)
        self.connect("button_release_event", self.__button_release)
        self.connect("enter-notify-event", self.__enter_notify_event)
        self.connect("leave-notify-event", self.__leave_notify_event)

        self.imagen = gtk.Image()
        self.add(self.imagen)

        self.show_all()

    def set_colores(self, colornormal=False,
        colorselect=False, colorclicked=False):

        if colornormal:
            self.cn = colornormal

        if colorselect:
            self.cs = colorselect

        if colorclicked:
            self.cc = colorclicked

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        if self.estado_select:
            self.seleccionar()

        else:
            self.des_seleccionar()

    def seleccionar(self):
        """
        Marca como seleccionado
        """

        self.estado_select = True
        self.colornormal = self.cc
        self.colorselect = self.cc
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def des_seleccionar(self):
        """
        Desmarca como seleccionado
        """

        self.estado_select = False

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def __button_release(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def __leave_notify_event(self, widget, event):

        self.modify_bg(0, self.colornormal)

    def __enter_notify_event(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def button_press(self, widget, event):

        self.seleccionar()

        if event.button == 1:
            self.emit("clicked", event)

        elif event.button == 3:
            self.emit("click_derecho", event)

    def set_tooltip(self, texto):

        self.set_tooltip_text(texto)

    def set_label(self, texto):

        for child in self.get_children():
            child.destroy()

        label = gtk.Label(texto)
        label.show()
        self.add(label)

    def set_imagen(self, archivo):

        self.imagen.set_from_file(archivo)

    def set_tamanio(self, w, h):

        self.set_size_request(w, h)


class WidgetEfecto_en_Pipe(JAMediaButton):
    """
    Representa un efecto agregado al pipe de JAMediaVideo.
    Es simplemente un objeto gráfico que se agrega debajo del
    visor de video, para que el usuario tenga una referencia de
    los efectos que ha agregado y en que orden se encuentran.
    """

    def __init__(self):

        JAMediaButton.__init__(self)

        self.show_all()

        self.set_colores(
            colornormal=get_color("NEGRO"),
            colorselect=get_color("NEGRO"),
            colorclicked=get_color("NEGRO"))

        self.modify_bg(0, self.colornormal)

    def seleccionar(self):
        pass

    def des_seleccionar(self):
        pass
'''
