#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import commands

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import JAMedia
from JAMedia.JAMedia import JAMediaPlayer

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects
from JAMediaObjects import JAMFileSystem as JAMF

JAMediaObjectsPath = JAMediaObjects.__path__[0]
    
class Ventana(Gtk.Window):
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMedia")
        self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.pistas = ""
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaplayer = JAMediaPlayer()
        self.socket.add_id(self.jamediaplayer.get_id())
        self.show_all()
        self.realize()
        
        self.connect("destroy", self.salir)
        self.jamediaplayer.connect('salir', self.salir)
        
        GObject.idle_add(self.setup_init)
        
    def set_pistas(self, pistas):
        
        self.pistas = pistas
        
    def setup_init(self):
        
        self.jamediaplayer.setup_init()
        self.jamediaplayer.pack_standar()
        
        if self.pistas:
            GObject.idle_add(self.jamediaplayer.set_nueva_lista, self.pistas)
        
        self.jamediaplayer.pack_efectos()
        
    def salir(self, widget = None, senial = None):
        
        import commands
        commands.getoutput('killall mplayer')
        sys.exit(0)
        

def get_item_list(path):
    
    if os.path.exists(path):
        if os.path.isfile(path):
            archivo = os.path.basename(path)
            
            if 'audio' in JAMF.describe_archivo(path) or \
                'video' in JAMF.describe_archivo(path):
                    return [archivo, path]
        
    return False

if __name__ == "__main__":
    
    items = []
    
    if len(sys.argv) > 1:
        
        for campo in sys.argv[1:]:
            path = os.path.join(campo)
            
            if os.path.isfile(path):
                item = get_item_list(path)
                
                if item:
                    items.append( item )
                    
            elif os.path.isdir(path):
                
                for arch in os.listdir(path):
                    newpath = os.path.join(path, arch)
                    
                    if os.path.isfile(newpath):
                        item = get_item_list(newpath)
                        
                        if item:
                            items.append( item )
                            
        if items:
            jamedia = Ventana()
            jamedia.set_pistas(items)
            
        else:
            jamedia = Ventana()
        
    else:
        jamedia = Ventana()
        
    Gtk.main()
    
    '''
    items = []
    
    if len(sys.argv) > 1:
        for item in sys.argv[1:]:
            path = os.path.join(item)
            
            if os.path.exists(path):
                # FIXME: Agregar detectar tipo de archivo
                # para que abra solo video y audio.
                archivo = os.path.basename(path)
                items.append( [archivo,path] )
                
        if items:
            jamedia = Ventana()
            jamedia.set_pistas(items)
            
        else:
            jamedia = Ventana()
        
    else:
        jamedia = Ventana()
        
    Gtk.main()'''
    