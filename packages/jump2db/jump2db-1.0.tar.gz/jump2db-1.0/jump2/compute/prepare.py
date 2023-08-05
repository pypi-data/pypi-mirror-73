# prepare
from os.path import exists,join
import os

class Prepare(object):
    
    @classmethod
    def pool(cls,func):
        return pool_prepare(func)

    @classmethod
    def cluster(cls,system='pbs'):
        import shutil, json
        system = system.lower()
        default='{0}/.jump2/env/{1}.json'.format(os.environ['HOME'],system)
        status = False
        if exists('.cluster'): 
            #try:
                with open('.cluster','r') as f:
                    params = json.load(f)
                if params["manager"].lower() != system:
                    shutil.copy('.cluster','.'+system)
                else:
                    status = True
            #except:
            #    raise SyntaxError("Please correct Syntax error in .cluster!")

        if status == False:
            try:
                shutil.copy(default,'.cluster')
            except:
                raise IOError ("File %s not exist!" %default)

    @classmethod
    def incar(cls,tasks,default=os.environ['HOME']+'/.jump2/env/incar.json'):
        import json
        # load default_incar %
        if exists(default):
            try:
                with open(default,'r') as f:
                    default_incar = json.load(f)
            except:
                raise IOError ("Syntax error in ~/.jump2/env/incar.json")
        else:
            raise ("incar.json not exists in ~/.jump2/env/")
        # load incar in local path %
        current_incar = {}
        if exists('.incar'):
            try:
                with open('.incar','r') as f:
                    current_incar = json.load(f)
            except:
                pass

        # build incar base and nonscf %
        base_task = ['default','scf','band']
        if 'nonscf' in tasks:
            base_task.extend(tasks['nonscf'])
        if 'xc' in tasks: 
            base_task.extend(tasks['xc'])
            if 'gw' in tasks['xc']:
                base_task.append('optics') 

        for task in base_task:
            if task not in current_incar: 
                if task in default_incar:
                    current_incar[task] = default_incar[task]
                else:
                    print('missing {} parameter in default_incar. '.format(task))
                    current_incar[task] = {}

        with open('.incar','w') as f:
            f.write(json.dumps(current_incar,indent = 3))

        # build diy_input %
        if 'diyflow' in tasks:
            diy_dict = {}
            from jump2.abtools.diyflow import import_diy_moudle
            for task in tasks['diyflow']:
                diy_class = import_diy_moudle(task)
                diy_dict[task] = diy_class.default_json(type='blank')
            if len(diy_dict) > 0:
                diy_class.write_json(os.getcwd(),**diy_dict)
            
         
    @classmethod
    def checkdb(cls,db='mysqld'):
        user = os.environ['USER']
        dbrun = True
        # database check %
        lines = os.popen("ps -ef|grep %s" %db).readlines()
        for line in lines:
            if line.startswith(user) and line.split()[2] == '1':
                dbrun = False
        if dbrun:
            print("Database %s is not running" %db)


        
class pool_extra(object):
    
    def __init__(self,poolname):
        import pickle
        with open(poolname,'rb') as f:
            self.pool=pickle.load(f)
        self.name = poolname
        self.index_flush()

    def __index(self):
        for key,value in self.pool.items():
            yield key,value['functional'].structure
        print('Error: list index out of range')

    def index_flush(self):
        self.p = self.__index()

    @property
    def magmom(self):
        return self.__m

    @magmom.setter
    def magmom(self,value):
        self.__m,s = next(self.p)
        s.is_magnetic = value

    @property
    def ldau(self):
        return self.__l

    @ldau.setter
    def ldau(self,value):
        self.__l,s = next(self.p)
        s.is_ldau = value

    def save(self):
        import pickle
        with open(self.name,'wb') as f:
            pickle.dump((self.pool), f)
        print('%d structure set success' %len(self.pool))



class pool_prepare(object):


    def __init__(self,func):
        super(pool_prepare,self).__init__()
        self.func = func

    def set_structure(self,poolpath,calpath='./CAL',operation = None,prior = None):
        from .pool import Pool
        from copy import deepcopy
        from jump2.structure import read

        pool = Pool()
        if isinstance(prior,int):
            pool.prior = prior
        for i in os.walk(poolpath).__next__()[2]:
            pool.functional = deepcopy(self.func)
            poscar = read(poolpath+'/'+i)
            if operation:
                poscar = operation(poscar)
            pool.functional.structure = poscar
            pool.outdir = calpath.rstrip('/') + '/' + i
        self.pool = pool

    def set_magnetic(self,type='cl'):
        '''
        create magmom configuration file with default format
        type:
            cl : colinear, need to set magmom for each atom
            ncl: non-colinear, need to set all three directions of magmom 
        '''
        import json
        if self.func.xc_func == 'soc':
            type = 'ncl'

        magnetic = {}
        for key,format in self.pool.mainkey.items():
            magnetic['%s %s' %(key,format)] = ''

        with open('.magnetic','w') as f:
            f.write(json.dumps(magnetic,indent = 1))

    def set_ldau(self,type='The'):
        '''
        create magmom configuration file with default format
        type:
            cl : colinear, need to set magmom for each atom
            ncl: non-colinear, need to set all three directions of magmom 
        '''

        ldau = {}
        for key,format in self.pool.mainkey.items():
            ldau['%s %s' %(key,format)] = ''

        with open('.ldau','w') as f:
            f.write(json.dumps(ldau,indent = 1))


    def save(self,name ='JUMP2.pbs',overwrite ='True'):
        self.pool.save(name,overwrite)    
 
#    def fpass(self,value):
#        return value
#
#    def __getattr__(self,value):
#        if value == 'operation':
#            return self.fpass 


        
 
         
