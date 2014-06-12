#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   AudioBins.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
#
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

import gst
import gobject

gobject.threads_init()


class Audio_src_Bin(gst.Bin):

    def __init__(self):

        gst.Bin.__init__(self)

        autoaudiosrc = gst.element_factory_make(
            'autoaudiosrc', "autoaudiosrc")
        audiorate = gst.element_factory_make(
            'audiorate', "audiorate")

        capaaudio = gst.Caps(
            "audio/x-raw-int,rate=16000,channels=2,depth=16")
        filtroaudio = gst.element_factory_make(
            "capsfilter", "filtroaudio")
        filtroaudio.set_property("caps", capaaudio)

        audioconvert = gst.element_factory_make(
            'audioconvert', "audioconvert")

        self.add(autoaudiosrc)
        self.add(audiorate)
        self.add(filtroaudio)
        self.add(audioconvert)

        autoaudiosrc.link(audiorate)
        audiorate.link(filtroaudio)
        filtroaudio.link(audioconvert)

        self.add_pad(gst.GhostPad(
            "src", audioconvert.get_static_pad("src")))


class Vorbis_bin(gst.Bin):
    """
    Comprime Audio utilizando vorbisenc.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Vorbis_bin')

        autoaudiosrc = gst.element_factory_make(
            'autoaudiosrc', "autoaudiosrc")
        audiorate = gst.element_factory_make(
            'audiorate', "audiorate")

        capaaudio = gst.Caps(
            "audio/x-raw-int,rate=16000,channels=2,depth=16")
        filtroaudio = gst.element_factory_make(
            "capsfilter", "filtroaudio")
        filtroaudio.set_property("caps", capaaudio)

        audioconvert = gst.element_factory_make(
            'audioconvert', "audioconvert")

        vorbisenc = gst.element_factory_make(
            'vorbisenc', 'vorbisenc')

        self.add(autoaudiosrc)
        self.add(audiorate)
        self.add(filtroaudio)
        self.add(audioconvert)
        self.add(vorbisenc)

        autoaudiosrc.link(audiorate)
        audiorate.link(filtroaudio)
        filtroaudio.link(audioconvert)
        audioconvert.link(vorbisenc)

        self.add_pad(gst.GhostPad("src",
            vorbisenc.get_static_pad("src")))
