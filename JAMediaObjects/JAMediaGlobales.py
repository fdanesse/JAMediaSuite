#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGlobals.py por:
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

canales = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/canales'
radios = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/radios'


def make_base_directory():
    """
    Crea toda la estructura de Directorios de JAMedia.
    """

    import os
    import commands

    if not os.path.exists(os.path.join(os.environ["HOME"], "JAMediaDatos")):
        os.mkdir(os.path.join(os.environ["HOME"], "JAMediaDatos"))
        os.chmod(os.path.join(os.environ["HOME"], "JAMediaDatos"), 0755)

    ### unificar directorios de JAMedia, JAMediaVideo y JAMediaImagenes
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


def get_boton(archivo, flip=False, rotacion=None, pixels=0, tooltip_text=None):
    """
    Devuelve un toolbutton generico.
    """

    from gi.repository import Gtk
    from gi.repository import GdkPixbuf

    if not pixels:
        pixels = get_pixels(1)

    boton = Gtk.ToolButton()

    imagen = Gtk.Image()
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, pixels, pixels)

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


def get_togle_boton(archivo, flip=False,
    color=get_color("GRIS"), pixels=0):
    # Gdk.Color(65000, 65000, 65000)
    """
    Devuelve un toggletoolbutton generico.
    """

    from gi.repository import Gtk
    from gi.repository import GdkPixbuf

    if not pixels:
        pixels = get_pixels(1.5)

    boton = Gtk.ToggleToolButton()
    imagen = Gtk.Image()
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, pixels, pixels)

    if flip:
        pixbuf = pixbuf.flip(True)

    imagen.set_from_pixbuf(pixbuf)
    boton.set_icon_widget(imagen)

    imagen.show()
    boton.show()

    return boton


# >>> JAMedia
def descarga_lista_de_streamings(url):
    """
    Recibe la web donde se publican los streamings
    de radio o televisión de JAMedia y devuelve la lista
    de streamings.

    Un streaming se representa por una lista:
        [nombre, url]
    """

    print "Conectandose a:", url
    print "\tDescargando Streamings . . ."

    cont = 0
    urls = []

    try:
        import urllib

        streamings = []

        web = urllib.urlopen(url)
        lineas = web.readlines()
        web.close()

        for linea in lineas:

            #if 'dir="ltr"><div><div>' in linea:
            #    print linea

            if 'table' in linea:
                l = linea.split('table')

                for x in l:
                    if '<div>' in x:
                        xx = x.split('<div>')

                        for z in xx:
                            if "," in z:
                                s = z.split('</div>')[0]
                                stream = s.split(",")
                                #print stream
                                streamings.append(stream)

                                temp_url = stream[1]
                                if temp_url in urls:
                                    print "\tURL Repetida:", temp_url

                                urls.append(stream[1])
                                cont += 1

        print "\tSe han Descargado:", cont, "Estreamings.\n"
        return streamings

    except:
        return []


def clear_lista_de_streamings(path):
    """
    Limpia la lista de streamings en un archivo.
    """

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

    archivo = shelve.open(path)
    items = archivo.items()
    archivo.close()

    return items


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
        os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")
        ]

    for archivo in listas:
        if not os.path.exists(archivo):
            jamedialista = shelve.open(archivo)
            jamedialista.close()
            os.chmod(archivo, 0666)

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    archivo = shelve.open(
        os.path.join(
            DIRECTORIO_DATOS,
            "JAMediaTV.JAMedia"))

    lista = archivo.items()
    archivo.close()

    if not lista:
        try:
            # Streamings JAMediatv
            lista_canales = descarga_lista_de_streamings(canales)

            guarda_lista_de_streamings(
                os.path.join(
                DIRECTORIO_DATOS,
                "JAMediaTV.JAMedia"),
                lista_canales)

        except:
            print "Error al descargar Streamings de TV."

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    archivo = shelve.open(
        os.path.join(
            DIRECTORIO_DATOS,
            "JAMediaRadio.JAMedia"))

    lista = archivo.items()
    archivo.close()

    if not lista:
        try:
            # Streamings JAMediaradio
            lista_radios = descarga_lista_de_streamings(radios)

            guarda_lista_de_streamings(
                os.path.join(
                    DIRECTORIO_DATOS,
                    "JAMediaRadio.JAMedia"),
                    lista_radios)

        except:
            print "Error al descargar Streamings de Radios."


def get_streaming_default():
    """
    Descarga los streaming desde la web de JAMedia
    cuando el usuario lo solicita.
    """

    import os

    DIRECTORIO_DATOS = get_data_directory()

    try:
        # Streamings JAMediatv
        lista_canales = descarga_lista_de_streamings(canales)

        clear_lista_de_streamings(
            os.path.join(
                DIRECTORIO_DATOS,
                "JAMediaTV.JAMedia"))

        guarda_lista_de_streamings(
            os.path.join(
                DIRECTORIO_DATOS,
                "JAMediaTV.JAMedia"),
                lista_canales)

    except:
        print "Error al descargar Streamings de TV."

    try:
        # Streamings JAMediaradio
        lista_radios = descarga_lista_de_streamings(radios)

        clear_lista_de_streamings(
            os.path.join(
                DIRECTORIO_DATOS,
                "JAMediaRadio.JAMedia"))

        guarda_lista_de_streamings(
            os.path.join(
                DIRECTORIO_DATOS,
                "JAMediaRadio.JAMedia"),
                lista_radios)

    except:
        print "Error al descargar Streamings de Radios."


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

    else:
        return

    import shelve

    archivo = shelve.open(path)
    items = archivo.items()

    for item in items:
        if url == str(item[1]):
            del (archivo[item[0]])

    archivo.close()


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
# <<< JAMedia


# >>> JAMediaVideo
    # clockoverlay
    # circle
    # fpsdisplaysink
    # InputSelector

def get_video_efectos():

    VIDEOEFECTOS = [
        # Filter/Effect/Video:
        #'frei0r-filter-scale0tilt',
        #'frei0r-filter-curves',
        'frei0r-filter-color-distance',
        #'frei0r-filter-scanline0r',
        #'frei0r-filter-3-point-color-balance',
        #'frei0r-filter-b',
        #'frei0r-filter-g',
        'frei0r-filter-cartoon',
        #'frei0r-filter-threelay0r',
        #'frei0r-filter-3dflippo',
        #'frei0r-filter-rgb-parade',
        #'frei0r-filter-r',
        #'frei0r-filter-edgeglow',
        #'frei0r-filter-squareblur',
        #'frei0r-filter-lens-correction',
        #'frei0r-filter-threshold0r',
        #'frei0r-filter-gamma',
        #'frei0r-filter-glow',
        #'frei0r-filter-tint0r',
        'frei0r-filter-baltan',
        #'frei0r-filter-water',
        #'frei0r-filter-contrast0r',
        'frei0r-filter-vertigo',
        'frei0r-filter-bw0r',
        'frei0r-filter-equaliz0r',
        #'frei0r-filter-letterb0xed',
        'frei0r-filter-tehroxx0r',
        'frei0r-filter-invert0r',
        #'frei0r-filter-brightness',
        #'frei0r-filter-vectorscope',
        #'frei0r-filter-delay0r',
        #'frei0r-filter-dealygrab',
        #'frei0r-filter-bluescreen0r',
        'frei0r-filter-twolay0r',
        #'frei0r-filter-saturat0r',
        #'frei0r-filter-nosync0r',
        #'frei0r-filter-levels',
        'frei0r-filter-nervous',
        #'frei0r-filter-perspective',
        'frei0r-filter-primaries',
        #'frei0r-filter-hueshift0r',
        #'frei0r-filter-k-means-clustering',        ***
        'frei0r-filter-sobel',
        'frei0r-filter-luminance',
        #'frei0r-filter-white-balance',
        'frei0r-filter-distort0r',
        #'frei0r-filter-mask0mate',
        #'frei0r-filter-flippo',
        #'frei0r-filter-transparency',
        'frei0r-filter-pixeliz0r',
        #'gdkpixbufoverlay',                        # gst-plugins-good
        #'videocrop',                               # gst-plugins-good
        #'aspectratiocrop',                         # gst-plugins-good
        #'gamma',                                   # gst-plugins-good
        #'videobalance',                            # gst-plugins-good
        #'videoflip',                               # gst-plugins-good
        #'videomedian',                             # gst-plugins-good
        'edgetv',                                   # gst-plugins-good
        'agingtv',                                  # gst-plugins-good
        'dicetv',                                   # gst-plugins-good
        'warptv',                                   # gst-plugins-good
        #'shagadelictv',                            # gst-plugins-good
        'vertigotv',                                # gst-plugins-good
        'revtv',                                    # gst-plugins-good
        #'quarktv',                                 # gst-plugins-good Demasiado Lento
        #'optv',                                    # gst-plugins-good
        'radioactv',                                # gst-plugins-good
        'streaktv',                                 # gst-plugins-good
        'rippletv',                                 # gst-plugins-good
        #'burn',
        'chromium',
        #'dilate',
        'dodge',
        'exclusion',
        'solarize',
        #'gaussianblur',
        #'navigationtest',                          # gst-plugins-good
        #'smooth',
        #'coloreffects',
        #'chromahold',
        #'deinterlace',                             # gst-plugins-good
        #'alpha',                                   # gst-plugins-good
        #'videobox',                                # gst-plugins-good
        #'videorate',                               # gst-plugins-base
        #'avdeinterlace',

        # Transform/Effect/Video:
        #'circle',
        #'diffuse',                                 # Demasiado Lento
        'kaleidoscope',
        'marble',
        'pinch',
        #'rotate',
        'sphere',
        'twirl',
        'waterripple',
        'stretch',
        'bulge',
        'tunnel',
        'square',
        'mirror',
        'fisheye',
        ]

    return VIDEOEFECTOS


def get_jamedia_video_efectos():

    JAMedia_VIDEOEFECTOS = [
        # Filter/Effect/Video:
        #'frei0r-filter-scale0tilt',
        #'frei0r-filter-curves',                    # color curvas
        'frei0r-filter-color-distance',
        #'frei0r-filter-scanline0r',                # Se cuelga todo
        #'frei0r-filter-3-point-color-balance',
        #'frei0r-filter-b',
        #'frei0r-filter-g',
        'frei0r-filter-cartoon',
        'frei0r-filter-threelay0r',
        #'frei0r-filter-3dflippo',
        #'frei0r-filter-rgb-parade',
        #'frei0r-filter-r',
        #'frei0r-filter-edgeglow',
        #'frei0r-filter-squareblur',
        #'frei0r-filter-lens-correction',
        #'frei0r-filter-threshold0r',
        #'frei0r-filter-gamma',
        #'frei0r-filter-glow',
        #'frei0r-filter-tint0r',
        'frei0r-filter-baltan',
        #'frei0r-filter-water',
        #'frei0r-filter-contrast0r',
        'frei0r-filter-vertigo',
        'frei0r-filter-bw0r',
        #'frei0r-filter-equaliz0r',
        #'frei0r-filter-letterb0xed',
        'frei0r-filter-tehroxx0r',
        'frei0r-filter-invert0r',
        #'frei0r-filter-brightness',
        #'frei0r-filter-vectorscope',
        #'frei0r-filter-delay0r',
        'frei0r-filter-dealygrab',
        #'frei0r-filter-bluescreen0r',
        #'frei0r-filter-twolay0r',
        #'frei0r-filter-saturat0r',
        #'frei0r-filter-nosync0r',
        #'frei0r-filter-levels',
        #'frei0r-filter-nervous',
        #'frei0r-filter-perspective',
        'frei0r-filter-primaries',
        #'frei0r-filter-hueshift0r',
        #'frei0r-filter-k-means-clustering',        #***
        'frei0r-filter-sobel',
        #'frei0r-filter-luminance',
        #'frei0r-filter-white-balance',
        'frei0r-filter-distort0r',
        #'frei0r-filter-mask0mate',
        #'frei0r-filter-flippo',
        #'frei0r-filter-transparency',
        #'frei0r-filter-pixeliz0r',
        #'gdkpixbufoverlay',                        # gst-plugins-good
        #'videocrop',                               # gst-plugins-good
        #'aspectratiocrop',                         # gst-plugins-good
        #'gamma',                                   # gst-plugins-good
        #'videobalance',                            # gst-plugins-good
        #'videoflip',                               # gst-plugins-good
        #'videomedian',                             # gst-plugins-good
        'edgetv',                                   # gst-plugins-good
        'agingtv',                                  # gst-plugins-good
        'dicetv',                                   # gst-plugins-good
        'warptv',                                   # gst-plugins-good
        #'shagadelictv',                            # gst-plugins-good
        'vertigotv',                                # gst-plugins-good
        #'revtv',                                   # gst-plugins-good
        #'quarktv',                                 # gst-plugins-good Demasiado Lento
        #'optv',                                    # gst-plugins-good
        'radioactv',                                # gst-plugins-good
        'streaktv',                                 # gst-plugins-good
        'rippletv',                                 # gst-plugins-good
        #'burn',
        'chromium',
        #'dilate',
        'dodge',
        'exclusion',
        'solarize',
        #'gaussianblur',
        #'navigationtest',                          # gst-plugins-good
        #'smooth',
        #'coloreffects',
        #'chromahold',
        #'deinterlace',                             # gst-plugins-good
        #'alpha',                                   # gst-plugins-good
        #'videobox',                                # gst-plugins-good
        #'videorate',                               # gst-plugins-base
        #'avdeinterlace',

        # Transform/Effect/Video:
        #'circle',
        #'diffuse',                                 # Demasiado Lento
        'kaleidoscope',
        'marble',
        #'pinch',
        #'rotate',
        'sphere',
        #'twirl',
        #'waterripple',
        'stretch',
        'bulge',
        'tunnel',
        'square',
        'mirror',
        'fisheye',
        ]

    return JAMedia_VIDEOEFECTOS


def get_visualizadores():

    AUDIOVISUALIZADORES = [
        'wavescope',
        'synaescope',
        'spectrascope',
        'monoscope',
        #'spacescope',                               # problemas en calidad de grabacion de audio
        #'goom',                                     # problemas en calidad de grabacion de audio
        #'goom2k1',                                  # Al parecer no funciona
        'libvisual_oinksie',
        'libvisual_lv_scope',
        'libvisual_lv_analyzer',
        'libvisual_jess',
        'libvisual_jakdaw',
        'libvisual_infinite',
        'libvisual_corona',
        #'libvisual_bumpscope',                      # Feo
        ]

    return AUDIOVISUALIZADORES


def get_widget_config_efecto(nombre):
    """
    Devulve el widget de configuración de un
    determinado efecto de video o visualizador de audio.
    """

    if nombre == 'radioactv':
        from JAMediaGstreamer.WidgetsEfectosGood import Radioactv
        return Radioactv()

    elif nombre == 'agingtv':
        from JAMediaGstreamer.WidgetsEfectosGood import Agingtv
        return Agingtv()

    else:
        return False

# <<< JAMediaVideo

'''
Anotaciones para describir las clases de JAMedia:
    import pydoc
    import JAMediaObjects
    from JAMediaObjects.JAMediaReproductor import JAMediaReproductor

    pydoc.writedoc(JAMediaReproductor)'''
