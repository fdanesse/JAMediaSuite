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


def get_ip():
    """
    Devuelve ip rango de difusión en la red.
    """
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        ret = s.getsockname()[0]
        s.close()
        return ret
    except:
        return ""


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


def get_colors(key):
    from gtk import gdk
    _dict = {
        "window": "#ffffff",
        "barradeprogreso": "#778899",
        "toolbars": "#f0e6aa",
        "drawingplayer": "#000000",
        }
    return gdk.color_parse(_dict.get(key, "#ffffff"))


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


def make_base_directory():
    """
    Crea toda la estructura de Directorios de JAMedia.
    """
    import os
    import commands
    if not os.path.exists(os.path.join(
        os.environ["HOME"], "JAMediaDatos")):
        os.mkdir(os.path.join(os.environ["HOME"], "JAMediaDatos"))
        os.chmod(os.path.join(os.environ["HOME"], "JAMediaDatos"), 0755)

    # unificar directorios de JAMedia, JAMediaVideo y JAMediaImagenes
    directorio_viejo = os.path.join(os.environ["HOME"], ".JAMediaDatos")
    directorio_nuevo = os.path.join(os.environ["HOME"], "JAMediaDatos")

    if os.path.exists(directorio_viejo):
        for elemento in os.listdir(directorio_viejo):
            commands.getoutput('mv %s %s' % (os.path.join(directorio_viejo,
                elemento), directorio_nuevo))

        commands.getoutput('rm -r %s' % (directorio_viejo))

    # Directorios JAMedia
    DIRECTORIO_MIS_ARCHIVOS = os.path.join(
        os.environ["HOME"], "JAMediaDatos", "MisArchivos")

    DIRECTORIO_DATOS = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Datos")

    if not os.path.exists(DIRECTORIO_MIS_ARCHIVOS):
        os.mkdir(DIRECTORIO_MIS_ARCHIVOS)
        os.chmod(DIRECTORIO_MIS_ARCHIVOS, 0755)

    if not os.path.exists(DIRECTORIO_DATOS):
        os.mkdir(DIRECTORIO_DATOS)
        os.chmod(DIRECTORIO_DATOS, 0755)

    # Directorio JAMediaTube
    DIRECTORIO_YOUTUBE = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "YoutubeVideos")

    if not os.path.exists(DIRECTORIO_YOUTUBE):
        os.mkdir(DIRECTORIO_YOUTUBE)
        os.chmod(DIRECTORIO_YOUTUBE, 0755)

    # Directorios JAMediaVideo
    AUDIO_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Audio")

    if not os.path.exists(AUDIO_JAMEDIA_VIDEO):
        os.mkdir(AUDIO_JAMEDIA_VIDEO)
        os.chmod(AUDIO_JAMEDIA_VIDEO, 0755)

    VIDEO_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Videos")

    if not os.path.exists(VIDEO_JAMEDIA_VIDEO):
        os.mkdir(VIDEO_JAMEDIA_VIDEO)
        os.chmod(VIDEO_JAMEDIA_VIDEO, 0755)

    IMAGENES_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
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


def get_audio_directory():
    """
    Devuelve el Directorio de Audio de JAMedia y JAMediaTube.
    """
    import os
    AUDIO_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Audio")
    if not os.path.exists(AUDIO_JAMEDIA_VIDEO):
        make_base_directory()
    return AUDIO_JAMEDIA_VIDEO


def get_imagenes_directory():
    """
    Devuelve el Directorio de Imagenes de JAMediaVideo y JAMediaImagenes.
    """
    import os
    IMAGENES_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Fotos")
    if not os.path.exists(IMAGENES_JAMEDIA_VIDEO):
        make_base_directory()
    return IMAGENES_JAMEDIA_VIDEO


def get_video_directory():
    """
    Devuelve el Directorio de Video de JAMediaVideo.
    """
    import os
    VIDEO_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Videos")
    if not os.path.exists(VIDEO_JAMEDIA_VIDEO):
        make_base_directory()
    return VIDEO_JAMEDIA_VIDEO

'''
def get_my_files_directory():
    """
    Devuelve el Directorio de Archivos del usuario en JAMedia.
    """
    import os
    DIRECTORIO_MIS_ARCHIVOS = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "MisArchivos")
    if not os.path.exists(DIRECTORIO_MIS_ARCHIVOS):
        make_base_directory()
    return DIRECTORIO_MIS_ARCHIVOS
'''


def get_separador(draw=False, ancho=0, expand=False):
    """
    Devuelve un separador generico.
    """
    import gtk
    separador = gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador

'''
def get_togle_boton(archivo, flip=False,
    color=get_color("GRIS"), pixels=24):
    # Gdk.Color(65000, 65000, 65000)
    """
    Devuelve un toggletoolbutton generico.
    """
    import gtk
    boton = gtk.ToggleToolButton()
    imagen = gtk.Image()
    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
        archivo, pixels, pixels)

    if flip:
        pixbuf = pixbuf.flip(True)

    imagen.set_from_pixbuf(pixbuf)
    boton.set_icon_widget(imagen)
    imagen.show()
    boton.show()
    return boton
'''


def get_boton(archivo, flip=False, rotacion=None,
    pixels=24, tooltip_text=None):
    """
    Devuelve un toolbutton generico.
    """
    import gtk

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
