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


class wav_bin(gst.Bin):

    def __init__(self, location):

        gst.Bin.__init__(self)

        self.set_name('audio-out')

        audioconvert = gst.element_factory_make(
            "audioconvert", "audioconvert")
        #audioresample = gst.element_factory_make(
        #    "audioresample", "audioresample")
        #audioresample.set_property('quality', 10)

        wavenc = gst.element_factory_make(
            "wavenc", "wavenc")

        filesink = gst.element_factory_make(
            "filesink", "filesinkwav")

        self.add(audioconvert)
        #self.add(audioresample)
        self.add(wavenc)
        self.add(filesink)

        #audioconvert.link(audioresample)
        #audioresample.link(wavenc)
        audioconvert.link(wavenc)
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
        #audioresample = gst.element_factory_make(
        #    "audioresample", "audioresample")
        #audioresample.set_property('quality', 10)

        lamemp3enc = gst.element_factory_make(
            "lamemp3enc", "lamemp3enc")
        filesink = gst.element_factory_make(
            "filesink", "filesinkmp3")

        self.add(audioconvert)
        #self.add(audioresample)
        self.add(lamemp3enc)
        self.add(filesink)

        #audioconvert.link(audioresample)
        #audioresample.link(lamemp3enc)
        audioconvert.link(lamemp3enc)
        lamemp3enc.link(filesink)

        filesink.set_property(
            'location', location)

        pad = audioconvert.get_static_pad("sink")
        self.add_pad(gst.GhostPad("sink", pad))


class ogg_bin(gst.Bin):

    def __init__(self, location):

        gst.Bin.__init__(self)

        self.set_name('audio-out')

        audioconvert = gst.element_factory_make(
            "audioconvert", "audioconvert")
        #audioresample = gst.element_factory_make(
        #    "audioresample", "audioresample")
        #audioresample.set_property('quality', 10)

        vorbisenc = gst.element_factory_make(
            "vorbisenc", "vorbisenc")
        oggmux = gst.element_factory_make(
            "oggmux", "oggmux")
        filesink = gst.element_factory_make(
            "filesink", "filesinkogg")

        self.add(audioconvert)
        #self.add(audioresample)
        self.add(vorbisenc)
        self.add(oggmux)
        self.add(filesink)

        #audioconvert.link(audioresample)
        #audioresample.link(vorbisenc)
        audioconvert.link(vorbisenc)
        vorbisenc.link(oggmux)
        oggmux.link(filesink)

        filesink.set_property(
            'location', location)

        pad = audioconvert.get_static_pad("sink")
        self.add_pad(gst.GhostPad("sink", pad))


class mp2_bin(gst.Bin):
    """
    Comprime Audio utilizando ffenc_mp2.
        Salida de audio para video avi.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('mp2_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 0)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        audioconvert = gst.element_factory_make('audioconvert', "audioconvert")
        ffenc_mp2 = gst.element_factory_make('ffenc_mp2', 'ffenc_mp2')

        self.add(queue)
        self.add(audioconvert)
        self.add(ffenc_mp2)

        queue.link(audioconvert)
        audioconvert.link(ffenc_mp2)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            ffenc_mp2.get_static_pad("src")))


class mpeg2_bin(gst.Bin):
    """
    Comprime video utilizando ffenc_mpeg2video.
        Salida de video para mpeg.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('mpeg2_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        videorate = gst.element_factory_make(
            'videorate', "videorate")
        ffenc_mpeg2video = gst.element_factory_make(
            'ffenc_mpeg2video', 'ffenc_mpeg2video')

        try:
            videorate.set_property("max-rate", 60)

        except:
            pass

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(videorate)
        self.add(ffenc_mpeg2video)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(videorate)
        videorate.link(ffenc_mpeg2video)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            ffenc_mpeg2video.get_static_pad("src")))


class Vorbis_bin(gst.Bin):
    """
    Comprime Audio utilizando vorbisenc.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Vorbis_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 0)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        audioconvert = gst.element_factory_make('audioconvert', "audioconvert")
        vorbisenc = gst.element_factory_make('vorbisenc', 'vorbisenc')

        self.add(queue)
        self.add(audioconvert)
        self.add(vorbisenc)

        queue.link(audioconvert)
        audioconvert.link(vorbisenc)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            vorbisenc.get_static_pad("src")))


class Theora_bin(gst.Bin):
    """
    Comprime video utilizando theoraenc.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('Theora_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        videorate = gst.element_factory_make(
            'videorate', "videorate")
        theoraenc = gst.element_factory_make(
            'theoraenc', 'theoraenc')
        theoraenc.set_property("quality", 63)

        try:
            videorate.set_property("max-rate", 30)

        except:
            pass

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(videorate)
        self.add(theoraenc)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(videorate)
        videorate.link(theoraenc)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            theoraenc.get_static_pad("src")))


class jpegenc_bin(gst.Bin):
    """
    Codifica video a imágenes utilizando jpegenc.
        Salida de video para videos avi.
    """

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('jpegenc_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        videorate = gst.element_factory_make(
            'videorate', "videorate")
        jpegenc = gst.element_factory_make(
            'jpegenc', 'jpegenc')

        try:
            videorate.set_property("max-rate", 30)

        except:
            pass

        self.add(queue)
        self.add(ffmpegcolorspace)
        self.add(videorate)
        self.add(jpegenc)

        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(videorate)
        videorate.link(jpegenc)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            jpegenc.get_static_pad("src")))


class audio_avi_bin(gst.Bin):

    def __init__(self):

        gst.Bin.__init__(self)

        self.set_name('audio_avi_bin')

        queue = gst.element_factory_make('queue', "queue")
        queue.set_property("max-size-buffers", 0)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        audioconvert = gst.element_factory_make('audioconvert', "audioconvert")

        self.add(queue)
        self.add(audioconvert)

        queue.link(audioconvert)

        self.add_pad(gst.GhostPad("sink",
            queue.get_static_pad("sink")))
        self.add_pad(gst.GhostPad("src",
            audioconvert.get_static_pad("src")))
