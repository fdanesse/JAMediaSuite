import os

import gtk
from gtk import gdk
import gobject

from Globales import get_colors

from JAMediaWebCamView import JAMediaWebCamView
from Widgets import Visor


class BasePanel(gtk.HPaned):

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.jamediawebcam = None
        self.pantalla = Visor()
        #vbox.pack_start(self.pantalla, True, True, 0)
        self.pack1(self.pantalla, resize=True, shrink=True)

        self.show_all()

        self.pantalla.connect("button_press_event",
            self.__clicks_en_pantalla)

    def run(self):

        xid = self.pantalla.get_property('window').xid
        self.jamediawebcam = JAMediaWebCamView(xid)
        gobject.idle_add(self.jamediawebcam.play)

    def __clicks_en_pantalla(self, widget, event):
        """
        Hace fullscreen y unfullscreen sobre la
        ventana principal cuando el usuario hace
        doble click en el visor.
        """

        if event.type.value_name == "GDK_2BUTTON_PRESS":

            self.get_toplevel().set_sensitive(False)

            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w, h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())

            #self.__cancel_toolbars_flotantes()

            if ww == w and hh == h:
                #ventana.set_border_width(2)
                gobject.idle_add(ventana.unfullscreen)

            else:
                #ventana.set_border_width(0)
                gobject.idle_add(ventana.fullscreen)

            self.get_toplevel().set_sensitive(True)
