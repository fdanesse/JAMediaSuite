#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
	name = "JAMedia",
	version = "15.0.0",
	author = "Flavio Danesse",
	author_email = "fdanesse@gmail.com",
	url = "https://sites.google.com/site/sugaractivities/jamediaobjects/jam",
	license = "GPL3",

	scripts = ["jamedia_run.sh", "jamedia_uninstall.sh"],

	py_modules = [],

	data_files =[
		("/usr/share/applications/", ["JAMedia.desktop"]),
		("",[
			"JAMediaUninstall.py",
			"JAMedia",
			"Estilo.css"]),

		("Iconos/",[
		    "Iconos/agregar.svg",
			"Iconos/dialog-ok.svg",
			"Iconos/help-3.svg",
			"Iconos/JAMediaCredits.svg",
			"Iconos/JAMedia.svg",
			"Iconos/play.svg",
			"Iconos/sonido.svg",
			"Iconos/button-cancel.svg",
			"Iconos/help-1.svg",
			"Iconos/help-4.svg",
			"Iconos/jamedia_cursor.svg",
			"Iconos/lista.svg",
			"Iconos/rotar.svg",
			"Iconos/stop.svg",
			"Iconos/configurar.svg",
			"Iconos/help-2.svg",
			"Iconos/iconplay.svg",
			"Iconos/JAMedia-help.svg",
			"Iconos/pausa.svg",
			"Iconos/siguiente.svg",
			"Iconos/video.svg"]),
            ])

import commands
commands.getoutput("chmod -R 755 /usr/share/JAMedia")
commands.getoutput("chmod 755 /usr/share/applications/JAMedia.desktop")
