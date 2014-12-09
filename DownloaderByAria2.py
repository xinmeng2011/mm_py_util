#!/usr/bin/env python
#coding=utf-8


import os
from LoggerUtil import LoggerUtil
from FileUtil import FileUtil

class Downloader(object):
    '''
    Downloader is used to download the file from internet.
    '''
    
    def __init__(self, log_obj = None):
        '''
        The constructor function of class Downloader.
        @param log_obj: the loggerutil object
        '''
        
        if log_obj:
            self.log_obj = log_obj
        else:
            self.log_obj = LoggerUtil(os.path.join(os.path.dirname(__file__), 'log.txt')).getLogger()
            
    def aria2(self, url, download_dir, file_name):
        '''
        Based on the specific url, download a file and store in a specific directory.
        @param url: the url of a file
        @param download_dir: a directory to store the downloaded file
        
        '''
        
        tool = 'aria2c '
        cmd = '%s -c -s10 -x10 -j10 -d %s -o %s "%s"' % (tool, download_dir, file_name, url)
            
        self.log_obj.info('Ready for downloading, the command is "%s".' % cmd)
        os.popen(cmd.decode().encode('gbk'))
        self.log_obj.info('Complete download.')
                
    def download(self, download_dir, seg_urls):
        count = len(seg_urls)
        
        for i in xrange(count):
            file_name = '%04d' % i
            self.aria2(seg_urls[i], download_dir, file_name)
    
if __name__ == '__main__':
    pass

