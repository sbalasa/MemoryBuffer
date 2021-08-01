"""
MemLogging Module is responsible for logging in System for debugging purposes.
This module will let you write debug messages into a 500MB memory buffer which is Circular.

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

# To modify the buffer size in MB
    logger.updateBufferSize(1000)

# Finally close the logger
    logger.close()
"""

import time
import mmap

from functools import wraps

FILE = "/tmp/debug.log"
DEFAULTSIZE = 500
BUFFERSIZE = 1024 * 1024 * DEFAULTSIZE  # 500MB


def Singleton(cls):
    """
    Singleton Class representing a in memory buffer used to log debug messages.
    """
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
        self.level = "INFO"
        self.name = __name__
        self.pos = 0
        self.mm = "Empty Buffer"

    def enable(self):
        """
        Method to enable Memory Buffer
        """
        try:
            with open(FILE, "wb+") as f:
                f.truncate(BUFFERSIZE)
            self.enabled = True
            self.fd = open(FILE, "r+")
            self.mm = mmap.mmap(self.fd.fileno(), 0)
        except Exception as e:
            print("Error: Unable to enable Memory Buffer")
            print(e)

    def setLevel(self, level):
        """
        Method to set the levels in Memory Buffer either INFO or DEBUG
        """
        if level in ["INFO", "DEBUG"]:
            self.level = level

    def close(self):
        """
        Method to close the File descriptor & Memory Buffer
        """
        self.mm.close()
        self.fd.close()
        self.enabled = False

    def tellBufferPosition(self):
        """
        Method to show the current byte position pointed in Memory Buffer
        """
        return self.pos

    def printBuffer(self):
        """
        Method to print the entire space of used Memory Buffer
        """
        if self.enabled and self.pos <= self.mm.size() - 1:
            print(self.mm[: self.pos])

    def info(self, data):
        """
        Method to log info messages into Memory Buffer
        """
        if self.enabled:
            _data = "%s %s" % (self.level, data)
            self._writeBuffer(_data)

    def debug(self, data):
        """
        Method to log debug messages into Memory Buffer
        """
        if self.enabled and self.level == "DEBUG":
            _data = "%s %s" % (self.level, data)
            self._writeBuffer(_data)

    def _writeBuffer(self, data):
        if self.pos >= self.mm.size() - 1:  # Circular Buffer
            self.pos = 0
        _data = "%s %s %s\n" % (time.asctime(), self.name, data)
        end = self.pos + len(_data)
        try:
            self.mm.write(bytes(_data, "utf-8"))
        except ValueError:
            pass
        self.pos = end

    def flushBuffer(self):
        """
        Method to flush the buffer into the file.
        """
        self.mm.flush()
        self.pos = 0

    def updateBufferSize(self, buff_size):
        """
        Method to update the buffer size.
        """
        global DEFAULTSIZE
        DEFAULTSIZE = buff_size


def instrument(func):
    """@instrument decorator which provides the entry and exit
    time of a function along with the total time consumed by it."""

    @wraps(func)
    def innerFunc(*args, **kwargs):
        """inner function in the decorator"""
        logger.setLevel("DEBUG")
        logger.debug(f"Entering -> {func.__name__}")
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        logger.debug(f"Exiting <- {func.__name__} after {end - start} seconds")
        return return_value

    return innerFunc


logger = MemoryBuffer()
