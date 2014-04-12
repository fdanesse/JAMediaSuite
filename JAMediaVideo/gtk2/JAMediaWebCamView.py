#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWebCam.py por:
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

import gobject
import gst

gobject.threads_init()


class JAMediaWebCamView(gobject.GObject):

    def __init__(self, xid):

        gobject.GObject.__init__(self)

        self.ventana_id = xid

        # https://github.com/phillipgreenii/photobooth/blob/master/camera_manager.py
        self.camerabin = gst.element_factory_make(
            'camerabin', 'camerabin')

        src = gst.element_factory_make("v4l2src","src")
        src.set_property("device", "/dev/video0")
        self.camerabin.set_property("video-source", src)

        #pantalla = gst.element_factory_make(
        #    'xvimagesink', "pantalla")
        #pantalla.set_property(
        #    "force-aspect-ratio", True)

        self.bus = self.camerabin.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)
                message.src.set_property(
                    "force-aspect-ratio", True)

        elif message.type == gst.MESSAGE_ERROR:
            print "JAMediaReproductor ERROR:"
            print message.parse_error()

    def play(self):
        """
        Pone el pipe de gst en gst.STATE_PLAYING
        """

        self.camerabin.set_state(gst.STATE_PLAYING)

    def stop(self):
        """
        Pone el pipe de gst en gst.STATE_NULL
        """

        self.player.set_state(gst.STATE_NULL)
