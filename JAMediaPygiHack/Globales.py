#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globales.py por:
#       Flavio Danesse <fdanesse@gmail.com>, <fdanesse@activitycentral.com>
#       CeibalJAM - Uruguay - Activity Central

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

BASEPATH = os.path.dirname(__file__)
WorkPath = os.environ["HOME"]

# http://docs.python.org/2.7/py-modindex.html
BASEDICT = {
    "python": [
        '__builtin__', '__future__', '__main__',
        'abc', 'aifc', 'anydbm', 'argparse', 'array',
        'ast', 'asynchat', 'asyncore', 'atexit', 'audioop',
        'base64', 'BaseHTTPServer', 'bdb', 'binascii',
        'Bastion', 'binhex', 'bisect', 'bsddb', 'bz2',
        'calendar', 'cgi', 'CGIHTTPServer', 'cgitb', 'chunk',
        'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections',
        'colorsys', 'commands', 'compileall', 'compile',
        'ConfigParser', 'contextlib', 'Cooke', 'cookielib',
        'copy', 'copy_reg', 'cPickle', 'cProfile', 'crypt',
        'cStringIO', 'csv', 'ctypes', 'curses',
        'datetime', 'dbhash', 'dbm', 'decimal', 'DEVICE',
        'difflib', 'dircache', 'dis', 'distutils', 'dl',
        'doctest', 'DocXMLRPCServer', 'dumdbbm', 'dummy_thread',
        'dummy_threading', 'email', 'encodings', 'errno',
        'exceptions', 'fcntl', 'filecmp', 'fileinput', 'fnmatch',
        'formatter', 'fpectl', 'fpformat', 'fractions', 'ftplib',
        'functools', 'future_builtins',
        'gc', 'gdbm', 'getopt', 'getpass', 'gettext', 'glob',
        'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'hotshot',
        'htmlentitydefs', 'htmllib', 'HTMLParser', 'httplib',
        'imageop', 'imaplib', 'imghdr', 'imp', 'importlib',
        'imputil', 'inspect', 'io', 'itertools', 'json',
        'keyword', 'lib2to3', 'linecache', 'locale', 'logging',
        'macpath', 'mailbox', 'mailcap', 'marshal', 'math',
        'md5', 'mhlib', 'mimetools', 'mimetypes', 'MimeWriter',
        'mimify', 'mmap', 'modulefinder', 'multifile',
        'multiprocessing', 'mutex', 'netrc', 'new', 'nis',
        'nntplib', 'numbers', 'operator', 'optparse', 'os',
        'ossaudiodev', 'parser', 'pdb', 'pickle', 'pickletools',
        'pipes', 'pkgutil', 'platform', 'plistlib', 'popen2',
        'poplib', 'posix', 'posixfile', 'pprint', 'profile',
        'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc',
        'Queue', 'quopri', 'random', 're', 'readline', 'repr',
        'resource', 'rexec', 'rfc822', 'rlcompleter',
        'robotparser', 'runpy', 'sched', 'ScrolledText',
        'select', 'sets', 'sgmllib', 'sha', 'shelve', 'shlex',
        'shutil', 'signal', 'SimpleHTTPServer',
        'SimpleXMLRPCServer', 'site', 'smtpd', 'smptlib',
        'sndhdr', 'socket', 'SocketServer', 'spwd', 'sqlite3',
        'ssl', 'stat', 'statvfs', 'string', 'StringIO',
        'stringprep', 'struct', 'subprocess', 'sunau',
        'symbol', 'symtable', 'sys', 'sysconfig', 'syslog',
        'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios',
        'test', 'textwrap', 'thread', 'threading', 'time',
        'timeit', 'Tix', 'Tkinter', 'token', 'tokenize', 'trace',
        'traceback', 'ttk', 'tty', 'turtle', 'types',
        'unicodedata', 'unittest', 'urllib', 'urllib2',
        'urlparse', 'user', 'UserDict', 'UserList', 'UserString',
        'uu', 'uuid', 'warnings', 'wave', 'weakref', 'webbrowser',
        'whichdb', 'wsgiref', 'xdrlib', 'xml', 'xmlrpclib',
        'zipfile', 'zipimport', 'zlib'],
        
    "python-gi": sorted([
        'Abi', 'AccountsService', 'Atk', 'Atspi',
        'Avahi', 'AvahiCore', 'Babl', 'Cally',
        'Champlain', 'Cheese', 'Clutter', 'ClutterGst',
        'ClutterJson', 'ClutterX11', 'Cogl', 'DBus',
        'DBusGLib', 'Dbusmenu', 'Dee', 'Epiphany', 'Everything',
        'EvinceDocument', 'EvinceView', 'GConf', 'GES',
        'GIMarshallingTests', 'GIRepository', 'GL', 'GLib',
        'GMenu', 'GModule', 'GObject', 'GSSDP', 'GUPnP',
        'GWeather', 'Gda', 'Gdaui', 'Gdk', 'GdkPixbuf',
        'GdkX11', 'Gedit', 'Gio', 'Gkbd', 'Gladeui',
        'GnomeBluetooth', 'GnomeKeyring', 'GnomeVFS',
        'GooCanvas', 'Gsf', 'Gst', 'GstApp', 'GstAudio',
        'GstBase', 'GstCheck', 'GstController', 'GstFft',
        'GstInterfaces', 'GstNet', 'GstNetbuffer', 'GstPbutils',
        'GstRiff', 'GstRtp', 'GstRtsp', 'GstSdp', 'GstTag',
        'GstVideo', 'Gtk', 'GtkChamplain', 'GtkClutter',
        'GtkSource', 'Gtop', 'Gucharmap', 'JSCore', 'Json',
        'MPID', 'Midgard', 'Nautilus', 'NetworkManager',
        'Notify', 'PanelApplet', 'Pango', 'PangoCairo',
        'PangoFT2', 'PangoX', 'PangoXft', 'Peas', 'PeasGtk',
        'PeasUI', 'Polkit', 'PolkitAgent', 'Poppler', 'Rsvg',
        'Soup', 'SoupGNOME', 'SugarExt', 'TelepathyGLib',
        'TelepathyLogger', 'Totem', 'UPowerGlib', 'Unique',
        'Unity', 'Vte', 'WebKit', 'Wnck', 'cairo', 'fontconfig',
        'freetype2', 'libbonobo', 'libc', 'libxml2', 'sqlite3',
        'xfixes', 'xft', 'xlib', 'xrandr']),
        
    "Otros": sorted([
        'cairo', 'gobject', 'gst', 'pygame', 'pygst',
        'simplejson', 'gtk', 'pygtk', 'telepathy', 'dbus',
        'numpy', 'scipy']),
        }
    
def set_dict(dict):
    """
    Crea el json base desde donde opera
    la función get_dict()
    """
    
    import json
    
    archivo = os.path.join(WorkPath, "JAMediaPyGiHack.cfg")
    archivo = open(archivo, "w")
    archivo.write(
            json.dumps(
                dict,
                indent=4,
                separators=(", ", ":"),
                sort_keys=True
            )
        )
    archivo.close()
    
def get_dict():
    """
    Devuelve Los módulos.
    """
    
    #import json
    #import codecs
    
    #archivo = os.path.join(WorkPath, "JAMediaPyGiHack.cfg")
    
    #if not os.path.exists(archivo):
    #    set_dict(BASEDICT)
        
    #archivo = codecs.open(archivo, "r", "utf-8")
    #dict = json.JSONDecoder("utf-8").decode(archivo.read())
    #archivo.close()
    
    #return dict
    return BASEDICT
