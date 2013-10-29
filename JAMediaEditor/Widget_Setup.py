#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widget_Setup.py por:
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
import commands
import shutil

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GtkSource
from gi.repository import GLib

BASEPATH = os.path.dirname(__file__)

def get_boton(stock, tooltip):
    """
    Devuelve un botón generico.
    """

    boton = Gtk.ToolButton.new_from_stock(stock)
    boton.set_tooltip_text(tooltip)
    boton.TOOLTIP = tooltip
    
    return boton
    
def get_separador(draw = False, ancho = 0, expand = False):
    """
    Devuelve un separador generico.
    """
    
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    
    return separador

HELP_TEXT = """
Guía para Realizar Modificaciones en Archivos Instaladores:
    
    Archivos Instaladores para gnome:
        
        setup.cfg:
            Establece donde se instalará tu aplicación.
            No es necesario que hagas modificaciones en
            este archivo a menos que comprendas bien como
            funciona el instalador.
            
        *.desktop:
            Es el lanzador de tu aplicación que aparecerá
            en el escritorio y menú de tu sistema.
            
            Por defecto, este instalador te deja 3 campos libres
            que debes llenar tu si es que deseas hacerlo,
            si no lo haces, el instalador de todas formas
            funcionará correctamente.
            
            Los campos libres son:
                Comment:
                    Para ingresar una descripción de tu aplicación.
                    
                MimeType:
                    Determina que formatos de archivos puede leer tu aplicación.
                    Esto permite que puedas abrir archivos desde el explorador
                    de archivos de tu sistema.
                    
                Categories:
                    Para ingresar la categoría en el menú de tu escritorio
                    en la cual deseas que aparezca el lanzador, por ejemplo:
                        GTK;GNOME;AudioVideo;Player;Video;
            
        MANIFEST:
            Contiene la lista completa de archivos a distribuir en tu instalador
            No debieras tocarlo a menos que comprendas como funciona el instalador.
            
        setup.py:
            Contiene el guión python de instalación.
            No debieras tocarlo a menos que comprendas el
            funcionamiento del instalador.
            
            Pero puede serte muy útil para agregar sentencias.
            Por ejemplo para decirle al instalador que instale otras
            bibliotecas de código que sean necesarias para que tu
            aplicación funcione.
            
        lanzador:
            sentencia bash que lanzará tu aplicación cuando el usuario la ejecute
            desde terminal o desde el escritorio de su sistema.
            
            No se necesario que modifiques este archivo a menos que comprendas
            como funciona el instalador.
            
        desinstalador:
            Guión python para facilitar la desinstalación de tu aplicación.
            No se necesario que modifiques este archivo a menos que comprendas
            como funciona el instalador.
            
    Archivos Instaladores para gnome ceibal:
        install.py:
            Guión instalador para sistemas donde no tienes acceso al root.
            
            Este archivo simplemente creará un directorio con el nombre de tu
            aplicación en el home de tu sistema y copiará tu aplicación allí.
            
            Luego creará un archivo desktop para ella y lo agregará en el menú
            del sistema donde sea instalada la aplicación.
            
            No es necesario que modifiques nada en este archivo a menos que
            comprendas bien como funciona el instalador, salvo en la parte
            donde se genera el archivo desktop. Allí debieras modificar:
                
                Categories=GTK;GNOME;Juegos;
                    Por la categoría del menú del sistema donde quieras que
                    aparezca el lanzador de tu aplicación.
                    
                También puedes agregar los campos Comment y MimeType para
                definir los datos deseados como se explica en la descripción
                del archivo desktop del instalador para gnome.
            
    Archivos Instaladores para sugar:
        activity.info:
            Determina el nombre y versión de la aplicación y cual es el
            archivo y clase que debe iniciarse cuando el usuario ejecute
            tu aplicación.
            
            Para aclarar el funcionamiento de este archivo, a continuación se
            describen los campos más importantes del mismo:
                
                bundle_id:
                    Esto establece el nombre único de la aplicación.
                    En sugar no pueden haber dos aplicaciones con el mismo nombre.
                    
                exec:
                    Esto establece cual es el archivo y la clase en tu proyecto
                    que deben ejecutarse cuando el usuario lance la aplicación.
                    
            Ninguno de estos campos debieras modificarlos a menos que comprendas
            bien el funcionamiento del instalador.
            
            Otros campos que quedan libres para que tu llenes como desees son:
                mime_types y summary.
                
            Esos campos deben contener lo mismo que contienen los campos
            MimeType y Comment en los instaldores anteriores (gnome y gnome ceibal).
"""

class DialogoSetup(Gtk.Dialog):
    """
    Dialogo para presentar Información de Instaladores.
    """
    
    __gtype_name__ = 'DialogoSetup'
    
    def __init__(self, parent_window = None, proyecto = None):

        Gtk.Dialog.__init__(self,
            title = "Generador de Instaladores",
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = ["Cerrar", Gtk.ResponseType.ACCEPT])
        
        self.set_size_request(640, 480)
        self.set_border_width(15)
        
        self.notebook = Notebook_Setup(proyecto)
        
        help = Gtk.TextView()
        help.set_editable(False)
        help.set_border_width(15)
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add(help)
        
        help.get_buffer().set_text(HELP_TEXT)
    
        hpaned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        
        hpaned.pack1(self.notebook,
            resize = False, shrink = False)
        hpaned.pack2(scroll,
            resize = False, shrink = True)
            
        self.vbox.pack_start(hpaned, True, True, 0)
        
        self.vbox.show_all()
        self.maximize()
        
        self.connect("realize", self.__reescalar, scroll)
        
    def __reescalar(self, widget, scroll):
        
        rect = self.get_allocation()
        scroll.set_size_request(rect.width/3, -1)
        
class Notebook_Setup(Gtk.Notebook):
    """
    Contenedor de Información de Instaladores gnome y sugar.
    """
    
    __gtype_name__ = 'Notebook_Setup'
    
    def __init__(self, proyecto):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)
        
        self.proyecto = proyecto
        
        self.gnome_notebook = Gnome_Notebook(proyecto)
        self.ceibal_notebook = Ceibal_Notebook(proyecto)
        self.sugar_notebook = Sugar_Notebook(proyecto)
        
        box = Gtk.VBox()
        
        gnome_widget_icon = Widget_icon(tipo = "gnome", proyecto = proyecto)
        
        box.pack_start(gnome_widget_icon, False, False, 0)
        box.pack_start(self.gnome_notebook, True, True, 0)
        
        self.append_page(box, Gtk.Label("Proyecto Gnome"))
        
        box = Gtk.VBox()
        
        ceibal_widget_icon = Widget_icon(tipo = "ceibal", proyecto = proyecto)
        
        box.pack_start(ceibal_widget_icon, False, False, 0)
        box.pack_start(self.ceibal_notebook, True, True, 0)
        
        self.append_page(box, Gtk.Label("Proyecto Gnome Ceibal"))
        
        box = Gtk.VBox()
        
        sugar_widget_icon = Widget_icon(tipo = "sugar", proyecto = proyecto)
        
        box.pack_start(sugar_widget_icon, False, False, 0)
        box.pack_start(self.sugar_notebook, True, True, 0)
        
        self.append_page(box, Gtk.Label("Proyecto Sugar"))
        
        self.show_all()
        
        gnome_widget_icon.connect("iconpath", self.__set_icon, "gnome")
        ceibal_widget_icon.connect("iconpath", self.__set_icon, "ceibal")
        sugar_widget_icon.connect("iconpath", self.__set_icon, "sugar")
        
        gnome_widget_icon.connect("make", self.__make, "gnome")
        ceibal_widget_icon.connect("make", self.__make, "ceibal")
        sugar_widget_icon.connect("make", self.__make, "sugar")
        
        self.connect('switch_page', self.__switch_page)
        
    def __switch_page(self, widget, widget_child, indice):
        """
        Cuando el usuario selecciona una lengüeta,
        Reconstruye el instalador.
        """
        
        ### Detener inspectores y activar solo el seleccionado
        paginas = self.get_children()
        
        notebook = widget_child.get_children()[1]
        if notebook.iconpath:
            notebook.setup_install(notebook.iconpath)
            
    def __make(self, widget, tipo):
        """
        Construye los instaladores.
        """
        
        if tipo == "gnome":
            self.gnome_notebook.make()
            
            dialog = DialogoInstall(
                parent_window = self.get_toplevel(),
                dirpath = self.gnome_notebook.activitydirpath,
                destino_path = self.proyecto["path"])
        
            respuesta = dialog.run()
            
            dialog.destroy()
            
            ### Mover Instalador
            dist_path = os.path.join(self.gnome_notebook.activitydirpath, "dist")
            destino = os.path.join(self.proyecto["path"], "dist")
            
            if not os.path.exists(destino):
                os.mkdir(destino)
                
            for archivo in os.listdir(dist_path):
                path = os.path.join(dist_path, archivo)
                commands.getoutput("cp %s %s" % (path, destino))
            
        elif tipo == "sugar":
            self.sugar_notebook.make()
            
            dialog = DialogoInfoInstall(
                parent_window = self.get_toplevel(),
                distpath = os.path.join(self.proyecto["path"], "dist"))
    
            respuesta = dialog.run()
        
            dialog.destroy()
            
        elif tipo == "ceibal":
            self.ceibal_notebook.make()
            
            dialog = DialogoInfoInstall(
                parent_window = self.get_toplevel(),
                distpath = os.path.join(self.proyecto["path"], "dist"))
        
            respuesta = dialog.run()
            
            dialog.destroy()
        
    def __set_icon(self, widget, iconpath, valor):
        """
        Setea el icono de la aplicación.
        """
        
        if valor == "gnome":
            self.gnome_notebook.setup_install(iconpath)

        elif valor == "sugar":
            self.sugar_notebook.setup_install(iconpath)
            
        elif valor == "ceibal":
            self.ceibal_notebook.setup_install(iconpath)
        
class Gnome_Notebook(Gtk.Notebook):
    """
    Contenedor de información de instalador gnome.
    """
    
    __gtype_name__ = 'Gnome_Notebook'
    
    def __init__(self, proyecto):

        Gtk.Notebook.__init__(self)
        
        self.set_scrollable(True)
        
        self.proyecto = proyecto
        self.iconpath = False
        
        self.setupcfg = Setup_SourceView()
        self.setupcfg.get_buffer().set_text("")
        
        self.append_page(
            self.get_scroll(self.setupcfg),
            Gtk.Label("setup.cfg"))
            
        self.setupdesktop = Setup_SourceView()
        self.setupdesktop.get_buffer().set_text("")
        
        self.append_page(
            self.get_scroll(self.setupdesktop),
            Gtk.Label("%s.desktop" % self.proyecto["nombre"]))
            
        self.setupmanifest = Setup_SourceView()
        self.setupmanifest.get_buffer().set_text("")
        
        self.append_page(
            self.get_scroll(self.setupmanifest),
            Gtk.Label("MANIFEST"))
        
        self.setuppy = Setup_SourceView()
        self.setuppy.get_buffer().set_text("")
        
        self.append_page(
            self.get_scroll(self.setuppy),
            Gtk.Label("setup.py"))
        
        self.lanzador = Setup_SourceView()
        self.lanzador.get_buffer().set_text("")
        
        self.append_page(
            self.get_scroll(self.lanzador),
            Gtk.Label("lanzador"))
            
        self.desinstalador = Setup_SourceView()
        self.desinstalador.get_buffer().set_text("")
        
        self.append_page(
            self.get_scroll(self.desinstalador),
            Gtk.Label("desinstalador"))
        
        ### Comenzar a generar el temporal
        self.activitydirpath = os.path.join("/tmp", "%s" % self.proyecto["nombre"])
        
        self.show_all()
        
    def setup_install(self, iconpath):
        """
        Recolecta la información necesaria para generar los
        archivos de instalación y los presenta al usuario para
        posibles correcciones.
        """
        
        ### Borrar anteriores
        if os.path.exists(self.activitydirpath):
            commands.getoutput("rm -r %s" % self.activitydirpath)
            
        ### Copiar contenido del proyecto.
        shutil.copytree(self.proyecto["path"], self.activitydirpath, symlinks=False, ignore=None)
        
        ### Generar Archivos Necesarios para Construir Instalador.
        self.archivo_lanzador = "%s/%s_run" % (self.activitydirpath, self.proyecto["nombre"].lower())
        self.archivo_desinstalador = "%s/%s_uninstall" % (self.activitydirpath, self.proyecto["nombre"].lower())
        self.archivo_setup_py = "%s/setup.py" % (self.activitydirpath)
        self.archivo_setup_cfg = "%s/setup.cfg" % (self.activitydirpath)
        self.archivo_manifest = "%s/MANIFEST" % (self.activitydirpath)
        self.archivo_desktop = "%s/%s.desktop" % (self.activitydirpath, self.proyecto["nombre"])
        
        lista = [
            self.archivo_lanzador,
            self.archivo_desinstalador,
            self.archivo_setup_py,
            self.archivo_setup_cfg,
            self.archivo_manifest,
            self.archivo_desktop]
            
        for archivo in lista:
            if not os.path.exists(archivo):
                arch = open(archivo, "w")
                arch.write("")
                arch.close()
        
        self.iconpath = iconpath
        
        if not self.proyecto["path"] in iconpath:
            newpath = os.path.join(self.activitydirpath, os.path.basename(iconpath))
            shutil.copyfile(iconpath, newpath)
            iconpath = newpath
        
        else:
            newpath = iconpath.split("%s/" % self.proyecto["path"])[1]
            iconpath = os.path.join(self.activitydirpath, newpath)
            
        newpath = iconpath.split("%s/" % self.activitydirpath)[1]
        iconpath = os.path.join("/usr/local/share", self.proyecto["nombre"], newpath)
        
        ### setup.cfg
        cfg = "[install]\ninstall_lib=/usr/local/share/%s\ninstall_data=/usr/local/share/%s\ninstall_scripts=/usr/local/bin""" % (self.proyecto["nombre"], self.proyecto["nombre"])
        self.setupcfg.get_buffer().set_text(cfg)
        
        ### lanzador
        lanzador = "%s_run" % (self.proyecto["nombre"].lower())
        desinstalador = "%s_uninstall" % (self.proyecto["nombre"].lower())
        
        ### desktop
        desktop = "[Desktop Entry]\nEncoding=UTF-8\nName=%s\nGenericName=%s\nComment=%s\nExec=%s\nTerminal=false\nType=Application\nIcon=%s\nCategories=%s\nStartupNotify=true\nMimeType=%s" % (self.proyecto["nombre"], self.proyecto["nombre"], self.proyecto["descripcion"], os.path.join("/usr/local/bin", lanzador), iconpath, self.proyecto["categoria"], self.proyecto["mimetypes"])
        self.setupdesktop.get_buffer().set_text(desktop)
        
        ### MANIFEST
        import ApiProyecto
        
        manifest_list, data_files = ApiProyecto.get_installers_data(self.activitydirpath)
        
        manifest = ""
        
        for item in manifest_list:
            manifest = "%s\n%s" % (item, manifest)
            
        self.setupmanifest.get_buffer().set_text(manifest)
        
        ### setup.py
        setup_py = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n\nfrom distutils.core import setup\n\nsetup(\n\tname = \"%s\",\n\tversion = \"%s\",\n\t" % (self.proyecto["nombre"], self.proyecto["version"])
        
        autores = ""
        mails = ""
        
        for autor in self.proyecto["autores"]:
            autores = "%s%s - " % (autores, autor[0])
            mails = "%s%s - " % (mails, autor[1])
            
        if autores: autores = str(autores[:-3])
        if mails: mails = str(mails[:-3])
        
        setup_py = "%sauthor = \"%s\",\n\tauthor_email = \"%s\",\n\t" % (setup_py, autores, mails)
        setup_py = "%surl = \"%s\",\n\tlicense = \"%s\",\n\n\t" % (setup_py, self.proyecto["url"], self.proyecto["licencia"])
        setup_py = "%sscripts = [\"%s\", \"%s\"],\n\n\tpy_modules = [\"%s\"],\n\n\t" % (setup_py, lanzador, desinstalador, self.proyecto["main"].split(".")[0])
        setup_py = "%sdata_files =[\n\t\t(\"/usr/share/applications/\", [\"%s.desktop\"]),\n\t\t" % (setup_py, self.proyecto["nombre"])
        
        for key in data_files.keys():
            newkey = key
            
            if key.startswith("/"):
                newkey = ""
                
                for l in key[1:]:
                    newkey = "%s%s" % (newkey, l)
                
            if newkey:
                setup_py = "%s(\"%s/\",[\n\t\t\t" % (setup_py, newkey)
                
            else:
                setup_py = "%s(\"%s\",[\n\t\t\t" % (setup_py, newkey)
            
            for item in data_files[key]:
                setup_py = "%s\"%s\",\n\t\t\t" % (setup_py, item)
        
            setup_py = "%s]),\n\n\t\t" % (str(setup_py[:-5]))
            
        setup_py = "%s])\n\n" % (str(setup_py[:-5]))
        
        setup_py = "%s%s\n" % (setup_py, "import commands")
        setup_py = "%s%s\n" % (setup_py, "commands.getoutput(\"chmod -R 755 /usr/local/share/%s\")" % self.proyecto["nombre"])
        setup_py = "%s%s\n" % (setup_py, "commands.getoutput(\"chmod 755 /usr/share/applications/%s.desktop\")" % self.proyecto["nombre"])
        
        self.setuppy.get_buffer().set_text(setup_py)
        
        ### lanzador.
        lanzador = "#!/bin/sh\nexec \"/usr/bin/python\" \"/usr/local/share/%s/%s\" \"$@\"" % (self.proyecto["nombre"], self.proyecto["main"])
        self.lanzador.get_buffer().set_text(lanzador)
        
        ### desinstalador.
        desinstalador = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n\nimport os\nimport commands\n\n"
        desinstalador = "%sprint commands.getoutput(\"rm -r /usr/local/share/%s\")\n" % (desinstalador, self.proyecto["nombre"])
        desinstalador = "%sprint commands.getoutput(\"rm /usr/share/applications/%s.desktop\")\n" % (desinstalador, self.proyecto["nombre"])
        desinstalador = "%sprint commands.getoutput(\"rm /usr/local/bin/%s_run\")\n" % (desinstalador, self.proyecto["nombre"].lower())
        desinstalador = "%sprint commands.getoutput(\"rm /usr/local/bin/%s_uninstall\")\n" % (desinstalador, self.proyecto["nombre"].lower())
    
        self.desinstalador.get_buffer().set_text(desinstalador)
        
    def make(self):
        """
        Construye los archivos instaladores para su distribución.
        """
        
        cfg = self.__get_text(self.setupcfg.get_buffer())
        desktop = self.__get_text(self.setupdesktop.get_buffer())
        manifest = self.__get_text(self.setupmanifest.get_buffer())
        setuppy = self.__get_text(self.setuppy.get_buffer())
        lanzador = self.__get_text(self.lanzador.get_buffer())
        desinstalador = self.__get_text(self.desinstalador.get_buffer())
        
        self.__escribir_archivo(self.archivo_setup_cfg, cfg)
        self.__escribir_archivo(self.archivo_desktop, desktop)
        self.__escribir_archivo(self.archivo_manifest, manifest)
        self.__escribir_archivo(self.archivo_setup_py, setuppy)
        self.__escribir_archivo(self.archivo_lanzador, lanzador)
        self.__escribir_archivo(self.archivo_desinstalador, desinstalador)
    
    def __get_text(self, buffer):
        """
        Devuelve el contenido de un text buffer.
        """
        
        inicio, fin = buffer.get_bounds()
        texto = buffer.get_text(inicio, fin, 0)
        
        return texto
    
    def __escribir_archivo(self, archivo, contenido):
        """
        Escribe los archivos de instalación.
        """
        
        arch = open(archivo, "w")
        arch.write(contenido)
        arch.close()
        
    def get_scroll(self, sourceview):
        
        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scroll.add(sourceview)
        
        return scroll
    
class Sugar_Notebook(Gtk.Notebook):
    """
    Contenedor de información de instalador sugar.
    """
    
    __gtype_name__ = 'Sugar_Notebook'
    
    def __init__(self, proyecto):

        Gtk.Notebook.__init__(self)
        
        self.set_scrollable(True)
        
        self.proyecto = proyecto
        self.iconpath = False
        
        self.activity_sourceview = Setup_SourceView()
        self.setup_sourceview = Setup_SourceView()
        
        self.append_page(
            self.get_scroll(self.activity_sourceview),
            Gtk.Label("activity.info"))
            
        self.append_page(
            self.get_scroll(self.setup_sourceview),
            Gtk.Label("setup.py"))
        
        self.show_all()
        
    def get_scroll(self, sourceview):
        
        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scroll.add(sourceview)
        
        return scroll
        
    def setup_install(self, iconpath):
        """
        Recolecta la información necesaria para generar los
        archivos de instalación y los presenta al usuario para
        posibles correcciones.
        """
        
        self.iconpath = iconpath
        
        main_path = os.path.join(self.proyecto["path"], self.proyecto["main"])
        extension = os.path.splitext(os.path.split(main_path)[1])[1]
        main_name = self.proyecto["main"].split(extension)[0]
        
        extension = os.path.splitext(os.path.split(iconpath)[1])[1]
        newiconpath = os.path.basename(iconpath).split(extension)[0]
        
        activity = "[Activity]\nname = %s\nactivity_version = %s\nbundle_id = org.laptop.%s\nicon = %s\nexec = sugar-activity %s.%s -s\nmime_types =%s\nlicense = %s\nsummary = " % (self.proyecto["nombre"], self.proyecto["version"], self.proyecto["nombre"], newiconpath, main_name, main_name, self.proyecto["mimetypes"], self.proyecto["licencia"])
        setup = "#!/usr/bin/env python\n\nfrom sugar3.activity import bundlebuilder\nbundlebuilder.start()"
        
        ### Comenzar a generar el temporal
        activitydirpath = os.path.join("/tmp", "%s.activity" % self.proyecto["nombre"])
        activityinfodirpath = os.path.join(activitydirpath, "activity")
        
        ### Borrar anteriores
        if os.path.exists(activitydirpath):
            commands.getoutput("rm -r %s" % activitydirpath)
            
        ### Copiar contenido del proyecto.
        shutil.copytree(self.proyecto["path"], activitydirpath, symlinks=False, ignore=None)

        ### Escribir archivos de instalación.
        if not os.path.exists(activityinfodirpath): os.mkdir(activityinfodirpath)
        
        newpath = os.path.join(activityinfodirpath, os.path.basename(iconpath))
        shutil.copyfile(iconpath, newpath)
        
        self.activity_sourceview.get_buffer().set_text(activity)
        self.setup_sourceview.get_buffer().set_text(setup)
        
    def make(self):
        """
        Construye los archivos instaladores para su distribución.
        """
        
        activitydirpath = os.path.join("/tmp", "%s.activity" % self.proyecto["nombre"])
        activityinfodirpath = os.path.join(activitydirpath, "activity")
        
        infopath = os.path.join(activityinfodirpath, "activity.info")
        setuppath = os.path.join(activitydirpath, "setup.py")
        
        activity = self.__get_text(self.activity_sourceview.get_buffer())
        setup = self.__get_text(self.setup_sourceview.get_buffer())
        
        self.__escribir_archivo(infopath, activity)
        self.__escribir_archivo(setuppath, setup)
        
        ### Borrar archivos innecesarios
        nombre = self.proyecto["nombre"]
        ejecutable = ("%s_run" % nombre).lower()
        desinstalador = ("%s_uninstall" % nombre).lower()
        desktop = "%s.desktop" % nombre
        
        borrar = [ejecutable, desinstalador, "MANIFEST", desktop, "setup.cfg"]
        
        for file in borrar:
            path = os.path.join(activitydirpath, file)
            
            if os.path.exists(path):
                os.remove(path)
            
        ### Generar archivo de distribución "*.xo"
        import zipfile
        
        zippath = "%s.xo" % (activitydirpath)
        
        if os.path.exists(zippath):
            commands.getoutput("rm %s" % zippath)
            
        zipped = zipfile.ZipFile(zippath, "w")
        
        RECHAZAExtension = [".pyc", ".pyo", ".bak"]
        RECHAZAFiles = ["proyecto.ide", ".gitignore"]
        RECHAZADirs = [".git", "build", "dist"]
        
        for (archiveDirPath, dirNames, fileNames) in os.walk(activitydirpath):
            if not os.path.basename(archiveDirPath) in RECHAZADirs:
                for fileName in fileNames:
                    if not fileName in RECHAZAFiles:
                        filePath = os.path.join(archiveDirPath, fileName)
                        extension = os.path.splitext(os.path.split(filePath)[1])[1]
                        
                        if not extension in RECHAZAExtension:
                            zipped.write(filePath, filePath.split(activitydirpath)[1])
        
        zipped.close()
        
        distpath = os.path.join(self.proyecto["path"], "dist")
        
        if not os.path.exists(distpath):
            os.mkdir(distpath)
            
        ### Copiar el *.xo a la estructura del proyecto.
        commands.getoutput("cp %s %s" % (zippath, distpath))
        os.chmod(os.path.join(distpath, os.path.basename(zippath)), 0755)
        
    def __get_text(self, buffer):
        """
        Devuelve el contenido de un text buffer.
        """
        
        inicio, fin = buffer.get_bounds()
        texto = buffer.get_text(inicio, fin, 0)
        
        return texto
    
    def __escribir_archivo(self, archivo, contenido):
        """
        Escribe los archivos de instalación.
        """
        
        arch = open(archivo, "w")
        arch.write(contenido)
        arch.close()
        
class Setup_SourceView(GtkSource.View):
    """
    Widget para mostrar contenido de archivos instaladores.
    """
    
    __gtype_name__ = 'Setup_SourceView'
    
    def __init__(self):

        GtkSource.View.__init__(self)
        
        self.set_buffer(GtkSource.Buffer())
        
        from gi.repository import Pango
        self.modify_font(Pango.FontDescription('Monospace 10'))

        self.show_all()
        
class Widget_icon(Gtk.Frame):
    """
    Widget que permite al usuario seleccionar el ícono de la aplicación.
    """
    
    __gtype_name__ = 'Widget_icon'

    __gsignals__ = {
     'iconpath': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
     'make': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
        
    def __init__(self, tipo = "gnome", proyecto = None):
        
        Gtk.Frame.__init__(self)
        
        self.set_label(" Selecciona un Icono para Tu Aplicación ")
        self.set_border_width(15)
        
        self.tipo = tipo # FIXME: tipo debe determinar que formato de ico se permite (svg para sugar)
        self.proyecto = proyecto
        
        toolbar = Gtk.Toolbar()
        
        self.image = Gtk.Image()
        self.image.set_size_request(50, 50)
        
        boton = get_boton(Gtk.STOCK_OPEN, "Buscar Archivo")
        self.aceptar = Gtk.Button("Construir Instalador")
        self.aceptar.set_sensitive(False)
        
        toolbar.insert(get_separador(draw = False, ancho = 10, expand = False), -1)
        
        item = Gtk.ToolItem()
        item.add(self.image)
        toolbar.insert(item, -1)
        
        toolbar.insert(get_separador(draw = False, ancho = 10, expand = False), -1)
        
        toolbar.insert(boton, -1)
        
        toolbar.insert(get_separador(draw = False, ancho = 0, expand = True), -1)
        
        item = Gtk.ToolItem()
        item.add(self.aceptar)
        toolbar.insert(item, -1)
        
        toolbar.insert(get_separador(draw = False, ancho = 10, expand = False), -1)
        
        self.add(toolbar)
        
        self.show_all()
    
        boton.connect("clicked", self.__open_filechooser)
        self.aceptar.connect("clicked", self.__Construir)
        
    def __Construir(self, widget):
        """
        Manda construir el instalador.
        """
        
        self.emit("make")
        
    def __open_filechooser(self, widget):
        """
        Abre un filechooser para seleccionar un ícono.
        """
        
        mime = "image/*"
        
        if self.tipo == "sugar": mime = "image/svg+xml"
        
        from Widgets import My_FileChooser
        
        filechooser = My_FileChooser(
            parent_window = self.get_toplevel(),
            action_type = Gtk.FileChooserAction.OPEN,
            title = "Seleccionar Icono . . .",
            path = self.proyecto["path"],
            mime_type = [mime])

        filechooser.connect('load', self.__emit_icon_path)
    
    def __emit_icon_path(self, widget, iconpath):
        """
        Cuando el usuario selecciona un icono para la aplicación.
        """
        
        from gi.repository import GdkPixbuf
        
        iconpath = str(iconpath).replace("//", "/")
        
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(iconpath, 50, 50)
        self.image.set_from_pixbuf(pixbuf)
        
        self.aceptar.set_sensitive(True)
        self.emit("iconpath", iconpath)
        
class DialogoInstall(Gtk.Dialog):
    """
    Dialogo para mostrar proceso de construcción de Instaladores.
    """
    
    __gtype_name__ = 'DialogoInstall'
    
    def __init__(self,
        parent_window = None,
        dirpath = None,
        destino_path = None):

        Gtk.Dialog.__init__(self,
            parent = parent_window,
            title = "Generador de Instaladores",
            flags = Gtk.DialogFlags.MODAL,
            buttons = ["Cerrar", Gtk.ResponseType.ACCEPT])
        
        self.set_size_request(640, 480)
        self.set_border_width(15)
        
        self.destino_path = destino_path
        self.dirpath = dirpath
        
        from JAMediaTerminal import JAMediaTerminal
        
        self.terminal = JAMediaTerminal()
        
        self.vbox.pack_start(self.terminal, True, True, 0)
        
        self.terminal.toolbar.hide()
        
        notebook = self.terminal.notebook
        cerrar = notebook.get_tab_label(notebook.get_children()[0]).get_children()[1]
        cerrar.set_sensitive(False)
        
        self.maximize()
        
        self.terminal.connect("reset", self.__end_make)
        
        GLib.idle_add(self.__run_gnome_install)
        
    def __end_make(self, jamediaterminal, notebook, terminal, pag_indice):
        """
        Cuando Finaliza el proceso de construcción del
        instalador, se informa al usuario.
        """

        dialog = DialogoInfoInstall(
            parent_window = self.get_toplevel(),
            distpath = os.path.join(self.destino_path, "dist"))
    
        respuesta = dialog.run()
        
        dialog.destroy()
        
    def __run_gnome_install(self):
        """
        Ejecuta: python setup.py sdist
        Construyendo el instalador gnome.
        """
        
        python_path = "/usr/bin/python"
        
        if os.path.exists(os.path.join("/bin", "python")):
            python_path = os.path.join("/bin", "python")
            
        elif os.path.exists(os.path.join("/usr/bin", "python")):
            python_path = os.path.join("/usr/bin", "python")
            
        elif os.path.exists(os.path.join("/sbin", "python")):
            python_path = os.path.join("/sbin", "python")
            
        elif os.path.exists(os.path.join("/usr/local", "python")):
            python_path = os.path.join("/usr/local", "python")
            
        self.terminal.ejecute_script(
            self.dirpath,
            python_path,
            os.path.join(self.dirpath, "setup.py"),
            "sdist")
            
        return False
        
class DialogoInfoInstall(Gtk.Dialog):
    """
    Dialogo para informar al usuario donde encontrar el
    paquete de distribución de su proyecto.
    """
    
    __gtype_name__ = 'DialogoInfoInstall'
    
    def __init__(self, parent_window = None, distpath = None):

        Gtk.Dialog.__init__(self,
            title = "Generador de Instaladores",
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = ["Cerrar", Gtk.ResponseType.ACCEPT])
        
        self.set_size_request(420, 180)
        self.set_border_width(15)
        
        label = Gtk.Label(u"Proceso de Construcción de Instalador Culminado.\nPuedes Encontrar el Instalador de tu Proyecto en:\n\n%s" % (distpath))
        
        label.show()
        
        self.vbox.pack_start(label, True, True, 0)
        
class Ceibal_Notebook(Gtk.Notebook):
    """
    Contenedor de información de instalador gnome ceibal.
    """
    
    __gtype_name__ = 'Ceibal_Notebook'
    
    def __init__(self, proyecto):

        Gtk.Notebook.__init__(self)
        
        self.set_scrollable(True)
        
        self.proyecto = proyecto
        self.iconpath = False
        
        self.install = Setup_SourceView()
        self.install.get_buffer().set_text("")
        
        self.append_page(
            self.get_scroll(self.install),
            Gtk.Label("install.py"))
        
        self.show_all()
        
    def setup_install(self, iconpath):
        """
        Recolecta la información necesaria para generar los
        archivos de instalación y los presenta al usuario para
        posibles correcciones.
        """
        
        self.iconpath = iconpath
        
        ### Comenzar a generar el temporal
        activitydirpath = os.path.join("/tmp", "%s" % self.proyecto["nombre"])
        
        ### Borrar anteriores
        if os.path.exists(activitydirpath):
            commands.getoutput("rm -r %s" % activitydirpath)
        
        ### Copiar contenido del proyecto.
        shutil.copytree(self.proyecto["path"], activitydirpath, symlinks=False, ignore=None)
        
        if not self.proyecto["path"] in iconpath:
            newpath = os.path.join(activitydirpath, os.path.basename(iconpath))
            shutil.copyfile(iconpath, newpath)
            iconpath = newpath
        
        import shelve
        
        archivo = shelve.open(os.path.join(BASEPATH, "plantilla"))
        text = u"%s" % archivo.get('install', "")
        archivo.close()
        
        iconpath = iconpath.split(self.proyecto["path"])[-1]
        
        text = text.replace('mainfile', self.proyecto["main"])
        text = text.replace('iconfile', iconpath)
        text = text.replace('GnomeCat', self.proyecto["categoria"])
        text = text.replace('GnomeMimeTypes', self.proyecto["mimetypes"])
        
        self.install.get_buffer().set_text(text)
        
    def make(self):
        """
        Construye los archivos instaladores para su distribución.
        """
        
        import zipfile
        
        activitydirpath = os.path.join("/tmp", "%s" % self.proyecto["nombre"])
        
        ### Escribir instalador.
        archivo_install = os.path.join(activitydirpath, "install.py")
        install = self.__get_text(self.install.get_buffer())
        self.__escribir_archivo(archivo_install, install)

        ### Generar archivo de distribución "*.zip"
        zippath = "%s.zip" % (activitydirpath)
        
        ### Eliminar anterior.
        if os.path.exists(zippath):
            os.remove(zippath)
            
        zipped = zipfile.ZipFile(zippath, "w")
        
        RECHAZAExtension = [".pyc", ".pyo", ".bak", ".ide", ".gitignore", ".git"]
        RECHAZAFiles = ["proyecto.ide", ".gitignore", "plantilla"]
        RECHAZADirs = [".git", "build", "dist"]
        
        ### Forzar eliminacion de dist
        for dir in os.listdir(activitydirpath):
            d = os.path.join(activitydirpath, dir)
            
            if os.path.isdir(d):
                if d.split("/")[-1] in RECHAZADirs:
                    commands.getoutput("rm -r %s" % d)
            
        for (archiveDirPath, dirNames, fileNames) in os.walk(activitydirpath):
            
            if not archiveDirPath.split("/")[-1] in RECHAZADirs:
                for fileName in fileNames:
                    if not fileName in RECHAZAFiles:
                        filePath = os.path.join(archiveDirPath, fileName)
                        extension = os.path.splitext(os.path.split(filePath)[1])[1]
                        
                        if not extension in RECHAZAExtension:
                            zipped.write(filePath, filePath.split(activitydirpath)[1])
        
        zipped.close()
        
        distpath = os.path.join(self.proyecto["path"], "dist")
        
        if not os.path.exists(distpath):
            os.mkdir(distpath)
            
        ### Copiar el *.zip a la estructura del proyecto.
        commands.getoutput("cp %s %s" % (zippath, distpath))
        os.chmod(os.path.join(distpath, os.path.basename(zippath)), 0755)
        
        if os.path.exists(zippath):
            os.remove(zippath)
            commands.getoutput("rm -r %s" % activitydirpath)
    
    def __get_text(self, buffer):
        """
        Devuelve el contenido de un text buffer.
        """
        
        inicio, fin = buffer.get_bounds()
        texto = buffer.get_text(inicio, fin, 0)
        
        return texto
    
    def __escribir_archivo(self, archivo, contenido):
        """
        Escribe los archivos de instalación.
        """
        
        arch = open(archivo, "w")
        arch.write(contenido)
        arch.close()
        
    def get_scroll(self, sourceview):
        
        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scroll.add(sourceview)
        
        return scroll
    