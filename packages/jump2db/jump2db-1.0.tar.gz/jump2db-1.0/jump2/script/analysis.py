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
        #print keywords
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

class __Analysis(object):

    def __init__(self, params=None, *args, **kwargs):
        import os
        if 'pool' in params:
            self.poolname = os.path.abspath(params['pool']) 
            self.__loadtask__(self.poolname)
        else:
            raise ("Please add -f [poolname]")
        
        if params['extract']  == 'log':
            self.__log__()
        elif params['extract'] == 'db':
            self.__db__()

    def __log__(self):
        import json
        print(self.pool)
        for stdin,tasks in self.pool.items():
            self.case = {}
            for task in tasks:
                self.__analysis__(stdin,task)
            if isinstance(self.case['emass'],dict):
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
            if isinstance(self.case['bandgap'],dict):
                self.case.update(self.case.pop('bandgap'))
            self.pool[stdin] = self.case
        with open('output.json','w') as f:
            f.write(json.dumps(self.pool,indent=3))
        #with open('OUTPUT','w') as f:
        #    for stdin in self.pool:
        #        f.write(stdin+'\n')
        #        for property,value in self.pool[stdin].items():
        #            #if isinstance(value,np.ndarray): continue
        #            f.write('{0:<10} = {1}\n'.format(property,value))

    def __db__(self):
        print(self.pool)
        for stdin,tasks in self.pool.items():
            dc = DjangoCase(stdin,os.path.abspath(stdin))
            self.case = {}
            dc.set_structure(stdin+'/scf/POSCAR')
            for task in tasks:
                self.__analysis__(stdin,task)
            dc.update_params(self.case)
            #self.pool[stdin] = self.case
        #with open('output.json','w') as f:
        #    f.write(json.dumps(self.pool,indent=3))

    def __analysis__(self,stdin,task):
        if task == "scf":
            self.__scf__(stdin)
        elif task == "relax":
            pass
        elif task == "band":
            self.__band__(stdin)
        elif task == "emass":
            self.__emass__(stdin)
        elif task == "dos":
            pass

    def __scf__(self,stdin):
        from jump2.abtools.grep import Vasp_grep
        vg = Vasp_grep(stdin+'/scf')
        for property in default['scf']:
            self.case[property] = vg.grep(property)

    def __emass__(self,stdin):
        from jump2.abtools.grep import Jump2band
        jb = Jump2band(stdin)
        if 'emass' in default['emass']:                           
            self.case['emass'] = jb.get_emass()

    def __band__(self,stdin):
        from jump2.abtools.grep import Jump2band
        band = os.listdir(stdin+'/nonscf/band')
        jb = Jump2band(stdin,band)
        if 'bandgap' in default['band']:
            self.case['bandgap'] = {'direct':jb.get_bandgap(True)[0],
                                    'indirect':jb.get_bandgap()[0]}

    def __loadtask__(self,pool):
        from os.path import exists,join,isdir
        self.pool = {}
        if isdir(pool):
            for i in os.listdir(pool):
                if isdir(join(pool,i)) and exists(join(pool,i,'.status')):
                    self.pool[join(pool,i)] = self.__loadstatus__(join(pool,i,'.status'))

    def __loadstatus__(self,log):
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
