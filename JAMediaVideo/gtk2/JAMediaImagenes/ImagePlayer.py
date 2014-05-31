#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ImagePlayer.py por:
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

import os

import gobject
import gst

gobject.threads_init()


class ImagePlayer(gobject.GObject):

    def __init__(self, ventana_id, width, height):
        gobject.GObject.__init__(self)

        self.ventana_id = ventana_id
        self.player = None
        self.bus = None

        self.player = gst.element_factory_make(
            "playbin2", "player")

        self.video_bin = Video_Out(width, height)

        self.player.set_property('video-sink', self.video_bin)

        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __bus_handler(self, bus, message):
        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        elif message.type == gst.MESSAGE_ERROR:
            print "ImagePlayer ERROR:"
            print message.parse_error()
            print

        return gst.BUS_PASS

    def __play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def rotar(self, valor):
        self.stop()
        self.video_bin.rotar(valor)
        self.__play()

    def set_zoom(self, accion):
        print accion

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

    def load(self, uri):
        self.stop()

        if not uri:
            return

        if os.path.exists(uri):
            direccion = "file://" + uri
            self.player.set_property("uri", direccion)
            self.__play()

        return False

    def set_dimension(self, width, height):
        self.video_bin.set_dimension(width, height)


class Video_Out(gst.Pipeline):

    def __init__(self, width, height):

        gst.Pipeline.__init__(self)

        self.set_name('video_out')

        imagefreeze = gst.element_factory_make(
            'imagefreeze', "imagefreeze")

        videoconvert = gst.element_factory_make(
            'ffmpegcolorspace', 'ffmpegcolorspace')

        videoflip = gst.element_factory_make(
            'videoflip', "videoflip")

        caps = gst.Caps(
            'video/x-raw-rgb,framerate=30/1,width=%s,height=%s' % (
            width,height))
        filtro = gst.element_factory_make(
            "capsfilter", "filtro")
        filtro.set_property("caps", caps)

        ximagesink = gst.element_factory_make(
            'ximagesink', "ximagesink")

        ximagesink.set_property(
            "force-aspect-ratio", True)

        self.add(imagefreeze)
        self.add(videoconvert)
        self.add(videoflip)
        self.add(filtro)
        self.add(ximagesink)

        imagefreeze.link(videoconvert)
        videoconvert.link(videoflip)
        videoflip.link(filtro)
        filtro.link(ximagesink)

        self.ghost_pad = gst.GhostPad(
            "sink", imagefreeze.get_static_pad("sink"))

        self.ghost_pad.set_target(
            imagefreeze.get_static_pad("sink"))

        self.add_pad(self.ghost_pad)

    def rotar(self, valor):
        """
        Rota el Video.
        """

        videoflip = self.get_by_name("videoflip")
        rot = videoflip.get_property('method')

        if valor == "Derecha":
            if rot < 3:
                rot += 1

            else:
                rot = 0

        elif valor == "Izquierda":
            if rot > 0:
                rot -= 1

            else:
                rot = 3

        videoflip.set_property('method', rot)
