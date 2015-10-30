#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands
import json
import codecs
#import urllib
import socket
import gtk

radios = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-radios-2014'


def get_colors(key):
    _dict = {
        "window": "#ffffff",
        "toolbars": "#778899",
        "widgetvideoitem": "#f0e6aa",
        "drawingplayer": "#000000",
        "naranaja": "#ff6600",
        }
    return gtk.gdk.color_parse(_dict.get(key, "#ffffff"))


def get_ToggleToolButton(archivo, flip=False, rotacion=None,
    pixels=24, tooltip_text=None):
    button = gtk.ToggleToolButton()
    imagen = gtk.Image()
    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(archivo, pixels, pixels)
    if flip:
        pixbuf = pixbuf.flip(True)
    if rotacion:
        pixbuf = pixbuf.rotate_simple(rotacion)
    imagen.set_from_pixbuf(pixbuf)
    button.set_icon_widget(imagen)
    imagen.show()
    button.show()
    if tooltip_text:
        button.set_property("tooltip_text", tooltip_text)
    return button


def get_SeparatorToolItem(draw=False, ancho=0, expand=False):
    separador = gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


def get_boton(archivo, flip=False, rotacion=None,
    pixels=24, tooltip_text=None):
    boton = gtk.ToolButton()
    imagen = gtk.Image()
    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
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
        boton.set_property("tooltip-text", tooltip_text)
    return boton


def describe_archivo(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    -z, --uncompress para ver dentro de los zip.
    """
    datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
    retorno = ""
    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)
    return retorno


def describe_uri(uri):
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
        if os.path.isfile(origen):
            os.remove("%s" % (os.path.join(origen)))
        else:
            return False
        return True
    except:
        print "ERROR Al Intentar Borrar:", origen
        return False


def __make_base_directory():
    if not os.path.exists(os.path.join(os.environ["HOME"], "JAMediaDatos")):
        os.mkdir(os.path.join(os.environ["HOME"], "JAMediaDatos"))
        os.chmod(os.path.join(os.environ["HOME"], "JAMediaDatos"), 0755)
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


def __get_data_directory():
    DIRECTORIO_DATOS = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Datos")
    if not os.path.exists(DIRECTORIO_DATOS):
        __make_base_directory()
    return DIRECTORIO_DATOS


def __convert_shelve_to_json(path):
    print "Convert:", path
    import shelve
    _dict = {}
    try:
        archivo = shelve.open(path)
        _dict = dict(archivo)
        archivo.close()
        borrar(path)
        set_dict(path, _dict)
    except:
        pass
    return _dict


def __get_dict(path):
    if not os.path.exists(path):
        return {}
    try:
        archivo = codecs.open(path, "r", "utf-8")
        _dict = json.JSONDecoder(encoding="utf-8").decode(archivo.read())
        archivo.close()
    except:
        _dict = __convert_shelve_to_json(path)
    return _dict


def __set_dict(path, _dict):
    archivo = open(path, "w")
    archivo.write(
        json.dumps(
            _dict,
            indent=4,
            separators=(", ", ":"),
            sort_keys=True))
    archivo.close()


def get_radios():
    DIRECTORIO_DATOS = __get_data_directory()
    archivo = os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia")
    if not os.path.exists(archivo):
        __set_dict(archivo, {})
        os.chmod(archivo, 0666)
    items = []
    _dict = __get_dict(archivo)
    keys = sorted(_dict.keys())
    for key in keys:
        items.append([key, _dict[key]])
    return items


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        ret = s.getsockname()[0]
        s.close()
        return bool(ret)
    except:
        return False
