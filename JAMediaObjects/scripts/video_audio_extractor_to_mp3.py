#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
'gst-launch-1.0 filesrc location=/home/flavio/Documentos/001 ! \
    decodebin name=t ! \
        queue ! audioconvert ! lamemp3enc ! filesink \
            location=/home/flavio/Documentos/002.mp3 \
        t. ! queue ! autovideosink')
"""

import os
import sys
import commands

contador = 0


def extraer(origen):

    if not os.path.exists(origen):
        print "No se encontró:", origen
        return

    if not os.path.isfile(origen):
        print origen, "no es un archivo"
        return

    print "Extrayendo audio de:", origen

    destino = "%s.mp3" % origen

    comando = "gst-launch-1.0 filesrc location=\"%s\" !" % origen
    comando = "%s decodebin name=t !" % comando
    comando = "%s queue ! audioconvert ! lamemp3enc !" % comando
    comando = "%s filesink location=\"%s\"" % (comando, destino)
    comando = "%s t. ! queue ! autovideosink" % comando

    commands.getoutput(comando)


def get_data(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    """

    datos = commands.getoutput(
        'file -ik %s%s%s' % ("\"", archivo, "\""))

    retorno = ""

    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)

    return retorno


if not len(sys.argv) == 2:
    print "Debes ingresar el nombre de un archivo o directorio."
    sys.exit(0)

origen = sys.argv[1]

if os.path.isdir(origen):

    for archivo in os.listdir(origen):
        arch = os.path.join(origen, archivo)

        if "video" in get_data(arch):
            contador += 1
            extraer(arch)

elif os.path.isfile(origen):
    contador += 1
    extraer(origen)

print "Proceso Terminado. Se han procesado %s archivos." % contador

sys.exit(0)
