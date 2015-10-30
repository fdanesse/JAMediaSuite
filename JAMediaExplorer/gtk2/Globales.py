#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globals.py por:
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

import gtk


def get_separador(draw=False, ancho=0, expand=False):
    separador = gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


def get_boton(archivo, flip=False, rotacion=None,
    pixels=24, tooltip_text=None):
    boton = gtk.ToolButton()
    imagen = gtk.Image()
    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(archivo, pixels, pixels)

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
