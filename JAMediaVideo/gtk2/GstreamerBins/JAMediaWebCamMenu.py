#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWebCamMenu.py por:
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
import pygst
import gst
import gtk

PR = False


class JAMediaWebCamMenu(gobject.GObject):

    def __init__(self, ventana_id, device="/dev/video0"):

        gobject.GObject.__init__(self)

        if PR:
            print "JAMediaWebCamMenu Iniciada"

        self.ventana_id = ventana_id
        self.pipeline = gst.Pipeline()

        camara = gst.Bin()

        if "Escritorio" in device:
            from VideoBins import ximagesrc_bin
            camara = ximagesrc_bin()

        else:
            if "/dev/video" in device:
                from VideoBins import v4l2src_bin
                camara = v4l2src_bin()
                camara.set_device(device)

            else:
                from VideoBins import In_lan_udpsrc_bin
                camara = In_lan_udpsrc_bin(device)

        from VideoBins import Balance_bin
        balance = Balance_bin()

        from VideoBins import xvimage_bin
        xvimage = xvimage_bin()

        self.pipeline.add(camara)
        self.pipeline.add(balance)
        self.pipeline.add(xvimage)

        camara.link(balance)
        balance.link(xvimage)

        self.bus = self.pipeline.get_bus()
        #self.bus.set_sync_handler(self.__bus_handler)
        self.bus.add_signal_watch()                             # ****
        #self.bus.connect('message', self.__on_mensaje)          # ****
        self.bus.enable_sync_message_emission()                 # ****
        self.bus.connect('sync-message', self.__sync_message)   # ****

    '''
    def __bus_handler(self, bus, message):
        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)

        elif message.type == gst.MESSAGE_ERROR:
            print "JAMediaWebCamMenu ERROR:"
            print message.parse_error()

        return gst.BUS_PASS
    '''

    def __sync_message(self, bus, message):
        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                gtk.gdk.threads_enter()
                gtk.gdk.display_get_default().sync()
                message.src.set_xwindow_id(self.ventana_id)
                gtk.gdk.threads_leave()

        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            if PR:
                print "JAMediaWebCamMenu ERROR:"
                print "\t%s" % err
                print "\t%s" % debug

    def get_rotacion(self):
        if PR:
            print "\tJAMediaWebCamMenu.get_rotacion"
        balance = self.pipeline.get_by_name("Balance_bin")
        return balance.get_rotacion()

    def set_rotacion(self, rot):
        if PR:
            print "\tJAMediaWebCamMenu.set_rotacion"
        balance = self.pipeline.get_by_name("Balance_bin")
        balance.set_rotacion(rot)

    def get_config(self):
        if PR:
            print "\tJAMediaWebCamMenu.get_config"
        balance = self.pipeline.get_by_name("Balance_bin")
        return balance.get_config()

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        if PR:
            print "\tJAMediaWebCamMenu.set_balance"
        balance = self.pipeline.get_by_name("Balance_bin")

        balance.set_balance(
            brillo=brillo,
            contraste=contraste,
            saturacion=saturacion,
            hue=hue,
            gamma=gamma)

    def stop(self):
        if PR:
            print "\tJAMediaWebCamMenu.stop"
        self.pipeline.set_state(gst.STATE_NULL)

    def play(self):
        if PR:
            print "\tJAMediaWebCamMenu.play"
        self.pipeline.set_state(gst.STATE_PLAYING)
