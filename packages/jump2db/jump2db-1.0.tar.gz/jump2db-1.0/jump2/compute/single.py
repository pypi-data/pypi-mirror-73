import os
from jump2.abtools.vasp.vaspflow import VaspFlow

class __VaspFlow__(VaspFlow):

    def __init__(self, vasp=None, stdout=None, *args, **kwargs):

        import sys
        sys.path.insert(0,self.realpath)
        VaspFlow.__init__(self,vasp,stdout,*args,**kwargs)

class SingleManager(object):

    def __init__(self,root=None):
        if root == None:
            self.root = os.path.abspath(root)
        else:
            self.root = os.getcwd()

    def submit(self,func,stdout):
        from .manager import TaskManager
        taskdict = TaskManager().get_task_by_user()
        if stdout in taskdict.values():
            print("Warning! A program is running in the current directory")
            return False

        self.write_log(stdout,'start')
        self.calculator(func,stdout)
        self.write_log(stdout,'end')
        return True

    def write_log(self,stdout,status):
        import time
        # tag the task status % 
        logfile = os.path.join(self.root,'single.log')
        with open(logfile,'a') as f:
            f.write('{0} {1} at {2}\n'.format(stdout,status,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    @property
    def mpirun(self):
        return self.__command__

    @mpirun.setter
    def mpirun(self, command=None):
        if command is None:
            self.__command__ = self.default_command
        else:
            self.__command__ = command

    def calculator(self, func=None, stdout=None):

        from jump2.abtools.vasp.setvasp import SetVasp

        if isinstance(func, SetVasp):
            __VaspFlow__(func, stdout)

        else:
            raise IOError ("only vasp WorkFlow is valid ...")
