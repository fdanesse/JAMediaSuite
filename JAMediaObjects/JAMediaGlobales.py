#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGlobals.py por:
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

'''
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
'''
'''
def get_pixels(centimetros):
    """
    Recibe un tamaño en centimetros y
    devuelve el tamaño en pixels que le corresponde,
    según tamaño del monitor que se está utilizando.

    # 1 px = 0.026458333 cm #int(centimetros/0.026458333)
    # 1 Pixel = 0.03 Centimetros = 0.01 Pulgadas.
    """
    """
    from gi.repository import GdkX11

    screen = GdkX11.X11Screen()

    res_w = screen.width()
    res_h = screen.height()

    mm_w = screen.width_mm()
    mm_h = screen.height_mm()

    ancho = int (float(res_w) / float(mm_w) * 10.0 * centimetros)
    alto = int (float(res_h) / float(mm_h) * 10.0 * centimetros)
    if centimetros == 5.0: print ">>>>", centimetros, int(min([ancho, alto]))
    return int(min([ancho, alto]))"""

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
'''
'''
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
'''
'''
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
'''
'''
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
'''

# >>> JAMediaVideo
    # clockoverlay
    # circle
    # fpsdisplaysink
    # InputSelector
'''
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
'''
'''
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
'''
'''
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
'''

# <<< JAMediaVideo

'''
Anotaciones para describir las clases de JAMedia:
    import pydoc
    import JAMediaObjects
    from JAMediaObjects.JAMediaReproductor import JAMediaReproductor

    pydoc.writedoc(JAMediaReproductor)'''
