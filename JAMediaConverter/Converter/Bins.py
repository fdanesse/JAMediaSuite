#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaBins.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay
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

from gi.repository import Gst
from gi.repository import GstVideo  # necesario

#GObject.threads_init()


class wav_bin(Gst.Bin):

    def __init__(self, location):

        Gst.Bin.__init__(self)

        self.set_name('wav_bin')

        wavenc = Gst.ElementFactory.make(
            "wavenc", "wavenc")

        filesink = Gst.ElementFactory.make(
            "filesink", "filesinkwav")

        self.add(wavenc)
        self.add(filesink)

        wavenc.link(filesink)

        filesink.set_property(
            'location', location)

        pad = wavenc.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))


class mp3_bin(Gst.Bin):

    def __init__(self, location):

        Gst.Bin.__init__(self)

        self.set_name('mp3_bin')

        lamemp3enc = Gst.ElementFactory.make(
            "lamemp3enc", "lamemp3enc")

        filesink = Gst.ElementFactory.make(
            "filesink", "filesinkmp3")

        self.add(lamemp3enc)
        self.add(filesink)

        lamemp3enc.link(filesink)

        filesink.set_property(
            'location', location)

        pad = lamemp3enc.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))


class ogg_bin(Gst.Bin):

    def __init__(self, location):

        Gst.Bin.__init__(self)

        self.set_name('ogg_bin')

        vorbisenc = Gst.ElementFactory.make(
            "vorbisenc", "vorbisenc")
        oggmux = Gst.ElementFactory.make(
            "oggmux", "oggmux")
        filesink = Gst.ElementFactory.make(
            "filesink", "filesinkogg")

        self.add(vorbisenc)
        self.add(oggmux)
        self.add(filesink)

        vorbisenc.link(oggmux)
        oggmux.link(filesink)

        filesink.set_property(
            'location', location)

        pad = vorbisenc.get_static_pad("sink")
        self.add_pad(Gst.GhostPad.new("sink", pad))
