#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   SpyderHack.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

import os
import sys
import shelve
import types
import commands

BASEPATH = os.path.dirname(__file__)

arch = open("/tmp/JAMediaEditorLog.txt", "w") ### LOG
'''
def UnoRun(im, modulos):
    """
    Casos:
        from JAMedia.JAMedia import JAMediaPlayer, otros . . .
    FIXMEs:
        from JAMediaObjects.JAMediaGestreamer.JAMediaBins import JAMedia_Efecto_bin
    """
    
    #arch.write("1- Intentando importar: %s\n" % str(im))
    
    temp_list = im.split()
    prev = temp_list[1]
    temp_list = temp_list[3:]

    for item in temp_list:
        name = item.replace(",", "").strip()
        modulos[name] = []
        
        try:
            mod = __import__("%s" % prev)
            modulo = mod.__getattribute__(str(prev.split(".")[-1]))
            modulos_name = modulo.__getattribute__(name)
            #arch.write("\t1- Se importó: %s\n" % (str(modulos_name)))
            
            for func in dir(modulos_name):
                try:
                    attr_name = getattr(modulos_name, func).__name__
                    if not "GObjectMeta" in attr_name and not attr_name.endswith("__"):
                        modulos[name].append(attr_name)
                        #arch.write("\t1- Se importó: %s\n" % getattr(modulos_name, func).__name__)
                    
                except:
                    #arch.write("\t\t1- No se pudo importar: %s %s %s\n" % (str(prev), str(name), str(func)))
                    # FIXME: casos como: JAMedia.JAMedia JAMediaPlayer __dict__
                    pass
            
        except:
            # FIXME: caso: JAMediaObjects.JAMediaGstreamer.JAMediaBins JAMedia_Efecto_bin
            # La solucion parece ser copiar el instrospector a ese directorio y hacer el import allí.
            # Esto además cambiará el caso de importacion actual, ya que sería: from JAMediaBins JAMedia_Efecto_bin
            #arch.write("\t\t1- No se pudo importar: %s %s\n" % (str(prev), str(name)))
            pass'''
            
def evaluar_import(im):
    
    if "from" in im:
        if "gi.repository" in im and not " as " in im and not "*" in im:
            return 0
        
        elif "." in im and not " as " in im and not "*" in im:
            # from JAMedia.JAMedia import JAMediaPlayer, otros . . .
            return 1
        
        elif not "." in im and not " as " in im and not "*" in im:
            # from JAMedia import JAMediaPlayer, otros . . .
            return 2
        
    else:
        if not "." in im and not " as " in im and not "*" in im:
            # import os, sys, commands
            return 3
        
        elif "." in im and " as " in im:
            #import JAMediaObjects.JAMediaYoutube as YT
            return 4

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
        
        if os.path.exists(temp_path):
            return (temp_path, "dir", imports)
        
        else:
            return (None, None, imports)
    
def Run(workpath, expresion, imports):
    """
    path = Donde debe guardar el diccionario.
    workpath = Directorio base donde debe hurgar Spyder.
    """
    '''
    print "*** Frase que llama a SpyderHack:", expresion
    print "*** workpath:", workpath
    print "*** imports:", imports'''
    
    path = os.path.join("/dev/shm", "shelvein")
    
    archivo = shelve.open(path)
    for key in archivo.keys():
        del(archivo[key])
    archivo.close()
    
    for im in imports:
        
        valor = evaluar_import(im)
        
        if valor == 0:
            ### Todo Gtk 3
            ejecutable = os.path.join(BASEPATH, "Cero_Run.py")
            imp = im.replace(",", " ")
            commands.getoutput('python %s %s %s' % (ejecutable, path, imp))
            
            if not "from" in expresion and not "import" in expresion and "." in expresion:
                ejecutable = os.path.join(BASEPATH, "Dynamic_Cero_Run.py")
                commands.getoutput('python %s %s %s' % (ejecutable, path, expresion))
            
        if valor == 1:
            (relative_path, tipo, lista_imports) = get_dir(im, valor, workpath)
            
            if tipo == "dir":
                # En este caso, lo que se importa es una lista de módulos, por lo tanto:
                #   Su Spyder se mueve a relative_path.
                #   Importa los módulos.
                #   Guarda la información.
                #   Retorna un valor.
                
                ejecutable = os.path.join(relative_path, "UnoDir_Run.py")
                uno = os.path.join(BASEPATH, "UnoDir_Run.py")
                commands.getoutput('cp %s %s' % (uno, relative_path))
                commands.getoutput('python %s %s %s' % (ejecutable, path, lista_imports))
                os.remove(ejecutable)
                
                #if not "from" in expresion and not "import" in expresion and "." in expresion:
                
            elif tipo == "file":
                # En este caso, lo que se importa es una lista de Clases o Funciones, por lo tanto:
                #   Su espyder se mueve os.dirname(relative_path).
                #   Importa el módulo.
                #   Importa las clases o funciones solicitadas.
                #   Guarda la información.
                #   Retorna un Valor.
                pass
            
            else:
                # En este caso:
                #   Se ejecuta el Spyder sin moverlo de lugar.
                #   Importa las clases, funciones o modulos solicitados.
                #   Guarda la información.
                #   Retorna un Valor.
                pass
            
            #UnoRun(im, modulos)
    
    modulos = {}
    archivo = shelve.open(path)
    
    for key in archivo.keys():
        modulos[key] = archivo[key]
        
    archivo.close()
    arch.close()
    
    return modulos
