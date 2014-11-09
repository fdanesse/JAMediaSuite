#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globales.py por:
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

canales = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-tv-2014'
radios = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-radios-2014'
webcams = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-webcams-2014'


def get_colors(key):
    from gtk import gdk

    _dict = {
        "window": "#ffffff",
        "toolbars": "#778899",
        "widgetvideoitem": "#f0e6aa",
        "drawingplayer": "#000000",
        "naranaja": "#ff6600",
        }

    return gdk.color_parse(_dict.get(key, "#ffffff"))


def get_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        ret = s.getsockname()[0]
        s.close()
        return bool(ret)
    except:
        return False


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


def describe_uri(uri):
    """
    Explica de que se trata el uri, si existe.
    """
    import os
    existe = False

    try:
        existe = os.path.exists(uri)
    except:
        return False

    if existe:
        unidad = os.path.ismount(uri)
        directorio = os.path.isdir(uri)
        archivo = os.path.isfile(uri)
        enlace = os.path.islink(uri)
        return [unidad, directorio, archivo, enlace]
    else:
        return False


def describe_acceso_uri(uri):
    """
    Devuelve los permisos de acceso sobre una uri.
    """
    import os
    existe = False

    try:
        existe = os.access(uri, os.F_OK)
    except:
        return False

    if existe:
        lectura = os.access(uri, os.R_OK)
        escritura = os.access(uri, os.W_OK)
        ejecucion = os.access(uri, os.X_OK)
        return [lectura, escritura, ejecucion]

    else:
        return False


def borrar(origen):
    try:
        import os
        import shutil

        if os.path.isdir(origen):
            shutil.rmtree("%s" % (os.path.join(origen)))
        elif os.path.isfile(origen):
            os.remove("%s" % (os.path.join(origen)))
        else:
            return False

        return True

    except:
        print "ERROR Al Intentar Borrar un Archivo"
        return False


def mover(origen, destino):
    try:
        import os
        if os.path.isdir(origen):
            copiar(origen, destino)
            borrar(origen)
            return True

        elif os.path.isfile(origen):
            expresion = "mv \"" + origen + "\" \"" + destino + "\""
            os.system(expresion)
            return True

    except:
        print "ERROR Al Intentar Mover un Archivo"
        return False


def copiar(origen, destino):
    try:
        import os
        if os.path.isdir(origen):
            expresion = "cp -r \"" + origen + "\" \"" + destino + "\""
        elif os.path.isfile(origen):
            expresion = "cp \"" + origen + "\" \"" + destino + "\""

        os.system(expresion)
        return True

    except:
        print "ERROR Al Intentar Copiar un Archivo"
        return False


def make_base_directory():
    """
    Crea toda la estructura de Directorios de JAMedia.
    """
    import os
    import commands

    if not os.path.exists(os.path.join(os.environ["HOME"], "JAMediaDatos")):
        os.mkdir(os.path.join(os.environ["HOME"], "JAMediaDatos"))
        os.chmod(os.path.join(os.environ["HOME"], "JAMediaDatos"), 0755)

    # unificar directorios de JAMedia,
    # JAMediaVideo y JAMediaImagenes
    directorio_viejo = os.path.join(os.environ["HOME"], ".JAMediaDatos")
    directorio_nuevo = os.path.join(os.environ["HOME"], "JAMediaDatos")

    if os.path.exists(directorio_viejo):
        for elemento in os.listdir(directorio_viejo):
            commands.getoutput('mv %s %s' % (os.path.join(directorio_viejo,
                elemento), directorio_nuevo))

        commands.getoutput('rm -r %s' % (directorio_viejo))

    # Directorios JAMedia
    DIRECTORIO_MIS_ARCHIVOS = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "MisArchivos")

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


def get_JAMedia_Directory():
    import os
    path = os.path.join(os.environ["HOME"], "JAMediaDatos")
    if not os.path.exists(path):
        make_base_directory()
    return path


def eliminar_streaming(url, lista):
    """
    Elimina un Streaming de una lista de jamedia.
    """
    import os
    DIRECTORIO_DATOS = get_data_directory()

    if lista == "Radios":
        path = os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia")

    elif lista == "TVs":
        path = os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")

    elif lista == "JAM-Radio":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia")

    elif lista == "JAM-TV":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia")

    elif lista == "WebCams":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaWebCams.JAMedia")

    else:
        return

    import shelve
    archivo = shelve.open(path)
    items = archivo.items()

    for item in items:
        if url == str(item[1]):
            del (archivo[item[0]])
    archivo.close()


def add_stream(tipo, item):
    """
    Agrega un streaming a la lista correspondiente de jamedia.
    """
    import os
    DIRECTORIO_DATOS = get_data_directory()

    if "TV" in tipo or "Tv" in tipo:
        path = os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")
    elif "Radio" in tipo:
        path = os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia")
    else:
        return

    import shelve
    archivo = shelve.open(path)
    archivo[item[0].strip()] = item[1].strip()
    archivo.close()


def set_listas_default():
    """
    Crea las listas para JAMedia si es que no existen y
    llena las default en caso de estar vacías.
    """
    import os
    import shelve
    DIRECTORIO_DATOS = get_data_directory()

    listas = [
        os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "JAMediaWebCams.JAMedia")
        ]

    for archivo in listas:
        if not os.path.exists(archivo):
            jamedialista = shelve.open(archivo)
            jamedialista.close()
            os.chmod(archivo, 0666)

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    archivo = shelve.open(os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"))
    lista = archivo.items()
    archivo.close()

    if not lista:
        try:
            # Streamings JAMediatv
            lista_canales = descarga_lista_de_streamings(canales)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
                "JAMediaTV.JAMedia"), lista_canales)
        except:
            print "Error al descargar Streamings de TV."

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    archivo = shelve.open(os.path.join(DIRECTORIO_DATOS,
        "JAMediaRadio.JAMedia"))
    lista = archivo.items()
    archivo.close()

    if not lista:
        try:
            # Streamings JAMediaradio
            lista_radios = descarga_lista_de_streamings(radios)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
                "JAMediaRadio.JAMedia"), lista_radios)
        except:
            print "Error al descargar Streamings de Radios."

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    archivo = shelve.open(os.path.join(DIRECTORIO_DATOS,
        "JAMediaWebCams.JAMedia"))
    lista = archivo.items()
    archivo.close()

    if not lista:
        try:
            # Streamings JAMediaWebCams
            lista_webcams = descarga_lista_de_streamings(webcams)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
                "JAMediaWebCams.JAMedia"), lista_webcams)
        except:
            print "Error al descargar Streamings de WebCams."


def get_streaming_default():
    """
    Descarga los streaming desde la web de JAMedia.
    """

    import os

    DIRECTORIO_DATOS = get_data_directory()

    try:
        # Streamings JAMediatv
        lista_canales = descarga_lista_de_streamings(canales)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaTV.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaTV.JAMedia"), lista_canales)

    except:
        print "Error al descargar Streamings de TV."

    try:
        # Streamings JAMediaradio
        lista_radios = descarga_lista_de_streamings(radios)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaRadio.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaRadio.JAMedia"), lista_radios)

    except:
        print "Error al descargar Streamings de Radios."

    try:
        # Streamings JAMediaWebCams
        lista_webcams = descarga_lista_de_streamings(webcams)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaWebCams.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaWebCams.JAMedia"), lista_webcams)

    except:
        print "Error al descargar Streamings de webcams."


def descarga_lista_de_streamings(url):
    """
    Recibe la web donde se publican los streamings de radio o televisión de
    JAMedia y devuelve la lista de streamings.

    Un streaming se representa por una lista:
        [nombre, url]
    """

    print "Conectandose a:", url, "\n\tDescargando Streamings . . ."

    import urllib

    cont = 0
    urls = []
    cabecera = 'JAMedia Channels:'
    streamings = []

    try:
        web = urllib.urlopen(url)
        t = web.readlines()
        web.close()

        text = ""
        for l in t:
            text = "%s%s" % (text, l)

        streamings_text = text.split(cabecera)[1]
        streamings_text = streamings_text.replace('</div>', "")
        streamings_text = streamings_text.replace('/>', "")
        lista = streamings_text.split('<br')

        for s in lista:
            if not len(s.split(",")) == 2:
                continue

            name, direc = s.split(",")
            name = name.strip()
            direc = direc.strip()

            if not direc in urls:
                urls.append(direc)
                stream = [name, direc]
                streamings.append(stream)
                cont += 1

            else:
                print "Direccion Descartada por Repetición:", name, direc

        print "\tSe han Descargado:", cont, "Estreamings.\n"
        return streamings

    except:
        return []


def clear_lista_de_streamings(path):
    import shelve
    archivo = shelve.open(path)
    archivo.clear()
    archivo.close()


def guarda_lista_de_streamings(path, items):
    """
    Recibe el path a un archivo de lista de streamings
    de JAMedia y una lista de items [nombre, url] y los almacena
    en el archivo.
    """
    import shelve
    archivo = shelve.open(path)
    for item in items:
        archivo[item[0].strip()] = item[1].strip()
    archivo.close()


def get_streamings(path):
    """
    Recibe el path a un archivo de streamings
    y devuelve la lista de streamings que contiene.
    """
    import shelve
    items = []
    archivo = shelve.open(path)
    keys = sorted(archivo.keys())
    for key in keys:
        items.append([key, archivo[key]])
    archivo.close()
    return items


def stream_en_archivo(streaming, path):
    """
    Verifica si un streaming está en
    un archivo de lista de jamedia determinado.
    """
    import shelve
    archivo = shelve.open(path)
    items = archivo.values()
    for item in items:
        if streaming == item:
            archivo.close()
            return True
    archivo.close()
    return False


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
