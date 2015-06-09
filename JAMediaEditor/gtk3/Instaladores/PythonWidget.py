#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PythonWidget.py por:
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
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GdkPixbuf
from Globales import CONFPATH
from Globales import get_guion_lanzador_sh
from Globales import get_guion_desktop
from Globales import get_guion_setup_cfg
from Globales import get_guion_setup_py
from Globales import DialogoLoad
from Globales import DialogoInformar
from ScrollPage import ScrollPage
from WidgetIcon import WidgetIcon
from ApiProyecto import get_installers_data
from Terminal import Terminal

BASEPATH = os.path.dirname(__file__)


class PythonWidget(Gtk.EventBox):

    __gtype_name__ = 'JAMediaEditorPythonWidget'

    def __init__(self, proyecto_path):

        Gtk.EventBox.__init__(self)

        archivo = os.path.join(proyecto_path, "proyecto.ide")
        arch = open(archivo, "r")
        self.proyecto = json.load(arch, "utf-8")
        arch.close()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.install_path = os.path.join(CONFPATH, self.proyecto["nombre"])
        self.widgeticon = WidgetIcon("python", self.install_path)
        self.notebook = Notebook(proyecto_path)
        self.terminal = Terminal()

        label = Gtk.Label(u"Instalador python para: %s versión: %s" % (
            self.proyecto["nombre"], self.proyecto["version"]))
        label.modify_font(Pango.FontDescription("%s %s" % ("Monospace", 12)))
        label.modify_fg(0, Gdk.Color(0, 0, 65000))

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image = Gtk.Image()
        arch = os.path.join(BASEPATH, "Iconos", "gandalftux.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(arch, 100, 100)
        image.set_from_pixbuf(pixbuf)
        hbox.pack_start(image, False, False, 0)
        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox2.pack_start(label, False, False, 0)
        vbox2.pack_start(self.widgeticon, False, False, 0)
        hbox.pack_start(vbox2, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)

        vbox.pack_start(self.notebook, True, True, 0)
        vbox.pack_start(self.terminal, True, True, 5)

        self.add(vbox)
        self.connect("realize", self.__realize)
        self.show_all()

        self.widgeticon.connect("iconpath", self.__set_iconpath)
        self.widgeticon.connect("make", self.__make)

    def __realize(self, widget):
        self.terminal.hide()

    def __make(self, widget):
        t = "Construyendo el Instalador."
        t = "%s\n%s" % (t, "Por favor espera un momento . . .")
        dialogo = DialogoLoad(self.get_toplevel(), t)
        dialogo.connect("running", self.__run_make)
        dialogo.run()

    def __run_make(self, dialogo):
        self.terminal.reset()
        self.notebook.guardar()
        desktop = os.path.join(self.install_path,
            "%s.desktop" % self.proyecto["nombre"])
        lanzador = os.path.join(self.install_path, self.proyecto["nombre"].lower())
        setup = os.path.join(self.install_path, "setup.py")
        for path in [setup, desktop, lanzador]:
            os.chmod(path, 0755)

        python_path = "/usr/bin/python"
        if os.path.exists(os.path.join("/bin", "python")):
            python_path = os.path.join("/bin", "python")
        elif os.path.exists(os.path.join("/usr/bin", "python")):
            python_path = os.path.join("/usr/bin", "python")
        elif os.path.exists(os.path.join("/sbin", "python")):
            python_path = os.path.join("/sbin", "python")
        elif os.path.exists(os.path.join("/usr/local", "python")):
            python_path = os.path.join("/usr/local", "python")

        self.terminal.show_all()
        self.terminal.connect("reset", self.__Informar, dialogo)
        self.terminal.ejecute_script(self.install_path, python_path, setup, "sdist")

    def __Informar(self, terminal, dialogo):
        origen = os.path.join(self.install_path, "dist")
        for f in os.listdir(origen):
            arch = os.path.join(origen, f)
            commands.getoutput('mv %s %s' % (arch, CONFPATH))
            destino = os.path.join(CONFPATH, f)
            os.chmod(destino, 0755)
        if os.path.exists(origen):
            shutil.rmtree(origen)
        dialogo.destroy()
        t = "Proceso Concluido."
        t = "%s\n%s" % (t, "El instalador se encuentra en")
        t = "%s: %s" % (t, CONFPATH)
        # FIXME: Pedir para borrar directorio temporal ?
        dialogo = DialogoInformar(self.get_toplevel(), t)
        dialogo.run()
        dialogo.destroy()
        self.terminal.disconnect_by_func(self.__Informar)

    def __set_iconpath(self, widget, iconpath):
        new = iconpath
        if not self.install_path in iconpath:
            new = os.path.join(self.install_path, os.path.basename(iconpath))
            shutil.copyfile(iconpath, new)
        self.notebook.set_icon(new)


class Notebook(Gtk.Notebook):

    __gtype_name__ = 'JAMediaEditorNotebookInstalador3'

    def __init__(self, proyecto_path):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)

        self.proyecto_path = proyecto_path
        self.proyecto = False

        self.connect("realize", self.__run)
        self.show_all()

    def __run(self, dialog):
        # cargar proyecto
        archivo = os.path.join(self.proyecto_path, "proyecto.ide")
        arch = open(archivo, "r")
        self.proyecto = json.load(arch, "utf-8")
        arch.close()

        # crear estructura
        temppath = os.path.join(CONFPATH, self.proyecto["nombre"])
        if os.path.exists(temppath):
            shutil.rmtree(temppath)

        # copiar proyecto
        commands.getoutput('cp -r \"%s\" \"%s\"' % (
            self.proyecto_path, CONFPATH))
        self.proyecto_path = temppath

        # setup.cfg
        path = os.path.join(temppath, "setup.cfg")
        texto = get_guion_setup_cfg(self.proyecto)
        page = ScrollPage(path, "txt", texto)
        self.append_page(page, Gtk.Label("setup.cfg"))
        self.set_tab_reorderable(page, True)
        page.source.guardar()

        # Lanzador
        path = os.path.join(temppath, self.proyecto["nombre"].lower())
        texto = get_guion_lanzador_sh(self.proyecto)
        page = ScrollPage(path, "sh", texto)
        self.append_page(page, Gtk.Label("Lanzador"))
        self.set_tab_reorderable(page, True)
        page.source.guardar()

        # desktop
        path = os.path.join(temppath, "%s.desktop" % self.proyecto["nombre"])
        texto = get_guion_desktop(self.proyecto, "")
        page = ScrollPage(path, "desktop", texto)
        self.append_page(page, Gtk.Label("Desktop"))
        self.set_tab_reorderable(page, True)
        page.source.guardar()

        # manifest
        path = os.path.join(temppath, "MANIFEST")
        texto = ""
        manifestpage = ScrollPage(path, "txt", texto)
        self.append_page(manifestpage, Gtk.Label("MANIFEST"))
        self.set_tab_reorderable(manifestpage, True)
        manifestpage.source.guardar()

        # setup.py
        path = os.path.join(temppath, "setup.py")
        texto = ""
        setuppage = ScrollPage(path, "python", texto)
        self.append_page(setuppage, Gtk.Label("setup.py"))
        self.set_tab_reorderable(setuppage, True)
        setuppage.source.guardar()

        # Llenar MANIFEST
        manifest_list, data_files = get_installers_data(temppath)
        texto = ""
        for item in manifest_list:
            texto = "%s\n%s" % (item, texto)
        manifestpage.source.get_buffer().set_text(texto)
        manifestpage.source.guardar()

        # Llenar setup.py
        texto = get_guion_setup_py(self.proyecto, data_files)
        setuppage.source.get_buffer().set_text(texto)
        setuppage.source.guardar()

        self.show_all()
        GLib.timeout_add(30, self.__hide)

    def __hide(self):
        self.hide()
        return False

    def set_icon(self, iconpath):
        self.show_all()
        iconpath = "/usr/share/%s%s" % (self.proyecto["nombre"],
            iconpath.split(self.proyecto_path)[-1])
        paginas = len(self.get_children())
        temppath = os.path.join(CONFPATH, self.proyecto["nombre"])

        # desktop
        texto = get_guion_desktop(self.proyecto, iconpath)
        for x in range(paginas):
            label = self.get_tab_label_text(self.get_nth_page(x))
            if label == "Desktop":
                self.get_nth_page(x).get_child().get_buffer().set_text(texto)
                break

        # MANIFEST
        manifest_list, data_files = get_installers_data(temppath)
        texto = ""
        for item in manifest_list:
            texto = "%s\n%s" % (item, texto)
        for x in range(paginas):
            label = self.get_tab_label_text(self.get_nth_page(x))
            if label == "MANIFEST":
                self.get_nth_page(x).get_child().get_buffer().set_text(texto)
                break

        # setup.py
        texto = get_guion_setup_py(self.proyecto, data_files)
        for x in range(paginas):
            label = self.get_tab_label_text(self.get_nth_page(x))
            if label == "setup.py":
                self.get_nth_page(x).get_child().get_buffer().set_text(texto)
                break

    def guardar(self):
        paginas = len(self.get_children())
        for x in range(paginas):
            self.get_nth_page(x).get_child().guardar()
