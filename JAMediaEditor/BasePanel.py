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

import gi
from gi.repository import Gtk
from gi.repository import GObject

from InfoNotebook import InfoNotebook
from WorkPanel import WorkPanel

from Widgets import ToolbarProyecto
from Widgets import ToolbarArchivo
from Widgets import ToolbarBusquedas
from Widgets import My_FileChooser
from Widgets import DialogoProyecto
from Widgets import DialogoBuscar

home = os.environ["HOME"]

BatovideWorkSpace = os.path.join(
    home, 'BatovideWorkSpace')

class BasePanel(Gtk.Paned):
    """
    Panel Horizontal:
        Izquierda:
            Estructura de Proyecto e Introspección sobre el mismo.
            
        Derecha:
            Archivos y terminales.
    """
    
    __gtype_name__ = 'BasePanel'

    __gsignals__ = {
     'update': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
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
        toolbarbusquedas = ToolbarBusquedas()

        self.infonotebook_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.infonotebook_box.pack_start(self.toolbarproyecto, False, False, 0)
        self.infonotebook_box.pack_start(self.infonotebook, True, True, 0)
        self.infonotebook_box.pack_end(toolbarbusquedas, False, False, 0)
        
        workpanel_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        workpanel_box.pack_start(self.toolbararchivo, False, False, 0)
        workpanel_box.pack_end(self.workpanel, True, True, 0)

        self.pack1(self.infonotebook_box, resize = False, shrink = False)
        self.pack2(workpanel_box, resize = True, shrink = True)

        self.show_all()
        
        self.infonotebook_box.set_size_request(280, -1)
        
        self.workpanel.connect('new_select', self.__set_introspeccion)
        self.workpanel.connect('update_ejecucion', self.__update_ejecucion)
        self.toolbararchivo.connect('accion', self.set_accion_archivo)
        self.toolbarproyecto.connect('accion', self.set_accion_proyecto)
        toolbarbusquedas.connect("buscar", self.__buscar)
        toolbarbusquedas.connect("accion", self.__buscar_mas)
        self.infonotebook.connect('new_select', self.__set_linea)
        self.infonotebook.connect('open', self.__open_file)
        self.infonotebook.connect('search_on_grep', self.__search_grep)
        self.infonotebook.connect('remove_proyect', self.__remove_proyect)
        
    def __search_grep(self, widget, datos, parent):
        """
        Cuando se hace una busqueda grep en la
        estructura del proyecto y luego se selecciona
        una linea en los resultados de dicha búsqueda.
        
            Se abre el archivo
            Se selecciona y
            Se abre el dialogo buscar.
        """
        
        self.__open_file(None, datos[0])
        
        paginas = self.workpanel.notebook_sourceview.get_n_pages()
        
        for indice in range(paginas):
            sourceview = self.workpanel.notebook_sourceview.get_nth_page(indice).get_child()
            
            visible = sourceview.get_show_line_numbers()
            sourceview.set_show_line_numbers(True)
            
            if sourceview.archivo == datos[0]:
                self.workpanel.notebook_sourceview.set_current_page(indice)
                break
            
        dialogo = DialogoBuscar(sourceview,
            parent_window = parent,
            title = "Buscar Texto", texto = datos[2])

        dialogo.run()
        
        dialogo.destroy()
        
        sourceview.set_show_line_numbers(visible)
        
    def __update_ejecucion(self, widget, valor):
        """
        Actualiza las toolbars según ejecución.
        """
        
        if self.proyecto:
            if valor:
                self.toolbarproyecto.dict_proyecto["Ejecutar Proyecto"].set_sensitive(False)
                self.toolbarproyecto.dict_proyecto["Detener Ejecución"].set_sensitive(True)
                
            else:
                self.toolbarproyecto.dict_proyecto["Ejecutar Proyecto"].set_sensitive(True)
                self.toolbarproyecto.dict_proyecto["Detener Ejecución"].set_sensitive(False)
                
        else:
            self.toolbarproyecto.dict_proyecto["Ejecutar Proyecto"].set_sensitive(False)
            self.toolbarproyecto.dict_proyecto["Detener Ejecución"].set_sensitive(False)
            
        if valor:
            self.toolbararchivo.dict_archivo["Ejecutar Archivo"].set_sensitive(False)
            self.toolbararchivo.dict_archivo["Detener Ejecución"].set_sensitive(True)
        
        else:
            self.toolbararchivo.dict_archivo["Ejecutar Archivo"].set_sensitive(True)
            self.toolbararchivo.dict_archivo["Detener Ejecución"].set_sensitive(False)
        
    def __open_file(self, widget, filepath):
        """
        Cuando se envia "abrir" un archivo desde el
        visor de estructura del proyecto.
        """
        
        self.workpanel.abrir_archivo(filepath)
        
    def __buscar(self, widget, texto):
        """
        Recibe el texto a buscar.
        """

        self.seleccionado_actual = 0
        self.infonotebook.buscar(texto)
        
    def __buscar_mas(self, widget, accion, texto):
        """
        Cuando se hace click en anterior o
        siguiente en la toolbar de busquedas.
        """
       
        self.infonotebook.buscar(texto)
        if self.infonotebook.get_current_page() == 0:
            tree = self.infonotebook.introspeccion
            seleccion = self.infonotebook.introspeccion.get_selection()
            posibles = self.infonotebook.introspeccion.posibles
            
        else:
            tree = self.infonotebook.estructura_proyecto
            seleccion = self.infonotebook.estructura_proyecto.get_selection()
            posibles = self.infonotebook.estructura_proyecto.posibles
        
        if accion == "Siguiente":
            self.seleccionado_actual += 1
            
        else:
            self.seleccionado_actual -= 1
        
        if self.seleccionado_actual > len(posibles) - 1:
            self.seleccionado_actual = 0
            
        elif self.seleccionado_actual < 0:
            self.seleccionado_actual = len(posibles) - 1

        if posibles != []:
            seleccion.select_iter(posibles[self.seleccionado_actual])
            new_path = tree.get_model().get_path(posibles[self.seleccionado_actual])
            tree.scroll_to_cell(new_path)
            
    def set_accion_codigo(self, widget, accion):
        """
        Cuando se hace click en una opción del menú Código.
        """
        
        self.workpanel.set_accion_codigo(accion)
        
    def set_accion_ver(self, widget, accion):
        """
        Cuando se hace click en una opción del menú ver.
        """
        
        if accion == "Panel inferior":
            self.workpanel.set_accion_ver(accion)
            
        elif accion == "Panel Lateral":
            if self.infonotebook_box.get_visible():
                self.infonotebook_box.hide()
                
            else:
                self.infonotebook_box.show()
                
        elif accion == "Numeracion":
            self.workpanel.set_accion_ver(accion)
            
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
            
            filechooser = My_FileChooser(
                parent_window = self.get_toplevel(),
                action_type = Gtk.FileChooserAction.OPEN,
                title = "Abrir Archivo",
                path = path,
                mime_type = ["text/*", "image/svg+xml"])
                
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
        
    def __set_linea(self, widget, texto):
        """
        Recibe la linea seleccionada en instrospeccion y
        y la pasa a workpanel para ser seleccionada en el código.
        """
        
        self.workpanel.set_linea(texto)

    def __set_introspeccion(self, widget, view, estructura):
        """
        Recibe nombre y contenido de archivo para
        realizar introspeccion sobre él.
        """
        
        buffer = view.get_buffer()
        archivo = view.archivo
        nombre = False
        
        if archivo:
            nombre = os.path.basename(archivo)
        
        inicio, fin = buffer.get_bounds()
        
        ### Setear Introspeción.
        self.infonotebook.set_introspeccion(nombre,
            buffer.get_text(inicio, fin, 0))
        
        ### Actualizar sourceview para actualizador de toolbars y menus.
        self.emit("update", view, True)
        
        # FIXME: Causa un bug cuando se abre un proyecto teniendo
        # archivos sin guardar de un proyecto anterior.
        ### Cuando se guarda un archivo.
        #if estructura:
        #    if self.proyecto:
        #        if self.proyecto["path"] in archivo:
        #            self.infonotebook.set_path_estructura(self.proyecto["path"])
        
    def __load(self, proyecto):
        """
        Carga los datos del proyecto en la interfaz
        de la aplicación.
        """
        
        self.proyecto = proyecto
        
        path = proyecto.get("path", False)
        main = proyecto.get("main", False)
        
        self.infonotebook.set_path_estructura(path)
        self.workpanel.abrir_archivo(os.path.join(path, main))

    def __abrir_archivo(self, widget, archivo):
        """
        Abre un archivo.
        """

        if archivo:
            import commands
            datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
            
            if "text" in datos or "x-python" in datos or "x-empty" in datos or "svg+xml" in datos:
                self.workpanel.abrir_archivo(archivo)
                
        else:
            self.workpanel.abrir_archivo(None)
        
    def set_accion_proyecto(self, widget, accion):
        """
        Cuando se hace click en la toolbar de proyecto o
        se manda ejecutar una acción desde el menú.
        """
        
        # FIXME: Cualquier acción en las toolbars o menu,
        # debe detener las ejecuciones en marcha?.

        if accion == "Nuevo Proyecto":
            dialog = DialogoProyecto(
                parent_window = self.get_toplevel(),
                title = "Crear Proyecto Nuevo")
            
            response = dialog.run()
            
            nueveoproyecto = False
            
            if Gtk.ResponseType(response) == Gtk.ResponseType.ACCEPT:
                nueveoproyecto = dialog.get_proyecto()
                
            dialog.destroy()
            
            ### El nuevo Proyecto se crea solo cuando se ha cerrado el anterior.
            if nueveoproyecto:
                anterior_cerrado = True
        
                if self.proyecto:
                    ### No se puede Crear un proyecto con el mismo nombre de uno existente
                    if nueveoproyecto["nombre"] in os.listdir(BatovideWorkSpace): return
                    anterior_cerrado = self.cerrar_proyecto()
        
                if anterior_cerrado:
                    self.proyecto = nueveoproyecto
                    self.__guardar_proyecto()
                    self.__load(self.proyecto)
                
        elif accion == "Editar Proyecto":
            if self.proyecto:
                dialog = DialogoProyecto(
                    parent_window = self.get_toplevel(),
                    title = "Editar Proyecto",
                    accion = "editar")
                    
                dialog.set_proyecto(self.proyecto)
                
                response = dialog.run()
                
                if Gtk.ResponseType(response) == Gtk.ResponseType.ACCEPT:
                    self.proyecto = dialog.get_proyecto()
                    self.__guardar_proyecto()
                    self.__load(self.proyecto)
                    
                dialog.destroy()
                
        elif accion == "Abrir Proyecto":
            filechooser = My_FileChooser(
                parent_window = self.get_toplevel(),
                action_type = Gtk.FileChooserAction.OPEN,
                filter_type = ["*.ide"],
                title = "Abrir proyecto",
                path = BatovideWorkSpace)
                
            filechooser.connect('load', self.__abrir_proyecto)

        elif accion == "Guardar Proyecto":
            self.__guardar_archivos_de_proyecto()
            self.__guardar_proyecto()
        
        elif accion == "Cerrar Proyecto":
            if self.cerrar_proyecto(): self.proyecto = {}
        
        elif accion == "Ejecutar Proyecto":
            if self.proyecto:
                main = os.path.join(self.proyecto["path"], self.proyecto["main"])
                self.workpanel.ejecutar(archivo=main)
            
        elif accion == "Detener Ejecución":
            self.workpanel.detener_ejecucion()
        
        elif accion == "Construir":
            from Widget_Setup import DialogoSetup
            
            dialog = DialogoSetup(
                parent_window = self.get_toplevel(),
                proyecto = self.proyecto)
        
            respuesta = dialog.run()
            
            dialog.destroy()

            if respuesta == Gtk.ResponseType.ACCEPT:
                pass
            
        else:
            print "Acccion sin asignar en BasePanel", accion

    def __abrir_proyecto(self, widget, archivo):
        """
        Abrir archivo de un proyecto.
        """
        
        extension = os.path.splitext(os.path.split(archivo)[1])[1]
        
        if not extension == ".ide": return
        
        import json
        import codecs
        
        pro = codecs.open(archivo, "r", "utf-8")
        proyecto = json.JSONDecoder("utf-8").decode(pro.read())
        
        proyecto["path"] = os.path.dirname(archivo)
        
        ### Validación de datos del proyecto.
        if not proyecto.get("nombre", False): return
        if not proyecto.get("main", False): return
        if not os.path.exists(os.path.join(proyecto["path"], proyecto["main"])): return
        
        anterior_cerrado = True
        
        if self.proyecto:
            if self.proyecto.get("path", False) == proyecto["path"]: return
            anterior_cerrado = self.cerrar_proyecto()
        
        ### El proyecto se carga sólo si se cerró el anterior.
        if anterior_cerrado:
            self.proyecto = {}
            self.__load(proyecto)
            self.__guardar_proyecto() ### Actualizando el path de proyecto.
        
    def __guardar_archivos_de_proyecto(self):
        """
        Guarda todos los archivos del proyecto abierto.
        """
        
        if not self.proyecto: return
    
        codeviews = self.workpanel.get_archivos_de_proyecto(self.proyecto["path"])
        
        for view in codeviews:
            view.guardar()
            
    def __guardar_proyecto(self):
        """
        Guarda el proyecto actual.
        """
        
        ### Todo Proyecto Requiere un Nombre.
        if not self.proyecto.get("nombre", False): return
        
        ### Seteo automático del path del proyecto.
        path = False
        
        if self.proyecto.get("path", False):
            path = self.proyecto["path"]
            
        else:
            path = os.path.join(BatovideWorkSpace, self.proyecto["nombre"])
            
        if not os.path.exists(path):
            os.mkdir(path)
        
        self.proyecto["path"] = path
        
        ### Seteo automático del main del proyecto.
        if not self.proyecto.get("main", False):
            self.proyecto["main"] = "Main.py"
            
        main_path = os.path.join(self.proyecto["path"], self.proyecto["main"])
        
        if not os.path.exists(main_path):
            arch = open(main_path, "w")
            arch.write("#!/usr/bin/env python\n# -*- coding: utf-8 -*-")
            arch.close()
            
        ### Seteo automático de licencia
        licencia_path = os.path.join(self.proyecto["path"], "COPYING")
        import Licencias as Lic
        
        arch = open(licencia_path, "w")
        arch.write(Lic.dict[self.proyecto["licencia"]])
        arch.close()
        
        ### Seteo automático de autores.
        autores_path = os.path.join(self.proyecto["path"], "AUTHORS")
        
        arch = open(autores_path, "w")
        for autor in self.proyecto["autores"]:
            arch.write("%s %s \n" % (autor[0].encode("utf-8"), autor[1].encode("utf-8")))

        arch.close()
        
        ### Guardar el Proyecto.
        proyecto = os.path.join(path, "proyecto.ide")
        
        import simplejson
        
        archivo = open(proyecto, "w")
        archivo.write(
            simplejson.dumps(
                self.proyecto,
                indent=4,
                separators=(", ", ":"),
                sort_keys=True
            )
        )
        archivo.close()
        
    def cerrar_proyecto(self):
        """
        Cierra el proyecto.
        """
        
        if not self.proyecto: return True
        
        codeviews = self.workpanel.get_archivos_de_proyecto(self.proyecto["path"])
        
        ### Cerrar Archivos.
        if codeviews:
            ### Cerrar Archivos. Esto pedirá guardar si hay cambios en él.
            for view in codeviews:
                view.set_accion("Cerrar Archivo")
        
        else:
            self.infonotebook.set_path_estructura(None)
            self.proyecto = {}
            return True
        
        ### Si algun archivo ha debido guardarse, no se ha cerrado.
        codeviews = self.workpanel.get_archivos_de_proyecto(self.proyecto["path"])
        
        if codeviews:
            ### Cerrar Archivos.
            for view in codeviews:
                view.set_accion("Cerrar Archivo")
                
        else:
            self.infonotebook.set_path_estructura(None)
            self.proyecto = {}
            return True
        
        ### Si todavía hay archivos abiertos, el usuario no desea cerrarlos.
        codeviews = self.workpanel.get_archivos_de_proyecto(self.proyecto["path"])
        
        if codeviews:
            return False
        
        else:
            self.infonotebook.set_path_estructura(None)
            self.proyecto = {}
            return True
        
    def __remove_proyect(self, widget):
        """
        Cuando se elimina el proyecto desde la vista de estructura.
        """
    
        self.workpanel.remove_proyect(self.proyecto["path"])
        
        self.infonotebook.set_path_estructura(None)
        self.proyecto = {}
        
        return True
