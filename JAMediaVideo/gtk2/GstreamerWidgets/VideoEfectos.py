#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VideoEfectos.py por:
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
        #'quarktv',                         # gst-plugins-good Demasiado Lento
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
