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
import codecs
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
from Widgets import Multiple_FileChooser
from DialogoProyecto import DialogoProyecto
from Widgets import My_FileChooser
from Widget_Setup import DialogoSetup

import Licencias as Lic

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

        self.workpanel = WorkPanel()
        self.infonotebook = InfoNotebook()
        self.seleccionado_actual = 0

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
        # FIXME: Continuar Desarrollo de esta funcionalidad
        text = ""
        _dict = self.infonotebook.introspeccion._dict
        for key in _dict:
            text = "%s\n%s" % (text, _dict[key])
        source = GtkSource.View()
        source.set_insert_spaces_instead_of_tabs(True)
        source.set_tab_width(4)
        source.set_auto_indent(True)
        source.set_highlight_current_line(True)
        source.set_editable(False)
        source.set_border_width(5)
        source.set_buffer(GtkSource.Buffer())
        win = Gtk.Window()
        win.set_transient_for(self.get_toplevel())
        win.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#f0e6aa"))
        win.set_title("Informe de Introspección")
        win.set_border_width(5)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_size_request(400, 400)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(source)
        source.get_buffer().set_text(text)
        win.add(scroll)
        win.show_all()

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
        # Recibe el texto a buscar.
        self.seleccionado_actual = 0
        self.infonotebook.buscar(texto)

    def __buscar_mas(self, widget, accion, texto):
        # Cuando se hace click en anterior o siguiente en toolbar de busquedas.
        self.infonotebook.buscar(texto)
        if self.infonotebook.get_current_page() == 0:
            tree = self.infonotebook.introspeccion
            seleccion = self.infonotebook.introspeccion.get_selection()
            posibles = self.infonotebook.introspeccion.posibles
        else:
            tree = self.infonotebook.estructura_proyecto
            seleccion = self.infonotebook.estructura_proyecto.get_selection()
            posibles = self.infonotebook.estructura_proyecto.posibles

        if accion == "Buscar Siguiente":
            self.seleccionado_actual += 1
        elif accion == "Buscar Anterior":
            self.seleccionado_actual -= 1
        else:
            print "Acción Desconocida:", self.__buscar_mas

        if self.seleccionado_actual > len(posibles) - 1:
            self.seleccionado_actual = 0
        elif self.seleccionado_actual < 0:
            self.seleccionado_actual = len(posibles) - 1

        if posibles:
            seleccion.select_iter(posibles[self.seleccionado_actual])
            new_path = tree.get_model().get_path(
                posibles[self.seleccionado_actual])
            tree.scroll_to_cell(new_path)

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
            codeviews = self.workpanel.get_archivos_de_proyecto(path)
            if codeviews:
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

    def __cargar_proyecto(self, proyecto):
        # Carga los datos del proyecto en la interfaz de la aplicación.
        self.proyecto = proyecto
        path = proyecto.get("path", False)
        main = proyecto.get("main", False)
        self.__abrir_archivo(False, os.path.join(path, main))

    def __abrir_archivo(self, widget, archivo):
        if archivo:
            archivo = os.path.realpath(archivo)
            datos = commands.getoutput('file -ik \"%s\"' % (archivo))
            if "text" in datos or "x-python" in datos or \
                "x-empty" in datos or "svg+xml" in datos or \
                "application/xml" in datos:
                self.workpanel.abrir_archivo(archivo)
            else:
                print "FIXME: Archivo no permitido por el Editor", datos, archivo
        else:
            self.workpanel.abrir_archivo(False)

    def __abrir_proyecto(self, widget, archivo):
        archivo = os.path.realpath(archivo)
        extension = os.path.splitext(os.path.split(archivo)[1])[1]
        if not extension == ".ide":
            return

        pro = codecs.open(archivo, "r", "utf-8")
        proyecto = json.JSONDecoder("utf-8").decode(pro.read())
        proyecto["path"] = os.path.dirname(archivo)

        # Validación de datos del proyecto.
        if not proyecto.get("nombre", False):
            return
        if not proyecto.get("main", False):
            return
        if not os.path.exists(os.path.join(
            proyecto["path"], proyecto["main"])):
                return

        anterior_cerrado = self.cerrar_proyecto()
        # El proyecto se carga sólo si se cerró el anterior.
        if anterior_cerrado:
            self.__cargar_proyecto(proyecto)

    def __guardar_archivos_de_proyecto(self):
        # Guarda todos los archivos del proyecto abierto.
        if not self.proyecto:
            return
        codeviews = self.workpanel.get_archivos_de_proyecto(
            self.proyecto["path"])
        for view in codeviews:
            view.guardar()

    def __guardar_proyecto(self, proyecto):
        # Guarda el proyecto actual.
        # Todo Proyecto Requiere un Nombre.
        if not proyecto.get("nombre", False):
            return

        # Seteo automático del path del proyecto.
        path = proyecto.get("path", False)
        if not path:
            path = os.path.join(BatovideWorkSpace, proyecto["nombre"])
        if not os.path.exists(path):
            os.mkdir(path)

        proyecto["path"] = path
        # Seteo automático del main del proyecto.
        if not proyecto.get("main", False):
            proyecto["main"] = "Main.py"

        main_path = os.path.join(proyecto["path"], proyecto["main"])
        if not os.path.exists(main_path):
            arch = open(main_path, "w")
            arch.write("#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n")
            arch.close()

        # Seteo automático de licencia
        licencia_path = os.path.join(proyecto["path"], "COPYING")
        arch = open(licencia_path, "w")
        arch.write(Lic.dict[proyecto["licencia"]])
        arch.close()

        # Seteo automático de autores.
        autores_path = os.path.join(proyecto["path"], "AUTHORS")
        arch = open(autores_path, "w")
        try:
            for autor in proyecto["autores"]:
                arch.write(u"%s %s\n" % (autor[0], autor[1]))
        except:
            print "FIXME: UnicodeEncodeError: 'ascii' codec can't encode"
            print "character u'\xed' in position 13: ordinal not in range(128)"
        arch.close()
        # Guardar el Proyecto.
        proyecto_file = os.path.join(path, "proyecto.ide")
        archivo = open(proyecto_file, "w")
        archivo.write(json.dumps(proyecto, indent=4,
            separators=(", ", ":"), sort_keys=True))
        archivo.close()

    def __remove_proyect(self, widget):
        # Cuando se elimina el proyecto desde la vista de estructura.
        self.workpanel.remove_proyect(self.proyecto["path"])
        self.infonotebook.set_path_estructura(False)
        self.proyecto = {}
        return True

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
        if accion == "Nuevo Proyecto":
            dialog = DialogoProyecto(parent_window=self.get_toplevel(),
                title="Crear Nuevo Proyecto")
            response = dialog.run()
            nuevoproyecto = False
            if Gtk.ResponseType(response) == Gtk.ResponseType.ACCEPT:
                nuevoproyecto = dialog.get_proyecto()
            dialog.destroy()
            # El Proyecto se crea solo cuando se ha cerrado el anterior.
            if nuevoproyecto:
                if nuevoproyecto["nombre"] in os.listdir(BatovideWorkSpace):
                    print "FIXME: Ya existe un Proyecto con este Nombre"
                    return
                anterior_cerrado = self.cerrar_proyecto()
                if anterior_cerrado:
                    self.__guardar_proyecto(nuevoproyecto)
                    self.__abrir_proyecto(None,
                        os.path.join(nuevoproyecto["path"], "proyecto.ide"))
        elif accion == "Editar Proyecto":
            if self.proyecto:
                dialog = DialogoProyecto(parent_window=self.get_toplevel(),
                    title="Editar Proyecto", accion="editar")
                dialog.set_proyecto(self.proyecto)
                response = dialog.run()
                if Gtk.ResponseType(response) == Gtk.ResponseType.ACCEPT:
                    nuevoproyecto = dialog.get_proyecto()
                    self.__guardar_proyecto(nuevoproyecto)
                    self.__abrir_proyecto(None,
                        os.path.join(nuevoproyecto["path"], "proyecto.ide"))
                dialog.destroy()
        elif accion == "Abrir Proyecto":
            filechooser = My_FileChooser(parent_window=self.get_toplevel(),
                action_type=Gtk.FileChooserAction.OPEN, filter_type=["*.ide"],
                title="Abrir proyecto", path=BatovideWorkSpace)
            filechooser.connect('load', self.__abrir_proyecto)
        elif accion == "Guardar Proyecto":
            self.__guardar_archivos_de_proyecto()
            self.__guardar_proyecto(self.proyecto)
        elif accion == "Cerrar Proyecto":
            if self.cerrar_proyecto():
                self.proyecto = {}
        elif accion == "Ejecutar Proyecto":
            if self.proyecto:
                main = os.path.join(self.proyecto["path"],
                    self.proyecto["main"])
                self.workpanel.ejecutar(archivo=main)
        elif accion == "Detener Ejecución":
            self.workpanel.detener_ejecucion()
        elif accion == "Construir":
            self.get_toplevel().set_sensitive(False)
            dialog = DialogoSetup(parent_window=self.get_toplevel(),
                proyecto=self.proyecto)
            dialog.run()
            dialog.destroy()
            self.get_toplevel().set_sensitive(True)
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
