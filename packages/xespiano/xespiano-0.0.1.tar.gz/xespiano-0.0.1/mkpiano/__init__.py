from time import sleep
from .boards import mbuild

import sys
import signal

_ports = []
_threads = []

def add_port(port):
    global _ports
    _ports.append(port)

def add_thread(thread):
    global _threads
    thread.daemon = True
    _threads.append(thread)

def quit():
    __exiting(0,0)
    
def __exiting(signal, frame):
    global _ports
    global _threads
    for port in _ports:
        port.exit()
    for thread in _threads:
        thread.exit()
    try:
        sys.exit(0)
    except Exception as e:
        print(e)

signal.signal(signal.SIGINT, __exiting)
piano = mbuild.piano
sleep(0.5)