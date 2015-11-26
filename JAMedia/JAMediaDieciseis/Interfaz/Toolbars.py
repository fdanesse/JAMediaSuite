#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
from Globales import get_colors
from Globales import get_ToggleToolButton
from Globales import get_SeparatorToolItem
from Globales import get_boton

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONS = os.path.join(BASE_PATH, "Iconos")


def desactivar(objeto):
    objeto.set_active(False)


class Toolbar(gtk.Toolbar):
    """
    Toolbar principal de JAMedia.
    """

    __gsignals__ = {
    'toggled': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, gobject.TYPE_BOOLEAN))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.set_property("toolbar-style", 0)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(ICONS, "JAMedia.svg")
        self.credits = get_ToggleToolButton(archivo, flip=False,
            pixels=35, tooltip_text="Creditos")
        self.credits.connect("toggled", self.__toggled_button)
        self.insert(self.credits, -1)

        archivo = os.path.join(ICONS, "help.svg")
        self.help = get_ToggleToolButton(archivo, flip=False,
            pixels=24, tooltip_text="Ayuda")
        self.help.connect("toggled", self.__toggled_button)
        self.insert(self.help, -1)

        self.insert(get_SeparatorToolItem(draw=True,
            ancho=1, expand=False), -1)

        archivo = os.path.join(ICONS, "Household-Tv-icon.png")
        self.tele = get_ToggleToolButton(archivo, flip=False,
            pixels=24, tooltip_text="Televisión")
        self.tele.connect("toggled", self.__toggled_button)
        self.insert(self.tele, -1)
        self.tele.set_sensitive(False)  #FIXME: Problemas en webkit

        archivo = os.path.join(ICONS, "Music-Radio-1-icon.png")
        self.radio = get_ToggleToolButton(archivo, flip=False,
            pixels=24, tooltip_text="Radio")
        self.radio.connect("toggled", self.__toggled_button)
        self.insert(self.radio, -1)

        archivo = os.path.join(ICONS, "file.png")
        self.arch = get_ToggleToolButton(archivo, flip=False,
            pixels=24, tooltip_text="Archivos")
        self.arch.connect("toggled", self.__toggled_button)
        self.insert(self.arch, -1)

        self.insert(get_SeparatorToolItem(draw=True,
            ancho=1, expand=False), -1)

        archivo = os.path.join(ICONS, "cloud-download.png")
        self.download = get_boton(archivo, flip=False,
            pixels=24, tooltip_text="Descargar Streamings")
        self.download.connect("clicked", self.__clicked_button)
        self.insert(self.download, -1)

        self.insert(get_SeparatorToolItem(draw=True,
            ancho=1, expand=False), -1)

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(ICONS, "button-cancel.svg")
        self.salir = get_ToggleToolButton(archivo, flip=False,
            pixels=18, tooltip_text="Salir")
        self.salir.connect("toggled", self.__toggled_button)
        self.insert(self.salir, -1)

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=3, expand=False), -1)

        self.show_all()

    def __toggled_button(self, button):
        text = button.get_property("tooltip-text")
        valor = button.get_property("active")
        if text == "Salir" and valor:
            dialog = gtk.Dialog(parent=self.get_toplevel(),
                title="Alerta",
                buttons=("Si", gtk.RESPONSE_ACCEPT,
                "No", gtk.RESPONSE_CANCEL))
            dialog.set_border_width(15)
            dialog.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
            label = gtk.Label("¿Salir de JAMedia?")
            label.show()
            dialog.vbox.pack_start(label, True, True, 5)
            run = dialog.run()
            dialog.destroy()
            if run == gtk.RESPONSE_ACCEPT:
                self.emit("toggled", text, True)
            else:
                self.emit("toggled", text, False)
            return
        elif text == "Salir" and not valor:
            return
        if valor:
            buttons = [
                self.credits, self.help, self.tele,
                self.radio, self.arch, self.salir]
            if button in buttons:
                buttons.remove(button)
            map(desactivar, buttons)
        self.emit("toggled", text, valor)

    def __clicked_button(self, button):
        text = button.get_property("tooltip-text")
        self.emit("toggled", text, False)
