# MemoryBuffer

This module will let you write debug messages into a 200MB memory buffer which is Circular..

Eg:
    from Memlogging import instrument, logger

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
