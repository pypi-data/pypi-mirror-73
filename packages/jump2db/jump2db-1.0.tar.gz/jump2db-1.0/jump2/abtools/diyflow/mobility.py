import os
import numpy as np
from .miniflow import MiniFlow

class Mobility(MiniFlow):
 

    def __init__(self,func,stdin=None,rootdir=None,*args,**kwargs):
        MiniFlow.__init__(self,func,stdin,rootdir)
        stdout = self.rootdir+'/diy/mobility'
        self.load_json(func)
        self.set_emass(func,stdin)
        self.structure_set = self.load_structure(stdin,func)
        self.diy_calculator(func,stdout=stdout,stdin=stdin)

    def diy_calculator(self,func,stdout,stdin=None):
        from os.path import join,exists

        if not exists(stdout):
            os.makedirs(stdout)

        # start calculation %
        for label,structure in self.structure_set.items():
            # structure start %
            func.structure = structure
            output = join(stdout,label)

            # scf %
            stdin,status = self.single_point(func,output+'/scf')

            # emass %
            self.emass_calculation(func,output+'/emass',stdin)

        print('mobility calculation finished')

    def emass_calculation(self,vasp,stdout,stdin=None):
        from os.path import join, exists, dirname
        from ..vasp.check import CheckStatus
        from copy import deepcopy
        import os

        check = CheckStatus()

        if 'emass' in vasp.tasks.nonscf:
            params = vasp.tasks.nonscf['emass']
            params.downdate(vasp.tasks.nonscf['band'])
        else:
            params = vasp.tasks.nonscf['band']

        num_band = self.__get_nband(stdin)
        if num_band is not None and 'nbands' not in params:
            params['nbands'] = int(num_band*2)
        insert = vasp.emass_insert

        bandvasp = deepcopy(vasp)
        # loop the kpoints % 
        for kpath,name in self.bands.items():
            bandvasp.kpoints = (name,insert, 'Line',kpath)
            self.calculator(bandvasp, join(stdout,name), stdin, incar=params)
            status = check.success(join(stdout,name,'OUTCAR'), task='nonscf')
            check.write_status(self.rootdir, status=status, task=join(stdout,name))


    @classmethod
    def default_json(self,type='default'):
        '''
        default mobility parameters
        '''
        blank = {'scale':'',
                 'axis' :'',
                 'emass_insert':''
                }

        default = {'scale':'0.98 0.99 1.00 1.01 1.02',
                   'axis' :'x y z',
                   'emass_insert':50
                  }

        if type == 'blank':
            return blank
        else:
            return default

    def load_json(self,func):
        '''
        load the phonopy parameter save with input.py        

        self.scale = '0.98 0.99 1.00 1.01 1.02'
        self.axis = 'x y z'
        self.band_insert = 50
        '''
        import json 
        with open(self.json,'r') as f:
            json_dict = json.load(f)
 
        params = Mobility.default_json('default')
        if 'mobility' in json_dict:
            custom = json_dict['mobility']
            for key,value in custom.items():
                if value == '':
                    custom.pop(key)
            params.update(custom)

        # initialize parameters %
        self.scale = np.array(params['scale'].split(),dtype=float)
        self.axis = params['axis'].split()
        func.emass_insert = int(params['emass_insert'])
        
    def load_structure(self,stdin,func):
        '''
        Prapare the task and stop if any parameters error.
        '''
        from os.path import exists,join
        from jump2.structure.operation import Operation

        # restart from previous calculation % 
        if exists(self.stdin):
            try:
                structure = read(join(stdin,'CONTCAR'))
            except:
                try:
                    structure = read(join(stdin,'POSCAR'))
                except:
                    structure = func.structure
        else:
            structure = func.structure
         
        structure_set = {}
        opera = Operation()
        for axis in self.axis:
            struct,label=opera.lattice(structure,axis,self.scale)
            structure_set.update(dict(zip(label,struct)))

        return structure_set
        

    def set_emass(self,func,stdin=None):
        cvdict = self.__get_band_edge(func,stdin)
        if 'nogap' in cvdict and cvdict['nogap'] == True: return False
        self.bands = self.__set_emass_band(cvdict)

    def update_status(self):
        from os.path import exists,join
        path = join(self.rootdir,'.status')
        if exists(path):
            f = open(path,'a+')
        else:
            f = open(path,'wb')
        for task in self.status.keys():
            f.write("task: diy/{0:<20s}    ".format(task))
            for k,v in self.status[task].items():
                print(k,v)
                if v is True: v = 'True'
                elif v is False: v = 'False'
                f.write("{0:>8s}: {1: <8}".format(k,v))
            f.write('\n')
        f.close()

    def __set_emass_band(self,cvdict):
        __axis = {0:'x',1:'y',2:'z'}
        bands = {}
        basepath = '{0[0]:>16.8f} {0[1]:>16.8f} {0[2]:>16.8f} ! K0\n{1[0]:>16.8f} {1[1]:>16.8f} {1[2]:>16.8f} ! K1'
        for bm in ['cbm','vbm']:
            kpoint = cvdict[bm]['kpoint']
            for axis in [0,1,2]:
                kpoint1 = [0 if axis == i else value for i,value in enumerate(kpoint)]
                kpoint2 = [0.5 if axis == i else value for i,value in enumerate(kpoint)]
                kpath = basepath.format(kpoint1,kpoint2)
                if kpath not in bands.keys(): 
                    bands[kpath] = '{0}-{1}'.format(__axis[axis],bm)
                else:
                    bands[kpath] = bands[kpath]+'-'+bm
        return bands

    def __get_band_edge(self, vasp, stdin=None, banddir=None, task='default'):
        from os.path import join,isdir,isfile
        from ..vasp.check import CheckStatus
        check = CheckStatus() 

        if banddir == None: 
            banddir = join(self.rootdir,'nonscf','band')

        # check if bandstructure is finished %
        if vasp.tasks.nonscf['band'].finish is False:
            status = False
        elif isdir(banddir) and len(os.listdir(banddir)):
            num = 0
            status = True
            #print("%s band_edge_search start:" %task)
            for i in os.listdir(banddir):
                bandpath = join(banddir,i,'OUTCAR')
                if isfile(bandpath):
                    suc = check.success(bandpath, task='nonscf')['success']
                    if suc is True:
                        num += 1
                    else:
                        status = False
                        break

            if status and num == 0:
                status = False
        else:
            status = False

        if not status:
            print('-'*20+'\n'+stdin+'\n'+'-'*20)
            status = self.calc_property(vasp, 'band', stdin, banddir) 
            if not status['success']: 
                raise IOError ('Failed in calculation band structure!')
        try:
            from jump2.abtools.grep import Jump2band
            if hasattr(vasp,'kpath'):
                kpath = list(vasp.kpath.keys())
                bd = Jump2band(self.rootdir,kpath)
            else:
                bd = Jump2band(self.rootdir)
            cvdict = bd.get_cbmvbm()
            print(cvdict)
        except:
            raise IOError ('Error! cannot find cbmvbm')

        return cvdict

    def __get_nband(self, stdin=None):
	
        import os 
        from jump2.utils import FindKeys

        try:
            line = os.popen('grep -a {0} {1}/OUTCAR'.format('NBANDS',stdin)).readline()
            return FindKeys('NBANDS', line)['NBANDS'] 
        except:
            line = os.popen('grep -a {0} {1}/OUTCAR'.format('NELECT',stdin)).readline()
            return FindKeys('NELECT', line)['NELECT'] 
        finally:
            pass 
            
        return None

