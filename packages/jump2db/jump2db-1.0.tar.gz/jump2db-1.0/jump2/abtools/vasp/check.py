import os

class CheckStatus(object):
    """
    cls to check the VASP
    """

    def __init__(self, threshold=0.10, overwrite=False, \
                 constrain=False, *args, **kwargs):

        self.__threshold = threshold
        self.overwrite = overwrite
        self.constrain = constrain

    def success(self, path=None, task='scf', *args, **kwargs):
        """check vasp task run_status"""
        if os.path.exists(path):
            #try:
            return self.get_status(path, task)
            #except:
                #return {'success':False}
        else:
            return {'success':False}

    def discrete(self,path1,path2,task='nonscf',**kwargs):
        from jump2.abtools.grep.outcar import GrepOutcar
        from jump2.structure import read
        from os.path import join

        # calculation finished %
        try:
            status = self.get_status(join(path1,'OUTCAR'))
            assert status['success'] is True
        except:
            path1 = None

        try:
            status = self.get_status(join(path2,'OUTCAR'))
            assert status['finished'] is True
        except:
            path2 = None

        if path1 is None:
            return path2
        elif path2 is None:
            return path1

        # read structure %
        try:
            structure1 = read(join(path1,'CONTCAR'))
        except:
            structure1 = read(join(path1,'POSCAR'))

        try:
            structure2 = read(join(path2,'CONTCAR'))
        except:
            structure2 = read(join(path2,'POSCAR'))

        # volume compare % 
        volume_radio = structure1.get_volume() / structure2.get_volume()
        if volume_radio > 1.25 or volume_radio < 0.8:
            with open('/home/kzhou/example/cc.txt','a') as f:
                f.write('volume')
            return path1

        # free_energy compare %
        energy1 = GrepOutcar().free_energy(path1)
        energy2 = GrepOutcar().free_energy(path2)
        if energy2 > energy1 *1.25:
            return path1

        return path2

    def _continue(self,vasptask,root,**kwargs):
        from .tasks import VaspIncar

        stdin,status = self.load_status(root)
        ispath = False

        # reset vasptask - status %
        if 'relax' in status and status['relax']:
            ispath = True
            status.pop('relax')
            if vasptask.optimize is None:
                vasptask.optimize = VaspIncar('optimize',finish=True)
            else:
                vasptask.optimize.finish = True
        if 'scf' in status and status['scf']:
            ispath = True
            status.pop('scf')
            if vasptask.scf is None:
                vasptask.scf = VaspIncar('scf',finish=True)
            else:
                vasptask.scf.finish = True
        if vasptask.nonscf:
            finish = True
            for key in vasptask.nonscf:
                if key in status and status[key]:
                    if vasptask.nonscf[key] is None:
                        vasptask.nonscf[key] = VaspIncar(key,finish=True)
                    else:
                        vasptask.nonscf[key].finish = True
                else:
                    finish = False
            vasptask.nonscf.finish = finish
        if vasptask.diyflow:
            finish = True
            for key in vasptask.diyflow:
                if key in status and status[key]:
                    vasptask.diyflow[key].finish = True
                else:
                    finish = False
            vasptask.diyflow.finish = finish

        # reset stdin %
        if ispath or self.overwrite:
            return stdin
        else:
            return None

    def write_error_status(self,root=None,error=None,task=None):
        status = {'error':error,'finished':False,'success':False}
        self.write_status(root,status,task)

    def write_status(self,root=None, status=None, task=None, rel=True):
        """write vasp task run_status in root/.status"""

        from os.path import exists,join,relpath
        if rel:
            task = relpath(task,root)
        
        if exists(join(root, '.status')):
            f = open(join(root,'.status'), 'a+')
        else:
            f = open(join(root,'.status'), 'w')

        f.write("task: {0:<25s}    ".format(task))
        for k,v in status.items():
            if v is True: v = 'True'
            if v is False: v = 'False'
            if v is None: v = 'None'
            f.write("{0:>8s}: {1: <8}".format(k,v))
        f.write('\n')
        f.close()


    def load_status(self, root=None):
        from os.path import join, exists

        path = None
        params = {}

        if not exists(join(root,'.status')):
            return path,params

        with open(join(root,'.status')) as f:
            for line in f:
                if line.startswith('task: relax/S'):
                    if line.split()[-1] == 'True':
                        path = join(root,line.split()[1])
                        params['relax'] = True
                    else:
                        params['relax'] = False

                elif line.startswith('task: scf'):
                    if line.split()[-1] == 'True':
                        path = join(root,line.split()[1])
                        params['scf'] = True
                    else:
                        params['scf'] = False       

                elif line.startswith('task: nonscf'):
                    key = line.split()[1].split('/')[1]
                    if line.split()[-1] == 'True':
                        params[key] = True
                    else:
                        params[key] = False         
        return path,params
        
    def __finished(self,path):
        '''grep vasp end tag '''
        self.__getparams(path)
        try:
            line = os.popen("grep 'Total CPU time used (sec)' "+path).readline()
            if len(line) > 0:
                return True, self.__getparams(path)
            else:
                line1 = os.popen("grep 'vasp will stop now' "+path).readline()
                line2 = os.popen("grep 'VASP will stop now' "+path).readline()
                if len(line) > 0 or len(line2) >0 :
                    return True, None
                else:
                    return False, None
        except:
            print("CodeError: Invalid path in abtools/check.py",path)
            return False,None
        
    def __converged(self,path):
        ''' grep vasp relax converged tag'''

        try:
            line = os.popen("grep 'reached required accuracy - stopping structural energy minimisation' "+path).readline() 
            num= os.popen("grep 'energy  without entropy=' {0} | wc -l".format(path)).readline().rstrip()
            if len(line) > 0 and num.isdigit():
                return int(num),True
            else:
                return 0, False
        except:
            return 0, False

    def __electronic_steps(self, path):
        """get vasp the electronic steps """

        try:
            line= os.popen("grep 'Iteration ' {0} | tail -1".format(path)).readline()
            num = int(line.split('(')[-1].split(')')[0])
            return num

        except:
            return None

    def __getparams(self,path):
        from jump2.abtools.grep import GrepOutcar
        if path.endswith('OUTCAR'):
            path = path.rstrip('OUTCAR')
            path = path.rstrip(os.sep)
        
        go = GrepOutcar()
        params = {'ISIF': go.isif(path),
                  'NSW' : go.nsw(path),
                  'IBRION': go.ibrion(path),
                  'NELM': go.nelm(path),
                  'force': None}
        try:
            params['force']=go.max_force(path)
        except:
            if self.constrain:
                raise IOError("Failed to get force information")
        return params

    def get_status(self, path=None, task='scf'):
	
        import numpy as np 

        # possible status % 
	
        # step 0: calculation not finished % 	
        finished, params = self.__finished(path)
        if not finished:
            return {'finished':False,'success':False}
        elif params is None:
            return {'finished':True,'success':True}

        # step 1: check outcar convergence parameters % 
        status = {'force':None, 'ionic':None, 'electronic':None,
                  'finished':True, 'success':False}

        if params['ISIF'] >= 2.0 and task in ['relax','scf']:

            # force converged or not % 
            status['force'] = params['force']
            if self.constrain and params['force'] >= self.__threshold:
                return status

            # ionic %
            if params['IBRION'] > -1.0 and params['NSW'] > 0:
                num, converged = self.__converged(path)
                if converged and params['NSW'] > float(num) :
                    status['ionic'] = True  
                else:
                    status['ionic']= False
                    return status

        # electronic % 
        num = self.__electronic_steps(path)
        if num and params['NELM'] >= num:
            status['electronic'] = True
        else:
            status['electronic'] = False 
            return status

        # final % 
        status['success'] = True 
        return status  

    def rebuild_status(self,root,tasks):
        from os.path import exists,join
        from .tasks import __Task__
        if not isinstance(tasks,list):
            raise TypeError("Tasks should be list type")

        if exists(root) and exists(join(root,'pbsscript')):
            status={}
        else:
            raise IoError('Invalid calculation path')


        for task in tasks:
            if task == 'relax':
                if not exists(join(root,'relax')): continue
                relaxs = os.listdir(join(root,'relax'))
                if not len(relaxs): continue
                status['relax/'+max(relaxs)]=self.success(path=join(root,'relax',max(relaxs),'OUTCAR'),task=task) 
            elif task == 'scf':
                if not exists(join(root,'scf')): continue
                status['scf']=self.success(path=join(root,'scf','OUTCAR'),task=task) 
            elif task in ['band','emass','partchg']:
                subpath = join(root,'nonscf',task)
                if not exists(subpath): continue
                for subdir in os.listdir(subpath):
                    status['nonscf/%s/%s'%(task,subdir)]=self.success(path=join(subpath,subdir,'OUTCAR'),task=task) 
            elif task in __Task__:
                if not exists(join(root,'nonscf',task)): continue
                status['nonscf/'+task]=self.success(path=join(root,'nonscf',task,'OUTCAR'),task=task) 
        return status
