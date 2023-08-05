import threading

def Writelog(path,text):
    import time
    with open('log.txt','a') as f:
        f.write('{0} monitor {1} at {2}\n'.format(path,text,time.strftime('%Y-%m-%d %H:%M:%S')))

class MonitorLog():
    def __init__(self, vasp=None, stdout=None, path=None, **kwargs):
        pass

    def monitor(self, vasp, stdout, stdin, rootdir, incar, **kwargs):
        from .correcting import CorrectingFlow
        import os, time
        import subprocess
        
        logFile = os.path.join(stdout,'pbs.log')
        self.errorlist = self.get_errorlist()
        self.error = None

        # wait calculation start %
        wait_time = 0
        while True:
            if os.path.exists(logFile):
                break
            elif wait_time < 20:
                time.sleep(5)
                wait_time += 1
            else:
                Writelog('Error!','killed program for timeout')
                os._exit(0)

        self.pointer=0
        # monitor vasp_log %
        while threading.currentThread().name == 'run':
            status = os.popen('lsof ' + logFile + '|grep mpirun').readline()
            self.read_logs(logFile)
            if not status:
                break
            time.sleep(10)

        if threading.currentThread().name == 'debug' and self.error is not None:
            stdout,debug_incar = CorrectingFlow(rootdir).calculator(self.error, vasp, stdout, stdin, incar)
            vasp.tasks.debug = debug_incar


    def read_logs(self,filename):
        from os.path import dirname,join
        logCheck = join(dirname(filename),"moi.txt")
        with open(filename,"rb") as f:
             f.seek(self.pointer,1)
             lines = f.readlines()
             with open(logCheck,'a') as g:
                 g.write('Pointer = %s\n' %self.pointer) 
                 g.write('Tell = %s\n' %f.tell())
                 if len(lines):
                     g.write(lines[0].decode()) 
                     g.write(lines[-1].decode()) 
             for line in lines:
                 for key,value in self.errorlist.items():
                     if value in str(line.decode()):
                        threading.currentThread().setName('debug')
                        self.error = key
                        return 0 
             self.pointer = f.tell()
        return 0

    def get_codepath(self,name=''):
        from os.path import join,abspath,dirname,realpath
        return join(abspath(dirname(realpath(__file__))),name)
    
    def get_errorlist(self):
        from .errorkey import ERROR,timestamp
        from os.path import getmtime,expanduser
        file = expanduser('~')+'/.jump2/env/error.json'
        if getmtime(file) - timestamp > 1e-3:
            return self.write_errorlist(file,getmtime(file))
        else:
            return ERROR

    def write_errorlist(self,path,timestamp=0):
        import json
        with open(path,'r') as f:
            ed = json.load(f)
    
        ned = {}
        codepath = self.get_codepath('errorkey.py') 
        with open(codepath,'w') as f:
            f.write('timestamp = %s\n' %timestamp)
            f.write('ERROR = {\n')
            for k,v in ed.items():
                ned[k] = v[0]
                f.write("  '{0}': '{1}',\n".format(k,v[0]))
            f.write('}')
    
        print('rewrite errorlist')
        return ned


def Monitor(func):
    def warp(self, vasp, stdout, stdin, incar={}, overwrite=True, **kwargs):
        import json
        import os,time

        m=MonitorLog()
        monitor1=threading.Thread(target=m.monitor, name='run', args=[vasp, stdout, stdin, self.rootdir, incar])
        monitor1.start()

        taskname = os.path.relpath(stdout,self.rootdir)
        Writelog(taskname,'start')
        restdin=func(self, vasp, stdout, stdin, incar, overwrite, **kwargs)
        Writelog(taskname,'end')

        # Analyze subprogress status %
        if threading.activeCount() > 1:
            if monitor1.getName() == 'debug':
                monitor1.join()
            else:
                monitor1.join(30.0)
                monitor1.setName('stop')
        Writelog(taskname,'join')

        if hasattr(vasp.tasks,'debug'):
            print('debug finish')
            incar.update(vasp.tasks.debug)
            del vasp.tasks.debug
            errorpath = os.path.join(self.rootdir,'debug',taskname.replace('/','_'))
            debugpath = os.path.join(self.rootdir,'debug','tmp')
            os.popen("mv {0} {1}".format(restdin,errorpath)).readline() 
            os.popen("mv {0} {1}".format(debugpath,restdin)).readline()
        return restdin
    return warp
