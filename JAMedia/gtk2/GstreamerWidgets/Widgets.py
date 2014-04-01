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

BASE_PATH = os.path.dirname(__file__)


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

    from gtk import gdk

    colors = {
        "GRIS": gdk.Color(60156, 60156, 60156),
        "AMARILLO": gdk.Color(65000, 65000, 40275),
        "NARANJA": gdk.Color(65000, 26000, 0),
        "BLANCO": gdk.Color(65535, 65535, 65535),
        "NEGRO": gdk.Color(0, 0, 0),
        "ROJO": gdk.Color(65000, 0, 0),
        "VERDE": gdk.Color(0, 65000, 0),
        "AZUL": gdk.Color(0, 0, 65000),
        }

    return colors.get(color, None)


class JAMediaButton(gtk.EventBox):
    """
    Un Boton a medida.
    """

    __gsignals__ = {
    "clicked": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    "click_derecho": (gobject.SIGNAL_RUN_FIRST,
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


class WidgetsGstreamerEfectos(gtk.Frame):
    """
    Frame exterior de Contenedor de widgets que
    representan efectos de video para gstreamer.
    """

    __gsignals__ = {
    "click_efecto": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'configurar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.set_label(" Efectos: ")
        self.set_label_align(0.0, 0.5)

        self.gstreamer_efectos = GstreamerVideoEfectos()
        self.gstreamer_efectos.connect(
            'agregar_efecto', self.__emit_click_efecto)
        self.gstreamer_efectos.connect(
            'configurar_efecto', self.__configurar_efecto)
        self.add(self.gstreamer_efectos)

        self.show_all()

    def __configurar_efecto(self, widget, efecto, propiedad, valor):

        self.emit('configurar_efecto', efecto, propiedad, valor)

    def __emit_click_efecto(self, widget, nombre_efecto):

        self.emit('click_efecto', nombre_efecto)

    def cargar_efectos(self, elementos):
        """
        Agrega los widgets de efectos.
        """

        self.gstreamer_efectos.cargar_efectos(elementos)

    def des_seleccionar_efecto(self, nombre):

        self.gstreamer_efectos.des_seleccionar_efecto(nombre)

    def seleccionar_efecto(self, nombre):

        self.gstreamer_efectos.seleccionar_efecto(nombre)


class GstreamerVideoEfectos(gtk.VBox):
    """
    Contenedor de widgets que representan
    efectos de video para gstreamer.
    """

    __gsignals__ = {
    'agregar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'configurar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.VBox.__init__(self)

        self.show_all()

    def cargar_efectos(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """

        if not elementos:
            #self.get_toplevel().set_sensitive(True)
            return False

        nombre = elementos[0]
        # Los efectos se definen en globales
        # pero hay que ver si están instalados.
        import commands
        datos = commands.getoutput('gst-inspect-1.0 %s' % (nombre))

        #if 'gst-plugins-good' in datos and \
        #    ('Filter/Effect/Video' in datos or \
        # 'Transform/Effect/Video' in datos):
        if 'Filter/Effect/Video' in datos or \
            'Transform/Effect/Video' in datos:
            botonefecto = Efecto_widget_Config(nombre)
            botonefecto.connect(
                'agregar_efecto', self.agregar_efecto)
            botonefecto.connect(
                'configurar_efecto', self.__configurar_efecto)
            self.pack_start(botonefecto, False, False, 0)

        self.show_all()
        elementos.remove(elementos[0])

        gobject.idle_add(self.cargar_efectos, elementos)

        return False

    def __configurar_efecto(self, widget, efecto, propiedad, valor):

        self.emit('configurar_efecto', efecto, propiedad, valor)

    def agregar_efecto(self, widget, nombre_efecto):
        """
        Cuando se hace click en el botón del efecto
        se envía la señal 'agregar-efecto'.
        """

        self.emit('agregar_efecto', nombre_efecto)

    """
    def efecto_click_derecho(self, widget, void):

        #print "Click", widget.get_tooltip_text(),
            "Select", widget.estado_select
        pass
    """

    def des_seleccionar_efecto(self, nombre):

        efectos = self.get_children()

        for efecto in efectos:

            if efecto.botonefecto.get_tooltip_text() == nombre:
                efecto.des_seleccionar()
                return

    def seleccionar_efecto(self, nombre):

        efectos = self.get_children()

        for efecto in efectos:

            if efecto.botonefecto.get_tooltip_text() == nombre:
                efecto.seleccionar()
                return


class Efecto_widget_Config(gtk.EventBox):
    """
    Contiene el botón para el efecto y los
    controles de configuración del mismo.
    """

    __gsignals__ = {
    'agregar_efecto': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'configurar_efecto': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self, nombre):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gdk.color_parse("#ffffff"))
        self.set_border_width(4)

        frame = gtk.Frame()
        text = nombre
        if "-" in nombre:
            text = nombre.split("-")[-1]

        frame.set_label(text)
        #frame.set_label_align(0.5, 1.0)
        box = gtk.VBox()
        frame.add(box)

        self.botonefecto = JAMediaButton()
        self.botonefecto.set_border_width(4)
        self.botonefecto.connect('clicked', self.__efecto_click)
        #self.botonefecto.connect('click_derecho', self.__efecto_click_derecho)
        self.botonefecto.set_tooltip(nombre)
        self.botonefecto.set_tamanio(150, 24)

        box.pack_start(self.botonefecto, False, False, 0)
        #path = os.path.dirname(BASE_PATH)
        #archivo = os.path.join(path,
        #    "Iconos", 'configurar.svg')

        #pixbuf = gdk.pixbuf_new_from_file_at_size(archivo, lado, lado)
        #self.botonefecto.imagen.set_from_pixbuf(pixbuf)

        self.widget_config = get_widget_config_efecto(nombre)

        if self.widget_config:
            box.pack_start(self.widget_config, False, True, 0)
            self.widget_config.connect('propiedad', self.__set_efecto)

        self.add(frame)
        self.show_all()
        # y ocultar configuraciones.

    def __set_efecto(self, widget, propiedad, valor):

        self.emit('configurar_efecto',
            self.botonefecto.get_tooltip_text(),
            propiedad, valor)

    def __efecto_click(self, widget, void):
        """
        Cuando se hace click en el botón del efecto
        se envía la señal 'agregar-efecto'.
        """

        self.emit('agregar_efecto', widget.get_tooltip_text())

    """
    def efecto_click_derecho(self, widget, void):

        #print "Click", widget.get_tooltip_text(),
            "Select", widget.estado_select
        pass
    """

    def seleccionar(self):
        """
        Marca como seleccionado
        """

        self.botonefecto.seleccionar()
        # y mostrar configuracion

    def des_seleccionar(self):
        """
        Desmarca como seleccionado
        """

        self.botonefecto.des_seleccionar()
        #y ocultar configuracion


def get_widget_config_efecto(nombre):
    """
    Devulve el widget de configuración de un
    determinado efecto de video o visualizador de audio.
    """

    if nombre == 'radioactv':
        from WidgetsEfectosGood import Radioactv
        return Radioactv()

    elif nombre == 'agingtv':
        from WidgetsEfectosGood import Agingtv
        return Agingtv()

    else:
        return False
