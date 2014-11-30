#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaSystemState.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

# https://code.google.com/p/psutil/
# https://github.com/nicolargo/glances
# https://github.com/elventear/psutil

# http://linux.die.net/man/2/ioprio_get
# http://docs.python.org/2.7/library/pkgutil.html?highlight=__file__
# http://docs.python.org/2.7/library/os.html?highlight=os#os

import os

CPU_CLOCK = os.sysconf(os.sysconf_names["SC_CLK_TCK"])

# Tomado desde: /fs/proc/array.c
STATUS_MAP = {
    "R" : (0, "running"),
    "S" : (1, "sleeping"),
    "D" : (2, "disk sleep"),
    "T" : (3, "stopped"),
    "t" : (4, "tracing stop"),
    "Z" : (5, "zombie"),
    "X" : (6, "dead"),
    "x" : (6, "dead"),
    "K" : (7, "wake kill"),
    "W" : (8, "waking")}


### PROCESADORES ###
def get_cpus():
    """
    Devuelve la Cantidad de CPUs en el Sistema.
    """
    num = 0
    f = open('/proc/cpuinfo', 'r')
    for line in f:
        if line.startswith('processor'):
            num += 1
    f.close()
    return num


### MEMORIA ###
def get_memory():
    """
    Devuelve la memoria total del sistema en MB.
    """
    f = open('/proc/meminfo', 'r')
    for line in f:
        if line.startswith('MemTotal:'):
            f.close()
            return int(line.split()[1]) / 1024


def get_memory_free():
    """
    Devuelve la cantidad de Memoria libre en el Sistema, en MB.
    """
    f = open('/proc/meminfo', 'r')
    free = None
    _flag = False
    for line in f:
        if line.startswith('MemFree:'):
            free = int(line.split()[1]) / 1024
            break
    f.close()
    return free


def get_virtual_memory():
    """
    Devuelve el total de memoria virtual en el sistema, en MB.
    """
    f = open('/proc/meminfo', 'r')
    for line in f:
        if line.startswith('SwapTotal:'):
            f.close()
            return int(line.split()[1]) / 1024


def get_virtual_memory_free():
    """
    Devuelve el total de memoria virtual libre en el sistema, en MB.
    """
    f = open('/proc/meminfo', 'r')
    for line in f:
        if line.startswith('SwapFree:'):
            f.close()
            return int(line.split()[1]) / 1024


### PROCESOS ###
def get_pids():
    """
    Returns a list of PIDs currently running on the system.
    """
    pids = [int(x) for x in os.listdir('/proc') if x.isdigit()]
    # Caso especial para 0 (kernel process) PID
    pids.insert(0, 0)
    return pids


def get_process_name(pid):
    """
    Devuelve el nombre de un proceso segun pid.
    """
    if pid == 0:
        return 'sched'  # special case for kernel process
    name = ''
    try:
        f = open("/proc/%s/stat" % pid)
        name = f.read().split(' ')[1].replace('(', '').replace(')', '')
        f.close()
    except:
        pass
    return name


def get_process_cmdline(pid):
    """
    Comando lanzador.
    """
    if pid == 0:
        return []   # special case for kernel process
    try:
        f = open("/proc/%s/cmdline" % pid)
        return [x for x in f.read().split('\x00') if x]
        f.close()
    except:
        return []


def get_process_io_counters(pid):
    try:
        f = open("/proc/%s/io" % pid)
    except:
        return [0,0,0,0]
    for line in f:
        if line.startswith("rchar"):
            read_count = int(line.split()[1])
        elif line.startswith("wchar"):
            write_count = int(line.split()[1])
        elif line.startswith("read_bytes"):
            read_bytes = int(line.split()[1])
        elif line.startswith("write_bytes"):
            write_bytes = int(line.split()[1])
    return [read_count, write_count, read_bytes, write_bytes]


def get_cpu_times(pid):
    if pid == 0:
        return (0.0, 0.0)
    f = open("/proc/%s/stat" % pid)
    st = f.read().strip()
    f.close()
    # ignore the first two values ("pid (exe)")
    st = st[st.find(')') + 2:]
    values = st.split(' ')
    utime = float(values[11]) / CPU_CLOCK
    stime = float(values[12]) / CPU_CLOCK
    return (utime, stime)


def get_memory_info(pid):
    if pid == 0:
        return (0, 0)
    f = open("/proc/%s/status" % pid)
    virtual_size = 0
    resident_size = 0
    _flag = False
    for line in f:
        if (not _flag) and line.startswith("VmSize:"):
            virtual_size = int(line.split()[1]) / 1024
            _flag = True
        elif line.startswith("VmRSS"):
            resident_size = int(line.split()[1]) / 1024
            break
    f.close()
    return (resident_size, virtual_size)


def get_process_cwd(pid):
    """
    path donde se lanza. (no el lanzador, sino su entorno).
    """
    if pid == 0:
        return ''
    try:
        path = os.readlink("/proc/%s/cwd" % pid)
        return path.replace('\x00', '')
    except:
        pass


def get_process_num_threads(pid):
    if pid == 0:
        return 0
    f = open("/proc/%s/status" % pid)
    for line in f:
        if line.startswith("Threads:"):
            f.close()
            return int(line.split()[1])


### OK ###
def get_process_threads(pid):
    """
    Devuelve los Procesos Hijos de un Determinado Proceso segun pid.
    """
    if pid == 0: return []
    try:
        thread_ids = os.listdir("/proc/%s/task" % pid)
        thread_ids.sort()
        if str(pid) in thread_ids:
            thread_ids.remove(str(pid))
        return thread_ids
    except:
        return []

    '''
    retlist = []
    for thread_id in thread_ids:
        try:
            f = open("/proc/%s/task/%s/stat" % (pid, thread_id))
        except (OSError, IOError), err:
            continue
        st = f.read().strip()
        f.close()
        # ignore the first two values ("pid (exe)")
        st = st[st.find(')') + 2:]
        values = st.split(' ')
        utime = float(values[11]) / CPU_CLOCK
        stime = float(values[12]) / CPU_CLOCK
        retlist.append( [int(thread_id), utime, stime] )
    return retlist'''


def get_process_status(pid):
    if pid == 0:
        return (0, '')
    try:
        f = open("/proc/%s/status" % pid)
        for line in f:
            if line.startswith("State:"):
                f.close()
                letter = line.split()[1]
                if letter in STATUS_MAP:
                    return STATUS_MAP[letter]
                return (-1, '?')
    except:
        return (-1, '?')


def get_open_files(pid):
    """
    Devuelve lista de path de archivos que mantiene abiertos este proceso.
    """
    retlist = []
    try:
        files = os.listdir("/proc/%s/fd" % pid)
    except:
        return []
    for fd in files:
        file = "/proc/%s/fd/%s" % (pid, fd)
        if os.path.islink(file):
            file = os.readlink(file)
            if file.startswith("socket:["):
                continue
            if file.startswith("pipe:["):
                continue
            if file == "[]":
                continue
            if os.path.isfile(file) and not file in retlist:
                retlist.append( [file, int(fd)] )
    return retlist


### OK ###
def get_archivos_abiertos_por_proceso(pid):
    """
    Devuelve datos de archivos abiertos por un determinado proceso segun pid.
    """
    import commands
    cmd = "lsof -a -p %s" % pid
    stdout = commands.getoutput(cmd)
    if stdout:
        lineas = stdout.split("\n")
        salida = []
        for linea in lineas[1:]:
            info = linea.split()[2:] # 0 y 1 son pid y nombre.
            if len(info) < 7:
                info.insert(3,"")
                salida.append( info )
        return salida
