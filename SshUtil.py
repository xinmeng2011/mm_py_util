
import os
import paramiko 
import sys
import threading
import time
project_path = os.path.abspath(__file__)
project_path = project_path[:project_path.rfind('org')]
sys.path.append(project_path)
from LoggerUtil import LoggerUtil

log_obj = LoggerUtil(os.path.join(os.path.dirname(__file__), 'log.txt')).getLogger()

class SshUtil(object): 
    '''
    SshUtil is used to connect the remote server use the ssh protocol, it also can upload files.
    '''
    
    @staticmethod
    def getSSHObject():
        '''
        Get the ssh object
        @return: return the ssh object
        '''

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        
        return ssh
    
    @staticmethod
    def connect(ip, username, password):
        '''
        Use the ssh connect the remote server
        @param ip: ip address of the remote server
        @param username: username of the remote server
        @param password: password of the remote server 
        @return: return the ssh object 
        '''
        ssh = SshUtil.getSSHObject() 
#        privatekeyfile = os.path.expanduser('z:/id_rsa')
#        pkey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
#        ssh.connect(hostname = ip, username = username, pkey=pkey)
        ssh.connect(hostname = ip, username = username, password = password)
        
        return ssh
    
    @staticmethod  
    def executeCommand(ip, cmd, username = 'root', password = '1234.asd'):#HtCh&2nb,1234.asd
        ssh = SshUtil.connect( ip, username, password )
        stdin, stdout, stderr = ssh.exec_command( cmd )
        error_info = stderr.read()
        
        if error_info != '':
            return error_info
        else:
            return stdout.read()
    
    @staticmethod
    def transportFile(ip, sourceFile, destFile, username = 'root', password = '1234.asd'):
        t = paramiko.Transport((ip,22)) 
        t.connect(username = username, password = password) 
        sftp = paramiko.SFTPClient.from_transport(t) 
        destDir = os.path.dirname(destFile)
        SshUtil.executeCommand(ip, 'mkdir -p %s' % destDir)
        sftp.put(sourceFile, destFile)
        
        if sourceFile.find('.zip') > -1:
            cmd = 'rm -fr %s && mkdir -p %s && cd %s && unzip -o %s && rm -fr %s' \
                    % (os.path.splitext(destFile)[0], destDir, destDir, destFile, destFile)
            log_obj.info('Ready the whole process, the command is "%s".' % cmd)
            SshUtil.executeCommand(ip, cmd)
            
        t.close()
        
class TestCmd(threading.Thread):
    def __init__(self, threadname, ip, cmd):    
        threading.Thread.__init__(self,name = threadname)
        self.ip = ip
        self.cmd = cmd
        
    def run(self):
        begin = time.time()
        print SshUtil.executeCommand(self.ip, self.cmd)
        end = time.time()
        print '%s take time:%ss' % (self.getName(), end - begin)
        
def createThreads(ip_list, cmd):
    thread_list = []
    begin = time.time()
    
    for ip in ip_list:
        t = TestCmd(ip, ip, cmd)
        thread_list.append(t)
        
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    
    for t in thread_list:
        threading.Thread.join(t)
    
    end = time.time()    
    print 'excute time:%s' % (end - begin) 
                 
if __name__ == '__main__':
    pass