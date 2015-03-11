#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   SinRoot.py por:
#       Flavio Danesse      <fdanesse@gmail.com>

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
import json
import commands
import shutil
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango

from Globales import CONFPATH
from Globales import get_guion_lanzador_python
from Globales import get_guion_deb_control
from Globales import get_guion_desktop
from Globales import DialogoLoad
from Globales import DialogoInformar
from ScrollPage import ScrollPage
from WidgetIcon import WidgetIcon
from ApiProyecto import get_installers_data


class SinRootWidget(Gtk.EventBox):

    __gtype_name__ = 'JAMediaEditorSinRootWidget'

    def __init__(self, proyecto_path):

        Gtk.EventBox.__init__(self)

        self.proyecto_path = proyecto_path
        archivo = os.path.join(proyecto_path, "proyecto.ide")
        arch = open(archivo, "r")
        self.proyecto = json.load(arch, "utf-8")
        arch.close()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.notebook = Notebook(proyecto_path)
        self.widgeticon = WidgetIcon("sinroot", proyecto_path)

        label = Gtk.Label(u"Instalador sin root para: %s versión: %s" % (
            self.proyecto["nombre"], self.proyecto["version"]))
        label.modify_font(Pango.FontDescription("%s %s" % ("Monospace", 12)))
        label.modify_fg(0, Gdk.Color(0, 0, 65000))
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(self.widgeticon, False, False, 0)
        vbox.pack_start(self.notebook, True, True, 0)

        self.add(vbox)
        self.show_all()

        self.widgeticon.connect("iconpath", self.__set_iconpath)
        self.widgeticon.connect("make", self.__make)

    def __make(self, widget):
        t = "Construyendo el Instalador."
        t = "%s\n%s" % (t, "Por favor espera un momento . . .")
        dialogo = DialogoLoad(self.get_toplevel(), t)
        dialogo.connect("running", self.__run_make)
        dialogo.run()

    def __run_make(self, dialogo):
        '''
        self.notebook.guardar()
        install_path = os.path.join(CONFPATH, self.proyecto["nombre"])
        # Limpiar y establecer permisos de archivos y directorios
        get_installers_data(install_path)
        control = os.path.join(install_path, "DEBIAN", "control")
        desktop = os.path.join(install_path, "usr", "share", "applications",
            "%s.desktop" % self.proyecto["nombre"])
        lanzador = os.path.join(install_path, "usr", "bin",
            self.proyecto["nombre"].lower())
        for path in [control, desktop, lanzador]:
            os.chmod(path, 0755)
        destino = os.path.join(CONFPATH, "%s_%s.deb" % (
            self.proyecto["nombre"],
            self.proyecto["version"].replace(".", "_")))
        print commands.getoutput('dpkg -b %s %s' % (install_path, destino))
        os.chmod(destino, 0755)
        dialogo.destroy()
        '''
        t = "Proceso Concluido."
        t = "%s\n%s" % (t, "El instalador se encuentra en")
        t = "%s: %s" % (t, CONFPATH)
        dialogo = DialogoInformar(self.get_toplevel(), t)
        dialogo.run()
        dialogo.destroy()

    def __set_iconpath(self, widget, iconpath):
        new = iconpath
        if not self.proyecto_path in iconpath:
            install_path = os.path.join(CONFPATH,
                self.proyecto["nombre"])
            new = os.path.join(install_path, "usr", "share",
                self.proyecto["nombre"], os.path.basename(iconpath))
            shutil.copyfile(iconpath, new)
        self.notebook.set_icon(new)


class Notebook(Gtk.Notebook):

    #__gtype_name__ = 'JAMediaEditorNotebookInstalador'

    def __init__(self, proyecto_path):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)

        self.proyecto_path = proyecto_path
        self.proyecto = False
        self.path = False
        self.deb_path = False
        self.usr_path = False

        self.connect("realize", self.__run)
        self.show_all()

    def __run(self, dialog):
        # cargar proyecto
        archivo = os.path.join(self.proyecto_path, "proyecto.ide")
        arch = open(archivo, "r")
        self.proyecto = json.load(arch, "utf-8")
        arch.close()
        '''
        # crear estructura
        self.path = os.path.join(CONFPATH, self.proyecto["nombre"])
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        self.deb_path = os.path.join(self.path, "DEBIAN")
        self.usr_path = os.path.join(self.path, "usr")
        os.mkdir(self.path)
        os.mkdir(self.deb_path)
        os.mkdir(self.usr_path)
        os.mkdir(os.path.join(self.usr_path, "bin"))
        os.mkdir(os.path.join(self.usr_path, "share"))
        os.mkdir(os.path.join(self.usr_path, "share", "applications"))

        # copiar proyecto a os.path.join(self.usr_path, "share")
        commands.getoutput('cp -r \"%s\" \"%s\"' % (self.proyecto_path,
            os.path.join(self.usr_path, "share")))
        # FIXME: bug en shutil al copiar directorios o archivos que
        # poseen ñ en el path: UnicodeDecodeError:
        # 'ascii' codec can't decode byte 0xc3 in position 5:
        # ordinal not in range(128)

        # deb control
        path = os.path.join(self.deb_path, "control")
        texto = get_guion_deb_control(self.proyecto)
        page = ScrollPage(path, "txt", texto)
        self.append_page(page, Gtk.Label("Control"))
        self.set_tab_reorderable(page, True)

        # Lanzador
        path = os.path.join(self.usr_path, "bin",
            self.proyecto["nombre"].lower())
        texto = get_guion_lanzador_python(self.proyecto)
        page = ScrollPage(path, "sh", texto)
        self.append_page(page, Gtk.Label("Lanzador"))
        self.set_tab_reorderable(page, True)

        # desktop
        path = os.path.join(self.usr_path, "share", "applications",
            "%s.desktop" % self.proyecto["nombre"])
        texto = get_guion_desktop(self.proyecto, "")
        page = ScrollPage(path, "desktop", texto)
        self.append_page(page, Gtk.Label("Desktop"))
        self.set_tab_reorderable(page, True)
        '''
        self.show_all()

    def set_icon(self, iconpath):
        texto = get_guion_desktop(self.proyecto, iconpath)
        paginas = len(self.get_children())
        for x in range(paginas):
            label = self.get_tab_label_text(self.get_nth_page(x))
            if label == "Desktop":
                self.get_nth_page(x).get_child().get_buffer().set_text(texto)
                break

    def guardar(self):
        paginas = len(self.get_children())
        for x in range(paginas):
            self.get_nth_page(x).get_child().guardar()