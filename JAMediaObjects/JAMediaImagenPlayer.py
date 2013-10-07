#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaImagenPlayer.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM! - Uruguay
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

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gst
from gi.repository import GstVideo

GObject.threads_init()
Gst.init([])
    
# Guia: http://developer.gnome.org/gstreamer/stable/libgstreamer.html

class JAMediaImagenPlayer(GObject.GObject):
    
    def __init__(self, ventana_id):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """
        
        GObject.GObject.__init__(self)
        
        self.ventana_id = ventana_id
        
        from JAMediaGstreamer.JAMediaBins import JAMedia_Video_Pipeline
        
        # Gestor de la salida de Video del reproductor.
        self.video_pipeline = JAMedia_Video_Pipeline()
        
        self.efectos = []
        
        self.__reset()
        
    def __reset(self):
        
        # gst-launch-1.0 filesrc location="linux3.jpg" ! decodebin ! imagefreeze !
        # videoconvert ! frei0r-filter-cartoon ! videoconvert ! autovideosink
        
        # Reproductor.
        self.player = Gst.ElementFactory.make(
            "playbin", "player")
        self.player.set_property(
            'force-aspect-ratio', True)
        
        # Si no se establecen los valores al original, se produce un error.
        self.video_pipeline.reset_balance()
        
        self.player.set_window_handle(self.ventana_id)
        self.player.set_property('video-sink', self.video_pipeline)
        '''
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)
        
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)'''
        
    def load(self, uri):
        """
        Carga un archivo o stream en el pipe de Gst.
        """
        
        self.stop()
        self.__reset()
        
        if os.path.exists(uri):
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)
            self.__play()
            
        else:
            # FIXME: Funciona con la radio pero no con la Tv
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.__play()
                
    def __play(self):
        """
        Pone el pipe de Gst en Gst.State.PLAYING
        """
        
        self.player.set_state(Gst.State.PLAYING)
        
    def stop(self):
        """
        Pone el pipe de Gst en Gst.State.NULL
        """
        
        self.player.set_state(Gst.State.NULL)
        
    def pause_play(self):
        """
        Llama a play() o pause()
        segun el estado actual del pipe de Gst.
        """
        
        if self.estado == Gst.State.PAUSED \
            or self.estado == Gst.State.NULL \
            or self.estado == Gst.State.READY:
            self.__play()
            
        elif self.estado == Gst.State.PLAYING:
            self.__pause()
            