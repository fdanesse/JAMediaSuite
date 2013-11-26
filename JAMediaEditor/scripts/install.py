#!/usr/bin/env python
# -*- coding: utf-8 -*-

# JAMediaEditor.py (path relativo)
# /JAMediaObjects/Iconos/JAMediaEditor2.svg (path relativo)
# GTK;Development;IDE (GTK;GNOME;Juegos;)
# application/x-ide

import os
import commands

self_path = os.path.abspath(os.path.dirname(__file__))

NAME = self_path.split("/")[-1]

final_path = os.path.join(os.environ["HOME"], NAME)
print "final_path =", final_path

### borrar anterior.
if os.path.exists(final_path):
    print "Eliminando Version Anterior."
    commands.getoutput('rm -r %s' % (final_path))

### Copiar proyecto a destino final.
commands.getoutput('cp -r %s %s' % (self_path, os.environ["HOME"]))
commands.getoutput('chmod 755 -R %s' % final_path)
print "Copiando:", self_path, "En:", os.environ["HOME"]

main_path = os.path.join(final_path, "JAMediaEditor.py")
icon_path = final_path + "/JAMediaObjects/Iconos/JAMediaEditor2.svg"

desktoptext = """[Desktop Entry]
Encoding=UTF-8
Name=%s
GenericName=%s
Exec=%s
Terminal=false
Type=Application
Icon=%s
Categories=%s
MimeType=%s;text/plain;text/x-chdr;text/x-csrc;text/x-c++hdr;text/x-c++src;text/x-java;text/x-dsrc;text/x-pascal;text/x-perl;text/x-python;application/x-php;application/x-httpd-php3;application/x-httpd-php4;application/x-httpd-php5;application/xml;text/html;text/css;text/x-sql;text/x-diff;
Keywords=Code;Editor;Programming;
StartupNotify=true""" % (NAME, NAME, main_path,
    icon_path, "GTK;Development;IDE", "application/x-ide")

print "\t Generando Archivo Desktop:"
print desktoptext

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local'))

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local/bin')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local/bin'))

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local/share')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local/share'))

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local/share/applications')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local/share/applications'))

if not os.path.exists(os.path.join(os.environ["HOME"],
    '.local/share/mime')):
    os.mkdir(os.path.join(os.environ["HOME"], '.local/share/mime'))

mime_path = os.path.join(os.environ["HOME"],
    ".local/share/mime/packages/")

if not os.path.exists(mime_path):
    os.mkdir(mime_path)

commands.getoutput("cp jamediaeditor.xml %s" % mime_path)

desktop = open(os.path.join(os.environ["HOME"],
    ".local/share/applications/%s.desktop" % NAME), "w")
desktop.write(desktoptext)
desktop.close()

commands.getoutput('chmod 755 %s' % os.path.join(os.environ["HOME"],
    ".local/share/applications/%s.desktop" % NAME))
commands.getoutput("update-desktop-database %s" % os.path.join(
    os.environ["HOME"], ".local/share/applications/"))
commands.getoutput('update-mime-database %s' % mime_path)
print "Instalacion Finalizada."
