import os
from jump2.compute.launch import __LaunchTasks
from jump2.compute.__cluster__ import __Script__
from jump2.compute.pool import Pool 
from jump2.analysis.analysis import Analysis, DjangoCase

class __Analysis(Analysis):
    
    def __init__(self,pool,stdin):
        # load job_id %
        self.id = self.get_id(pool,stdin)
        # check stdout %
        pwd = os.getcwd()
        if pwd.endswith(stdin):
            self.__path = pwd
        elif os.path.exists(os.path.join(pwd,stdin)):
            self.__path = os.path.join(pwd,stdin)
        else:
            raise IOError('Stdin not exist')
        # get finished tasklist %
        self.pool = {self.path: self.__loadstatus('.status')}
        
    def savedb(self):
        dc = DjangoCase(self.id,os.path.abspath(self.path))
        self.case = {}
        dc.set_structure(self.stdin+'/scf/POSCAR')
        for task in self.tasks:
            self.__analysis__(self.stdin,task)
        dc.update_params(self.case)


    def get_id(self,pool,stdin):
        '''
        load poolfile and get cluster_id %
        such as ['198725'], int
        ''' 
        import pickle
        with open(pool,'rb') as f:
            pool=pickle.load(f)
        return pool[stdin]['job_id']



# step 0: open the jobs pool % 
# step 1: check current jobs and analysis % 
# step 2: update status of current jobs % 
# step 3: update resource % 
# step 4: load unfinished jobs % 
# step 5: submit jobs % 
class TaskManager(Pool):
    
    def __init__(self, manager='pbs',**kwargs):
        self.manager = manager.lower()
         
    def get_task_by_user(self,user=None):
        if self.manager == 'pbs':
            return self.get_pbs_task_by_user(user)
        elif self.manager == 'lsf':
            return self.get_lsf_task_by_user(user)

    def get_task_by_id(self,jobid=None):
        if self.manager == 'pbs':
            return self.get_pbs_task_by_id(jobid)
        elif self.manager == 'lsf':
            return self.get_lsf_task_by_id(jobid)

    def get_lsf_task_by_user(self,user=None):
        import re
        if user is None:
            user = os.environ['USER']
        lines = os.popen('bjobs -u %s' %user).readlines()
        if len(lines) < 2 : return {}

        # normally 3th slice is run-status %
        for i,line in enumerate(lines):
            if re.match('JOBID',line):
                index = line.split().index('STAT')
                break

        # get self tasks %
        mytasks = []
        for line in lines[i:]:
            if re.match(r'\d+',line):
                if line.split()[index] in ['RUN','PEND']:
                    mytasks.append(re.match(r'\d+',line).group())

        mtpath = {}
        for jobid in mytasks:
            mtpath[jobid] = self.get_lsf_task_by_id(jobid)

        return mtpath

    def get_lsf_task_by_id(self,jobid=None):
        lines = os.popen('bjobs -l '+jobid+' | grep -A2 CWD|tail -3 ').readlines()
        line = lines[0].split('CWD <')[-1]
        if '>' in line:
            path = line.split('>')[0]
        else:
            path = line.rstrip()
            line_index = 1
            for line in lines[1:]:
                if '>' in line:
                    path += line.split('>')[0].lstrip()
                    line == True 
                    break
                else:
                    path += line.strip()
                    line_index += 1
         
            while line is not True:
                line = os.popen('bjobs -l '+jobid+' | grep -A{0} CWD|tail -1 '.format(line_index)).readline()
                if '>' in line:
                    path += line.split('>')[0].lstrip()
                    break
                else:
                    path += line.strip()
                    line_index += 1
        return path

    def get_pbs_task_by_user(self,user=None):
        import re
        if user is None:
            user = os.environ['USER']
        lines = os.popen('qstat -u %s' %user).readlines()
        if len(lines) == 0 : return {}

        # normally 10th slice is run-status %
        for i,line in enumerate(lines):
            if re.match('Job',line):
                index = line.split().index('S')-1
                break

        # get self tasks %
        mytasks = []
        for line in lines[i:]:
            if re.match(r'\d+',line):
                if line.split()[index] != 'C':
                    mytasks.append(re.match(r'\d+',line).group())

        mtpath = {}
        for jobid in mytasks:
            mtpath[jobid] = self.get_pbs_task_by_id(jobid)

        return mtpath

    def get_pbs_task_by_id(self,jobid=None):
        lines = os.popen('qstat -f '+jobid+' | grep -A2 PBS_O_WORKDIR|tail -3').readlines()
        line = lines[0].split('PBS_O_WORKDIR=')[-1]
        if ',' in line:
            path = line.split(',')[0]
        else:
            path = line.rstrip()
            line_index = 1
            for line in lines[1:]:
                if ',' in line:
                    path += line.split(',')[0].lstrip()
                    line == True
                    break
                else:
                    path += line.strip()
                    line_index += 1
         
            while line is not True:
                lines = os.popen('qstat -f '+jobid+' | grep -A{0} PBS_O_WORKDIR|tail -1'.format(line_index)).readline()
                if ',' in line:
                    path += line.split(',')[0].lstrip()
                    break
                else:
                    path += line.strip()
                    line_index += 1
        return path 

    def get_queue_num(self,username,root=None):
        taskdict = self.get_task_by_user(username)
        print(taskdict)
        jump2_num = 0
        if len(taskdict) and root is not None:
            root = os.path.abspath(root)
            for jobid,path in taskdict.items():
                if path.startswith(root):
                    jump2_num += 1 
        return len(taskdict),jump2_num 

        
    def set_queue_num(self,username=None,root=None,type = 'mini'):
        from time import sleep
        import json
        path = os.path.join(root,'.cluster')
        with open(path,'r') as f:
            dic = json.load(f)
        set_num = dic['maximum']
        #sleep(set_num*3)
        user_num,jump2_num = self.get_queue_num(root,username)
        print(set_num,user_num,jump2_num)
        if type == 'prior':
            return set_num-jump2_num
        if type == 'mini':
            return max(set_num-user_num,1-jump2_num)




    def getfunc(self,poolfile,key):
        pool = self.loader(poolfile)
        self.__release__()
        return self.pool[key]['functional']

    def calculator(self, func=None, stdout=None):

        from jump2.abtools.vasp.setvasp import SetVasp
        from jump2.abtools.vasp.vaspflow import VaspFlow

        if isinstance(func, SetVasp):
            VaspFlow(func, stdout)
        else:
            raise IOError ("only vasp WorkFlow is valid ...")	

# main program % 
if __name__ == '__main__':
    import sys

    username=sys.argv[4]
    hostname=sys.argv[3]
    stdout = sys.argv[2]
    pool   = sys.argv[1] 
    root   = os.path.dirname(pool) 

    # load overwrite/restart %
    cluster = __Script__(root)
    overwrite = cluster.overwrite
    restart = cluster.restart 

    task=TaskManager()
    task_num = 0 
    for path in task.get_task_by_user(username).values():
        if path == os.getcwd():
            task_num += 1
    if task_num >1:
        print("Warning! A program is running in the current directory")
        print("Task stop.")
    else:
        func=task.getfunc(pool,stdout)
 
        if overwrite:
            func.overwrite = True

        # tag the status % 
        if os.path.exists('.wait'):
            os.system('rm .wait')
 
        # start calculation %
        task.calculator(func,os.getcwd())
 
        # save data % 
        if getattr(func,'save',False) or getattr(func,'savedb',False):
            a = __Analysis(pool,stdout)
            if getattr(func,'save',False):
                a.savelog()
            if getattr(func,'savedb',False):
                a.savedb()

    # next calculation %
    os.chdir(root)
    new_task_number = task.set_queue_num(username,root) + 1
    #print 'maxinum=',new_task_number
    newjob = {'run':'qsub','pool':pool,'maximum':new_task_number,\
              'restart':restart,'overwrite':overwrite}
    __LaunchTasks(newjob,*[stdout])
