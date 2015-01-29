import os
import shelve

"""
Genera plantilla que es el modelo de instalador gnome ceibal para
proyectos de JAMediaEditor.
"""

arch = open("install_model", "r")

text = ""
for line in arch.readlines():
    text=text+line

arch.close()

archivo = shelve.open("plantilla")
archivo['install'] = text
archivo.close()

archivo = shelve.open("plantilla")
items = archivo.items()
archivo.close()

print items
