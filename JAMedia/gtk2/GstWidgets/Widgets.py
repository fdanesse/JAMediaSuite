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

"""
Descripción:

Contiene Widgets para activar/desactivar y/o Configurar efectos de video
    sobre un pipe de gstreamer:

    Utilice:
        cargar_efectos(elementos)

            para agregar una lista de widget que represente a los efectos
            correspondientes según "elementos".
                Para hacer esto, Vea la función:
                    VideoEfectos.get_jamedia_video_efectos()

        clear

            para desactivar todos los efectos.

        reemit_config_efecto(efecto)

            para foorzar la emisión de la señal 'configurar_efecto' la cual
            envía la configuración del mismo según su widget de configuración.

    Conéctese a la señal:
        "click_efecto": gobject.TYPE_STRING, gobject.TYPE_BOOLEAN

            para activar o desactivar un determinado efecto en el
            pipe de gstreamer segúna acciones del usuario sobre el widget.

        'configurar_efecto': gobject.TYPE_STRING, gobject.TYPE_STRING,
            gobject.TYPE_PYOBJECT

            para configurar un determinado efecto en el
            pipe de gstreamer según acciones del usuario sobre el widget.
"""

import os
import commands
import gtk
import gobject

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class VideoEfectos(gtk.Frame):
    """
    Frame Contenedor de widgets efectos de video para gstreamer.
    """

    __gsignals__ = {
    "click_efecto": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN)),
    'configurar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.set_label(" Efectos de Video: ")
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

    def __emit_click_efecto(self, widget, nombre_efecto, valor):
        self.emit('click_efecto', nombre_efecto, valor)

    def cargar_efectos(self, elementos):
        self.gstreamer_efectos.cargar_efectos(elementos)

    def clear(self):
        self.gstreamer_efectos.clear()

    def reemit_config_efecto(self, efecto):
        self.gstreamer_efectos.reemit_config_efecto(efecto)


class GstreamerVideoEfectos(gtk.VBox):
    """
    Contenedor de widgets que representan efectos de video para gstreamer.
    """

    __gsignals__ = {
    'agregar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN)),
    'configurar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.VBox.__init__(self)

        self.show_all()

    def __configurar_efecto(self, widget, efecto, propiedad, valor):
        self.emit('configurar_efecto', efecto, propiedad, valor)

    def __agregar_efecto(self, widget, nombre_efecto, valor):
        self.emit('agregar_efecto', nombre_efecto, valor)

    def clear(self):
        for child in self.get_children():
            child.clear()

    def reemit_config_efecto(self, efecto):
        for child in self.get_children():
            if child.botonefecto.get_label() == efecto:
                child.reemit_config_efecto(efecto)

    def cargar_efectos(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """
        self.set_sensitive(False)
        if not elementos:
            self.set_sensitive(True)
            return False

        nombre = elementos[0]
        # FIXME: Los efectos se definen en globales
        # pero hay que ver si están instalados.

        datos = commands.getoutput('gst-inspect-0.10 %s' % (nombre))

        #if 'gst-plugins-good' in datos and \
        #    ('Filter/Effect/Video' in datos or \
        # 'Transform/Effect/Video' in datos):
        if 'Filter/Effect/Video' in datos or 'Transform/Effect/Video' in datos:
            botonefecto = Efecto_widget_Config(nombre)
            botonefecto.connect('agregar_efecto', self.__agregar_efecto)
            botonefecto.connect('configurar_efecto', self.__configurar_efecto)
            self.pack_start(botonefecto, False, False, 0)

        self.show_all()
        elementos.remove(elementos[0])
        gobject.idle_add(self.cargar_efectos, elementos)
        return False


class Efecto_widget_Config(gtk.EventBox):
    """
    Contiene el botón para el efecto y los controles de
    configuración del mismo.
    """

    __gsignals__ = {
    'agregar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN)),
    'configurar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self, nombre):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.set_border_width(4)

        frame = gtk.Frame()
        box = gtk.VBox()
        frame.add(box)

        self.botonefecto = gtk.CheckButton()
        self.botonefecto.set_label(nombre.split("-")[-1])
        self.botonefecto.connect('toggled', self.__efecto_click)
        self.botonefecto.set_tooltip_text(nombre)

        box.pack_start(self.botonefecto, False, False, 0)

        self.widget_config = get_widget_config_efecto(nombre)

        if self.widget_config:
            box.pack_start(self.widget_config, False, True, 0)
            self.widget_config.connect('propiedad', self.__set_efecto)

        self.add(frame)
        self.show_all()

    def __set_efecto(self, widget, propiedad, valor):
        if not self.botonefecto.get_active():
            self.botonefecto.set_active(True)
        self.emit('configurar_efecto', self.botonefecto.get_tooltip_text(),
            propiedad, valor)

    def __efecto_click(self, widget):
        activo = widget.get_active()
        if not activo and self.widget_config:
            self.widget_config.reset()
            widget.set_active(False)
        self.emit('agregar_efecto', widget.get_tooltip_text(), activo)

    def clear(self):
        if self.widget_config:
            self.widget_config.reset()
        self.botonefecto.set_active(False)

    def reemit_config_efecto(self, efecto):
        if self.widget_config:
            self.widget_config.reemit_config()


def get_widget_config_efecto(nombre):
    """
    Devulve el widget de configuración de un determinado efecto.
    """

    if nombre == 'radioactv':
        from Good import Radioactv
        return Radioactv()
    elif nombre == 'agingtv':
        from Good import Agingtv
        return Agingtv()
    else:
        return False
