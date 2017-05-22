"""
MemLogging Module is responsible for logging in System for debugging purposes.

This module will let you write debug messages into memory buffer and 
flushes automatically to a specified file once its full.

Eg:
    from MemLogging import instrument, logger

    logger.enable()
    logger.name = __name__
    logger.info("This is my info message")

    logger.setLevel('DEBUG')
    logger.debug("This is my debug message")

    @instrument
    def my_function():
        logger.info('Inside my_function')
        return True

# To Print Buffer
    logger.printBuffer()

# To flush the buffer onto a file
    logger.flushBuffer()

#Finally close the logger
    logger.close()
"""

import time
import mmap

from functools import wraps

FILE = "/logs/debug.log"
FILESIZE = 1024 * 1024 * 200 # 200MB

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class MemoryBuffer(object):

    def __init__(self):
        self.enabled = False
        self.level = 'INFO'
        self.name = __name__
        self.pos = 0
        self.mm = 'Empty Buffer'

    def enable(self):
        self.enabled = True
        self._generateFile()
        self.fd = open(FILE, 'r+')
        self.mm = mmap.mmap(self.fd.fileno(), 0)

    def _generateFile(self):
        with open(FILE, 'wb') as f:
            f.write('\0' * FILESIZE)
            f.close()

    def setLevel(self, level):
        if level in ['INFO', 'DEBUG']:
            self.level = level

    def close(self):
        self.mm.close()
        self.fd.close()
        self.enabled = False

    def tellBufferPosition(self):
        return self.pos

    def printBuffer(self):
        if self.pos <= self.mm.size():
            print self.mm[:self.pos]

    def info(self, data):
        if self.enabled and self.level == 'INFO':
            self._writeBuffer(self.level + ' ' + str(data))

    def debug(self, data):
        if self.enabled and self.level == 'DEBUG':
            self._writeBuffer(self.level + ' ' + str(data))

    def _writeBuffer(self, data):
        if self.pos == self.mm.size(): #Automatically flush after reaching end
            self.flushBuffer()
            self.pos = 0
        _data = time.asctime() + ' ' + str(self.name) + ' ' + str(data) + '\n'
        end = self.pos + len(_data)
        self.mm[self.pos:end] = _data
        self.pos = end

    def flushBuffer(self):
        self.mm.flush()
        self.pos = 0

def instrument(func):
    """@instrument decorator which provides the entry and exit
    time of a function along with the total time consumed by it."""
    @wraps(func)
    def innerFunc(*args, **kwargs):
        """inner function in the decorator"""
        logger.debug('Entering -> {}'.format(func.func_name))
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        logger.debug('Exiting <- {} after {} '
            'seconds'.format(func.func_name, end - start))
        return return_value
    return innerFunc

logger = MemoryBuffer()
