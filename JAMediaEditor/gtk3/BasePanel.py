#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BasePanel.py por:
#       Cristian García     <cristian99garcia@gmail.com>
#       Ignacio Rodriguez   <nachoel01@gmail.com>
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

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import GtkSource
from gi.repository import Gdk

from InfoNotebook import InfoNotebook
from WorkPanel import WorkPanel
from Toolbars import ToolbarProyecto
from Toolbars import ToolbarArchivo
from JAMediaPyGiHack.Widgets import ToolbarBusquedas
from JAMediaPyGiHack.InformeWidget import InformeWidget
from Widgets1 import Multiple_FileChooser
from DialogoProyecto import DialogoProyecto
from Widgets1 import My_FileChooser
from Widget_Setup import DialogoSetup

home = os.environ["HOME"]
BatovideWorkSpace = os.path.join(home, 'BatovideWorkSpace')


class BasePanel(Gtk.Paned):

    __gtype_name__ = 'JAMediaEditorBasePanel'

    __gsignals__ = {
    'update': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
    'proyecto_abierto': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,)),
    'ejecucion': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN))}

    def __init__(self):

        Gtk.Paned.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.set_border_width(5)
        self.proyecto = {}
        self.dialogo_proyecto = False
        self.informewidget = False

        self.workpanel = WorkPanel()
        self.infonotebook = InfoNotebook()

        self.toolbarproyecto = ToolbarProyecto()
        self.toolbararchivo = ToolbarArchivo()
        self.toolbarbusquedas = ToolbarBusquedas()

        self.infonotebook_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.infonotebook_box.pack_start(self.toolbarproyecto, False, False, 0)
        self.infonotebook_box.pack_start(self.infonotebook, True, True, 0)
        self.infonotebook_box.pack_end(self.toolbarbusquedas, False, False, 0)

        workpanel_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        workpanel_box.pack_start(self.toolbararchivo, False, False, 0)
        workpanel_box.pack_end(self.workpanel, True, True, 0)

        self.pack1(self.infonotebook_box, resize=False, shrink=False)
        self.pack2(workpanel_box, resize=True, shrink=True)

        self.show_all()
        self.infonotebook_box.set_size_request(280, -1)

        self.workpanel.connect('new_select', self.__set_introspeccion)
        self.workpanel.connect('ejecucion', self.__re_emit_ejecucion)
        self.workpanel.connect('update', self.__re_emit_update)

        self.toolbararchivo.connect('accion', self.set_accion_archivo)
        self.toolbarproyecto.connect('accion', self.set_accion_proyecto)

        self.toolbarbusquedas.connect("buscar", self.__buscar)
        self.toolbarbusquedas.connect("accion", self.__buscar_mas)
        self.toolbarbusquedas.connect("informe", self.__informar)

        self.infonotebook.connect('new_select', self.__set_linea)
        self.infonotebook.connect('open', self.__abrir_archivo)
        self.infonotebook.connect('search_on_grep', self.__search_grep)
        self.infonotebook.connect('remove_proyect', self.__remove_proyect)

    def __informar(self, widget):
        """
        Abre nueva lengueta en Workpanel con la información de Introspección
        del archivo seleccionado.
        """
        if self.informewidget:
            self.informewidget.destroy()
        self.informewidget = InformeWidget(self.get_toplevel())
        text = self.infonotebook.get_estructura()
        self.informewidget.setting(text)

    def __re_emit_update(self, widget, _dict):
        # Emite una señal con el estado general del archivo.
        self.emit("update", _dict)

    def __search_grep(self, widget, datos, parent):
        """
        Cuando se hace una busqueda grep en la estructura del proyecto y luego
        se selecciona una linea en los resultados de dicha búsqueda.
            Se abre el archivo
            Se selecciona y
            Se abre el dialogo buscar.
        """
        print "FIXME:", self.__search_grep
        '''
        self.__abrir_archivo(None, datos[0])

        paginas = self.workpanel.notebook_sourceview.get_n_pages()
        for indice in range(paginas):
            sourceview = self.workpanel.notebook_sourceview.get_nth_page(
                indice).get_child()

            visible = sourceview.get_show_line_numbers()
            sourceview.set_show_line_numbers(True)

            if sourceview.archivo == datos[0]:
                self.workpanel.notebook_sourceview.set_current_page(indice)
                break

        from Widgets import DialogoBuscar

        dialogo = DialogoBuscar(sourceview, parent_window=parent,
            title="Buscar Texto", texto=datos[2])

        dialogo.run()
        dialogo.destroy()
        sourceview.set_show_line_numbers(visible)
        '''

    def __buscar(self, widget, texto):
        self.infonotebook.buscar(texto)

    def __buscar_mas(self, widget, accion, texto):
        self.infonotebook.buscar_mas(accion, texto)

    def __set_linea(self, widget, index, texto):
        """
        Recibe la linea seleccionada en instrospeccion y
        y la pasa a workpanel para ser seleccionada en el código.
        """
        self.workpanel.set_linea(index, texto)

    def __re_emit_ejecucion(self, widget, tipo, valor):
        # Cuando se ejecutan o detienen archivos en terminales.
        self.emit("ejecucion", tipo, valor)

    def __set_introspeccion(self, widget, view, tipo):
        """
        Cuando se selecciona una lengüeta en el Notebook:
            Recibe nombre y contenido de archivo para realizar
            introspeccion sobre él.
        """
        nombre = "Introspección"
        text = ''
        if view:
            _buffer = view.get_buffer()
            archivo = view.archivo
            if archivo:
                nombre = os.path.basename(archivo)
            inicio, fin = _buffer.get_bounds()
            text = _buffer.get_text(inicio, fin, 0)
        # Setear Introspeción.
        self.infonotebook.set_introspeccion(nombre, text, view, tipo)
        self.toolbarbusquedas.activar(bool(text))
        GLib.idle_add(self.__set_estructura, view, tipo)

    def __set_estructura(self, view, tipo):
        # FIXME: Verifica si hay archivos de proyecto y si los hay, actualiza
        # la vista de estructura. Otro punto de vista sería actualizar según
        # que archivo se ha seleccionado, en este caso, la vista de proyecto
        # solo sería activa si el archivo seleccionado está en el proyecto.
        path = self.proyecto.get("path", False)
        if path:
            if self.workpanel.get_archivos_de_proyecto(path):
                self.infonotebook.set_path_estructura(path)
                self.emit("proyecto_abierto", True)
            else:
                self.proyecto = {}
                self.emit("proyecto_abierto", False)
                self.infonotebook.set_path_estructura(False)
        else:
            self.proyecto = {}
            self.emit("proyecto_abierto", False)
            self.infonotebook.set_path_estructura(False)

    def __abrir_archivo(self, widget, archivo):
        if archivo:
            archivo = os.path.realpath(archivo)
            datos = commands.getoutput('file -ik \"%s\"' % (archivo))
            if "text" in datos or "x-python" in datos or \
                "x-empty" in datos or "svg+xml" in datos or \
                "application/xml" in datos:
                self.workpanel.abrir_archivo(archivo)
            else:
                print "FIXME: No se pudo abrir:", archivo, datos
        else:
            self.workpanel.abrir_archivo(False)

    def __abrir_proyecto(self, widget, archivo):
        archivo = os.path.realpath(archivo)
        extension = os.path.splitext(os.path.split(archivo)[1])[1]
        if not extension == ".ide":
            return

        arch = open(archivo, "r")
        proyecto = json.load(arch, "utf-8")
        arch.close()
        proyecto["path"] = os.path.dirname(archivo)

        # Validación de datos del proyecto.
        if not proyecto.get("nombre", False):
            return
        if not proyecto.get("main", False):
            proyecto["main"] = "main.py"

        main_path = os.path.join(proyecto["path"], proyecto["main"])
        if not os.path.exists(main_path):
            arch = open(main_path, "w")
            arch.write("#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n")
            arch.close()

        if self.cerrar_proyecto():
            self.proyecto = proyecto
            self.__abrir_archivo(False, main_path)

    def __guardar_archivos_de_proyecto(self):
        if not self.proyecto:
            return
        codeviews = self.workpanel.get_archivos_de_proyecto(
            self.proyecto["path"])
        for view in codeviews:
            view.guardar()

    def __remove_proyect(self, widget):
        # Cuando se elimina el proyecto desde la vista de estructura.
        pass
        #self.workpanel.remove_proyect(self.proyecto["path"])
        #self.infonotebook.set_path_estructura(False)
        #self.proyecto = {}
        #return True

    def __dialogo_proyecto_run(self, title="Nuevo Proyecto", path=""):
        if self.dialogo_proyecto:
            self.dialogo_proyecto.destroy()
        self.dialogo_proyecto = DialogoProyecto(
            parent_window=self.get_toplevel())
        self.dialogo_proyecto.connect("load", self.__abrir_proyecto)
        self.dialogo_proyecto.setting(title, path)

    def cerrar_proyecto(self):
        if not self.proyecto:
            self.proyecto = {}
            self.infonotebook.set_path_estructura(False)
            return True
        codeviews = self.workpanel.get_archivos_de_proyecto(
            self.proyecto.get("path", ""))
        if codeviews:
            # Cerrar Archivos. Esto pedirá guardar si hay cambios en él.
            for view in codeviews:
                view.set_accion("Cerrar Archivo")
        else:
            self.proyecto = {}
            self.infonotebook.set_path_estructura(False)
            return True
        # Si algún archivo ha debido guardarse, no se ha cerrado.
        if not self.proyecto:
            self.proyecto = {}
            self.infonotebook.set_path_estructura(False)
            return True
        codeviews = self.workpanel.get_archivos_de_proyecto(
            self.proyecto.get("path", ""))
        if codeviews:
            # Cerrar Archivos.
            for view in codeviews:
                view.set_accion("Cerrar Archivo")
        else:
            self.proyecto = {}
            self.infonotebook.set_path_estructura(False)
            return True
        # Si todavía hay archivos abiertos, el usuario no desea cerrarlos.
        if not self.proyecto:
            self.proyecto = {}
            self.infonotebook.set_path_estructura(False)
            return True
        codeviews = self.workpanel.get_archivos_de_proyecto(
            self.proyecto.get("path", ""))
        if codeviews:
            return False
        else:
            self.proyecto = {}
            self.infonotebook.set_path_estructura(False)
            return True

    def set_accion_proyecto(self, widget, accion):
        """
        Cuando se hace click en la toolbar de proyecto o
        se manda ejecutar una acción desde el menú.
        """
        if self.dialogo_proyecto:
            self.dialogo_proyecto.hide()
        if accion == "Nuevo Proyecto":
            if self.cerrar_proyecto():
                self.__dialogo_proyecto_run("Nuevo Proyecto")
        elif accion == "Editar Proyecto":
            if self.proyecto:
                self.__dialogo_proyecto_run("Editar Proyecto",
                    self.proyecto["path"])
        elif accion == "Abrir Proyecto":
            filechooser = My_FileChooser(parent_window=self.get_toplevel(),
                action_type=Gtk.FileChooserAction.OPEN, filter_type=["*.ide"],
                title="Abrir proyecto", path=BatovideWorkSpace)
            filechooser.connect('load', self.__abrir_proyecto)
        elif accion == "Guardar Proyecto":
            self.__guardar_archivos_de_proyecto()
        elif accion == "Cerrar Proyecto":
            self.cerrar_proyecto()
        elif accion == "Ejecutar Proyecto":
            if self.proyecto:
                main = os.path.join(self.proyecto["path"],
                    self.proyecto["main"])
                self.workpanel.ejecutar(archivo=main)
        elif accion == "Detener Ejecución":
            self.workpanel.detener_ejecucion()
        #elif accion == "Construir":
        #    self.get_toplevel().set_sensitive(False)
        #    dialog = DialogoSetup(parent_window=self.get_toplevel(),
        #        proyecto=self.proyecto)
        #    dialog.run()
        #    dialog.destroy()
        #    self.get_toplevel().set_sensitive(True)
        else:
            print "Acccion sin asignar en BasePanel", accion

    def set_accion_codigo(self, widget, accion):
        # Cuando se hace click en una opción del menú Código.
        self.workpanel.set_accion_codigo(accion)

    def set_accion_ver(self, widget, accion, valor):
        # Cuando se hace click en una opción del menú ver.
        if accion == "Panel lateral":
            if not valor:
                self.infonotebook_box.hide()
            else:
                self.infonotebook_box.show()
        elif accion == "Numeracion" or accion == "Panel inferior":
            self.workpanel.set_accion_ver(accion, valor)

    def set_accion_archivo(self, widget, accion):
        """
        Cuando se hace click en la toolbar de archivos o
        se manda ejecutar una acción desde el menú.
        """
        if accion == "Nuevo Archivo":
            self.__abrir_archivo(None, None)
        elif accion == "Abrir Archivo":
            path = self.workpanel.get_default_path()
            if not path:
                path = BatovideWorkSpace
                if self.proyecto:
                    path = self.proyecto["path"]
            filechooser = Multiple_FileChooser(
                parent_window=self.get_toplevel(), title="Abrir Archivo",
                path=path, mime_type=["text/*", "image/svg+xml"])
            filechooser.connect('load', self.__abrir_archivo)
        elif accion == "Guardar Archivo":
            self.workpanel.guardar_archivo()
        elif accion == "Guardar Como":
            self.workpanel.guardar_archivo_como()
        elif accion in ["Deshacer", "Rehacer", "Copiar",
            "Cortar", "Pegar", "Seleccionar Todo", "Cerrar Archivo",
            "Buscar Texto", "Remplazar Texto"]:
            self.workpanel.set_accion_archivos(accion)
        elif accion == "Ejecutar Archivo":
            self.workpanel.ejecutar()
        elif accion == "Detener Ejecución":
            self.workpanel.detener_ejecucion()
        else:
            print "Accion sin asignar en BasePanel", accion

    def external_open_proyect(self, ide_file):
        # Cuando se abre el editor con archivo como parámetro.
        self.__abrir_proyecto(None, ide_file)

    def external_open_file(self, archivo):
        # Cuando se abre el editor con archivo como parámetro.
        self.__abrir_archivo(None, archivo)
