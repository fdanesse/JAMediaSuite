#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   SpyderHack.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
Casos:
    from gi import repository, importer                     OK
    from gi.repository import Gtk, Gst                      OK
    
    from gi import repository as x                          OK
    from gi.repository import Gtk as X                      OK
    from gi.repository.Gtk import Window as W               OK
    
    import gi, os, sys                                      OK
    import gi.repository, os.path, etc . . .                OK
    
    import gi as Z                                          OK
    import gi.repository as D                               OK
    import gi.repository.Gtk as Z                           OK

    from gtk import gdk, Window, etc . . .                  OK
    from gtk.gdk import Color, etc . . .                    OK
    import os, gtk, sys                                     OK
    import gtk.gdk                                          OK
    from os import path as X                                OK
    from gtk.gdk import Color as Z                          OK
    import os as X                                          OK
    import os.path as X                                     OK
    from os import *                                        # No funcional - muy ineficiente.
    from os.path import *                                   # No funcional - muy ineficiente.

    from JAMedia import JAMediaPlayer                       OK
    from JAMedia.JAMedia import JAMediaPlayer               OK
    
    import JAMediaObjects, JAMedia.JAMedia, JAMediaEditor   OK
    import JAMediaObjects                                   OK
    import JAMediaObjects.JAMediaGstreamer                  OK
    import JAMedia                                          OK
    import JAMedia.JAMedia                                  OK
    
    import JAMediaObjects as X                              OK
    import JAMedia as X                                     OK
    import JAMedia.JAMedia as X                             OK
    self                                                    *****
"""

import os
import sys
import shelve
import commands
import time

BASEPATH = os.path.dirname(__file__)
path = os.path.join("/dev/shm", "shelvein")

def Import_Module_False_Path(base_key, modulo):
    
    ejecutable = os.path.join(BASEPATH, "Dir_Modulo.py")
    commands.getoutput('python %s %s %s' % (ejecutable, base_key, modulo))

def Import_Module_False_Path_From(base_key, modulo, attrib):
    
    ejecutable = os.path.join(BASEPATH, "Dir_Attrib.py")
    commands.getoutput('python %s %s %s %s' % (ejecutable, base_key, modulo, attrib))
    
def Import_Module_False_Path_From_Recursive(base_key, modulo1, modulo2, modulo3):
    
    ejecutable = os.path.join(BASEPATH, "Recursive_Dir_Attrib.py")
    commands.getoutput('python %s %s %s %s %s' % (ejecutable, base_key, modulo1, modulo2, modulo3))
    
def Import_Module_gi(base_key, attrib):

    ejecutable = os.path.join(BASEPATH, "Dir_Modulo_gi.py")
    commands.getoutput('python %s %s %s' % (ejecutable, base_key, attrib))
    
def Import_Module_gi_From(base_key, modulo, attrib):

    ejecutable = os.path.join(BASEPATH, "Dir_Attrib_gi.py")
    commands.getoutput('python %s %s %s %s' % (ejecutable, base_key, modulo, attrib))

### Modulos del Usuario.
def Import_Module_True_Path(base_key, real_path, modulo):
    
    try:
        file = os.path.join(BASEPATH, "Dir_Modulo_True.py")
        commands.getoutput('cp %s %s' % (file, real_path))
        ejecutable = os.path.join(real_path, "Dir_Modulo_True.py")
        commands.getoutput('python %s %s %s' % (ejecutable, base_key, modulo))
        os.remove(ejecutable)
    except:
        pass
    
### Módulos y Clases del usuario desde un path o módulo.
def Import_Module_True_Path_From(base_key, real_path, modulo, attrib):
    
    try:
        file = os.path.join(BASEPATH, "Dir_Attrib_True.py")
        commands.getoutput('cp %s %s' % (file, real_path))
        ejecutable = os.path.join(real_path, "Dir_Attrib_True.py")
        commands.getoutput('python %s %s %s %s' % (ejecutable, base_key, modulo, attrib))
        os.remove(ejecutable)
    except:
        pass
    
### Paquetes del Usuario.
def Import_Pakage_True_Path(base_key, real_path, modulo):
    
    try:
        file = os.path.join(BASEPATH, "Dir_Pakage_True.py")
        commands.getoutput('cp %s %s' % (file, real_path))
        ejecutable = os.path.join(real_path, "Dir_Pakage_True.py")
        commands.getoutput('python %s %s %s' % (ejecutable, base_key, modulo))
        os.remove(ejecutable)
    except:
        pass
    
def get_imports(buffer):
    """
    Devuelve las líneas dónde se hace import.
    """
    
    # FIXME: Mejorar:
    # Sólo se deben obtener los imports base y los internos de la función en que se escribe.
    
    inicio = buffer.get_start_iter()
    end = buffer.get_end_iter()
    
    texto = buffer.get_text(inicio, end, True) # O hasta linea activa (textiter) ?
    lineas = texto.splitlines()
    
    imports = []
    for linea in lineas:
        # FIXME: Analizar mejor los casos como 3 comillas.
        if linea.startswith("import ") or linea.startswith("from "):
            
            text = str(linea).strip()
            
            if not text in imports:
                imports.append(text)
    
    return imports

def traduce_path(workpath, import_path):
    """
    Convierte:
        Prueba.WidgetsDir.Widgets
        
    En:
        /home/flavio/BatovideWorkSpace/Prueba/Prueba/WidgetsDir/Widgets
    """
    
    real_path = import_path.replace(".", "/")
    real_path = os.path.join(workpath, real_path)
    
    return real_path
    
def determine_path(real_path):
    """
    Determina si el path es un directorio,
    un archivo o no existe.
    """
    
    valor = []
    if os.path.exists(real_path):
        if os.path.isdir(real_path):
            valor.append("dir")
        
    posible = "%s.py" % real_path
    if os.path.exists(posible):
        if os.path.isfile(posible):
            valor.append("file")
        
    return valor
    
def parse_modulos(imp):
    """
    Parsea la última parte del import
        os,sys, commands, etc . . .
    Devolviendo la lista de modulos a importar.
    """
    
    modulos = []
    
    for t in imp:
        if "," in t:
            li = t.split(",")
            for l in li:
                text = l.strip()
                if text:
                    modulos.append(text)
            
        else:
            modulos.append(t.replace(",", ""))
            
    return modulos

def parse_path_modulos(imp):
    """
    Parsea la segunda parte del import
        os.path.etc . . .
    Devolviendo la lista de modulos que marcan el path de importacion.
    """
    
    return imp.split(".")

def make_alias(workpath, modulo_attrib, alias):
    
    #print "-- Construyendo Alias:", alias, "==", modulo_attrib
    
    mod = shelve.open(path)
    
    try:
        key_dict = {}
        for key in mod[str(workpath)].keys():
            key_dict[key] = mod[str(workpath)][key]
            
        dict = mod[str(workpath)][modulo_attrib]#.get(attrib, {})
        
        key_dict[alias] = dict
        
        mod[str(workpath)] = key_dict
        
    except:
        #print "-- Error en __make_alias", workpath, modulo_attrib, alias
        pass
        
    mod.close()

def convert_alias(workpath, modulo_attrib, alias):
    
    #print "-- Convirtiendo Alias:", alias, "Remplaza a:", modulo_attrib
    
    mod = shelve.open(path)
    
    try:
        key_dict = {}
        for key in mod[str(workpath)].keys():
            key_dict[key] = mod[str(workpath)][key]
            
        dict = mod[str(workpath)][modulo_attrib]#.get(attrib, {})
        
        key_dict[alias] = dict
        del (key_dict[modulo_attrib])
        
        mod[str(workpath)] = key_dict
        
    except:
        #print "-- Error en __convert_alias", workpath, modulo_attrib, alias
        pass
        
    mod.close()
    
def is_py_gi(imp):
    
    if "gi.repository" in imp:
        return True
        
    elif not "gi.repository" in imp:
        if "import" in imp:
            if "gi" in parse_modulos(imp.split()[1:]):
                return True
            
            else:
                return False
            
        else:
            print "Caso gi no Previsto:", imp
    
    else:
        return False
    
class SpyderHack():
    
    def __init__(self):
        
        self.__id = str(int(time.time()))
        self.imports = []
        self.freeze = []
        self.workpath = ""
        
        """
        self.__id:
            key base en el diccionario para este autocompletado.
        self.imports:
            Imports vigentes.
        self.freeze:
            Cuando se hace import os y luego se hace import os as X
            import os se congela para que no sea reemplazado por el alias X,
            de esta forma coexisten X y os.
        """
        
    def __clear(self):
        """
        Autocompletado se resetea.
        """
        
        self.imports = []
        self.freeze = []
        modulos = shelve.open(path)
        modulos[self.__id] = {}
        modulos.close()
        
    def __get_diff_imports(self, imports):
        """
        Cuando el usuario cambia las declaraciones de imports
        El autocompletado se resetea.
        """
        
        for imp in self.imports:
            if not imp in imports:
                return True
                
        for imp in imports:
            if not imp in self.imports:
                return True
                
        return False
    
    def __append_to_freze(self, attrib):
        """
        Congela un import para no ser reemplazado por un alias.
        """
        
        if not attrib in self.freeze:
            self.freeze.append(attrib)
            
    def __gi_import_uno(self, base_key, imp):
        """
        Todo lo que se importa es de python-gi
        """
        ### Verificado.
        
        attribs = parse_modulos(imp.split()[3:])
        mods = parse_path_modulos(imp.split()[1])
        
        if len(mods) == 1:
            #   from gi import repository, importer
            # FIXME: Este caso no funciona.
            pass
        
        elif len(mods) == 2:
            #   from gi.repository import Gtk, Gst
            for attrib in attribs:
                Import_Module_gi(base_key, attrib)
                self.__append_to_freze(attrib)
                
        else:
            print "Caso imposible en __gi_import_uno:", imp
            
    def __gi_import_dos(self, base_key, imp):
        """
        Se importan módulos o paquetes de python-gi y además,
        módulos o paquete extras, algunos pueden ser
        módulos o paquetes del usuario.
        """
        ### Verificado.
        
        modulos = parse_modulos(imp.split()[1:])
        
        for modulo in modulos:
            real_path = traduce_path(self.workpath, modulo)
            tipo = determine_path(real_path)
            
            if tipo:
                self.__Gestione_True_Path_Uno(tipo, modulo, real_path, base_key, imp)
            
            else:
                mods = parse_path_modulos(modulo)
                
                if len(mods) == 1:
                    # import gi, os, sys
                    Import_Module_False_Path(base_key, modulo)
                    self.__append_to_freze(modulo)
                
                elif len(mods) == 2:
                    # import gi.repository, os.path, etc . . .
                    if modulo == "gi.repository":
                        Import_Module_False_Path(base_key, modulo)
                        self.__append_to_freze(modulo)
                    
                    else:
                        Import_Module_False_Path_From(base_key, mods[0], mods[1])
                        convert_alias(base_key, mods[1], "%s.%s" % (mods[0], mods[1]))
                        self.__append_to_freze("%s.%s" % (mods[0], mods[1]))
                
                else:
                    print "Caso imposible en __gi_import_dos:", imp
                
    def __gi_import_tres(self, base_key, imp):
        """
        Solo se importan modulos, paquetes o clases
        de python-gi creando alias.
        """
        ### Verificado.
        
        modulo = imp.split()[1]
        attrib = imp.split()[3]
        alias = imp.split()[-1]
        
        mods = parse_path_modulos(modulo)
        
        if len(mods) == 1:
            #   from gi import repository as x
            # FIXME: Este caso no funciona.
            pass
    
        elif len(mods) == 2:
            #   from gi.repository import Gtk as X
            Import_Module_gi(base_key, attrib)
            if not attrib in self.freeze:
                convert_alias(base_key, attrib, alias)
            else:
                make_alias(base_key, attrib, alias)
        
        elif len(mods) == 3:
            #   from gi.repository.Gtk import Window as W
            Import_Module_gi_From(base_key, mods[-1], attrib)
            if not attrib in self.freeze:
                convert_alias(base_key, attrib, alias)
            else:
                make_alias(base_key, attrib, alias)
                
        else:
            print "Caso imposible en __gi_import_tres:", imp
            
    def __gi_import_cuatro(self, base_key, imp):
        """
        Solo se importan modulos o paquetes
        de python-gi creando alias.
        """
        ### Verificado.
        
        modulo = imp.split()[1]
        alias = imp.split()[-1]
        
        mods = parse_path_modulos(modulo)
        
        if len(mods) == 1:
            #   import gi as Z
            Import_Module_False_Path(base_key, modulo)
            if not modulo in self.freeze:
                convert_alias(base_key, modulo, alias)
            else:
                make_alias(base_key, modulo, alias)
        
        elif len(mods) == 2:
            #   import gi.repository as D
            Import_Module_False_Path(base_key, modulo)
            if not modulo in self.freeze:
                convert_alias(base_key, modulo, alias)
            else:
                make_alias(base_key, modulo, alias)
        
        elif len(mods) == 3:
            #   import gi.repository.Gtk as Z
            attrib = mods[2]
            Import_Module_gi(base_key, attrib)
            if not attrib in self.freeze:
                convert_alias(base_key, attrib, alias)
            else:
                make_alias(base_key, attrib, alias)
        
        else:
            print "Caso imposible en __gi_import_cuatro:", imp
            
    def __Gestione_gi(self, imp, base_key):
        
        if_as = " as " in imp
        if_asterisco = " *" in imp
        is_from = imp.startswith("from ")
        is_import = imp.startswith("import ")
        
        if not if_as and not if_asterisco:
            if is_from:
                self.__gi_import_uno(base_key, imp)
                
            elif is_import:
                self.__gi_import_dos(base_key, imp)
                
            else:
                print "Caso no previsto en __Gestione_gi:", imp
                
        elif if_as and not if_asterisco:
            if is_from:
                self.__gi_import_tres(base_key, imp)
                
            elif is_import:
                self.__gi_import_cuatro(base_key, imp)
                
            else:
                print "Caso no previsto en __Gestione_gi:", imp
                
        else:
            print "Caso no previsto en __Gestione_gi:", imp
        
    def __false_path_uno(self, imp, base_key):
        """
        Se importa un módulo paquete o clase desde un path
        """
        ### Verificado.
        
        attribs = parse_modulos(imp.split()[3:])
        modulo = imp.split()[1]
        real_path = traduce_path(self.workpath, modulo)
        tipo = determine_path(real_path)
        
        if tipo:
            self.__Gestione_True_Path_Dos(modulo, attribs, base_key, imp)
        
        else:
            for attrib in attribs:
                mods = parse_path_modulos(modulo)
                
                if len(mods) == 1:
                    #   from gtk import gdk, Window, etc . . .
                    for attrib in attribs:
                        Import_Module_False_Path_From(base_key, mods[0], attrib)
                        self.__append_to_freze(attrib)
                        
                elif len(mods) == 2:
                    #   from gtk.gdk import Color, etc . . .
                    for attrib in attribs:
                        Import_Module_False_Path_From_Recursive(base_key, mods[0], mods[1], attrib)
                        convert_alias(base_key, "%s.%s.%s" % (mods[0], mods[1], attrib), attrib)
                        self.__append_to_freze(attrib)
                        
                else:
                    print "Caso imposible en __false_path_uno:", imp
            
    def __false_path_dos(self, imp, base_key):
        """
        Se importa un módulo o un paquete.
        """
        ### Verificado.
        
        modulos = parse_modulos(imp.split()[1:])
        
        for modulo in modulos:
            real_path = traduce_path(self.workpath, modulo)
            tipo = determine_path(real_path)
            
            if tipo:
                self.__Gestione_True_Path_Uno(tipo, modulo, real_path, base_key, imp)
            
            else:
                mods = parse_path_modulos(modulo)
                
                if len(mods) == 1:
                    #   import os, gtk, sys
                    Import_Module_False_Path(base_key, mods[0])
                    self.__append_to_freze(mods[0])
                    
                elif len(mods) == 2:
                    #   import gtk.gdk
                    Import_Module_False_Path_From(base_key, mods[0], mods[1])
                    if not mods[1] in self.freeze:
                        convert_alias(base_key, mods[1], "%s.%s" % (mods[0], mods[1]))
                    else:
                        make_alias(base_key, mods[1], "%s.%s" % (mods[0], mods[1]))
                    
                else:
                    print "Caso imposible en __false_path_dos:", imp, len(mods)
                
    def __false_path_tres(self, imp, base_key):
        """
        Se importa un módulo, paquete o clase creando un alias.
        """
        ### Verificado.
        
        attrib = imp.split()[3]
        modulo = imp.split()[1]
        alias = imp.split()[5]
        
        real_path = traduce_path(self.workpath, modulo)
        tipo = determine_path(real_path)
        
        if tipo:
            self.__Gestione_True_Path_Dos(modulo, [attrib], base_key, imp, alias=alias)
        
        else:
            modulos = parse_path_modulos(modulo)
            
            if len(modulos) == 1:
                #   from os import path as X
                Import_Module_False_Path_From(base_key, modulo, attrib)
                if not attrib in self.freeze:
                    convert_alias(base_key, attrib, alias)
                else:
                    make_alias(base_key, attrib, alias)
                
            elif len(modulos) == 2:
                #   from gtk.gdk import Color as Z
                Import_Module_False_Path_From_Recursive(base_key, modulos[0], modulos[1], attrib)   # gtk.gdk.Color
                convert_alias(base_key, "%s.%s.%s" % (modulos[0], modulos[1], attrib), alias)       # Z = gtk.gdk.Color
                
            else:
                print "Caso imposible en __false_path_tres:", imp
            
    def __false_path_cuatro(self, imp, base_key):
        """
        Se importa un paquete o un módulo construyendo un alias.
        """
        ### Verificado.
        
        modulo = imp.split()[1]
        alias = imp.split()[-1]
        
        real_path = traduce_path(self.workpath, modulo)
        tipo = determine_path(real_path)
        
        if tipo:
            self.__Gestione_True_Path_Uno(tipo, modulo, real_path, base_key, imp, alias=alias)
        
        else:
            modulos = parse_path_modulos(modulo)
            
            if len(modulos) == 1:
                #   import os as X
                Import_Module_False_Path(base_key, modulo)
                if not modulo in self.freeze:
                    convert_alias(base_key, modulo, alias)
                else:
                    make_alias(base_key, modulo, alias)
                
            elif len(modulos) == 2:
                #   import os.path as X
                Import_Module_False_Path_From(base_key, modulos[0], modulos[1])
                if not modulos[1] in self.freeze:
                    convert_alias(base_key, modulos[1], alias)
                else:
                    make_alias(base_key, modulos[1], alias)
                
            else:
                print "Caso imposible en __false_path_cuatro:", imp
            
    def __false_path_cinco(self, imp, base_key):
        pass
        #   from os import *
        #   from os.path import *
        # FIXME: Extremadamente ineficiente.
        """
        modulo = imp.split()[1]
        
        modulos = parse_path_modulos(modulo)
        
        if len(modulos) == 1:
            Import_Module_False_Path(base_key, modulo)
            
            modulos = shelve.open(path)
            attribs = modulos[base_key].get(modulo, {}).get("lista", [])
            modulos.close()
            
            for attrib in attribs:
                Import_Module_False_Path_From(base_key, modulo, attrib)
                self.__append_to_freze(attrib)
                
            # FIXME: borrar el modulo del dict
            
        elif len(modulos) == 2:
            pass
        
        else:
            print "Caso imposible en __false_path_cinco:", imp
        """
        
    def __Gestione_False_Path(self, imp, base_key):
        
        if_as = " as " in imp
        if_asterisco = " *" in imp
        is_from = imp.startswith("from ")
        is_import = imp.startswith("import ")
        
        if not if_as and not if_asterisco:
            if is_from:
                self.__false_path_uno(imp, base_key)
                
            elif is_import:
                self.__false_path_dos(imp, base_key)
                
            else:
                print "Caso no previsto en __Gestione_False_Path:", imp
                
        elif if_as and not if_asterisco:
            if is_from:
                self.__false_path_tres(imp, base_key)
                
            elif is_import:
                self.__false_path_cuatro(imp, base_key)
                
            else:
                print "Caso no previsto en __Gestione_False_Path:", imp
                
        elif is_from and if_asterisco:
            self.__false_path_cinco(imp, base_key)

        else:
            print "Caso no previsto en __Gestione_False_Path:", imp
        
    def __Gestione_True_Path_Uno(self, tipo, modulo, real_path, base_key, imp, alias=False):
        """
        Se importa un paquete o módulo del Usuario.
        """
        
        mods = parse_path_modulos(modulo)
        
        if "dir" in tipo and "file" in tipo:
            # Directorio y Archivo con el mismo nombre en el mismo path.
            # Siempre que esto ocurre, se importa el paquete.
            '''
            Import_Pakage_True_Path(base_key, os.path.dirname(real_path), mods[0])
            if not alias:
                convert_alias(base_key, "import", mods[0])
                self.__append_to_freze(mods[0])
            else:
                convert_alias(base_key, "import", alias)'''
            if len(mods) == 1:
                #   import JAMediaObjects
                #   import JAMediaObjects as X
                Import_Pakage_True_Path(base_key, os.path.dirname(real_path), mods[0])
                if not alias:
                    convert_alias(base_key, "import", mods[0])
                    self.__append_to_freze(mods[0])
                else:
                    convert_alias(base_key, "import", alias)
                    
            elif len(mods) == 2:
                #   import JAMediaObjects.JAMediaGstreamer
                #   import JAMediaObjects.JAMediaGstreamer as X
                Import_Pakage_True_Path(base_key, os.path.dirname(real_path), mods[1])
                if not alias:
                    convert_alias(base_key, "import", "%s.%s" % (mods[0], mods[1]))
                else:
                    convert_alias(base_key, "import", alias)
                    
        elif "dir" in tipo:
            if len(mods) == 1:
                #   import JAMediaObjects
                #   import JAMediaObjects as X
                Import_Pakage_True_Path(base_key, os.path.dirname(real_path), mods[0])
                if not alias:
                    convert_alias(base_key, "import", mods[0])
                    self.__append_to_freze(mods[0])
                else:
                    convert_alias(base_key, "import", alias)
                    
            elif len(mods) == 2:
                #   import JAMediaObjects.JAMediaGstreamer
                #   import JAMediaObjects.JAMediaGstreamer as X
                Import_Pakage_True_Path(base_key, os.path.dirname(real_path), mods[1])
                if not alias:
                    convert_alias(base_key, "import", "%s.%s" % (mods[0], mods[1]))
                else:
                    convert_alias(base_key, "import", alias)
                    
            else:
                print "Caso imposible en __gi_import_dos:", imp
        
        elif "file" in tipo:
            if len(mods) == 1:
                #   import JAMedia
                #   import JAMedia as X
                Import_Module_True_Path(base_key, os.path.dirname(real_path), mods[0])
                if not alias:
                    self.__append_to_freze(mods[0])
                else:
                    if not mods[0] in self.freeze:
                        convert_alias(base_key, mods[0], alias)
                    else:
                        make_alias(base_key, mods[0], alias)
                
            elif len(mods) == 2:
                #   import JAMedia.JAMedia
                #   import JAMedia.JAMedia as X
                Import_Module_True_Path_From(base_key, os.path.dirname(os.path.dirname(real_path)), modulo, mods[1])
                if not alias:
                    convert_alias(base_key, "import", "%s.%s" % (mods[0], mods[1]))
                else:
                    convert_alias(base_key, "import", alias)
                    
            else:
                print "Caso imposible en __gi_import_dos:", imp
                
    def __Gestione_True_Path_Dos(self, modulo, attribs, base_key, imp, alias=False):
        
        mods = parse_path_modulos(modulo)
        
        for attrib in attribs:
            real_path = traduce_path(self.workpath, "%s.%s" % (modulo, attrib))
            tipo = determine_path(real_path)
            
            if "dir" in tipo and "file" in tipo:
                # Se importa un paquete
                if len(mods) == 1:
                    Import_Pakage_True_Path(base_key, os.path.dirname(real_path), attrib)
                    if not alias:
                        convert_alias(base_key, "import", attrib)
                        self.__append_to_freze(attrib)
                    else:
                        convert_alias(base_key, "import", alias)
                
                elif len(mods) == 2:
                    Import_Pakage_True_Path(base_key, os.path.dirname(real_path), attrib)
                    if not alias:
                        convert_alias(base_key, "import", attrib)
                    else:
                        convert_alias(base_key, "import", alias)
                else:
                    print "1 - Caso imposible en __Gestione_True_Path_Dos:", imp
            
            elif "dir" in tipo:
                # Se importa un paquete.
                if len(mods) == 1:
                    Import_Pakage_True_Path(base_key, os.path.dirname(real_path), attrib)
                    if not alias:
                        convert_alias(base_key, "import", attrib)
                        self.__append_to_freze(attrib)
                    else:
                        convert_alias(base_key, "import", alias)
                
                elif len(mods) == 2:
                    Import_Pakage_True_Path(base_key, os.path.dirname(real_path), attrib)
                    if not alias:
                        convert_alias(base_key, "import", attrib)
                    else:
                        convert_alias(base_key, "import", alias)
                else:
                    print "2 - Caso imposible en __Gestione_True_Path_Dos:", imp
            
            elif "file" in tipo:
                #se importa un modulo
                if len(mods) == 1:
                    Import_Module_True_Path(base_key, os.path.dirname(real_path), attrib)
                    if not alias:
                        self.__append_to_freze(attrib)
                    else:
                        if not attrib in self.freeze:
                            convert_alias(base_key, attrib, alias)
                        else:
                            make_alias(base_key, attrib, alias)
                
                elif len(mods) == 2:
                    Import_Module_True_Path(base_key, os.path.dirname(real_path), attrib)
                    if not alias:
                        self.__append_to_freze(attrib)
                    else:
                        if not attrib in self.freeze:
                            convert_alias(base_key, attrib, alias)
                        else:
                            make_alias(base_key, attrib, alias)
                else:
                    print "3 - Caso imposible en __Gestione_True_Path_Dos:", imp
                
            else:
                # Se importa una Clase.
                real_path = traduce_path(self.workpath, modulo)
                
                if len(mods) == 1:
                    Import_Module_True_Path_From(base_key, os.path.dirname(real_path), mods[0], attrib)
                    if not alias:
                        convert_alias(base_key, "import", attrib)
                    else:
                        convert_alias(base_key, "import", alias)
                
                elif len(mods) == 2:
                    Import_Module_True_Path_From(base_key, os.path.dirname(real_path), mods[1], attrib)
                    if not alias:
                        convert_alias(base_key, "import", attrib)
                    else:
                        convert_alias(base_key, "import", alias)
                
                else:
                    print "4 - Caso imposible en __Gestione_True_Path_Dos:", imp
            
    def __Gestione_self(self, base_key, buffer):
        
        ### Obtener la clase a la que corresponde self.
        textiter = buffer.get_start_iter()
        end_iter = buffer.get_iter_at_mark(buffer.get_insert())
        
        texto = buffer.get_text(textiter, end_iter, True)
        
        clases = []
        for linea in texto.splitlines():
            if linea.startswith("class "):
                clases.append(linea)
                
        if not clases: return
    
        clase = str(clases[-1]).split("class")[1].split("(")[0].strip()
        
        ### Crear temporal
        inicio, fin = buffer.get_bounds()
        texto = buffer.get_text(inicio, fin, 0)
        
        text = ''
        for linea in texto.splitlines():
            
            if linea.endswith("self."):
                pass
                
            else:
                text = "%s%s\n" % (text, linea)
                
        archivo = os.path.join(self.workpath, "temp.py")
        
        arch = open(archivo, "w")
        arch.write(text)
        arch.close()
        
        Import_Module_True_Path_From(base_key, self.workpath, "temp", clase)
        convert_alias(base_key, "import", "self")
        
        try:
            os.remove(archivo)
            
        except:
            pass

    def Run(self, workpath, expresion, buffer):
        """
        Recibe:
            workpath = Directorio base donde debe hurgar Spyder.
            expresion = lo que el usuario está escribiendo.
            buffer = texto del archivo donde el usuario esta escribiendo.
        """
        
        # FIXME:
        #   Las importaciones se renuevan cuando cambian en el archivo en edición.
        #   Esto tiene el problema de que si se hacen cambios en un módulo que es
        #   importado desde el archivo en edición, esos cambios no se reflejan en
        #   las importaciones.
        
        #if os.path.exists(path): os.remove(path)
        
        ### Determinar importaciones en el archivo
        imports = get_imports(buffer)
        
        ### Determinar Diferencias en importaciones
        reset = self.__get_diff_imports(imports)
        if workpath != self.workpath:
            self.workpath = workpath
            reset = True
            
        if reset:
            self.__clear() ### Eliminar Todo
            self.imports = imports
            
            ### Crear información de nuevos imports
            for imp in self.imports:
                
                if is_py_gi(imp):
                    self.__Gestione_gi(imp, self.__id)
                    
                else:
                    self.__Gestione_False_Path(imp, self.__id)
        
        if expresion == "self":
            self.__Gestione_self(self.__id, buffer)
        
        ### Devolución:
        archivo = shelve.open(path)
        dict = {}
        for key in archivo.keys():
            dict[key] = archivo[key]
        archivo.close()
        
        #print "Control base keys:"
        #print "\t", dict.keys(), "\n"
        
        print "Keys in Dict:"
        for k in dict.get(self.__id, {}).keys():
            print "\t", k
            #for key in dict[self.__id][k].keys():
            #    print "\t\t", key
        
        return dict.get(self.__id, {}).get(expresion, {}).get("lista", [])
    