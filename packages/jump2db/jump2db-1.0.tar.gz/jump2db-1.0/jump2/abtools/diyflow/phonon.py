import os
import numpy as np
from phonopy.structure.atoms import PhonopyAtoms

class Phonon():
 
    def __init__(self,func=None,stdin=None,stdout=None,*args,**kwargs):
        from copy import deepcopy
        from os.path import dirname,join
        self.func = deepcopy(func)
        self.stdin = stdin
        self.rootdir =stdout
        self.json = join(dirname(dirname(stdout)),'.phonon')
        self.status = {}
        self.prepare()

    def load_json(self):
        '''
        load the phonopy parameter save with input.py        

        self.trans = '2,2,2' or '2 0 0 0 2 0 0 0 0'
        self.softmode = False
        self.modulations = {'dimension':[1,1,1],
                            'q':[0,0,0],
                            'band_index':0,
                            'amplitude':(0.0,15.0,0.5), 
                            'argument':0}
        '''
        import json 
        print(self.json)
        with open(self.json,'r') as f:
            params = json.load(f)

        self.params = params['params']

        try:
            self.force = params['force']
            trans = np.array(params['trans'].split(),dtype = int)
            if len(trans) == 3:
                self.trans = np.diag(trans)
            elif len(trans) == 9:
                self.trans = trans.reshape(3,3)
            else:
                raise IOError ('Invalid Phonopy trans input')
               
        except:
            pass
        try:
            self.softmode = params['softmode']
            self.modulations = params['modulations']
        except:
            pass
        
    def prepare(self):
        '''
        Prapare the task and stop if any parameters error.
        '''
        from os.path import exists,join

        # read structure %
        if os.path.exists(self.stdin):
            try:
               from phonopy.interface.calculator import read_crystal_structure
               self.unitcell = read_crystal_structure(join(self.stdin,'CONTCAR'),'vasp')[0] 
               print('initialize unitcell from {0}/CONTCAR'.format(self.stdin))
            except:
               self.unitcell = Phonon.jump2phonopy(self.func.structure)
               print('initialize from Setvasp')
        else:
            self.unitcell = Phonon.jump2phonopy(self.func.structure)
            print('initialize from Setvasp')

        
        # load params %
        try:
            params = self.load_json()
        except:
            raise IOError ('Please check .phonon save in prepare folder')

    def create_stdout(self,task):
        # mkdir calculation path %
        output = os.path.join(self.rootdir,'diy',task)
        if os.path.exists(output):
            dirs = os.listdir(os.path.join(self.rootdir,'diy'))
            num = len([dir for dir in dirs if task in dir])
            output = output + str(num)
        os.makedirs(output)
        self.stdout = output

    @staticmethod
    def ziplist(alist):
        key,value = [],{}
        for i in alist:
           if i not in key:
               key.append(i)
               value[i] = 1
           else:
               value[i] += 1
        return key,[value[i] for i in key]

    @staticmethod
    def jump2phonopy(structure):
        lattice = structure.lattice
        positions = structure.get_positions()
        elements = structure.get_elements('symbol')
        unitcell = PhonopyAtoms(symbols=elements,cell = lattice,
                                scaled_positions=positions)
        return unitcell

    @staticmethod
    def phonopy2jump2(poscar):
        from jump2.structure.structure import Structure
        obj = Structure()
        obj.comment_line = 'PHONOPY'
        obj.lattice = np.asarray(poscar.cell)
        obj.direct = True
        obj.frozen = False
        elements,numbers = Phonon.ziplist(poscar.symbols)
        obj.species_of_elements = elements
        obj.number_of_atoms = numbers
        obj.atomic_positions = np.asarray(poscar.scaled_positions)
        return obj


    def get_forces(self,path):
        import os
        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        
        def xml2varray(root):
            varray = []
            for i in root:
                varray.append(i.text.split())
            return varray

        forces = []
        for i in range(len(os.listdir(path))):
            dirname = '%04d'%i
            tree = ET.ElementTree(file=os.path.join(path,dirname,'vasprun.xml'))
            root = tree.getroot()
            force = root.findall("./calculation/varray[@name='forces']")[0]
            forces.append(xml2varray(force))
     
        return np.array(forces,dtype=float)
   
    def softmode_conf(self):

        def get_phmode(phdict,value):
            phmode = [phdict['q'],
                      phdict['band_index'],
                      value,
                      phdict['argument']]
            return phmode

        dim = self.modulations['dimension']
        amplitude = self.modulations['amplitude']
        if len(amplitude) == 1:
            phmode = [get_phmode(self.modulations,amplitude)]
     
        elif len(amplitude) == 3:
            phmode = []
            for i in np.arange(amplitude[0],amplitude[1],amplitude[2]):
                phmode.append(get_phmode(self.modulations,i))

        return [dim,phmode]


    def run(self,vaspflow): 
        from phonopy import Phonopy
        from phonopy.file_IO import parse_FORCE_SETS,write_FORCE_SETS
        from jump2.abtools.vasp.vaspflow import VaspFlow
        
        # init phonon and create displacements
        unitcell = self.unitcell
        phonon = Phonopy(unitcell,self.trans)
        phonon.generate_displacements()
        vaspfunc = vaspflow("calculator")
         
        if os.path.exists(self.rootdir+'/FORCE_SETS'):
            pass

        elif self.force == True:
            self.create_stdout('phonon')
            self.status['phonon'] = {'path':self.stdout}
            supercells = phonon.supercells_with_displacements
            self.cal_forces(supercells,vaspfunc)
            phonon.set_forces(self.get_forces(self.stdout))
            dataset = phonon.displacement_dataset
            write_FORCE_SETS(dataset)
            self.status['phonon']['success'] = True

        if self.softmode == True:
            # read forces and calculation force_constants
            force_sets=parse_FORCE_SETS()
            phonon.set_displacement_dataset(force_sets)
            phonon.produce_force_constants(calculate_full_force_constants=False)

            # create modulations
            dim,phmode = self.softmode_conf()
            print(dim,phmode)
            phonon.set_modulations(dim,phmode)
            modulated_supercells = phonon.get_modulated_supercells()
            self.create_stdout('softmode')
            self.cal_modulations(modulated_supercells,vaspfunc)
            self.status['softmode'] = {'path':self.stdout,'success':True}

        self.update_status()

    def cal_forces(self,supercells,calculator,stdin=None):
        
        for i in range(len(supercells)):
            stdout = self.stdout+'/'+'%04d'%i
            self.func.structure = self.phonopy2jump2(supercells[i])
            if not os.path.exists(stdout): os.makedirs(stdout)
            calculator(self.func,stdout=stdout,stdin=stdin,overwrite=True,**self.params['force'])

    def cal_modulations(self,supercells,calculator,stdin=None):
        
        for i in range(len(supercells)):
            stdout = self.stdout+'/'+'%04d'%i
            self.func.structure = self.phonopy2jump2(supercells[i])
            if not os.path.exists(stdout): os.makedirs(stdout)
            calculator(self.func,stdout=stdout,stdin=stdin,overwrite=True,**self.params['softmode'])

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
                if v is True: v = 'True'
                elif v is False: v = 'False'
                f.write("{0:>8s}: {1: <8}".format(k,v))
            f.write('\n')
        f.close()










