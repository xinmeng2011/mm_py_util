

import logging
import os

class LoggerUtil(object):
    '''
    LoggerUtil is used to initiate the logging module parameters, 
    eg. set log level, log format, log handler
    '''
    
    def __init__(self, log_path, log_level = 'info'):
        '''
        The constructor of loggerutil class
        '''
        
        self.log_path = log_path
        log_type_hash = {'notset': logging.NOTSET,
                         'debug': logging.DEBUG,
                         'info': logging.INFO,
                         'warn': logging.WARN,
                         'error': logging.ERROR,
                         'critical': logging.CRITICAL,}
        self.log_level = log_type_hash[log_level.lower()]
        self._instance = logging.getLogger(log_path)

        if self._instance.level != self.log_level:
            self.setLogger()
        
    def setLogger(self):
        '''
        Initiate some parameters of logger, eg. the log level, add file hanlder and stream handler
        '''
        self._instance.setLevel(self.log_level)
        
        #create a handler to write log
        log_dir = os.path.split(self.log_path)[0]
        if not os.path.exists(log_dir) and not os.path.isfile(self.log_path):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(self.log_level)

        #create a handler to output message on the console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.log_level)

        #define the log format
        fmt = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d' + 
                                ' - %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(fmt)
        stream_handler.setFormatter(fmt)
        
        #add the handlers into logger
        self._instance.addHandler(file_handler)         #turn on the file handler, so the logger can write file
        self._instance.addHandler(stream_handler)       #turn on the console output
        
    def getLogger(self):
        '''
        The interface to get the logger instance.
        '''
        return self._instance

    def close(self):
        for handler in self._instance.handlers:
            handler.close()
            
        self._instance.handlers = []