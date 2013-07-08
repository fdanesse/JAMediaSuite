#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaMantree.py por:
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

import os

from gi.repository import Gtk
#from gi.repository import Gdk
#from gi.repository import GdkPixbuf
#from gi.repository import GObject

from Widgets import TreeView
from Widgets import SourceView

BASEPATH = os.path.dirname(__file__)

def ConstruyeMan():
    """
    Construye archivo shelve con información del man.
    """
    
    comandos = {
        "Directorios y Unidades":{
            "ls":"",
            "cd":"",
            "cp":"",
            "rm":"",
            "mkdir":"",
            "pwd":"",
            "dd":"",
            "mount":"",
            "umount":"",
            "mv":"",
            "df":"",
            "chmod":"",
            "chown":"",
            "find":"",
            "grep":"",
            "gzip":"",
            "cat":"",
            "more":"",
            "less":"",
            "tree":"",
            "du":"",
            "wget":"",
            "whereis":"",
            },
        "Redes":{
            "ifconfig":"",
            "ssh":"",
            "scp":"",
            },
        "Procesos y memoria":{
            "top":"",
            "ps":"",
            "free":"",
            "vmstat":"",
            "kill":"",
            "killall":"",
            },
        "Usuarios":{
            "w":"",
            "passwd":"",
            },
        "Hardware":{
            "lspci":"",
            "lshw":"",
            "xrandr":"",
            },
        }
    
    import commands
    temp_path = "/tmp/out.txt"
    
    for grupo in comandos.keys():
        for comando in comandos[grupo]:
            ### Obtener Man page.
            expresion = "man %s > %s" % (comando, temp_path)
            commands.getoutput(expresion)
            
            ### Actualizar Diccionario del man.
            file = open(temp_path, "r")
            comandos[grupo][comando] = file.read()
            file.close()
            
    ### Almacenar mantree.
    import shelve
    path = os.path.join(BASEPATH, "man.slv")
    archivo = shelve.open(path)
    
    for item in comandos.keys():
        archivo[item] = comandos[item]
        
    archivo.close()
    
class JAMediaManTree(Gtk.Window):
    
    __gtype_name__ = 'WindowManTree'
    
    def __init__(self):
        
        Gtk.Window.__init__(self)
        
        self.set_size_request(640, 480)
        
        basebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        ### Abrir man.
        import shelve
        path = os.path.join(BASEPATH, "man.slv")
        archivo = shelve.open(path)
        
        dict = {}
        for key in archivo.keys():
            dict[key] = archivo[key]
            
        archivo.close()
        
        self.panel = Panel(dict)
        
        basebox.pack_start(self.panel, True, True, 0)
        
        self.add(basebox)
        
        self.show_all()
        
        import sys
        self.connect("destroy", sys.exit)
        
class Panel(Gtk.Paned):
    
    __gtype_name__ = 'PanelManTree'
    
    def __init__(self, dict):
        
        Gtk.Paned.__init__(self,
            orientation=Gtk.Orientation.HORIZONTAL)
            
        self.dict = dict
        self.treeview = TreeView(self.dict)
        self.sourceview = SourceView()
        
        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scroll.add_with_viewport(self.treeview)
        scroll.set_size_request(200,-1)
        
        self.pack1(scroll, resize = False, shrink = False)
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scroll.add_with_viewport(self.sourceview)
        
        self.pack2(scroll, resize = True, shrink = False)
        
        self.show_all()
        
        self.treeview.connect('nueva-seleccion', self.__seleccion)
        
    def __seleccion(self, widget, seleccion):
        """
        Cuando se selecciona un item en la lista.
        """
        
        if not self.dict.get(seleccion, False):
            for key in self.dict.keys():
                if self.dict[key].get(seleccion, False):
                    self.sourceview.get_buffer().set_text(self.dict[key][seleccion])
                    return
        
if __name__=="__main__":
    #ConstruyeMan()
    JAMediaManTree()
    Gtk.main()
    