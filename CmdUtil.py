import os
import socket
from LoggerUtil import LoggerUtil

class CmdUtil(object):
    '''
    CmdUtil is used to execute the system command and get the local ip address.
    '''
    
    def __init__(self, log_obj = None):
        '''
        The constructor function of class cmdutil.
        @param log_obj: the loggerutil object
        '''
        
        if log_obj:
            self.log_obj = log_obj
        else:
            self.log_obj = LoggerUtil(os.path.join(os.path.dirname(__file__), 'log.txt')).getLogger()
        
    def executeCmd(self, cmd):
        '''
        Execute the system command, it does not need return value.
        @param cmd: the command
        '''
        
        self.log_obj.info('Ready to execute the command:"%s"' % cmd)
        status = os.system(cmd)
        
        if not status:
            self.log_obj.info('Execute successfully.')
            return 0
        else:
            self.log_obj.error('The command:"%s" execute faily.' % cmd)
            return 1
      
        
    def getlocalip(self):
        '''
        Get the local server ip address
        @return: return the server ip address
        '''
        if os.name.find('nt') != -1:
            ip = socket.gethostbyname(socket.gethostname())
        else:
            ip = os.popen("ifconfig | awk '$2 ~ /addr:(10.*|192.*)/{print $2}' | awk -F: '{print $2}'").read().strip('\n')
            
        self.log_obj.info('The ip of this server is "%s"' % ip)
        
        return ip
    
if __name__ == '__main__':
    pass
    