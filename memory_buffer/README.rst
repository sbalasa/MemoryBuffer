# MemoryBuffer

This module will let you write debug messages into a 500MB memory buffer which is Circular..

Eg:
    
    from memory_buffer.MemLogging import instrument, logger
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

# To install from pypi
   pip3 install memory_buffer
