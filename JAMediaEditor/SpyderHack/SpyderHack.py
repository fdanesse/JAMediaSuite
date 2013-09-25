#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   SpyderHack.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

import os
import sys
import shelve
import commands
import time

BASEPATH = os.path.dirname(__file__)
path = os.path.join("/dev/shm", "shelvein")

def Import_Module_False_Path(base_key, modulo):
    
    ejecutable = os.path.join(BASEPATH, "Dir_Modulo.py")
    print commands.getoutput('python %s %s %s' % (ejecutable, base_key, modulo))

def Import_Module_False_Path_From(base_key, modulo, attrib):
    
    ejecutable = os.path.join(BASEPATH, "Dir_Attrib.py")
    print commands.getoutput('python %s %s %s %s' % (ejecutable, base_key, modulo, attrib))
    
def Import_Module_False_Path_From_Recursive(base_key, modulo1, modulo2, modulo3):
    
    ejecutable = os.path.join(BASEPATH, "Recursive_Dir_Attrib.py")
    print commands.getoutput('python %s %s %s %s %s' % (ejecutable, base_key, modulo1, modulo2, modulo3))
    
def Import_Module_gi(base_key, attrib):

    ejecutable = os.path.join(BASEPATH, "Dir_Modulo_gi.py")
    print commands.getoutput('python %s %s %s' % (ejecutable, base_key, attrib))
    
def Import_Module_gi_From(base_key, modulo, attrib):

    ejecutable = os.path.join(BASEPATH, "Dir_Attrib_gi.py")
    print commands.getoutput('python %s %s %s %s' % (ejecutable, base_key, modulo, attrib))

'''
def get_dir(im, valor, workpath):
    """
    Modelo:
        from JAMediaObjects.JAMediaGstreamer.JAMediaBins import JAMedia_Efecto_bin, JAMedia_Camara_bin
        
    Devuelve:
        directorio, archivo o None según corresponda.
        "dir", "file" o None según valor anterior.
        Lista de Módulos, clases o funciones a importar.
    """
    
    if valor == 1:
        
        prevs = im.split()[1]       # JAMediaObjects.JAMediaGstreamer.JAMediaBins
        imports = im.split()[3:]    # JAMedia_Efecto_bin,JAMedia_Camara_bin # JAMedia_Efecto_bin, JAMedia_Camara_bin
        
        temp_imports = []
        for imp in imports:
            
            if "," in imp:
                list = imp.split(",")
                
                for l in list:
                    temp_imports.append(l)
                    
            else:
                temp_imports.append(imp)
        imports = temp_imports
        
        dirs = prevs.split(".")
        
        temp_path = workpath
        for dir in dirs:
            temp_path = os.path.join(temp_path, dir)
            
        if os.path.exists("%s.py" % temp_path):
            return ("%s.py" % temp_path, "file", imports)
        
        elif os.path.exists(temp_path):
            return (temp_path, "dir", imports)
        
        else:
            return (None, None, imports)
        
    elif valor == 2 or valor == 3:
        
        if valor == 3: print "*", valor, im
        
        prevs = im.split()[1]       # JAMediaObjects.JAMediaGstreamer.JAMediaBins
        imports = im.split()[3:]    # JAMedia_Efecto_bin,JAMedia_Camara_bin # JAMedia_Efecto_bin, JAMedia_Camara_bin
        
        temp_imports = []
        for imp in imports:
            
            if "," in imp:
                list = imp.split(",")
                
                for l in list:
                    temp_imports.append(l)
                    
            else:
                temp_imports.append(imp)
        imports = temp_imports
        
        temp_path = os.path.join(workpath, prevs)
        
        if os.path.exists("%s.py" % temp_path):
            return ("%s.py" % temp_path, "file", imports)
        
        elif os.path.exists(temp_path):
            return (temp_path, "dir", imports)
        
        else:
            return (None, None, imports)
        
    else:
        #print "*", valor, im
        pass
'''

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
    
    if os.path.exists(real_path):
        if os.path.isdir(real_path):
            return "dir"
        
    elif not os.path.exists(real_path):
        posible = "%s.py" % real_path
        if os.path.exists(posible):
            if os.path.isfile(posible):
                return "file"
            
    return False
    
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
    
    print "-- Construyendo Alias:", alias, "==", modulo_attrib
    
    mod = shelve.open(path)
    
    try:
        key_dict = {}
        for key in mod[str(workpath)].keys():
            key_dict[key] = mod[str(workpath)][key]
            
        dict = mod[str(workpath)][modulo_attrib]#.get(attrib, {})
        
        key_dict[alias] = dict
        
        mod[str(workpath)] = key_dict
        
    except:
        print "-- Error en __make_alias", workpath, modulo_attrib, alias
        
    mod.close()

def convert_alias(workpath, modulo_attrib, alias):
    
    print "-- Convirtiendo Alias:", alias, "Remplaza a:", modulo_attrib
    
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
        print "-- Error en __convert_alias", workpath, modulo_attrib, alias
        
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
            
    def __Gestione_False_Path(self, imp, base_key):
        """
        Cuando no se conoce el path desde donde se importa,
        no es un paquete o modulo de usuario.
        """
        
        if is_py_gi(imp):
            if not " as " in imp and not " *" in imp:
                if imp.startswith("from "):
                    
                    attribs = parse_modulos(imp.split()[3:])
                    mods = parse_path_modulos(imp.split()[1])
                    
                    if len(mods) == 1:
                        #   from gi import repository, importer
                        # FIXME: Este caso no funciona.
                        #for attrib in attribs:
                        #    Import_Module_gi(base_key, attrib)
                        #    self.__append_to_freze(attrib)
                        pass
                    
                    elif len(mods) == 2:
                        #   from gi.repository import Gtk, Gst
                        for attrib in attribs:
                            Import_Module_gi(base_key, attrib)
                            self.__append_to_freze(attrib)
                            
                    else:
                        print "Caso imposible en __Gestione_False_Path:", imp
                        
                elif imp.startswith("import "):
                    
                    modulos = parse_modulos(imp.split()[1:])
                    
                    for modulo in modulos:
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
                            print "Caso imposible en __Gestione_False_Path:", imp
                            
                else:
                    print "Caso no previsto en __Gestione_False_Path:", imp
                    
            elif " as " in imp and not " *" in imp:
                if imp.startswith("from "):
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
                        print "Caso imposible en __Gestione_False_Path:", imp
                        
                elif imp.startswith("import "):
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
                        print "Caso imposible en __Gestione_False_Path:", imp
                        
                else:
                    print "Caso no previsto en __Gestione_False_Path:", imp
                    
            else:
                print "Caso no previsto en __Gestione_False_Path:", imp
        
        else:
            if not " as " in imp and not " *" in imp:
                if imp.startswith("from "):
                    attribs = parse_modulos(imp.split()[3:])
                    mods = parse_path_modulos(imp.split()[1])
                    
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
                        print "Caso imposible en __Gestione_False_Path:", imp
                    
                elif imp.startswith("import "):
                    modulos = parse_modulos(imp.split()[1:])
                    
                    for modulo in modulos:
                        mods = parse_path_modulos(modulo)
                        
                        if len(mods) == 1:
                            #   import os, gtk, sys
                            Import_Module_False_Path(base_key, mods[0])
                            self.__append_to_freze(mods[0])
                            
                        elif len(mods) == 2:
                            #   import gtk.gdk
                            Import_Module_False_Path_From(base_key, mods[0], mods[1])
                            convert_alias(base_key, mods[1], "%s.%s" % (mods[0], mods[1]))
                            self.__append_to_freze("%s.%s" % (mods[0], mods[1]))
                            
                        else:
                            print "Caso imposible en __Gestione_False_Path, startswith('import'):", imp, len(mods)
                            
                else:
                    print "1- Caso no previsto en __Gestione_False_Path:", imp
                    
            elif " as " in imp and not " *" in imp:
                if imp.startswith("from "):
                    attrib = imp.split()[3]
                    modulo = imp.split()[1]
                    alias = imp.split()[5]
                    
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
                        Import_Module_False_Path_From_Recursive(base_key, modulos[0], modulos[1], attrib) # gtk.gdk.Color
                        convert_alias(base_key, "%s.%s.%s" % (modulos[0], modulos[1], attrib), alias) # Z = gtk.gdk.Color
                        
                    else:
                        print "Caso imposible en __Gestione_False_Path:", imp
                        
                elif imp.startswith("import "):
                    modulo = imp.split()[1]
                    alias = imp.split()[-1]
                    
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
                        print "Caso imposible en __Gestione_False_Path:", imp

                else:
                    print "2- Caso no previsto en __Gestione_False_Path:", imp
                    
            elif "from " in imp and " *" in imp:
                ### Casos:
                #   from os import *
                #   from os.path import *
                
                pass
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
                    print "Caso imposible en __Gestione_False_Path:", imp"""
                    
            else:
                print "3- Caso no previsto en __Gestione_False_Path:", imp
            
            # FIXME: Se puede Agregar Verificacion para casos Como el de JAMediaObjetcs.
            
    def __Gestione_True_Path(self, imp, base_key):
        
        print "--- PATH:", self.workpath
    
    def Run(self, workpath, expresion, buffer):
        """
        Recibe:
            workpath = Directorio base donde debe hurgar Spyder.
            expresion = lo que el usuario está escribiendo.
            buffer = texto del archivo donde el usuario esta escribiendo.
        """
        
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
                real_path = traduce_path(workpath, imp.split()[1])
                is_path = determine_path(real_path)
                
                if is_path:
                    self.__Gestione_True_Path(imp, self.__id)
                
                else:
                    self.__Gestione_False_Path(imp, self.__id)
        
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
    
    '''
    for im in imports:
        
        valor = evaluar_import(im)
        is_dir = get_dir(im, valor, workpath)

            elif valor == 1:
                (relative_path, tipo, lista_imports) = is_dir
                
                if tipo == "dir":
                    # En este caso, lo que se importa es una lista de módulos, por lo tanto:
                    #   Su Spyder se mueve a relative_path.
                    #   Importa los módulos.
                    #   Guarda la información.
                    #   Retorna un valor.
                    
                    ejecutable = os.path.join(relative_path, "Dir_Modulo.py")
                    uno = os.path.join(BASEPATH, "Dir_Modulo.py")
                    commands.getoutput('cp %s %s' % (uno, relative_path))
                    commands.getoutput('python %s %s %s' % (ejecutable, path, lista_imports))
                    os.remove(ejecutable)
                    
                    #if not "from" in expresion and not "import" in expresion and "." in expresion:
                    
                elif tipo == "file":
                    # En este caso, lo que se importa es una lista de Clases o Funciones, por lo tanto:
                    #   Su spyder se mueve os.dirname(relative_path).
                    #   Importa el módulo.
                    #   Importa las clases o funciones solicitadas.
                    #   Guarda la información.
                    #   Retorna un Valor.
                    
                    relative_path = os.path.dirname(relative_path)
                    modulo = im.split()[1].split(".")[-1].strip()
                    
                    ejecutable = os.path.join(relative_path, "Dir_Attrib.py")
                    dos = os.path.join(BASEPATH, "Dir_Attrib.py")
                    commands.getoutput('cp %s %s' % (dos, relative_path))
                    commands.getoutput('python %s %s %s %s' % (ejecutable, path, modulo, lista_imports))
                    os.remove(ejecutable)
                    
                    #if not "from" in expresion and not "import" in expresion and "." in expresion:
                    
                else:
                    print "Este caso no debiera existir: Caso 1 - tipo = None", relative_path, tipo, lista_imports
                    
            elif valor == 2:
                # En este caso, lo que se importa es una lista de módulos,
                # Clases o Funciones desde el path actual, por lo tanto:
                #   Su spyder no se mueve.
                #   Importa el módulo.
                #   Importa las clases o funciones solicitadas.
                #   Guarda la información.
                #   Retorna un Valor.
                
                (relative_path, tipo, lista_imports) = is_dir
                
                if tipo == "dir" and os.path.exists(relative_path):
                    ejecutable = os.path.join(relative_path, "Dir_Modulo.py")
                    dos = os.path.join(BASEPATH, "Dir_Modulo.py")
                    commands.getoutput('cp %s %s' % (dos, relative_path))
                    commands.getoutput('python %s %s %s' % (ejecutable, path, lista_imports))
                    os.remove(ejecutable)
                
                    #if not "from" in expresion and not "import" in expresion and "." in expresion:
            
                elif tipo == None:
                    modulo = im.split()[1]
                    ejecutable = os.path.join(BASEPATH, "Dir_Attrib.py")
                    commands.getoutput('python %s %s %s %s' % (ejecutable, path, modulo, lista_imports))
                
                    #if not "from" in expresion and not "import" in expresion and "." in expresion:
                    
                else:
                    "Caso 2 no previsto:", im'''
