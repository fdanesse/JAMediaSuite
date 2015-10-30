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


def make_base_directory():
    """
    Crea toda la estructura de Directorios de JAMedia.
    """

    import os
    import commands

    if not os.path.exists(os.path.join(
        os.environ["HOME"], "JAMediaDatos")):
        os.mkdir(os.path.join(
            os.environ["HOME"], "JAMediaDatos"))
        os.chmod(os.path.join(
            os.environ["HOME"], "JAMediaDatos"), 0755)

    # unificar directorios de JAMedia,
    # JAMediaVideo y JAMediaImagenes
    directorio_viejo = os.path.join(
        os.environ["HOME"], ".JAMediaDatos")
    directorio_nuevo = os.path.join(
        os.environ["HOME"], "JAMediaDatos")

    if os.path.exists(directorio_viejo):
        for elemento in os.listdir(directorio_viejo):
            commands.getoutput(
                'mv %s %s' % (os.path.join(directorio_viejo,
                elemento), directorio_nuevo))

        commands.getoutput('rm -r %s' % (directorio_viejo))

    # Directorios JAMedia
    DIRECTORIO_MIS_ARCHIVOS = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "MisArchivos")

    DIRECTORIO_DATOS = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "Datos")

    if not os.path.exists(DIRECTORIO_MIS_ARCHIVOS):
        os.mkdir(DIRECTORIO_MIS_ARCHIVOS)
        os.chmod(DIRECTORIO_MIS_ARCHIVOS, 0755)

    if not os.path.exists(DIRECTORIO_DATOS):
        os.mkdir(DIRECTORIO_DATOS)
        os.chmod(DIRECTORIO_DATOS, 0755)

    # Directorio JAMediaTube
    DIRECTORIO_YOUTUBE = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "YoutubeVideos")

    if not os.path.exists(DIRECTORIO_YOUTUBE):
        os.mkdir(DIRECTORIO_YOUTUBE)
        os.chmod(DIRECTORIO_YOUTUBE, 0755)

    # Directorios JAMediaVideo
    AUDIO_JAMEDIA_VIDEO = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "Audio")

    if not os.path.exists(AUDIO_JAMEDIA_VIDEO):
        os.mkdir(AUDIO_JAMEDIA_VIDEO)
        os.chmod(AUDIO_JAMEDIA_VIDEO, 0755)

    VIDEO_JAMEDIA_VIDEO = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "Videos")

    if not os.path.exists(VIDEO_JAMEDIA_VIDEO):
        os.mkdir(VIDEO_JAMEDIA_VIDEO)
        os.chmod(VIDEO_JAMEDIA_VIDEO, 0755)

    IMAGENES_JAMEDIA_VIDEO = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "Fotos")

    if not os.path.exists(IMAGENES_JAMEDIA_VIDEO):
        os.mkdir(IMAGENES_JAMEDIA_VIDEO)
        os.chmod(IMAGENES_JAMEDIA_VIDEO, 0755)


def get_data_directory():
    """
    Devuelve el Directorio de Datos de JAMedia y JAMediaTube.
    """

    import os

    DIRECTORIO_DATOS = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Datos")

    if not os.path.exists(DIRECTORIO_DATOS):
        make_base_directory()

    return DIRECTORIO_DATOS


def get_tube_directory():
    """
    Devuelve el Directorio de Videos de JAMediaTube.
    """

    import os

    DIRECTORIO_YOUTUBE = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "YoutubeVideos")

    if not os.path.exists(DIRECTORIO_YOUTUBE):
        make_base_directory()

    return DIRECTORIO_YOUTUBE


def describe_archivo(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    -z, --uncompress para ver dentro de los zip.
    """

    import commands

    datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
    retorno = ""

    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)

    return retorno


def get_color(color):
    """
    Devuelve Colores predefinidos.
    """

    from gi.repository import Gdk

    colors = {
        "GRIS": Gdk.Color(60156, 60156, 60156),
        "AMARILLO": Gdk.Color(65000, 65000, 40275),
        "NARANJA": Gdk.Color(65000, 26000, 0),
        "BLANCO": Gdk.Color(65535, 65535, 65535),
        "NEGRO": Gdk.Color(0, 0, 0),
        "ROJO": Gdk.Color(65000, 0, 0),
        "VERDE": Gdk.Color(0, 65000, 0),
        "AZUL": Gdk.Color(0, 0, 65000),
        }

    return colors.get(color, None)


def get_pixels(centimetros):
    """
    Recibe un tamaño en centimetros y
    devuelve el tamaño en pixels que le corresponde,
    según tamaño del monitor que se está utilizando.

    # 1 px = 0.026458333 cm #int(centimetros/0.026458333)
    # 1 Pixel = 0.03 Centimetros = 0.01 Pulgadas.
    """
    '''
    from gi.repository import GdkX11

    screen = GdkX11.X11Screen()

    res_w = screen.width()
    res_h = screen.height()

    mm_w = screen.width_mm()
    mm_h = screen.height_mm()

    ancho = int (float(res_w) / float(mm_w) * 10.0 * centimetros)
    alto = int (float(res_h) / float(mm_h) * 10.0 * centimetros)
    if centimetros == 5.0: print ">>>>", centimetros, int(min([ancho, alto]))
    return int(min([ancho, alto]))'''

    res = {
        1.0: 37,
        1.2: 45,
        0.5: 18,
        0.2: 7,
        0.5: 18,
        0.6: 22,
        0.8: 30,
        5.0: 189,
        }

    return res[centimetros]


def get_boton(archivo, flip=False, rotacion=None,
    pixels=0, tooltip_text=None):
    """
    Devuelve un toolbutton generico.
    """

    from gi.repository import Gtk
    from gi.repository import GdkPixbuf

    if not pixels:
        pixels = get_pixels(1)

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


def get_separador(draw=False, ancho=0, expand=False):
    """
    Devuelve un separador generico.
    """

    from gi.repository import Gtk

    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)

    return separador
