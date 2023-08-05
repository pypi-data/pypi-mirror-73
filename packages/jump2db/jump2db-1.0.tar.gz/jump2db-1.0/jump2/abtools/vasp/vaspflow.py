from .monitor import Monitor
from .check import CheckStatus
from pprint import pprint
import os

class VaspFlow(object):

    def __init__(self, vasp=None, stdout=None, *args, **kwargs):

        from .tasks import VaspTask
        from .setvasp import SetVasp 
        from os.path import dirname,abspath
        from jump2.compute.__cluster__ import __Script__

        # stdout directoty %
        if stdout:
            self.rootdir = abspath(stdout)
        else:
            self.rootdir = abspath(os.getcwd())

        # classify the tasks % 	
        if isinstance(vasp, SetVasp):
            vasp.tasks = VaspTask.fulltask(vasp.tasks,self.rootdir)
            vasp.tasks.set_energy(vasp.energy)
            vasp.tasks.set_force(vasp.force)
        else:
            raise TypeError('Invalid func. Make sure you input a SetVasp class!')
        
        self.cluster = __Script__(dirname(dirname(self.rootdir)))
        self.vasp_calculator(vasp, stdout)
	
    def vasp_calculator(self, vasp, stdout, stdin=None, **kwargs):
        
        import os
        from copy import deepcopy
        from os.path import exists, join, abspath 
        from .check import CheckStatus 
        from ..diyflow import import_diy_moudle
	
        params = {}
        next_flow = {'success':True} 

        check = CheckStatus(overwrite=vasp.overwrite)

        if exists(stdout) and exists(join(stdout,'.status')):
            stdin = check._continue(vasp.tasks, stdout)

        from pprint import pprint
        print('-'*30)
        pprint(vasp.tasks)
        print('stdin = %s' %stdin)
        print('-'*30)
        

        # optimization % 
        if vasp.tasks.optimize is not None and vasp.tasks.optimize.finish is False:
            output = join(stdout, 'relax')
            stdin, next_flow = self.relax_cell_ions(vasp, output, stdin, **params)

            # exit calculation-flow if task error % 
            if vasp.tasks.optimize.finish is True and not next_flow['success']:
                os.sys.exit()

        # single point calculation %
        if vasp.tasks.scf is not None and vasp.tasks.scf.finish is False:
            output = join(stdout, 'scf')
            stdin, next_flow = self.single_point(vasp, output, stdin, **params)

            # exit calculation-flow if task error % 
            if vasp.tasks.scf.finish and not next_flow['success']:
                os.sys.exit()	

        # properties calculation %
        if vasp.tasks.nonscf is not None and vasp.tasks.nonscf.finish is False:
            for prop in vasp.tasks.nonscf:
                if vasp.tasks.nonscf[prop].finish is False:
                    output = join(stdout, 'nonscf', prop) 
                    next_flow = self.calc_property(vasp, prop, stdin, output) 
		
        # diy calculation %
        if vasp.tasks.diyflow is not None and vasp.tasks.diyflow.finish is False:
            for name in vasp.tasks.diyflow:
                if vasp.tasks.diyflow[name].finish is False:
                    diy_class = import_diy_moudle(name)
                    diyflow = diy_class(func=deepcopy(vasp),stdin=stdin,rootdir=self.rootdir)
                #except:
                #    print 'Error in import {0}'.format(name)


        print('Calculation finished')

    def __get_phonon_kvectors(self, vasp=None, vectors=None, *args, **kwargs):

        """
        function to get the default K vectors for phonon calculation.
        """
        from ..brillouin_zone import HighSymmetryKpath
		
        kpath = {'all':{}, 'suggest':{}}	

        bz = HighSymmetryKpath()
        kpoint = bz.get_HSKP(vasp.structure.bandStructure())
        count = 0

        k = ''
        A = ''
        for p in kpoint['Path']:
            for i in range(len(p)):
                k += '{0[0]:>16.8f} {0[1]:>16.8f} {0[2]:>16.8f}    '.format(\
                     kpoint['Kpoints'][p[i]])

                A += p[i]+'   '
                if 'Gamma' in p[i]: A = 'Gamma'
            kpath['all'][A] = k
            if count == 0: kpath['suggest'][A] = k
            count += 1
	
        return kpath

 
    def __get_band_kpath(self, structure=None):
	
	
        from ..brillouin_zone import HighSymmetryKpath
        import numpy as np


        kpath = {'all':{}, 'suggest':{}}	
        bz = HighSymmetryKpath()
        kpoint = bz.get_HSKP(structure.bandStructure())

        count = 0
        tmp = []
        for p in kpoint['Path']:
            if len(tmp) > 0 and sum([i-int(i) for i in (np.array(\
                          kpoint['Kpoints'][p[0]])+tmp)]) < 0.001: 
                count -= 1
            for i in range(len(p)-1):
                k1 = '{0[0]:>16.8f} {0[1]:>16.8f} {0[2]:>16.8f} ! {1}'.format(\
                     kpoint['Kpoints'][p[i]], p[i])

                k2 = '{0[0]:>16.8f} {0[1]:>16.8f} {0[2]:>16.8f} ! {1}'.format(\
                     kpoint['Kpoints'][p[i+1]], p[i+1])

                A = p[i].strip('\\')
                B = p[i+1].strip('\\')
                key = '{0}-{1}'.format(A,B)
                kpath['all'][key] = k1+'+\n'+k2
                if count == 0: kpath['suggest'][key] = k1+'+\n'+k2
                if 'Gamma' in p[i+1]: B = 'Gamma'
            tmp = np.array(kpoint['Kpoints'][p[-1]])
            count += 1
        if len(kpath['suggest']) >= 5:
            return kpath['suggest']
        else:
            return kpath['all']
  
    @Monitor
    def calculator(self, vasp, stdout=None, stdin=None, incar={}, overwrite=True, **kwargs):

        from jump2.structure import read 
        from os.path import join, exists, getsize 
        import shutil
        import os  

        # restart from previous calculation % 
        if stdin is not None:

            # udpate the structure % 
            try:
                vasp.structure = read(join(stdin,'CONTCAR'))	
            except:
                try:
                    vasp.structure = read(join(stdin,'POSCAR'))
                except:
                    pass

            if stdin != stdout:
                if not exists(stdout): os.makedirs(stdout)
                overwrite = True 

                # copy chgcar %
                if exists(join(stdin,'CHGCAR')) and getsize(join(stdin,'CHGCAR')):
                    if 'icharg' not in incar:
                        incar['icharg'] = 1
                elif 'icharg' not in incar:
                    incar['icharg'] = 2
                elif incar['icharg'] == 11:
                    raise IOError('CHGCAR not exists!')

                if incar['icharg'] == 1 or incar['icharg'] == 11:
                    if 'lcharg' in incar and incar['lcharg'] is False:
                        os.symlink(join(stdin,'CHGCAR'),join(stdout,'CHGCAR'))
                        os.symlink(join(stdin,'CHG'),join(stdout,'CHG'))
                    else:
                        shutil.copyfile(join(stdin,'CHGCAR'),join(stdout,'CHGCAR'))
                        shutil.copyfile(join(stdin,'CHG'),join(stdout,'CHG'))

                # copy wavecar %
                if exists(join(stdin,'WAVECAR')) and getsize(join(stdin,'WAVECAR')):
                    if 'istart' not in incar:
                        incar['istart'] = 1
                else:
                    incar['istart'] = 0

                if incar['istart'] == 1:
                    if 'lwave' in incar and incar['lwave'] is False:
                        os.symlink(join(stdin,'WAVECAR'),join(stdout,'WAVECAR'))
                    else:
                        shutil.copyfile(join(stdin,'WAVECAR'),join(stdout,'WAVECAR'))

        incar = vasp.set_input(vasp.structure, stdout, overwrite, incar)

        # update vasp program %
        if isinstance(vasp.program, dict):
            if 'lsorbit' in incar or'LSORBIT' in incar:
                program = vasp.program['ncl'] 
            else:
                raise KeyError('Non-collinear version of the VASP is required for SOC calculations')
        else:
            program = vasp.program

        # run vasp progam % 
        self.run(stdout, program=program) 
        return stdout 

    # run % 
    def run(self, stdout=None, program=None):

        import os 
        from os.path import join
        os.chdir(join(self.rootdir,stdout))
	
        try:
            program = "{0} -np {1} {2}".format(self.cluster.mpi,self.cluster.cores,program)
        except:   
            raise AttributeError("VaspFlow.cluster object has no attribute 'mpi' or 'cores'")

        os.system('{program} > pbs.log'.format(program=program))

        os.chdir(self.rootdir)

 
    def single_point(self, vasp, stdout, stdin=None, **kwargs):
	
        from os.path import join

        # task start %
        self.calculator(vasp, stdout, stdin, incar=vasp.tasks.scf)

        # check force convergence or not, default is force% 
        if getattr(vasp,'constrain',False):
            check = CheckStatus(constrain=vasp.constrain)
        else:
            check = CheckStatus()

        # check status % 	
        status = check.success(join(stdout,'OUTCAR'), task='scf')
        check.write_status(self.rootdir, status=status, task=stdout)

        return stdout, status
	
    def relax_cell_ions(self, vasp, stdout, stdin=None, steps=3, **kwargs):
        """
        function to relax the cell shape, internal inons and volume.
        """
        from os.path import join  
        import shutil
        from .tasks import VaspIncar

        # check force convergence or not, default is force% 
        if getattr(vasp,'constrain',False):
            check = CheckStatus(constrain=vasp.constrain)
        else:
            check = CheckStatus()

        success = False	
        # get accelerate parameter % 
        if getattr(vasp,'accelerate',True):
            if isinstance(vasp.accelerate,list):
                accelerate = vasp.accelerate
            elif isinstance(vasp.accelerate,bool):
                step1 = {'kspacing':0.5, 'ediff':1E-3, 'ediffg':-0.10, 'nsw':20}
                step2 = {'kspacing':0.4, 'ediff':1E-4, 'ediffg':-0.05, 'nsw':20}
                vasp.accelerate = [step1,step2]
                accelerate = vasp.accelerate

            n = 0
            # run vasp object % 
            for acc in accelerate:
                acc.downdate(vasp.tasks.optimize) 
                if 'isif' in acc and acc['isif']== -1:
                    acc['isif'] = 7
                    stdin = self.calculator(vasp, stdout+'/S'+str(n), stdin, overwrite=True, incar=acc)
                    acc['isif'] = 2  
                    stdin = self.calculator(vasp, stdout+'/S'+str(n), stdin, overwrite=True, incar=acc)
                else:	
                    stdin = self.calculator(vasp, stdout+'/S'+str(n), stdin, overwrite=True, incar=acc)
       
            # check accelerate status % 	
            status = check.success(join(stdin,'OUTCAR'), task='relax')
            check.write_status(self.rootdir, status=status, task=stdin)

        n = 1
        iv = False
        params = vasp.tasks.optimize 
        if 'isif' in params and params['isif']== -1: 
            iv = True
        # run vasp object % 
        while (n <= steps) and (not success):
            if iv:
                params['isif'] = 7 
                stdin = self.calculator(vasp, stdout+'/S'+str(n), stdin, incar=params)
                params['isif'] = 2 
                stdin = self.calculator(vasp, stdout+'/S'+str(n), stdin, incar=params)
            else:
                stdin = self.calculator(vasp, stdout+'/S'+str(n), stdin, incar=params)

            status = check.success(join(stdin,'OUTCAR'), task='relax')
            check.write_status(self.rootdir, status=status, task=stdin)
            success = status['success']
            n += 1

        # delete invalid relax path %
        for dir in os.listdir(stdout):
            if dir > 'S'+str(n):
                shutil.rmtree(join(stdout,dir)) 
        
        return stdin, status
  
    def calc_property(self, vasp, case, stdin, stdout, **kwargs):

        """
        select the case of tasks
        """
        # from .vasp_analysis.extract import CheckStatus
        from os.path import join, exists, dirname
        from jump2.abtools.grep.band import GrepBand
        import numpy as np
        from copy import deepcopy
        from .incar import default  

        # get incar params%
        params = vasp.tasks.nonscf[case]
        check = CheckStatus()
	

        if case == 'band':
            # get kpath %
            # kpath of band from input.py %
            if hasattr(vasp,'kpath') and vasp.kpath is not None:
                band = vasp.kpath
            # kpath of band from automatic generation %
            else:
                band = self.__get_band_kpath(vasp.structure)

            # get nbands %
            num_band = self.__get_nband(stdin)
            if num_band is not None and 'nbands' not in params:
                params['nbands'] = int(num_band)

            # get band insert points number %
            if hasattr(vasp,'band_insert'):
                insert = vasp.band_insert
            else:
                insert = 30    
            
            # copy vasp and change vasp.kpoints %
            bandvasp = deepcopy(vasp)
            # loop the kpoints % 
            if hasattr(bandvasp,'band_split') and bandvasp.band_split is False:
                bandvasp.kpoints = ('Jump2', insert, 'Line', list(band.values()))
                print(bandvasp.num,bandvasp.modle)
                self.calculator(bandvasp, stdout, stdin, incar=params)
                status = check.success(join(stdout,'OUTCAR'), task='nonscf')
                check.write_status(self.rootdir, status=status, task=stdout)
            else:
                for k in band: 
                    bandvasp.kpoints = (k, insert, 'Line', band[k])
                    band_k = self.calculator(bandvasp, join(stdout,k), stdin, incar=params)
                    status = check.success(join(band_k,'OUTCAR'), task='nonscf')
                    check.write_status(self.rootdir, status=status, task=band_k)

        elif case == 'partchg':
            # step 1 : get band edge
            cvdict = self.__get_band_edge(vasp, stdin, task='partchg')
                
            # check whether a nogap bandstructure %
            if 'nogap' in cvdict and cvdict['nogap'] == True: 
                check.write_error_status(self.rootdir, error='no-gap', task=stdout)
                return False

            # get kpoints with weight %
            kpt = GrepBand()._get_kpoint(stdin,weight=True)
            for i in ['cbm','vbm']:
                k = np.append(cvdict[i]['kpoint'],0.0)
                kpt=np.vstack((kpt,k))

            # step 2 : calculation again, add cbmvbm into kpoints %
            if not exists(stdout): os.makedirs(stdout)
            # scf with bandedge kpoints %
            partchgvasp = deepcopy(vasp)
            partchgvasp.kpoints = ("PARTCHG KPOINTS",len(kpt),"Reciprocal",kpt)
            stdin = self.calculator(partchgvasp, join(stdout,'scf'), stdin, incar=vasp.tasks.scf)
            status = check.success(join(stdin,'OUTCAR'), task='nonscf')
            check.write_status(self.rootdir, status=status, task=stdin)

            # get iband %
            if not status['success']: return False
            ciband = gb._get_cbid(stdin)[0]

            params.downdate({'lpard': True,'lsepb': True,'lorbit': 11})
            # cbm partchg %
            params['kpuse'] = len(kpt)-1
            params['iband'] = ciband+1
            self.calculator(partchgvasp, join(stdout,'cbm'), stdin, incar=params)
            status = check.success(join(stdout,'cbm','OUTCAR'), task='nonscf')
            check.write_status(self.rootdir, status=status, task=join(stdout,'cbm'))
            # vbm partchg %
            params['kpuse'] = len(kpt)
            params['iband'] = ciband
            self.calculator(partchgvasp, join(stdout,'vbm'), stdin, incar=params)
            status = check.success(join(stdout,'vbm','OUTCAR'), task='nonscf')
            check.write_status(self.rootdir, status=status, task=join(stdout,'vbm'))


        elif case == 'emass':
            # step 1 : get band edge and set emass path %
            cvdict = self.__get_band_edge(vasp, stdin, task='emass')
            # check whether a nogap bandstructure %
            if 'nogap' in cvdict and cvdict['nogap'] == True: 
                check.write_error_status(self.rootdir, error='no-gap', task=stdout)
                return False
            band = self.__set_emass_band(cvdict)

            # get nbands %
            params.downdate(vasp.tasks.nonscf['band'])
            num_band = self.__get_nband(stdin)
            if num_band is not None and 'nbands' not in params:
                params['nbands'] = int(num_band)

            if hasattr(vasp,'emass_insert'):
                insert = vasp.emass_insert
            else:
                insert = 50    
	
            bandvasp = deepcopy(vasp)
            # loop the kpoints % 
            for kpath,name in band.items(): 
                bandvasp.kpoints = (name,insert, 'Line',kpath)
                self.calculator(bandvasp, join(stdout,name), stdin, incar=params)
                status = check.success(join(stdout,name,'OUTCAR'), task='nonscf')
                check.write_status(self.rootdir, status=status, task=join(stdout,name))

        elif case == 'phonon':
            from phonon import Phonon 
            if hasattr(self,'vectors'):
                vectors = self.vectors
            else:
                vectors = self.__get_phonon_kvectors(vasp)['all']
            phonon_params = Phonon().calculator_phonon(vasp, stdout, **params) # 
            self.calculator(vasp, stdout, stdin, phonon_params)
            # check_stutus % 
            status = self.__check__(stdin,task='nonscf',constrain=True)

        elif case == 'hse_gap':
                
            # step 1: get band edge % 
            edge = self.__get_band_edge(vasp, stdin, task='hse')
            if 'nogap' in edge and egde['nogap'] == True: 
                check.write_error_status(self.rootdir, error='no-gap', task=stdout)
                return False
            kpt = GrepBand()._get_kpoint(stdin,weight=True)
            for i in ['cbm','vbm']:
                k = np.append(edge[i]['kpoint'],0.0)
                kpt=np.vstack((kpt,k))

       	    # step 2: calculate HSE gap %    	
            hsevasp = deepcopy(vasp)
            hsevasp.kpoints = ("HSE KPOINTS",len(kpt),"Reciprocal",kpt)
            hsevasp.xc_func = 'hse'
            self.calculator(hsevasp, stdout, stdin, incar=params)
            status = check.success(join(stdout,'OUTCAR'), task='nonscf')
            check.write_status(self.rootdir, status=status, task=stdout)
	 
        elif case == 'gw_gap':

            # step 1: get band edge % 
            edge = self.__get_band_edge(vasp, stdin, task='gw')
            if 'nogap' in edge and egde['nogap'] == True: 
                check.write_error_status(self.rootdir, error='no-gap', task=stdout)
                return False
            kpt = GrepBand()._get_kpoint(stdin,weight=True)
            for i in ['cbm','vbm']:
                k = np.append(edge[i]['kpoint'],0.0)
                kpt=np.vstack((kpt,k))
            gwvasp = deepcopy(vasp)
            #gwvasp.kpoints = ("GW KPOINTS",len(kpt),"Reciprocal",kpt)

            # update nbands %
            if 'nbands' in params:
                num_band = params['nbands']
            elif 'nbands' in vasp.tasks.nonscf['optics']:
                num_band = vasp.tasks.nonscf['optics']['nbands']
            else:
                num_band = self.__get_nband(stdin)
            num_band = 40

            # step 2: calculate optics %
            opdir = os.path.join(self.rootdir,'nonscf','gw_optics')
            if not os.path.exists(opdir):
                optics_params = gwvasp.tasks.nonscf['optics']
                optics_params.update({'nbands':num_band,'isym':0})
                self.calculator(gwvasp, opdir, stdin, incar=optics_params)
                status = check.success(join(opdir,'OUTCAR'), task='nonscf')
                check.write_status(self.rootdir, status=status, task=opdir)
		
            if status is False:
                print("Failed in optics step. Stop GW calculation")

       	    # step 3: calculate GW gap %    	
            if not exists(stdout): os.makedirs(stdout)
            os.system('cp {0}/WAVECAR {1}/WAVECAR.DIAG'.format(opdir,stdout))
            os.system('cp {0}/WAVEDER {1}/WAVEDER.DIAG'.format(opdir,stdout))

            gwvasp.xc_func = 'gw'
            params['nbands'] = num_band
            self.calculator(gwvasp, stdout, opdir, params)
            status = check.success(join(stdout,'OUTCAR'), task='nonscf')
            check.write_status(self.rootdir, status=status, task=stdout)

        else:
            self.calculator(vasp, stdout, stdin, incar=params)
            # check_stutus % 
            status = check.success(join(stdout,'OUTCAR'), task='nonscf')
            check.write_status(self.rootdir, status=status, task=stdout)
	 
        vasp.tasks.nonscf[case].finish = True
        return status 

        #vasp.setvasp(structure, stdin, ouput, **params)

    def __get_nband(self, stdin=None):
	
        import numpy as np
        from jump2.abtools.grep.outcar import GrepOutcar

        if os.path.exists(stdin):
            nbands = GrepOutcar().nbands(stdin) 
        else:
            raise IOError('nbands grep failed.')
            
        nn = np.arange(nbands*1.2/self.cluster.cores,nbands*1.5/self.cluster.cores,dtype=int)
        return int(12*(nn[0]+1))

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

    def __get_edge(self,stdin):
        from os.path import join,exists
        from jump2.abtools.grep import Jump2band

        if exists(stdin):
            jb = Jump2band(self.rootdir,kpath='skip')
            cvdict = jb.get_force_cbmvbm(stdin)
        else:
            raise IOError
        return cvdict

    def __get_band_edge(self, vasp, stdin=None, banddir=None, task='default'):
        from os.path import join,isdir,isfile
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

    @property
    def realpath(self):
        from os.path import abspath,dirname,realpath
        return abspath(dirname(realpath(__file__)))
