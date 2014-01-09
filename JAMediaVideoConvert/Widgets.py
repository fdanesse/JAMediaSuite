#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib


class InfoBox(Gtk.Frame):

    def __init__(self):

        Gtk.Frame.__init__(self)

        self.info = ""

        self.set_size_request(250, -1)

        self.set_label("Archivos Restantes:")

        self.info_widget = Gtk.TextView()
        self.info_widget.set_editable(False)
        self.info_widget.set_buffer(Gtk.TextBuffer())

        from gi.repository import Pango

        self.info_widget.modify_font(
            Pango.FontDescription('Monospace 8'))

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.info_widget)

        self.add(scroll)
        self.show_all()

    def reset(self):

        self.info = ""
        self.set_cantidad(0)
        GLib.idle_add(self.__update_info, "")

    def set_info(self, info):

        if self.info:
            self.info = "%s\n%s" % (self.info, str(info))

        else:
            self.info = str(info)

        text = self.info

        GLib.idle_add(self.__update_info, text)

    def __update_info(self, text):

        buffer = self.info_widget.get_buffer()

        buffer.set_text(text)
        '''
        textmark = buffer.get_insert()
        textiter = buffer.get_iter_at_mark(textmark)
        id = textiter.get_line()

        linea_iter = buffer.get_iter_at_line(id)
        GLib.idle_add(
            self.info_widget.scroll_to_iter,
            linea_iter, 0.1, 1, 1, 0.1)
        '''
        return False

    def set_cantidad(self, cantidad):

        valor = "Archivos Restantes: %s" % cantidad
        if self.get_label() != valor:
            self.set_label(valor)


class Menu(Gtk.MenuBar):
    """
    Toolbar Principal.
    """

    __gtype_name__ = 'JAMediaVideoConvertMenu'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    'accion_formato': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        item_Procesar = Gtk.MenuItem('Procesar')
        menu_Procesar = Gtk.Menu()
        item_Procesar.set_submenu(menu_Procesar)
        self.append(item_Procesar)

        item = Gtk.MenuItem('Directorio ...')
        item.connect("activate", self.__emit_accion)
        menu_Procesar.append(item)

        item = Gtk.MenuItem('Archivos ...')
        item.connect("activate", self.__emit_accion)
        menu_Procesar.append(item)

        item_codec = Gtk.MenuItem('Seleccionar Formato')
        menu_codec = Gtk.Menu()
        item_codec.set_submenu(menu_codec)
        self.append(item_codec)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()

        except:
            pass

        hbox = Gtk.HBox()
        button1 = Gtk.RadioButton()
        button1.set_active(True)
        hbox.pack_start(button1, False, False, 0)
        label = Gtk.Label("ogg")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate",
            self.__emit_accion_formato, label.get_text())
        menu_codec.append(item)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()

        except:
            pass
        '''
        hbox = Gtk.HBox()
        button = Gtk.RadioButton()
        button.set_active(False)
        button.join_group(button1)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("avi")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate",
            self.__emit_accion_formato, label.get_text())
        menu_codec.append(item)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()

        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.RadioButton()
        button.set_active(False)
        button.join_group(button1)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("mpeg")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate",
            self.__emit_accion_formato, label.get_text())
        menu_codec.append(item)
        '''
        self.show_all()

    def __emit_accion_formato(self, widget, accion):

        valor = not widget.get_children()[0].get_children()[0].get_active()
        widget.get_children()[0].get_children()[0].set_active(valor)

        self.emit('accion_formato', accion)

    def __emit_accion(self, widget):

        valor = widget.get_label()

        if valor == 'Directorio ...':
            filechooser = FileChooser(
                parent_window=self.get_toplevel(),
                title="Cargar Archivos",
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                #path=path,
                #mime_type=["text/*", "image/svg+xml"]
                )

            filechooser.connect('load', self.__abrir_archivo)

        elif valor == 'Archivos ...':
            filechooser = FileChooser(
                parent_window=self.get_toplevel(),
                title="Cargar Archivos",
                action=Gtk.FileChooserAction.OPEN,
                #path=path,
                mime=["video/*"],
                )

            filechooser.connect('load', self.__abrir_archivo)

    def __abrir_archivo(self, widget, archivos):

        self.emit('load', archivos)


class Widget_extractor(Gtk.Frame):

    __gtype_name__ = 'JAMediaVideoConvertWidget_extractor'

    def __init__(self):

        Gtk.Frame.__init__(self)

        self.set_label("")

        self.visor = Gtk.DrawingArea()
        self.visor.set_size_request(320, 240)
        self.visor.modify_bg(0, Gdk.Color(0, 0, 0))

        self.add(self.visor)

        self.show_all()

    def set_extraccion(self, text):

        if len(text) > 25:
            text = "%s . . ." % text[:25]

        text = "Procesando: %s" % text

        self.set_label(text)

    def reset(self):

        self.set_label("JAMedia Video Convert")
        self.visor.modify_bg(0, Gdk.Color(0, 0, 0))


class FileChooser(Gtk.FileChooserDialog):

    __gtype_name__ = 'JAMediaVideoConvertFileChooser'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self,
        parent_window=None,
        filter_type=[],
        title=None,
        #path=None,
        action=Gtk.FileChooserAction.OPEN,
        mime=[]):

        Gtk.FileChooserDialog.__init__(self,
            parent=parent_window,
            action=action,
            flags=Gtk.DialogFlags.MODAL,
            title=title)

        self.action = action
        self.set_default_size(640, 480)

        #if os.path.isfile(path):
        #    self.set_filename(path)

        #else:
        #    self.set_current_folder_uri("file://%s" % path)

        if self.action == Gtk.FileChooserAction.OPEN:
            self.set_select_multiple(True)

            if filter_type:
                filter = Gtk.FileFilter()
                filter.set_name("Filtro")

                for fil in filter_type:
                    filter.add_pattern(fil)

                self.add_filter(filter)

            elif mime:
                filter = Gtk.FileFilter()
                filter.set_name("Filtro")

                for m in mime:
                    filter.add_mime_type(m)

                self.add_filter(filter)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        abrir = Gtk.Button("Abrir")
        salir = Gtk.Button("Salir")

        hbox.pack_end(salir, True, True, 5)
        hbox.pack_end(abrir, True, True, 5)

        self.set_extra_widget(hbox)

        salir.connect("clicked", self.__salir)
        abrir.connect("clicked", self.__abrir)

        self.show_all()

        #self.connect("file-activated", self.__file_activated)

    #def __file_activated(self, widget):
    #    """
    #    Cuando se hace doble click sobre un archivo.
    #    """

    #    self.__abrir(None)

    def __abrir(self, widget):
        """
        Emite el path del archivo seleccionado.
        """

        files = self.get_filenames()

        if self.action == Gtk.FileChooserAction.SELECT_FOLDER:
            self.emit('load', files)

        elif self.action == Gtk.FileChooserAction.OPEN:
            if not files:
                self.__salir(None)
                return

            archivos = []
            for file in files:
                direccion = str(file).replace("//", "/")

                if os.path.exists(direccion) and os.path.isfile(direccion):
                    archivos.append(direccion)

            self.emit('load', archivos)

        self.__salir()

    def __salir(self, widget=None):

        self.destroy()
