#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globales.py por:
#   Flavio Danesse <fdanesse@gmail.com>

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

radios = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-radios-2014'


def set_estilo(dict_colors):
    """
    Cuando se cambia el estilo,
    se guarda y se carga en la interfaz.
    """

    estilo = """
/*
opacidad = %s
formato = %s
*/

GtkWindow {
    background-color: %s;
    color: %s;
}

GtkMenuBar, GtkMenu, GtkMenuItem {
    background-color: %s;
    color: %s;
}

GtkEventBox {
    background-color: %s;
    color: %s;
}

UbuntuRadioDialogoConfig, UbuntuRadioDialogoDescarga,
    UbuntuRadioCreditos{
    background-color: #ffffff;
    color: #000000;
    }
""" % (
    dict_colors["opacidad"],
    dict_colors["formato"],
    dict_colors["color1"],
    dict_colors["color2"],
    dict_colors["color3"],
    dict_colors["color4"],
    dict_colors["color5"],
    dict_colors["color6"])

    import os

    path = os.path.join(
        get_data_directory(),
        "UbuntuRadio.css")

    archivo = open(path, "w")
    archivo.write(estilo)
    archivo.close()

    __load_estilo(path)


def get_estilo():
    """
    Crea y/o carga el estilo
    y devuelve config{}
    """

    import os

    path = os.path.join(
        get_data_directory(),
        "UbuntuRadio.css")

    if not os.path.exists(path):
        dict_colors = {
            "opacidad": 0.8,
            "formato": "ogg",
            "color1": "#8ae234",
            "color2": "#ffffff",
            "color3": "#c0fcf4",
            "color4": "#000000",
            "color5": "#b0e0e6",
            "color6": "#000000",
            }
        set_estilo(dict_colors)

    __load_estilo(path)

    return __get_config()


def __get_config():
    """
    Convierte los datos del estilo en un
    diccionario con la configuración.
    """

    import os

    path = os.path.join(
        get_data_directory(),
        "UbuntuRadio.css")

    archivo = open(path, "r")
    texto = archivo.readlines()
    archivo.close()

    config = {}

    colores = []

    for line in texto:
        if "opacidad" in line:
            config["opacidad"] = float(line.split()[-1].strip())
        if "formato" in line:
            config["formato"] = line.split()[-1].strip()

        if "#" in line:
            colores.append(line.split()[-1].replace(";", ""))

    config["color_ventana"] = colores[0]
    config["color_fuente_ventana"] = colores[1]
    config["color_menu"] = colores[2]
    config["color_fuente_menu"] = colores[3]
    config["color_descarga"] = colores[4]
    config["color_fuente_descarga"] = colores[5]

    return config


def __load_estilo(path):
    """
    Carga el estilo en la interfaz.
    """

    from gi.repository import Gtk
    from gi.repository import Gdk

    screen = Gdk.Screen.get_default()
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(path)
    context = Gtk.StyleContext()

    context.add_provider_for_screen(
        screen,
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER)


def __make_base_directory():
    """
    Crea toda la estructura de Directorios de JAMedia.
    """

    import os

    if not os.path.exists(os.path.join(
        os.environ["HOME"], "JAMediaDatos")):
        os.mkdir(os.path.join(
            os.environ["HOME"], "JAMediaDatos"))
        #os.chmod(os.path.join(
        #    os.environ["HOME"], "JAMediaDatos"), 0755)

    DIRECTORIO_MIS_ARCHIVOS = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "MisArchivos")

    DIRECTORIO_DATOS = os.path.join(
        os.environ["HOME"],
        "JAMediaDatos", "Datos")

    if not os.path.exists(DIRECTORIO_MIS_ARCHIVOS):
        os.mkdir(DIRECTORIO_MIS_ARCHIVOS)
        #os.chmod(DIRECTORIO_MIS_ARCHIVOS, 0755)

    if not os.path.exists(DIRECTORIO_DATOS):
        os.mkdir(DIRECTORIO_DATOS)
        #os.chmod(DIRECTORIO_DATOS, 0755)


def get_data_directory():
    """
    Devuelve el Directorio de Datos de JAMedia y JAMediaTube.
    """

    import os

    DIRECTORIO_DATOS = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "Datos")

    if not os.path.exists(DIRECTORIO_DATOS):
        __make_base_directory()

    return DIRECTORIO_DATOS


def get_my_files_directory():

    import os

    DIRECTORIO_MIS_ARCHIVOS = os.path.join(os.environ["HOME"],
        "JAMediaDatos", "MisArchivos")

    if not os.path.exists(DIRECTORIO_MIS_ARCHIVOS):
        __make_base_directory()

    return DIRECTORIO_MIS_ARCHIVOS


def get_streamings(path):

    import shelve

    archivo = shelve.open(path)
    items = archivo.items()
    archivo.close()

    return items


def __descarga_lista_de_streamings(url):

    print("Conectandose a:", url, "\n\tDescargando Streamings . . .")

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
                print("Direccion Descartada por Repetición:", name, direc)

        print("\tSe han Descargado:", cont, "Estreamings.\n")
        return streamings

    except:
        return []


def set_listas_default():

    import os
    import shelve

    DIRECTORIO_DATOS = get_data_directory()

    listas = [
        os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"),
        ]

    for archivo in listas:
        if not os.path.exists(archivo):
            jamedialista = shelve.open(archivo)
            jamedialista.close()
            #os.chmod(archivo, 0666)

    archivo = shelve.open(
        os.path.join(
            DIRECTORIO_DATOS,
            "JAMediaRadio.JAMedia"))

    lista = archivo.items()
    archivo.close()

    if not lista:
        try:
            lista_radios = __descarga_lista_de_streamings(radios)

            __guarda_lista_de_streamings(
                os.path.join(
                    DIRECTORIO_DATOS,
                    "JAMediaRadio.JAMedia"),
                    lista_radios)

        except:
            print("Error al descargar Streamings de Radios.")


def __clear_lista_de_streamings(path):

    import shelve

    archivo = shelve.open(path)
    archivo.clear()
    archivo.close()


def __guarda_lista_de_streamings(path, items):

    import shelve

    archivo = shelve.open(path)

    for item in items:
        archivo[item[0].strip()] = item[1].strip()

    archivo.close()


def get_streaming_default():

    import os

    DIRECTORIO_DATOS = get_data_directory()

    try:
        lista_radios = __descarga_lista_de_streamings(radios)

        __clear_lista_de_streamings(
            os.path.join(
                DIRECTORIO_DATOS,
                "JAMediaRadio.JAMedia"))

        __guarda_lista_de_streamings(
            os.path.join(
                DIRECTORIO_DATOS,
                "JAMediaRadio.JAMedia"),
                lista_radios)

    except:
        print("Error al descargar Streamings de Radios.")


def stream_en_archivo(streaming, path):

    import shelve

    archivo = shelve.open(path)
    items = archivo.values()

    for item in items:
        if streaming == item:
            archivo.close()
            return True

    archivo.close()

    return False


def eliminar_streaming(url, lista):
    """
    Elimina un Streaming de una lista de jamedia.
    """

    import os

    DIRECTORIO_DATOS = get_data_directory()

    if lista == "JAM-Radio":
        path = os.path.join(
            DIRECTORIO_DATOS, "JAMediaRadio.JAMedia")

    else:
        return

    import shelve

    archivo = shelve.open(path)
    items = archivo.items()

    for item in items:
        if url == str(item[1]):
            del (archivo[item[0]])

    archivo.close()
