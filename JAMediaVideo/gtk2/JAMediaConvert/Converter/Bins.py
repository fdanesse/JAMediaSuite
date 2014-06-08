#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaBins.py por:
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


class wav_bin(gst.Bin):

    def __init__(self, location):

        gst.Bin.__init__(self)

        self.set_name('audio-out')

        audioconvert = gst.element_factory_make(
            "audioconvert", "audioconvert")
        audioresample = gst.element_factory_make(
            "audioresample", "audioresample")
        audioresample.set_property('quality', 10)

        wavenc = gst.element_factory_make(
            "wavenc", "wavenc")

        filesink = gst.element_factory_make(
            "filesink", "filesinkwav")

        self.add(audioconvert)
        self.add(audioresample)
        self.add(wavenc)
        self.add(filesink)

        audioconvert.link(audioresample)
        audioresample.link(wavenc)
        wavenc.link(filesink)

        filesink.set_property(
            'location', location)

        pad = audioconvert.get_static_pad("sink")
        self.add_pad(gst.GhostPad("sink", pad))


class mp3_bin(gst.Bin):

    def __init__(self, location):

        gst.Bin.__init__(self)

        self.set_name('audio-out')

        audioconvert = gst.element_factory_make(
            "audioconvert", "audioconvert")
        audioresample = gst.element_factory_make(
            "audioresample", "audioresample")
        audioresample.set_property('quality', 10)

        lamemp3enc = gst.element_factory_make(
            "lamemp3enc", "lamemp3enc")
        filesink = gst.element_factory_make(
            "filesink", "filesinkmp3")

        self.add(audioconvert)
        self.add(audioresample)
        self.add(lamemp3enc)
        self.add(filesink)

        audioconvert.link(audioresample)
        audioresample.link(lamemp3enc)
        lamemp3enc.link(filesink)

        filesink.set_property(
            'location', location)

        pad = audioconvert.get_static_pad("sink")
        self.add_pad(gst.GhostPad("sink", pad))


class ogg_bin(gst.Bin):

    def __init__(self, location):

        gst.Bin.__init__(self)

        self.set_name('audio-out')

        vorbisenc = gst.element_factory_make(
            "vorbisenc", "vorbisenc")
        oggmux = gst.element_factory_make(
            "oggmux", "oggmux")
        filesink = gst.element_factory_make(
            "filesink", "filesinkogg")

        self.add(vorbisenc)
        self.add(oggmux)
        self.add(filesink)

        vorbisenc.link(oggmux)
        oggmux.link(filesink)

        filesink.set_property(
            'location', location)

        pad = vorbisenc.get_static_pad("sink")
        self.add_pad(gst.GhostPad("sink", pad))
