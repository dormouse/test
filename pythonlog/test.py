#!/usr/bin/env python
# -*- coding: UTF-8 -*
import logging
import sys  
mlogger = logging.getLogger("mlogger")  
formatter = logging.Formatter(
        '%(name)-12s %(asctime)s %(funcName)s %(levelname)-8s %(message)s',
        '%Y-%m-%d %H:%M:%S',)  
file_handler = logging.FileHandler("test.log")  
file_handler.setFormatter(formatter)  
stream_handler = logging.StreamHandler(sys.stderr)  
stream_handler.setFormatter(formatter)  
mlogger.addHandler(file_handler)  
mlogger.addHandler(stream_handler)  

class TestLog:
    def __init__(self):
        self.logger = logging.getLogger("mlogger.TestLog") 

    def a(self):
        self.logger.error("testlog.a")

    def b(self):
        self.logger.error("testlog.b")

def test():
    logger = logging.getLogger("mlogger.test_fun")  

    testlog = TestLog()
    testlog.a()
    testlog.b()

    logger.error("error 1")  
    logger.removeHandler(stream_handler)  
    logger.error("error 2")  


if __name__ == "__main__":
    test()
