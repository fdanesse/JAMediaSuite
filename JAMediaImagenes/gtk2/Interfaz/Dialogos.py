#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk


class OpenDialog(gtk.FileChooserDialog):

    def __init__(self, parent=None, dir_path=False):

        gtk.FileChooserDialog.__init__(self, parent=parent,
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            title="Abrir Archivo",
            buttons=(
                "Abrir", gtk.RESPONSE_ACCEPT,
                "Cancelar", gtk.RESPONSE_CANCEL))
        #FIXME: Agregar preview para imagen seleccionada
        self.set_border_width(15)
        if dir_path:
            self.set_current_folder_uri("file://%s" % dir_path)
        self.set_select_multiple(False)
        filtro = gtk.FileFilter()
        filtro.set_name("image")
        filtro.add_mime_type("image/*")
        self.add_filter(filtro)
