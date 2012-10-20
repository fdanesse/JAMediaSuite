#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMFileSystem.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
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

# Path => http://docs.python.org/library/os.path.html?highlight=islink
# Tipos de Sonidos => http://docs.python.org/library/sndhdr.html
# Tipos de Imagenes => http://docs.python.org/library/imghdr.html
# http://docs.python.org/library/archiving.html?highlight=zipfile

import os
import commands
import shutil

from gi.repository import GObject
from gi.repository import Gio
from gi.repository import Gtk

def describe_uri(uri):
    """ Explica de que se trata el uri, si existe."""
    
    existe = False
    try:
        existe = os.path.exists(uri)
    except:
        return None
    if existe:
        unidad = os.path.ismount(uri)
        directorio = os.path.isdir(uri)
        archivo = os.path.isfile(uri)
        enlace = os.path.islink(uri)
        return [unidad, directorio, archivo, enlace]
    else:
        return None

def describe_acceso_uri(uri):
    """ Devuelve los permisos de acceso sobre una uri."""
    
    existe = False
    try:
        existe = os.access(uri, os.F_OK)
    except:
        return None
    if existe:
        lectura = os.access(uri, os.R_OK)
        escritura = os.access(uri, os.W_OK)
        ejecucion = os.access(uri, os.X_OK)
        return [lectura, escritura, ejecucion]
    else:
        return None
    
def describe_archivo(archivo):
    """ Devuelve el tipo de un archivo (imagen, video, texto).
    -z, --uncompress para ver dentro de los zip."""
    
    datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
    retorno = ""
    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)
    return retorno

def get_path_link(link):
    """Devuelve el path al que apunta un link."""
    
    return os.readlink(link)

def get_tamanio(path):
    """Devuelve tamaño en bytes."""
    
    return os.path.getsize(path)

def borrar (origen):
    try:
        if os.path.isdir(origen):
            shutil.rmtree("%s" % (os.path.join(origen)) )
        elif os.path.isfile(origen):
            os.remove("%s" % (os.path.join(origen)) )
        else:
            return False
        return True
    except:
        print "ERROR Al Intentar Borrar un Archivo"
        return False
    
def mover(origen, destino):
    try:
        expresion = "mv \"" + origen + "\" \"" + destino + "\""
        os.system(expresion)
        return True
    except:
        print "ERROR Al Intentar Mover un Archivo"
        return False
    
def copiar(origen, destino):
    try:
        if os.path.isdir(origen):
            expresion = "cp -r \"" + origen + "\" \"" + destino + "\""
        elif os.path.isfile(origen):
            expresion = "cp \"" + origen + "\" \"" + destino + "\""
        os.system(expresion)
        return True
    except:
        print "ERROR Al Intentar Copiar un Archivo"
        return False
    
def crear_directorio (origen, directorionuevo):
    try:
        if os.path.isdir(origen) or os.path.ismount(origen):
            expresion = 'mkdir \"%s\"' % (os.path.join(origen, directorionuevo))
            os.system(expresion)
            return True
        else:
            return False
    except:
        print "ERROR Al Intentar Crear un Directorio"
        return False
    
def get_programa(programa):
    """ Devuelve true si programa se encuentra
    instaldo y false si no lo está."""
    
    paths = os.environ['PATH'].split(":")
    presente = False
    for directorio in paths:
        if os.path.exists(directorio):
            datos = os.listdir(directorio)
            if programa in datos:
                presente = True
                break
        else:
            print "Directorio Inexistente en el path", directorio
    # print programa, "Instalado en el sistema:", presente
    return presente

def verificar_Gstreamer():
    presente = False
    try:
        import gi
        gi.require_version('Gst', '1.0')
        presente = True
    except:
        presente = False
    return presente
    

class DeviceManager(GObject.GObject):
    """Demonio para unidades de montaje.
        
        Importa la clase e instánciala.
        
        Seguidamente, para obtener las unidades montadas
        en ese momento, llama a get_unidades.
        
        Para monitorear los cambios posteriormente, conectate a las señales."""
    
    __gsignals__ = {
    'nueva_unidad_conectada': (GObject.SignalFlags.RUN_FIRST,
        None, (GObject.TYPE_PYOBJECT, )),
    'nueva_unidad_desconectada': (GObject.SignalFlags.RUN_FIRST,
        None, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):
        
        GObject.GObject.__init__(self)
        
        self.unidades = {}
        self.demonio_unidades = Gio.VolumeMonitor.get()
        
        self.demonio_unidades.connect('mount-added', self.emit_unidad_conectada)
        self.demonio_unidades.connect('mount-removed', self.emit_unidad_desconectada)
        
    def get_unidades(self):
        """Devuelve una lista de diccionarios que representa
        las unidades montadas actualmente."""
        
        unidades = []
        for punto_montaje in self.demonio_unidades.get_mounts():
            propiedades = self.get_propiedades(punto_montaje)
            unidades.append(propiedades)
        return unidades
            
    def get_propiedades(self, punto_montaje):
        """Devuelve las propiedades de una unidad montada."""
        
        propiedades = {}
        propiedades['label'] = punto_montaje.get_name()
        propiedades['mount_path'] = punto_montaje.get_default_location().get_path()
        return propiedades
    
    def emit_unidad_conectada(self, demonio_unidades, unidad):
        """Cuando se conecta una unidad usb."""
        
        propiedades = self.get_propiedades(unidad)
        self.unidades[unidad] = propiedades
        self.emit('nueva_unidad_conectada', self.unidades[unidad])

    def emit_unidad_desconectada(self, demonio_unidades, unidad):
        """Cuando se desconecta una unidad usb."""
        
        self.emit('nueva_unidad_desconectada', self.unidades[unidad])
        del self.unidades[unidad]


def unidad_conectada(widget = None, senial = None):
    print widget, senial, widget.get_unidades()

def unidad_desconectada(widget = None, senial = None):
    print widget, senial, widget.get_unidades()
    
if __name__=="__main__":
    """Demonio para unidades de montaje."""
    
    manager = DeviceManager()
    manager.connect('nueva_unidad_conectada', unidad_conectada)
    manager.connect('nueva_unidad_desconectada', unidad_conectada)
    Gtk.main()
    
    
#def convert_mpeg(archivo):
#    "avconv -i WakaWaka WakaWaka.mpeg" # ffmpeg

#def convert_mp3(archivo):
#    pass