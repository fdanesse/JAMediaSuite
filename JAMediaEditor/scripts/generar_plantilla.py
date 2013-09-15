import os
import shelve

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