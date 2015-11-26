#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
from Globales import get_colors
from Toolbars import Toolbar
from AudioVideoPlayer.VideoPanel import VideoPanel
from RadioPlayer.RadioPanel import RadioPanel
#from TvPlayer.TvPanel import TvPanel

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def desactivar(objeto):
    objeto.hide()


class JAMedia(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("JAMedia")
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_icon_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMedia.svg"))
        self.set_resizable(True)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)

        self.set_property("urgency-hint", True)
        self.set_property("default-width", 640)
        self.set_property("default-height", 480)
        #self.set_property("deletable", False)

        self.vbox = gtk.VBox()
        self.toolbar = Toolbar()

        #self.creditos = VideoPanel()
        #self.ayuda = VideoPanel()
        ##self.config = VideoPanel()
        #self.television = TvPanel()
        self.radio = RadioPanel()
        self.audiovideo = VideoPanel()

        self.vbox.pack_start(self.toolbar, False, False, 0)
        #self.vbox.pack_start(self.creditos, False, False, 0)
        #self.vbox.pack_start(self.ayuda, False, False, 0)
        #self.vbox.pack_start(self.config, False, False, 0)
        #self.vbox.pack_start(self.television, True, True, 0)
        self.vbox.pack_start(self.radio, True, True, 0)
        self.vbox.pack_start(self.audiovideo, True, True, 0)
        self.add(self.vbox)

        self.toolbar.connect("toggled", self.__switch)
        self.audiovideo.connect("playing", self.__playing)
        self.radio.connect("playing", self.__playing)
        #self.television.connect("playing", self.__playing)

        self.show_all()
        self.audiovideo.hide()
        self.radio.hide()
        #self.television.hide()
        self.resize(640, 480)

    def __playing(self, widget):
        for wid in self.vbox.get_children()[1:]:
            if wid != widget:
                wid.stop()
                wid.playerlist.lista.get_selection().unselect_all()
                wid.playerlist.lista.valor_select = False
                wid.playerlist.lista.ultimo_select = False

    def __switch(self, toolbar, text, valor):
        #Creditos           Mostrar Creditos
        #Ayuda              Mostrar ayuda
        if text == "Descargar Streamings":
            print "Descargar Streamings"
            return
        if text == "Salir" and valor:
            self.stop()
        elif text == "Salir" and not valor:
            self.toolbar.salir.set_active(False)
            return
        if not valor:
            map(desactivar, self.vbox.get_children()[1:])
        else:
            if text == "Archivos":
                self.audiovideo.show()
            elif text == "Radio":
                self.radio.show()
            #elif text == "Televisión":
            #    self.television.show()

    def stop(self):
        self.radio.stop()
        self.audiovideo.stop()
        #self.television.stop()
        self.destroy()
