#!/usr/bin/env python
# -*- coding: utf-8 -*-

def doesDef(line, index=None):
    
    num = line.find("def ")
    
    if num < 0:
        return
    
    if (( line.__contains__(':') or line.__contains__('('))):
       def_name = line.__getslice__(4, line.__len__()).strip()
    
       while (':' not in def_name):
           if not index:
               index = lines.index(line).__add__(1)
            
           elif index:
               index = index.__add__(1)

           subline = lines[index]
           def_name += ' ' + subline.strip()
           
       def_name = def_name.rpartition(':').__getitem__(0).strip()
       def_name = def_name[4:def_name.find("(")]
    
       return def_name
       
def obtener_datos(texto):
    
    global lines
    
    lines = texto.splitlines()
    resultados = []
    
    for line in lines:
        resultado = doesDef(line)
        
        if resultado:
            resultados.append(resultado)
            
    return resultados
