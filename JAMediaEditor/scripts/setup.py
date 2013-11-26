#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
	name = "JAMediaEditor",
	version = "0.0.2",
	author = "Flavio Danesse - Ignacio Rodriguez - Cristian Garcia",
	author_email = "fdanesse@gmail.com - nachoel01@gmail.com - cristian99garcia@gmail.com",
	url = "https://sites.google.com/site/sugaractivities/jamediaobjects",
	license = "GPL3",

	scripts = ["jamediaeditor_run", "jamediaeditor_uninstall"],

	py_modules = ["JAMediaEditor"],

	data_files =[
		("/usr/share/applications/", ["JAMediaEditor.desktop"]),
		("",[
			"setup.py",
			"jamediaeditor.xml",
			"JAMediaEditor.py",
			"JAMediaEditor.desktop",
			"MANIFEST",
			"COPYING",
			"jamediaeditor_uninstall",
			"setup.cfg",
			"AUTHORS",
			"jamediaeditor_run"]),

		("JAMediaPyGiHack/SpyderHack/",[
			"JAMediaPyGiHack/SpyderHack/Gi_Check.py",
			"JAMediaPyGiHack/SpyderHack/Check.py",
			"JAMediaPyGiHack/SpyderHack/Dir_Modulo.py",
			"JAMediaPyGiHack/SpyderHack/Dir_Gi_Modulo.py",
			"JAMediaPyGiHack/SpyderHack/Make_gi_doc.py",
			"JAMediaPyGiHack/SpyderHack/Make_doc.py"]),

		("JAMediaGstreamer/",[
			"JAMediaGstreamer/Widgets.py",
			"JAMediaGstreamer/__init__.py",
			"JAMediaGstreamer/JAMediaGstreamer.py"]),

		("JAMediaEditor/pyflakes/scripts/",[
			"JAMediaEditor/pyflakes/scripts/pyflakes.py",
			"JAMediaEditor/pyflakes/scripts/__init__.py"]),

		("JAMediaObjects/",[
			"JAMediaObjects/JAMediaGlobales.py",
			"JAMediaObjects/__init__.py",
			"JAMediaObjects/JAMediaTerminal.py"]),

		("JAMediaEditor/",[
			"JAMediaEditor/Widgets.py",
			"JAMediaEditor/WorkPanel.py",
			"JAMediaEditor/BasePanel.py",
			"JAMediaEditor/Widget_Setup.py",
			"JAMediaEditor/InfoNotebook.py",
			"JAMediaEditor/Toolbars.py",
			"JAMediaEditor/__init__.py",
			"JAMediaEditor/plantilla",
			"JAMediaEditor/SourceView.py",
			"JAMediaEditor/ApiProyecto.py",
			"JAMediaEditor/Check2.py",
			"JAMediaEditor/DialogoProyecto.py",
			"JAMediaEditor/Estilo.css",
			"JAMediaEditor/Licencias.py",
			"JAMediaEditor/Check1.py"]),

		("JAMediaPyGiHack/",[
			"JAMediaPyGiHack/JAMediaPyGiHack.py",
			"JAMediaPyGiHack/Widgets.py",
			"JAMediaPyGiHack/BasePanel.py",
			"JAMediaPyGiHack/__init__.py",
			"JAMediaPyGiHack/Globales.py",
			"JAMediaPyGiHack/ApiWidget.py"]),

		("JAMediaEditor/SpyderHack/",[
			"JAMediaEditor/SpyderHack/Dir_Attrib_True.py",
			"JAMediaEditor/SpyderHack/__init__.py",
			"JAMediaEditor/SpyderHack/Dir_Modulo_gi.py",
			"JAMediaEditor/SpyderHack/SpyderHack.py",
			"JAMediaEditor/SpyderHack/Dir_Modulo.py",
			"JAMediaEditor/SpyderHack/Dir_Modulo_True.py",
			"JAMediaEditor/SpyderHack/Dir_Pakage_True.py",
			"JAMediaEditor/SpyderHack/Dir_Attrib_gi.py",
			"JAMediaEditor/SpyderHack/Dir_Attrib.py",
			"JAMediaEditor/SpyderHack/Recursive_Dir_Attrib.py"]),

		("JAMediaObjects/Iconos/",[
			"JAMediaObjects/Iconos/document-open.svg",
			"JAMediaObjects/Iconos/media-playback-start.svg",
			"JAMediaObjects/Iconos/edit-select-all.svg",
			"JAMediaObjects/Iconos/JAMediaEditorCredits.svg",
			"JAMediaObjects/Iconos/edit-find.svg",
			"JAMediaObjects/Iconos/editcut.svg",
			"JAMediaObjects/Iconos/editpaste.svg",
			"JAMediaObjects/Iconos/JAMediaEditor2.svg",
			"JAMediaObjects/Iconos/python.svg",
			"JAMediaObjects/Iconos/tab-new.svg",
			"JAMediaObjects/Iconos/button-cancel.svg",
			"JAMediaObjects/Iconos/go-next.svg",
			"JAMediaObjects/Iconos/edit-undo.svg",
			"JAMediaObjects/Iconos/PyGiHackCredits.svg",
			"JAMediaObjects/Iconos/bash.svg",
			"JAMediaObjects/Iconos/otros.svg",
			"JAMediaObjects/Iconos/document-new.svg",
			"JAMediaObjects/Iconos/gtk-edit.svg",
			"JAMediaObjects/Iconos/const.svg",
			"JAMediaObjects/Iconos/edit-redo.svg",
			"JAMediaObjects/Iconos/media-playback-stop.svg",
			"JAMediaObjects/Iconos/font.svg",
			"JAMediaObjects/Iconos/document-properties.svg",
			"JAMediaObjects/Iconos/edit-copy.svg",
			"JAMediaObjects/Iconos/def.svg",
			"JAMediaObjects/Iconos/PygiHack.svg",
			"JAMediaObjects/Iconos/document-save-as.svg",
			"JAMediaObjects/Iconos/class.svg",
			"JAMediaObjects/Iconos/document-save.svg",
			"JAMediaObjects/Iconos/go-next-rtl.svg"]),

		("JAMediaEditor/pyflakes/",[
			"JAMediaEditor/pyflakes/messages.py",
			"JAMediaEditor/pyflakes/__init__.py",
			"JAMediaEditor/pyflakes/checker.py"])])

import os
import commands

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local'))

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local/bin')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local/bin'))

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local/share')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local/share'))

mime_path = os.path.join(os.environ["HOME"],
    ".local/share/mime/packages/")

if not os.path.exists(mime_path):
    os.mkdir(mime_path)

commands.getoutput("cp jamediaeditor.xml %s" % mime_path)

user = commands.getoutput("whoami")
commands.getoutput("chown %s:%s %s" % (user, user, os.path.join(
    mime_path, "jamediaeditor.xml")))

commands.getoutput("chmod -R 755 /usr/local/share/JAMediaEditor")
commands.getoutput("chmod 755 /usr/share/applications/JAMediaEditor.desktop")
commands.getoutput("update-desktop-database %s" % os.path.join(
    "/usr/share/applications/"))
commands.getoutput('update-mime-database %s' % mime_path)
