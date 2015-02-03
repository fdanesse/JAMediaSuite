#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globales.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay

from gi.repository import Gtk
from gi.repository import GdkPixbuf


def get_separador(draw=False, ancho=0, expand=False):
    """
    Devuelve un separador generico.
    """
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


def get_boton(archivo, flip=False, rotacion=None,
    pixels=0, tooltip_text=None):
    """
    Devuelve un toolbutton generico.
    """
    if not pixels:
        pixels = 37
    boton = Gtk.ToolButton()
    imagen = Gtk.Image()
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
        archivo, pixels, pixels)
    if flip:
        pixbuf = pixbuf.flip(True)
    if rotacion:
        pixbuf = pixbuf.rotate_simple(rotacion)
    imagen.set_from_pixbuf(pixbuf)
    boton.set_icon_widget(imagen)
    imagen.show()
    boton.show()
    if tooltip_text:
        boton.set_tooltip_text(tooltip_text)
        boton.TOOLTIP = tooltip_text
    return boton
