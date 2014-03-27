#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globals.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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
