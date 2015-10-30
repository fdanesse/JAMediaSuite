#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import psutil
import json
import codecs

PATH = os.path.join(os.environ["HOME"], 'process.json')


def get_dict(path):
    if not os.path.exists(path):
        return {}
    archivo = codecs.open(path, "r", "utf-8")
    _dict = json.JSONDecoder(encoding="utf-8").decode(archivo.read())
    archivo.close()
    return _dict


def set_dict(path, _dict):
    archivo = open(path, "w")
    archivo.write(
        json.dumps(
            _dict,
            indent=4,
            separators=(", ", ":"),
            sort_keys=True))
    archivo.close()


def get_process():
    _dict = {}
    for proc in psutil.process_iter():
        try:
            dict_process = proc.as_dict(attrs=['pid'])
            pid = dict_process['pid']
            _dict[pid] = proc.as_dict(attrs=[])
        except psutil.NoSuchProcess:
            pass
        else:
            pass
    return _dict


class Control(gobject.GObject):

    def __init__(self):
        gobject.GObject.__init__(self)

    def __update(self):
        set_dict(PATH, get_process())
        gobject.timeout_add(2000, self.__update)
        return False

    def run(self):
        gobject.timeout_add(2000, self.__update)


if __name__ == "__main__":
    control = Control()
    gobject.MainLoop().run()
