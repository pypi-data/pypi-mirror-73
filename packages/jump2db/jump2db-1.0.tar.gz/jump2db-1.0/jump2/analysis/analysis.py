# -*- coding: utf-8 -*-
import os
from jump2.compute.pool import Pool

default={'scf':['free_energy','fermi_energy','date','datetime','vasp_version'],
         'band':['bandgap'],
         'emass':['emass']}


class DjangoCase(object):

    def __init__(self,name='default',path=None):
        import sys
        import django
        from jump2.db import dbpath
        sys.path.insert(0, os.environ['HOME']+'/.jump2/lib')
        sys.path.insert(0, dbpath)
        os.environ['DJANGO_SETTINGS_MODULE']='django_settings'
        django.setup()
        from materials.case import Case
        self.case = Case()
        self.case.name = name
        self.case.path = path

    def set_structure(self,path,isPersist=False):
        from iostream.read import Read
        from materials.structure import Structure
        raw=Read(path, dtype='vasp').run()
        self.case.structure=Structure().create(raw, isPersist=True)
        if self.case.name == 'default':
            self.case.name = raw['comment']

    def update_params(self,params={}):
        #keywords = [field.name for field in self.case._meta.fields]
        #print(keywords)
        if not isinstance(self.case.calculated_parameters,dict): 
            self.case.calculated_parameters = {} 
        for case,value in params.items():
            if case == "free_energy":
                setattr(self.case,'energy',value)
                setattr(self.case,'energy_per_atom',value/self.case.structure.natoms)
            elif case == "bandgap":
                setattr(self.case,'bandgap',value)
            elif case == "emass":
                cbm,vbm={},{}
                for key,mass in value.items():
                    if 'cbm' in key:
                        cbm[key[-1]]=mass
                    if 'vbm' in key:
                        vbm[key[-1]]=mass
                if len(cbm):
                    setattr(self.case,'hole_mass',cbm)
                if len(vbm):
                    setattr(self.case,'electron_mass',vbm)
            else:
                self.case.calculated_parameters[case] = value
        #print self.case.__dict__
        #print self.case.structure.__dict__
        self.case.create(self.case.name,True)


class Analysis(object):

    def __init__(self):
        pass

    def savelog(self):
        import json
        for stdin,tasks in self.pool.items():
            self.case = {}
            for task in tasks:
                self.task_analysis(stdin,task)
            if 'emass' in tasks and isinstance(self.case['emass'],dict):
                cbm,vbm=[],[]
                for key,mass in self.case.pop('emass').items():
                    if 'cbm' in key:
                        cbm.append(mass)
                    if 'vbm' in key:
                        vbm.append(mass)
                if len(cbm):
                    self.case['cbmass'] = round(len(cbm)/sum([1/i for i in cbm]),4)
                if len(vbm):
                    self.case['vbmass'] = round(len(vbm)/sum([1/i for i in vbm]),4)
            if 'band' in tasks and isinstance(self.case['bandgap'],dict):
                self.case.update(self.case.pop('bandgap'))
            self.pool[stdin] = self.case
        with open('output.json','w') as f:
            f.write(json.dumps(self.pool,indent=3))

    def savedb(self):
        for stdin,tasks in self.pool.items():
            dc = DjangoCase(stdin,os.path.abspath(stdin))
            self.case = {}
            dc.set_structure(stdin+'/scf/POSCAR')
            for task in tasks:
                self.task_analysis(stdin,task)
            dc.update_params(self.case)

    def task_analysis(self,stdin,task):
        if task == "scf":
            self.task_scf(stdin)
        elif task == "relax":
            pass
        elif task == "band":
            self.task_band(stdin)
        elif task == "emass":
            self.task_emass(stdin)
        elif task == "dos":
            pass

    def task_scf(self,stdin):
        from jump2.abtools.grep import Vasp_grep
        vg = Vasp_grep(stdin+'/scf')
        for property in default['scf']:
            self.case[property] = vg.grep(property)

    def task_emass(self,stdin):
        from jump2.abtools.grep import Jump2band
        jb = Jump2band(stdin)
        if 'emass' in default['emass']:                           
            self.case['emass'] = jb.get_emass()

    def task_band(self,stdin):
        from jump2.abtools.grep import Jump2band
        band = os.listdir(stdin+'/nonscf/band')
        jb = Jump2band(stdin,band)
        if 'bandgap' in default['band']:
            self.case['bandgap'] = {'direct':jb.get_bandgap(True)[0],
                                    'indirect':jb.get_bandgap()[0]}

    def path2task(self):
        from os.path import join
        from jump2.abtools.vasp.check import CheckStatus
        tasks = {}
        for path in self.__path:
            self.pool[path] = self.__loadstatus(join(path,'.status'))

    def __loadstatus(self,log):
        import re
        relax = None
        tasks = set([])
        with open(log,'r') as f:
            for line in f:
                if line.split()[-1] == "True":
                    if line.startswith("task: relax/"):
                        tasks.add("relax")
                        relax = line.split()[1]
                    elif line.startswith("task: scf"):
                        tasks.add("scf")   
                    elif line.startswith("task: nonscf"):
                        tmp = line.split()[1].split("/")[1]
                        tasks.add(tmp)
        return tasks                        

class __Analysis(Analysis):

    def __init__(self, params=None, *args, **kwargs):
        if 'pool' in params:
            self.path = os.path.abspath(params['pool']) 
            self.task = self.path2task()
        else:
            raise ("Please add -f [poolname]")
        
        if params['extract']  == 'log':
            self.savelog()
        elif params['extract'] == 'db':
            self.savedb()

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self,value=None):
        from os.path import exists,join,isdir,isfile,dirname
        paths = []
        if isdir(value):
            if exists(join(value,'.status')):
                paths.append(value)
            else:
                for dir in os.listdir(value):
                    if exists(join(value,dir,'.status')):
                        paths.append(join(value,dir))
        elif isfile(value):
            import pickle
            try:
                root = dirname(value)
                with open(value,'rb') as f:
                    pool=pickle.load(f)
                for dir in pool.keys():
                    if exists(join(root,dir,'.status')):
                        paths.append(join(root,dir))
            except:
                print('PathError: Invalid poolfile')
        
        else:
            print('PathError: Invalid directory')
        self.__path = paths
        print('Total = %s' %len(paths))
